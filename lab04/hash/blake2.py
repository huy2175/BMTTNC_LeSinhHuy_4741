import hashlib

if __name__ == '__main__':
    samples = ['','abc','The quick brown fox jumps over the lazy dog']
    for s in samples:
        h = hashlib.blake2b(s.encode()).hexdigest()
        print(f"BLAKE2b('{s}') = {h}")
