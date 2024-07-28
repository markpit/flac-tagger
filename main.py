def read_flac_metadata(file_path):
    with open(file_path, 'rb') as f:
        # Check the "fLaC" marker
        if f.read(4) != b'fLaC':
            raise ValueError("Not a valid FLAC file")

        metadata = {}
        while True:
            # Read the block header
            block_header = f.read(4)
            if len(block_header) < 4:
                break

            # Parse the block header
            last_block = block_header[0] & 0x80
            block_type = block_header[0] & 0x7F
            block_size = int.from_bytes(block_header[1:4], byteorder='big')

            # Read the block data
            block_data = f.read(block_size)

            if block_type == 4:  # VORBIS_COMMENT block
                vendor_length = int.from_bytes(block_data[0:4], byteorder='little')
                vendor_string = block_data[4:4 + vendor_length].decode('utf-8')
                metadata['vendor'] = vendor_string

                comment_list_length = int.from_bytes(block_data[4 + vendor_length:8 + vendor_length], byteorder='little')
                offset = 8 + vendor_length
                for _ in range(comment_list_length):
                    comment_length = int.from_bytes(block_data[offset:offset + 4], byteorder='little')
                    comment = block_data[offset + 4:offset + 4 + comment_length].decode('utf-8')
                    key, value = comment.split('=', 1)
                    metadata[key] = value
                    offset += 4 + comment_length

            if last_block:
                break

    return metadata







def main():
    file_path = 'test.flac'
    metadata = read_flac_metadata(file_path)
    for key, value in metadata.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()