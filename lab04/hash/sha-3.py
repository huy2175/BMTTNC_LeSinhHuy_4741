import hashlib

if __name__ == '__main__':
    samples = ['','abc','The quick brown fox jumps over the lazy dog']
    for s in samples:
        h = hashlib.sha3_256(s.encode()).hexdigest()
        print(f"SHA3-256('{s}') = {h}")
