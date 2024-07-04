// src/components/ErrorBoundary.tsx

import { Component, ErrorInfo, ReactNode } from "react"

interface ErrorBoundaryProps {
	children: ReactNode
}

interface ErrorBoundaryState {
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
		console.error("ErrorBoundary caught an error", error, errorInfo)
	}

	componentDidUpdate(prevProps: ErrorBoundaryProps) {
		if (this.state.hasError && prevProps.children !== this.props.children) {
			this.setState({ hasError: false })
		}
	}

	render() {
		if (this.state.hasError) {
			return <h2>Something unexpected happened. Please try again later.</h2>
		}
		return this.props.children
	}
}

export default ErrorBoundary
