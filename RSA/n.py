import base64
import struct
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def extract_rsa_pubkey_from_ssh(ssh_pub_key):
    """Extracts modulus (n) from an SSH RSA public key."""
    key_parts = ssh_pub_key.strip().split()
    key_data = base64.b64decode(key_parts[1])

    # Read SSH key format header
    parts = []
    while key_data:
        dlen = struct.unpack(">I", key_data[:4])[0]
        parts.append(key_data[4:4 + dlen])
        key_data = key_data[4 + dlen:]

    if parts[0] != b'ssh-rsa':
        raise ValueError("Not a valid RSA key")

    e = int.from_bytes(parts[1], byteorder="big")
    n = int.from_bytes(parts[2], byteorder="big")

    return n, e

# Load id_rsa.pub
with open("id_rsa.pub", "r") as f:
    ssh_pub_key = f.read()

n, e = extract_rsa_pubkey_from_ssh(ssh_pub_key)

print(f"Modulus (n): {int(n)}")
print(f"Exponent (e): {e}")


