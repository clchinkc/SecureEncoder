// src/components/Card.tsx

import { Suspense, ReactNode, FC } from "react"
import Loading from "./Loading"

type CardProps = {
	fallback?: ReactNode
	children: ReactNode
}

const Card: FC<CardProps> = ({ fallback = <Loading />, children }) => {
	return (
		<div className="card mb-3 flex flex-col border border-neutral-300 bg-neutral-100 p-3 dark:border-neutral-700 dark:bg-neutral-900">
			<Suspense fallback={fallback}>{children}</Suspense>
		</div>
	)
}

export default Card
