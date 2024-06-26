// src/components/Loading.tsx

import { FC } from 'react'

const Loading: FC = () => {
	return (
		<div className="animate-pulse">
			<div className="mb-2 h-4 w-3/4 rounded bg-gray-300"></div>
			<div className="mb-2 h-4 w-1/2 rounded bg-gray-300"></div>
			<div className="mb-2 h-4 w-full rounded bg-gray-300"></div>
		</div>
	)
}

export default Loading
