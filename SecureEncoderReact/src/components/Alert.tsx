// src/components/Alert.tsx

import { ReactNode, FC } from "react"

type AlertProps = {
	type: "alert-info" | "alert-success" | "alert-danger" | null
	children: ReactNode
}

const Alert: FC<AlertProps> = ({ type, children }) => {
	const baseStyle = "rounded-lg px-2 py-2"
	let typeStyle = ""

	switch (type) {
		case "alert-info":
			typeStyle = "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100"
			break
		case "alert-success":
			typeStyle = "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100"
			break
		case "alert-danger":
			typeStyle = "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100"
			break
		default:
			typeStyle = "bg-neutral-100 text-neutral-800 dark:bg-neutral-900 dark:text-neutral-100"
			break
	}

	return (
		<div className={`${baseStyle} ${typeStyle}`} role="alert" aria-live="assertive">
			{children}
		</div>
	)
}

export default Alert
