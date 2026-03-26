import os

def compress(DATA, key):
    key_bytes = key.encode()
    DATA_bytes = DATA.encode()
    key_len = len(key_bytes)
    return bytes([b ^ key_bytes[i % key_len] for i, b in enumerate(DATA_bytes)])

def decompress(DATA_bytes, key):
    key_bytes = key.encode()
    key_len = len(key_bytes)
    decoded = bytes([b ^ key_bytes[i % key_len] for i, b in enumerate(DATA_bytes)])
    return decoded.decode()

read = bool(int(input('Enter 1 to read/decode, 0 to write/compress: ')))
file_name = input('Enter a file name: ')
key = input('Enter a key: ')

if read:
    with open(file_name, 'rb') as f:   # read in binary mode
        data = f.read()
    print('Decoded message:')
    print(decompress(data, key))
else:
    with open(file_name, 'r', encoding='utf-8') as f:
        data = f.read()
    out_file = f'{os.path.splitext(file_name)[0]}.ktcx'
    with open(out_file, 'wb') as f:
        f.write(compress(data, key))
    print(f'Saved as {out_file}')