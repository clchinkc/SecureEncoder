// src/context/AppContext.tsx

import {
	createContext,
	useState,
	useContext,
	useEffect,
	useMemo,
	ReactNode,
	FC,
	Dispatch,
	SetStateAction,
} from "react"

interface AppContextProps {
	files: string[]
	setFiles: Dispatch<SetStateAction<string[]>>
	result: string
	setResult: Dispatch<SetStateAction<string>>
	operation: string
	setOperation: Dispatch<SetStateAction<string>>
	action: string
	setAction: Dispatch<SetStateAction<string>>
	text: string
	setText: Dispatch<SetStateAction<string>>
	loading: boolean
	setLoading: Dispatch<SetStateAction<boolean>>
}

const AppContext = createContext<AppContextProps | undefined>(undefined)

export const useAppContext = (): AppContextProps => {
	const context = useContext(AppContext)
	if (context === undefined) {
		throw new Error("useAppContext must be used within an AppContextProvider")
	}
	return context
}

interface AppContextProviderProps {
	children: ReactNode
	value?: Partial<AppContextProps>
}

export const AppContextProvider: FC<AppContextProviderProps> = ({
	children,
	value,
}: AppContextProviderProps) => {
	const getSessionStorageItem = (key: string, defaultValue: string): string => {
		const item = sessionStorage.getItem(key)
		return item !== null ? item : defaultValue
	}

	const getSessionStorageItemArray = (key: string): string[] => {
		const item = sessionStorage.getItem(key)
		return item !== null ? JSON.parse(item) : []
	}

	const [files, setFiles] = useState<string[]>(
		value?.files ?? getSessionStorageItemArray("files")
	)
	const [result, setResult] = useState<string>(
		value?.result ?? getSessionStorageItem("result", "")
	)
	const [operation, setOperation] = useState<string>(
		value?.operation ?? getSessionStorageItem("operation", "")
	)
	const [action, setAction] = useState<string>(
		value?.action ?? getSessionStorageItem("action", "")
	)
	const [text, setText] = useState<string>(value?.text ?? getSessionStorageItem("text", ""))
	const [loading, setLoading] = useState<boolean>(value?.loading ?? false)

	useEffect(() => {
		sessionStorage.setItem("files", JSON.stringify(files))
		sessionStorage.setItem("result", result)
		sessionStorage.setItem("operation", operation)
		sessionStorage.setItem("action", action)
		sessionStorage.setItem("text", text)
	}, [files, result, operation, action, text])

	const contextValue = useMemo(
		() => ({
			files,
			setFiles,
			result,
			setResult,
			operation,
			setOperation,
			action,
			setAction,
			text,
			setText,
			loading,
			setLoading,
		}),
		[files, result, operation, action, text, loading]
	)

	return <AppContext.Provider value={contextValue}>{children}</AppContext.Provider>
}
