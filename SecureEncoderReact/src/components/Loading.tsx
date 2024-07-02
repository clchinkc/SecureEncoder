// src/components/Loading.tsx

import { FC } from "react"

const Loading: FC = () => {
	return (
		<div className="animate-pulse" data-testid="skeleton-loader">
			<div
				className="mb-2 h-4 w-3/4 rounded bg-gray-300"
				data-testid="skeleton-element"
			></div>
			<div
				className="mb-2 h-4 w-1/2 rounded bg-gray-300"
				data-testid="skeleton-element"
			></div>
			<div
				className="mb-2 h-4 w-full rounded bg-gray-300"
				data-testid="skeleton-element"
			></div>
		</div>
	)
}

export default Loading
