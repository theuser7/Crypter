from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Protocol.KDF import scrypt
from argparse import RawDescriptionHelpFormatter
import argparse,os


class Crypter:
    def __init__(self, password, filein, fileout):
        self.password = password
        self.filein = filein
        self.fileout = fileout


    def Encrypter(self):
        salt = self.password.encode()
        key = scrypt(self.password.encode(), salt, 32, N=2**14, r=8, p=1)
        ctr = Counter.new(128)
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        with open(self.filein,'rb') as fi:
            with open(self.fileout,'wb') as fo:
                print("Encrypting...")
                while True:
                    chunk = fi.read()
                    if len(chunk) == 0:
                        break
                    enc = cipher.encrypt(chunk)
                    fo.write(enc)


    def Decrypter(self):
        salt = self.password.encode()
        key = scrypt(self.password.encode(), salt, 32, N=2**14, r=8, p=1)
        ctr = Counter.new(128)
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        with open(self.filein,'rb') as fi:
            with open(self.fileout,'wb') as fo:
                print("Decrypting...")
                while True:
                    chunk = fi.read()
                    if len(chunk) == 0:
                        break
                    dec = cipher.decrypt(chunk)
                    fo.write(dec)

def main():
    parser = argparse.ArgumentParser(prog='Crypter.py',formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Encrypt files with AES 256-bit using Crypter tool.",
        epilog="""

        Example to encrypt:
            python3 crypter.py -e -f filename.pdf -k password -o filename.pdf.bin
    

        Example to decrypt:
            python3 crypter.py -d -f filename.pdf.bin -k password -o filename.pdf""")

    parser.add_argument('-e','-E', action='store_true', help='  Action encrypt.')
    parser.add_argument('-d','-D', action='store_true', help='  Action decrypt.')
    parser.add_argument('-k', type=str, help='  Password, minimum password length 8 digits.',required=True)
    parser.add_argument('-f', type=str, help='  Input file path.', required=True)
    parser.add_argument('-o', type=str, help='  Output file path.', required=True)
    args = parser.parse_args()


    if args.e == True and args.d == True:
        raise Exception("Choose -e or -d action.")

    if args.e == False and args.d == False:
        raise Exception("Choose -e or -d action.")

    if not os.path.exists(args.f):
        raise Exception("File not found.")

    if os.path.exists(args.o):
        raise Exception("This filename already exists.")

    if len(args.k) < 8 or len(args.k) > 32:
        raise Exception("Very small password.")
    
    if args.e and args.f and args.k and args.o:
        if args.f.endswith(".bin"):
            raise Exception("The file is encrypted.")
        if not args.o.endswith(".bin"):
            raise Exception("Use the '.bin' extension after the encrypted output file extension.")
        cryp = Crypter(args.k, args.f, args.o)
        cryp.Encrypter()

    elif args.d and args.f and args.k and args.o:
        if not args.f.endswith(".bin"):
            raise Exception("The file is not encrypted.")
        if args.o.endswith(".bin"):
            raise Exception("Use the decrypted output file name without the '.bin' extension.")
        cryp = Crypter(args.k, args.f, args.o)
        cryp.Decrypter()


if __name__ == "__main__":
    main()
