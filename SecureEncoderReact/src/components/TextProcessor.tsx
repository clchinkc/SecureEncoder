// src/components/TextProcessor.tsx

import { useState, useEffect, useCallback, useRef, FC, RefObject, MouseEvent } from "react"
import { useAppContext } from "../context/AppContext"
import Button from "./Button"
import Alert from "./Alert"
import Card from "./Card"
import { useMutation } from "@tanstack/react-query"
import { throttle, debounce } from "../utils/throttleAndDebounce"

interface TextProcessorProps {
	encodingButtonRef: RefObject<HTMLButtonElement>
	decodingButtonRef: RefObject<HTMLButtonElement>
}

const TextProcessor: FC<TextProcessorProps> = ({ encodingButtonRef, decodingButtonRef }) => {
	const { setResult, operation, action, setAction, text, setText, loading, setLoading } =
		useAppContext()
	const [message, setMessage] = useState<string | null>("")
	const [alertType, setAlertType] = useState<"alert-info" | "alert-success" | "alert-danger">(
		"alert-info"
	)
	const lastSavedText = useRef(text)

	// Define mutation for saving text
	const saveTextMutation = useMutation<{ message: string }, Error, string>({
		mutationFn: async (newText: string) => {
			const response = await fetch(`${import.meta.env.VITE_APP_FLASK_URL}/api/save_text`, {
				method: "PATCH",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ new_text: newText || null }),
			})
			if (!response.ok) {
				const data = await response.json()
				throw new Error(data.error || "Failed to update text")
			}
			return response.json()
		},
		onSuccess: (data) => {
			console.log("Server response:", data.message)
			lastSavedText.current = text
		},
		onError: (error) => {
			console.error("Error updating text:", error.message)
		},
	})

	// Define mutation for processing text
	const processTextMutation = useMutation<
		{ result: string },
		Error,
		{ text: string; operation: string; action: string }
	>({
		mutationFn: async (data: { text: string; operation: string; action: string }) => {
			const response = await fetch(`${import.meta.env.VITE_APP_FLASK_URL}/api/process_text`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(data),
			})
			if (!response.ok) {
				const result = await response.json()
				throw new Error(result.error || "Failed to process text")
			}
			return response.json()
		},
		onSuccess: (data) => {
			setResult(data.result)
			setMessage("")
			setAlertType("alert-info")
		},
		onError: (error) => {
			console.error("Error processing text:", error)
			setMessage(`Failed to process text: ${error.message}`)
			setAlertType("alert-danger")
		},
		onSettled: () => {
			setLoading(false)
		},
	})

	const handleSubmit = (actionType: string, e: MouseEvent<HTMLButtonElement>) => {
		e.preventDefault()
		if (!text.trim() || !operation) {
			showMessage()
			return
		}
		setAction(actionType)
		setLoading(true)
		processTextMutation.mutate({ text, operation, action: actionType })
	}

	const handleImmediateSave = throttle(() => {
		if (text !== lastSavedText.current) {
			saveTextMutation.mutate(text)
		}
	}, 2000)

	const debouncedSave = useCallback(
		debounce((newText: string) => {
			saveTextMutation.mutate(newText)
		}, 5000),
		[]
	)

	useEffect(() => {
		if (text !== lastSavedText.current) {
			debouncedSave(text)
		}
	}, [text, debouncedSave])

	// Event listener for mouse click to clear the message
	document.addEventListener(
		"click",
		() => {
			setMessage("")
		},
		{ once: true }
	) // The { once: true } option ensures the event listener is only triggered once

	// Function to display a message if text or operation is missing
	const showMessage = () => {
		if (!text.trim()) {
			setMessage("Please enter text to process.")
			setAlertType("alert-danger")
		} else if (!operation) {
			setMessage("Please select an operation.")
			setAlertType("alert-danger")
		}
	}

	// Function to reset session data and refresh UI
	const handleCleanAll = () => {
		setResult("")
		setText("")
		lastSavedText.current = ""
		setAction("")
		setMessage("")
		setAlertType("alert-info")
	}

	return (
		<Card>
			<h2>Input Text:</h2>
			<textarea
				className="form overflow-y-auto"
				id="text"
				value={text}
				onChange={(e) => { setText(e.target.value); }}
				onBlur={() => { handleImmediateSave(); }}
				placeholder="Enter text here"
				rows={1}
				aria-label="Input text"
				aria-live="polite"
				required
			/>
			{message && <Alert type={alertType}>{message}</Alert>}
			<div className="flex space-x-2">
				<div className="w-1/2">
					<Button
						ref={encodingButtonRef}
						type="button-primary"
						className="w-full"
						disabled={!text.trim() || !operation || loading}
						onClick={(e) => { handleSubmit("encode", e); }}
						showAlert={showMessage}
					>
						{loading && action === "encode" ? "Encoding..." : "Encode / Encrypt"}
					</Button>
				</div>
				<div className="w-1/2">
					<Button
						ref={decodingButtonRef}
						type="button-secondary"
						className="w-full"
						disabled={!text.trim() || !operation || loading}
						onClick={(e) => { handleSubmit("decode", e); }}
						showAlert={showMessage}
					>
						{loading && action === "decode" ? "Decoding..." : "Decode / Decrypt"}
					</Button>
				</div>
			</div>
			<div className="mt-3 flex justify-end">
				<Button className="bg-black text-blue-100" onClick={handleCleanAll}>
					Clean All
				</Button>
			</div>
		</Card>
	)
}

export default TextProcessor
