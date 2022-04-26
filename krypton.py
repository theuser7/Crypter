from Crypto.Cipher import AES
import argparse,os


def Encrypter(key, iv, infile, outfile):
    print("Encrypting...")
    enc = AES.new(key,AES.MODE_CBC,iv)
    with open(infile,'rb') as f:
        with open(outfile,'wb') as f2:
            while True:
                buff = f.read(1024)
                if len(buff) == 0:
                    break
                if len(buff)%AES.block_size != 0:
                    buff = buff*16
                f2.write(enc.encrypt(buff))


def Decrypter(key, infile, outfile):
    print("Decrypting...")
    with open(infile,'rb') as f:
        iv = f.read(16)
        dec = AES.new(key,AES.MODE_CBC,iv)
        with open(outfile,'wb') as f2:
            while True:
                buff = f.read(1024)
                if len(buff) == 0:
                    break
                f2.write(dec.decrypt(buff))


def main():
    parser = argparse.ArgumentParser(prog='krypton.py')
    parser.add_argument('-e','-E', action='store_true', help='  Action encrypt.')
    parser.add_argument('-d','-D', action='store_true', help='  Action decrypt.')
    parser.add_argument('-k', type=str, help='  Key, sizes avaiable: 16, 24 or 32 digits.',required=True)
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

    if len(args.k) != 16 and len(args.k) != 24 and len(args.k) != 32:
        print(f"Size of your current key: {len(args.k)} digits.\n")
        raise Exception("Key sizes: 16, 24 or 32 digits.")

    if args.e and args.f and args.k and args.o: 
        ivgen = os.urandom(16)
        Encrypter(args.k.encode(), ivgen, args.f, args.o)

    elif args.d and args.f and args.k and args.o:
        Decrypter(args.k.encode(), args.f, args.o)


print("""
    
                                            ██╗  ██╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ ███╗   ██╗
                                            ██║ ██╔╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗████╗  ██║
                                            █████╔╝ ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║██╔██╗ ██║
                                            ██╔═██╗ ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║██║╚██╗██║
                                            ██║  ██╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝██║ ╚████║
                                            ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═══╝                                                                                                    
""")


main()

