// src/components/OperationSelector.tsx

import { RefObject, FC } from "react"
import { useAppContext } from "../context/AppContext"
import Card from "./Card"

interface OperationSelectorProps {
	chooseButtonRef: RefObject<HTMLSelectElement>
}

const OperationSelector: FC<OperationSelectorProps> = ({ chooseButtonRef }) => {
	const { operation, setOperation } = useAppContext()

	const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
		setOperation(event.target.value)
	}

	return (
		<Card>
			<h2>Choose Operation:</h2>
			<select
				ref={chooseButtonRef}
				className="form"
				id="operation"
				value={operation}
				onChange={handleChange}
				aria-label="Select an operation"
				aria-live="polite"
				required
			>
				<option defaultValue="" value="" disabled>
					Select an operation
				</option>
				<option disabled className="font-bold">
					───
				</option>
				<optgroup label="Encoding">
					<option value="base64">Base64</option>
					<option value="hex">Hex</option>
					<option value="utf8">UTF-8</option>
					<option value="latin1">Latin-1</option>
					<option value="ascii">ASCII</option>
					<option value="url">URL</option>
				</optgroup>
				<optgroup label="Encryption">
					<option value="aes">AES</option>
					<option value="rsa">RSA</option>
				</optgroup>
				<optgroup label="Hashing">
					<option value="md5">MD5</option>
				</optgroup>
				<optgroup label="Compression">
					<option value="huffman">Huffman</option>
					<option value="lz77">LZ77</option>
					<option value="lzw">LZW</option>
					<option value="zstd">Zstd</option>
					<option value="deflate">Deflate</option>
					<option value="brotli">Brotli</option>
				</optgroup>
			</select>
		</Card>
	)
}

export default OperationSelector
