// src/App.tsx

import { FC, useRef, useEffect } from "react"
import "./tailwind.css"
import "./App.css"
import { Route, Routes } from "react-router-dom"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"

const App: FC = () => {
	const uploadButtonRef = useRef<HTMLButtonElement>(null)
	const fileSelectionRef = useRef<HTMLInputElement>(null)
	const chooseButtonRef = useRef<HTMLSelectElement>(null)
	const encodingButtonRef = useRef<HTMLButtonElement>(null)
	const decodingButtonRef = useRef<HTMLButtonElement>(null)
	const copyToClipboardRef = useRef<HTMLButtonElement>(null)
	const downloadFileRef = useRef<HTMLButtonElement>(null)

	useEffect(() => {
		const resize = () => {
			const doc = document.documentElement
			const docHeight = doc.clientHeight / 48 + "px"
			const docWidth = doc.clientWidth / 96 + "px"
			doc.style.fontSize = docHeight < docWidth ? docHeight : docWidth
		}

		window.addEventListener("resize", resize)
		resize()
	}, [])

	return (
		<Routes>
			<Route
				path="/"
				element={
					<Home
						uploadButtonRef={uploadButtonRef}
						fileSelectionRef={fileSelectionRef}
						chooseButtonRef={chooseButtonRef}
						encodingButtonRef={encodingButtonRef}
						decodingButtonRef={decodingButtonRef}
						copyToClipboardRef={copyToClipboardRef}
						downloadFileRef={downloadFileRef}
					/>
				}
			/>
			<Route path="*" element={<NotFound />} />
		</Routes>
	)
}

export default App
