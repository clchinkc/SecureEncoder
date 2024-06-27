// src/components/Header.tsx

import { ReactNode, FC } from "react"
import small_logo from "../assets/android-chrome-192x192.png"
import big_logo from "../assets/android-chrome-512x512.png"
import ToggleButton from "./ToggleButton"

type HeaderProps = {
	title: string
	children: ReactNode
}

const Header: FC<HeaderProps> = ({ title, children }) => {
	return (
		<header className="header sticky top-0 z-50 w-full border-b-2 border-neutral-200 bg-white dark:border-neutral-500 dark:bg-neutral-900">
			<details className="relative select-none">
				<summary className="flex cursor-pointer items-center justify-between p-3 text-neutral-900 ">
					<img
						src={big_logo}
						style={{ backgroundImage: `url(${small_logo})` }}
						alt="Secure Encoder Website Logo"
						loading="lazy"
						className="mr-2 size-8"
						width="32"
						height="32"
					/>
					<h1 translate="no">{title}</h1>
					<ToggleButton />
				</summary>
				<div
					id="headerCollapse"
					className="absolute w-full bg-white shadow-xl dark:bg-neutral-900"
				>
					{children}
				</div>
			</details>
		</header>
	)
}

export default Header
