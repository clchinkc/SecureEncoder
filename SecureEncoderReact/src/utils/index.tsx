// src/utils.index.ts

export function classNames(...classes: unknown[]): string {
	return classes.filter(Boolean).join(" ")
}
