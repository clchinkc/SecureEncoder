// src/hoc/withKeyboardShortcuts.jsx

import {
	useEffect,
	useRef,
	useState,
	RefObject,
	ComponentType,
	FC
} from 'react'

type RefProps = {
	uploadButtonRef: RefObject<HTMLButtonElement>
	fileSelectionRef: RefObject<HTMLInputElement>
	chooseButtonRef: RefObject<HTMLSelectElement>
	encodingButtonRef: RefObject<HTMLButtonElement>
	decodingButtonRef: RefObject<HTMLButtonElement>
	copyToClipboardRef: RefObject<HTMLButtonElement>
	downloadFileRef: RefObject<HTMLButtonElement>
	isMounted: boolean
}

type KeyMapFunction = (refs: RefProps) => Record<string, () => void>

const withKeyboardShortcuts = <P extends object>(
	WrappedComponent: ComponentType<P>,
	createKeyMap: KeyMapFunction
) => {
	const WithKeyboardShortcuts: FC<P> = (props) => {
		const uploadButtonRef = useRef<HTMLButtonElement>(null)
		const fileSelectionRef = useRef<HTMLInputElement>(null)
		const chooseButtonRef = useRef<HTMLSelectElement>(null)
		const encodingButtonRef = useRef<HTMLButtonElement>(null)
		const decodingButtonRef = useRef<HTMLButtonElement>(null)
		const copyToClipboardRef = useRef<HTMLButtonElement>(null)
		const downloadFileRef = useRef<HTMLButtonElement>(null)
		const [isMounted, setIsMounted] = useState(false)

		useEffect(() => {
			setIsMounted(true)
		}, [])

		const keyMap = createKeyMap({
			uploadButtonRef,
			fileSelectionRef,
			chooseButtonRef,
			encodingButtonRef,
			decodingButtonRef,
			copyToClipboardRef,
			downloadFileRef,
			isMounted
		})

		useEffect(() => {
			const handleKeyDown = (event: KeyboardEvent) => {
				const key = event.key.toLowerCase()
				if (event.altKey && keyMap[key]) {
					event.preventDefault()
					keyMap[key]()
				}
			}

			window.addEventListener('keydown', handleKeyDown)

			return () => {
				window.removeEventListener('keydown', handleKeyDown)
			}
		}, [keyMap])

		const refs = {
			uploadButtonRef,
			fileSelectionRef,
			chooseButtonRef,
			encodingButtonRef,
			decodingButtonRef,
			copyToClipboardRef,
			downloadFileRef,
			isMounted
		}

		return <WrappedComponent {...(props as P)} {...refs} />
	}
	return WithKeyboardShortcuts
}

export default withKeyboardShortcuts
