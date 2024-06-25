// src/components/FileList.jsx

import { useEffect, useState, FC } from 'react'
import Button from './Button'
import Alert from './Alert'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import Card from './Card'

// Function to fetch files
const fetchFiles = async (): Promise<string[]> => {
	const response = await fetch(
		`${import.meta.env.VITE_APP_FLASK_URL}/api/files`
	)
	if (!response.ok) {
		throw new Error('Failed to load files')
	}
	const data: string[] = await response.json()
	return data.filter((file) => file.endsWith('.pem')) // Filter for .pem files only
}

// Function to download a file
const downloadFile = async (filename: string) => {
	const response = await fetch(
		`${import.meta.env.VITE_APP_FLASK_URL}/api/download_key/${filename}`
	)
	if (!response.ok) {
		throw new Error('Error downloading file')
	}
	const blob = await response.blob()
	const url = window.URL.createObjectURL(blob)
	const a = document.createElement('a')
	a.href = url
	a.download = filename
	document.body.appendChild(a)
	a.click()
	a.remove()
	window.URL.revokeObjectURL(url)
}

// Function to delete a file
const deleteFile = async (filename: string): Promise<string> => {
	const response = await fetch(
		`${import.meta.env.VITE_APP_FLASK_URL}/api/delete_key/${filename}`,
		{ method: 'DELETE' }
	)
	if (!response.ok) {
		throw new Error('Failed to delete file')
	}
	return filename
}

const FileList: FC = () => {
	const queryClient = useQueryClient()
	const [message, setMessage] = useState<string | null>(null)
	const [alertType, setAlertType] = useState<
		'alert-info' | 'alert-success' | 'alert-danger' | null
	>('alert-info')

	const {
		data: files,
		error,
		isLoading
	} = useQuery<string[], Error>({
		queryKey: ['files'],
		queryFn: fetchFiles,
		staleTime: 30000, // 30 seconds
		placeholderData: Array(3)
			.fill('')
			.map((_, idx) => `loading-file-${idx}.pem`) // Show 3 empty rows while loading
	})

	const downloadMutation = useMutation<void, Error, string>({
		mutationFn: downloadFile,
		onSuccess: () => {
			setMessage('File downloaded successfully!')
			setAlertType('alert-success')
		},
		onError: (error) => {
			setMessage(`Error downloading file: ${error.message}`)
			setAlertType('alert-danger')
		}
	})

	const deleteMutation = useMutation<string, Error, string>({
		mutationFn: deleteFile,
		onSuccess: (filename) => {
			queryClient.setQueryData<string[]>(['files'], (oldFiles) =>
				oldFiles ? oldFiles.filter((file) => file !== filename) : []
			)
			setMessage('File deleted successfully')
			setAlertType('alert-success')
		},
		onError: (error) => {
			setMessage(`Error deleting file: ${error.message}`)
			setAlertType('alert-danger')
		}
	})

	const handleDownload = (filename: string) =>
		downloadMutation.mutate(filename)
	const handleDelete = (filename: string) => deleteMutation.mutate(filename)

	// Event listener for mouse click to auto-hide the notification
	useEffect(() => {
		const handleAutoHideMessage = () => {
			setMessage(null)
			setAlertType('alert-info')
		}

		document.addEventListener('click', handleAutoHideMessage)
		return () => {
			document.removeEventListener('click', handleAutoHideMessage)
		}
	}, [])

	if (isLoading) return <div>Loading...</div>
	if (error) return <Alert type="alert-danger">Error: {error.message}</Alert>

	return (
		<Card>
			<h2>Available Keys:</h2>
			<table className="min-w-full table-auto whitespace-nowrap">
				<thead>
					<tr>
						<th
							scope="col"
							className="border-b-2 px-3 py-2 text-left tracking-wider"
						>
							File Name
						</th>
						<th
							scope="col"
							className="border-b-2 px-3 py-2 tracking-wider"
						>
							Actions
						</th>
					</tr>
				</thead>
				<tbody>
					{files?.map((file) => (
						<tr key={file}>
							<td className="border-b border-neutral-300 px-3 py-2">
								<i className="fas fa-file-image icon-style text-blue-500"></i>
								{file}
							</td>
							<td className="flex space-x-2 border-b border-neutral-300 px-3 py-2">
								<Button
									type="button-primary"
									outline
									className="w-1/2"
									onClick={() => handleDownload(file)}
								>
									Download
								</Button>
								<Button
									type="button-secondary"
									outline
									className="w-1/2"
									onClick={() => handleDelete(file)}
								>
									Delete
								</Button>
							</td>
						</tr>
					))}
				</tbody>
			</table>
			{message && <Alert type={alertType}>{message}</Alert>}
		</Card>
	)
}

export default FileList
