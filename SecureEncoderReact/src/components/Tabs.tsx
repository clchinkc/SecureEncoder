// src/components/Tabs.tsx

import { FC } from "react"
import { useAppContext } from "../context/AppContext"

type Option = {
	title: string
	value: string
}

const options: Option[] = [
	{ title: "Base64", value: "base64" },
	{ title: "Hex", value: "hex" },
	{ title: "UTF-8", value: "utf8" },
	{ title: "Latin-1", value: "latin1" },
	{ title: "ASCII", value: "ascii" },
	{ title: "URL", value: "url" },
	{ title: "AES", value: "aes" },
	{ title: "RSA", value: "rsa" },
	{ title: "MD5", value: "md5" },
	{ title: "Huffman", value: "huffman" },
	{ title: "LZ77", value: "lz77" },
	{ title: "LZW", value: "lzw" },
	{ title: "Zstd", value: "zstd" },
	{ title: "Deflate", value: "deflate" },
	{ title: "Brotli", value: "brotli" },
]

const Tabs: FC = () => {
	const { operation, setOperation } = useAppContext()

	return (
		<div className="mt-1 flex w-full overflow-x-auto">
			<h2 className="sr-only">Operation Tabs</h2>
			{options.map((option) => (
				<div
					onClick={() => setOperation(option.value)}
					className={`w-full rounded-t-xl border-2 p-1 px-3 ${
						operation === option.value
							? "bg-neutral-100 text-neutral-700 dark:bg-neutral-700 dark:text-neutral-100"
							: "bg-neutral-300 text-neutral-900 dark:bg-neutral-900 dark:text-neutral-300"
					} cursor-pointer text-center`}
					key={option.value}
				>
					<h3 className="whitespace-nowrap">{option.title}</h3>
				</div>
			))}
		</div>
	)
}

export default Tabs
