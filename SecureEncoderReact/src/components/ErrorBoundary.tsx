// src/components/ErrorBoundary.tsx

import { Component, ErrorInfo, ReactNode } from "react"

type ErrorBoundaryProps = {
	children: ReactNode
}

type ErrorBoundaryState = {
	hasError: boolean
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
	constructor(props: ErrorBoundaryProps) {
		super(props)
		this.state = { hasError: false }
	}

	static getDerivedStateFromError(): ErrorBoundaryState {
		return { hasError: true }
	}

	componentDidCatch(error: Error, errorInfo: ErrorInfo) {
		// Log error to an error reporting service
		console.error("ErrorBoundary caught an error", error, errorInfo)
	}

	render() {
		if (this.state.hasError) {
			return <h2>Something unexpected happened. Please try again later.</h2>
		}
		return this.props.children
	}
}

export default ErrorBoundary
