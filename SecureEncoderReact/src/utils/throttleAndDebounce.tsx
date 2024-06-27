// src/utils/throttleAndDebounce.tsx

type Procedure<T extends unknown[]> = (...args: T) => void

export const throttle = <T extends unknown[]>(func: Procedure<T>, delay: number) => {
	let lastCall = 0
	return function (...args: T) {
		const now = new Date().getTime()
		if (now - lastCall < delay) {
			return
		}
		lastCall = now
		return func(...args)
	}
}

export const debounce = <T extends unknown[]>(func: Procedure<T>, delay: number) => {
	let timeoutId: NodeJS.Timeout
	return function (...args: T) {
		if (timeoutId) {
			clearTimeout(timeoutId)
		}
		timeoutId = setTimeout(() => {
			func(...args)
		}, delay)
	}
}
