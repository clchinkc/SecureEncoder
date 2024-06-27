// src/pages/Home.tsx

import { lazy, RefObject, FC } from "react"
import { AppContextProvider } from "../context/AppContext"
import ErrorBoundary from "../components/ErrorBoundary"
import Header from "../components/Header"
import Tabs from "../components/Tabs"

// Lazy load components that are not immediately required
import KeyUploader from "../components/KeyUploader"
import FileList from "../components/FileList"
import OperationSelector from "../components/OperationSelector"
const TextProcessor = lazy(() => import("../components/TextProcessor"))
const ResultDisplay = lazy(() => import("../components/ResultDisplay"))
import withKeyboardShortcuts from "../hoc/withKeyboardShortcuts"

import "../tailwind.css"
import "../App.css"

type AppProps = {
	uploadButtonRef: RefObject<HTMLButtonElement>
	fileSelectionRef: RefObject<HTMLInputElement>
	chooseButtonRef: RefObject<HTMLSelectElement>
	encodingButtonRef: RefObject<HTMLButtonElement>
	decodingButtonRef: RefObject<HTMLButtonElement>
	copyToClipboardRef: RefObject<HTMLButtonElement>
	downloadFileRef: RefObject<HTMLButtonElement>
}

const App: FC<AppProps> = ({
	uploadButtonRef,
	fileSelectionRef,
	chooseButtonRef,
	encodingButtonRef,
	decodingButtonRef,
	copyToClipboardRef,
	downloadFileRef,
}) => {
	return (
		<div className="App">
			<AppContextProvider>
				<ErrorBoundary>
					<Header title="Secure Encoder">
						<p>
							Encode and decode text using various algorithms and keys. Expand your
							capabilities securely.
						</p>
					</Header>
					<Tabs />
					<div className="container mx-auto px-4">
						<div className="mt-1 flex flex-wrap">
							<div className="w-full xl:order-1 xl:w-1/3">
								<KeyUploader
									uploadButtonRef={uploadButtonRef}
									fileSelectionRef={fileSelectionRef}
								/>
								<FileList />
								<OperationSelector chooseButtonRef={chooseButtonRef} />
							</div>
							<div className="min-h-20 w-full xl:order-2 xl:min-h-[200px] xl:w-2/3">
								<div className="flex min-h-10 flex-col xl:h-1/2 xl:min-h-[100px]">
									<TextProcessor
										encodingButtonRef={encodingButtonRef}
										decodingButtonRef={decodingButtonRef}
									/>
								</div>
								<div className="flex min-h-10 flex-col xl:h-1/2 xl:min-h-[100px]">
									<ResultDisplay
										copyToClipboardRef={copyToClipboardRef}
										downloadFileRef={downloadFileRef}
									/>
								</div>
							</div>
						</div>
					</div>
				</ErrorBoundary>
			</AppContextProvider>
		</div>
	)
}

const createKeyMap = ({
	uploadButtonRef,
	fileSelectionRef,
	chooseButtonRef,
	encodingButtonRef,
	decodingButtonRef,
	copyToClipboardRef,
	downloadFileRef,
	isMounted,
}: AppProps & { isMounted: boolean }) => ({
	e: () => {
		if (isMounted && encodingButtonRef.current) {
			encodingButtonRef.current.focus()
			encodingButtonRef.current.click()
		}
	},
	d: () => {
		if (isMounted && decodingButtonRef.current) {
			decodingButtonRef.current.focus()
			decodingButtonRef.current.click()
		}
	},
	o: () => {
		if (isMounted && chooseButtonRef.current) {
			chooseButtonRef.current.focus()
			chooseButtonRef.current.click()
		}
	},
	f: () => {
		if (isMounted && fileSelectionRef.current) {
			fileSelectionRef.current.focus()
			fileSelectionRef.current.click()
		}
	},
	u: () => {
		if (isMounted && uploadButtonRef.current) {
			uploadButtonRef.current.focus()
			uploadButtonRef.current.click()
		}
	},
	b: () => {
		if (isMounted && copyToClipboardRef.current) {
			copyToClipboardRef.current.focus()
			copyToClipboardRef.current.click()
		}
	},
	w: () => {
		if (isMounted && downloadFileRef.current) {
			downloadFileRef.current.focus()
			downloadFileRef.current.click()
		}
	},
})

export default withKeyboardShortcuts(App, createKeyMap)
