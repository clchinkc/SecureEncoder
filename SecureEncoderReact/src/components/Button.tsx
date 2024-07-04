// src/components/Button.tsx

import { forwardRef, MouseEventHandler, ReactNode } from "react"

interface ButtonProps {
	onClick?: MouseEventHandler<HTMLButtonElement>
	children: ReactNode
	type?: "button-primary" | "button-secondary" | null
	outline?: boolean
	className?: string
	disabled?: boolean
	showAlert?: () => void
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
	(
		{
			onClick = () => {},
			children,
			type = null,
			outline = false,
			className = "",
			disabled = false,
			showAlert,
		},
		ref
	) => {
		const baseStyle =
			"py-2 px-2 rounded-lg inline-block text-center transition-colors duration-200 ease-in-out"
		let buttonStyle = ""

		// Define button style based on type and outline props
		if (outline) {
			switch (type) {
				case "button-primary":
					buttonStyle =
						"border border-blue-700 text-blue-700 hover:bg-blue-700 hover:text-neutral-100 dark:border-blue-300 dark:text-blue-300 dark:hover:bg-blue-300 dark:hover:text-black"
					break
				case "button-secondary":
					buttonStyle =
						"border border-neutral-700 text-neutral-700 hover:bg-neutral-700 hover:text-neutral-100 dark:border-neutral-300 dark:text-neutral-300 dark:hover:bg-neutral-300 dark:hover:text-black"
					break
				default:
					buttonStyle = "border border-neutral-500 text-inherit bg-inherit"
					break
			}
		} else {
			switch (type) {
				case "button-primary":
					buttonStyle =
						"bg-blue-700 text-neutral-100 hover:bg-blue-900 dark:bg-blue-500 dark:hover:bg-blue-700"
					break
				case "button-secondary":
					buttonStyle =
						"bg-neutral-700 text-neutral-100 hover:bg-neutral-900 dark:bg-neutral-500 dark:hover:bg-neutral-700"
					break
				default:
					buttonStyle = "text-inherit bg-inherit"
					break
			}
		}

		// Custom click handler to manage disabled state and alerts
		const handleOnClick: MouseEventHandler<HTMLButtonElement> = (e) => {
			e.stopPropagation()
			if (disabled) {
				showAlert && showAlert()
			} else {
				onClick(e)
			}
		}

		return (
			<button
				ref={ref}
				onClick={handleOnClick}
				className={`${baseStyle} ${buttonStyle} ${className} ${
					disabled ? "cursor-not-allowed opacity-50" : ""
				}`}
			>
				{children}
			</button>
		)
	}
)

Button.displayName = "Button"

export default Button
