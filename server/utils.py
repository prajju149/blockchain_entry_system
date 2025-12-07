import base64
import hashlib
import os

import qrcode
from PIL import Image


def ensure_dir(p):
    """Create directory if it doesn't exist."""
    try:
        os.makedirs(p, exist_ok=True)
    except Exception:
        pass


def image_fingerprint(path, size=(64, 64)):
    """Generate perceptual fingerprint for an image."""
    img = Image.open(path).convert('L').resize(size, Image.Resampling.BILINEAR)
    pixels = list(img.getdata())
    avg = sum(pixels) / len(pixels)
    bits = ''.join(['1' if p > avg else '0' for p in pixels])
    return hex(int(bits, 2))[2:]


def audio_fingerprint(path):
    """Generate fingerprint for audio file."""
    with open(path, 'rb') as f:
        data = f.read(4096)
    return hashlib.sha256(data).hexdigest()


def generate_qr_for_resident(resident, storage, out_dir=None):
    """Generate QR code for resident."""
    out_dir = out_dir or (storage.base / 'qrs')
    ensure_dir(out_dir)
    payload = resident['id']
    img = qrcode.make(payload)
    out_path = out_dir / f"{resident['id']}.png"
    img.save(out_path)
    return str(out_path)
