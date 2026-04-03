#import hashlib

#if __name__ == '__main__':
#    samples = ['','abc','The quick brown fox jumps over the lazy dog']
#    for s in samples:
#        h = hashlib.sha256(s.encode()).hexdigest()
#        print(f"SHA-256('{s}') = {h}")
import hashlib

def hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

if __name__ == "__main__":
    # same style như ảnh
    data = input("Nhập dữ liệu để hash bằng SHA-256: ")
    digest = hash_sha256(data)
    print("Giá trị hash SHA-256:", digest)