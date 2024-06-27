// src/pages/NotFound.tsx

import { FC } from "react"

const NotFound: FC = () => {
	return (
		<div className="flex h-screen flex-col items-center justify-center bg-gray-100">
			<h1 className="mb-4 text-4xl font-bold">404 Not Found</h1>
			<p className="text-lg">The page you are looking for does not exist.</p>
		</div>
	)
}

export default NotFound
