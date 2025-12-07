import sys

import qrcode

if __name__=='__main__':
    if len(sys.argv)<2:
        print('Usage: python generate_qr.py <resident_id> [out.png]')
        sys.exit(1)
    rid = sys.argv[1]
    out = sys.argv[2] if len(sys.argv)>2 else f'{rid}.png'
    img = qrcode.make(rid)
    img.save(out)
    print('Saved', out)
