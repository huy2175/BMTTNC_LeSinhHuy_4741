import hashlib


def main():
    text = input("Nhap chuoi van ban: ")
    sha3_hash = hashlib.sha3_256(text.encode()).hexdigest()

    print(f"Chuoi van ban da nhap: {text}")
    print(f"SHA-3 Hash: {sha3_hash}")


if __name__ == '__main__':
    main()
