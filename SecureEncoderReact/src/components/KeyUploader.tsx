// src/components/KeyUploader.tsx

import { useState, useEffect, RefObject, FC, ChangeEvent } from "react"
import Button from "./Button"
import Alert from "./Alert"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import Card from "./Card"

interface KeyUploaderProps {
	uploadButtonRef: RefObject<HTMLButtonElement>
	fileSelectionRef: RefObject<HTMLInputElement>
}

const KeyUploader: FC<KeyUploaderProps> = ({ uploadButtonRef, fileSelectionRef }) => {
	const [file, setFile] = useState<File | null>(null)
	const [message, setMessage] = useState<string | null>("")
	const [alertType, setAlertType] = useState<"alert-info" | "alert-success" | "alert-danger">(
		"alert-info"
	)
	const queryClient = useQueryClient()

	const uploadFile = async (file: File) => {
		const formData = new FormData()
		formData.append("file", file)

		const response = await fetch(`${import.meta.env.VITE_APP_FLASK_URL}/api/upload_key`, {
			method: "POST",
			body: formData,
		})
		if (!response.ok) {
			const data = await response.json()
			throw new Error(data.message || "Failed to upload file")
		}
		return file.name
	}

	const uploadMutation = useMutation<string, Error, File>({
		mutationFn: uploadFile,
		onSuccess: (filename) => {
			setMessage(`File ${filename} uploaded successfully!`)
			setAlertType("alert-success")
			void queryClient.invalidateQueries({ queryKey: ["files"] })
		},
		onError: (error) => {
			setMessage(`Error: ${error.message}`)
			setAlertType("alert-danger")
		},
	})

	const onFileChange = (event: ChangeEvent<HTMLInputElement>) => {
		const selectedFile = event.target.files ? event.target.files[0] : null
		if (selectedFile) {
			setFile(selectedFile)
			setMessage("")
			setAlertType("alert-info")
		}
	}

	const onFileUpload = () => {
		if (!file) {
			setMessage("Please select a file to upload.")
			setAlertType("alert-danger")
			return
		}
		uploadMutation.mutate(file)
	}

	// Event listener for mouse click to auto-hide the notification
	useEffect(() => {
		const handleAutoHideMessage = () => {
			setMessage(null)
			setAlertType("alert-info")
		}

		document.addEventListener("click", handleAutoHideMessage)
		return () => {
			document.removeEventListener("click", handleAutoHideMessage)
		}
	}, [])

	return (
		<Card fallback>
			<h2 id="fileHelp">Upload Existing Key:</h2>
			<input
				ref={fileSelectionRef}
				accept=".pem"
				type="file"
				id="file"
				className="form cursor-pointer text-sm"
				onChange={onFileChange}
				aria-label="file"
				aria-describedby="fileHelp"
			/>
			<Button
				ref={uploadButtonRef}
				type="button-secondary"
				className="mt-3 w-full"
				onClick={onFileUpload}
				aria-disabled={!file}
			>
				Upload
			</Button>
			{message && <Alert type={alertType}>{message}</Alert>}
		</Card>
	)
}

export default KeyUploader
