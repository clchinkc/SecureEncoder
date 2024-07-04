// src/components/ResultDisplay.tsx

import { useState, useEffect, RefObject, FC } from "react"
import { useAppContext } from "../context/AppContext"
import Button from "./Button"
import Alert from "./Alert"
import Card from "./Card"

interface ResultDisplayProps {
	copyToClipboardRef: RefObject<HTMLButtonElement>
	downloadFileRef: RefObject<HTMLButtonElement>
}

const ResultDisplay: FC<ResultDisplayProps> = ({ copyToClipboardRef, downloadFileRef }) => {
	const { operation, result } = useAppContext()
	const [message, setMessage] = useState<string | null>("")
	const [alertType, setAlertType] = useState<"alert-info" | "alert-success" | "alert-danger">(
		"alert-info"
	)

	const handleCopy = async () => {
		if (!result) return
		try {
			await navigator.clipboard.writeText(result)
			setMessage("Copied to clipboard!")
			setAlertType("alert-success")
		} catch (err) {
			setMessage(`Failed to copy: ${err}`)
			setAlertType("alert-danger")
		}
	}

	const handleDownload = () => {
		if (!result) return
		try {
			const file = new Blob([result], { type: "text/plain" })
			const filename = `${operation.replace(/ /g, "_")}_result.txt` || "result.txt"
			const url = window.URL.createObjectURL(file)
			const element = document.createElement("a")
			element.href = url
			element.download = filename
			document.body.appendChild(element)
			element.click()
			window.URL.revokeObjectURL(url)
			document.body.removeChild(element)
			setMessage("File downloaded successfully!")
			setAlertType("alert-success")
		} catch (err) {
			setMessage(`Failed to download: ${err}`)
			setAlertType("alert-danger")
		}
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

	const showMessage = () => {
		if (!result) {
			setMessage("No result to display or download yet")
			setAlertType("alert-info")
		}
	}

	return (
		<Card>
			<h2>Result:</h2>
			<textarea
				readOnly
				className="form cursor-not-allowed overflow-y-auto"
				id="result"
				value={result || "No result to display yet"}
				rows={1}
				aria-label="Result text"
				aria-live="polite"
				aria-disabled="true"
			/>
			{message && <Alert type={alertType}>{message}</Alert>}
			<div className="flex space-x-2">
				<div className="w-1/2">
					<Button
						ref={copyToClipboardRef}
						type="button-primary"
						outline
						className="w-full"
						disabled={!result}
						onClick={handleCopy}
						showAlert={showMessage}
					>
						Copy to Clipboard
					</Button>
				</div>
				<div className="w-1/2">
					<Button
						ref={downloadFileRef}
						type="button-secondary"
						outline
						className="w-full"
						disabled={!result}
						onClick={handleDownload}
						showAlert={showMessage}
					>
						Download as File
					</Button>
				</div>
			</div>
		</Card>
	)
}

export default ResultDisplay
