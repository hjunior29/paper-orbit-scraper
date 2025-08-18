#!/usr/bin/env python3

import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_key_pair():
    """Generate a new RSA key pair and return both keys as base64"""
    
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Convert to base64 for storing in .env
    private_key_b64 = base64.b64encode(private_pem).decode('utf-8')
    public_key_b64 = base64.b64encode(public_pem).decode('utf-8')
    
    return private_key_b64, public_key_b64, public_pem.decode('utf-8')

def main():
    print("🔐 RSA Key Pair Generator")
    print("=" * 40)
    
    try:
        private_key_b64, public_key_b64, public_key_pem = generate_rsa_key_pair()
        
        print("✅ RSA key pair generated successfully!")
        print("=" * 60)
        print("PRIVATE KEY (add to .env):")
        print("=" * 60)
        print(f"PRIVATE_KEY={private_key_b64}")
        print("=" * 60)
        print("PUBLIC KEY (add to .env):")
        print("=" * 60)
        print(f"PUBLIC_KEY={public_key_b64}")
        print("=" * 60)
        print("PUBLIC KEY PEM (for reference):")
        print("=" * 60)
        print(public_key_pem)
        print("=" * 60)
        
        print("\n📝 Next steps:")
        print("1. Copy both keys to your .env file")
        print("2. Share the PUBLIC_KEY with clients who need to encrypt data")
        print("3. Keep the PRIVATE_KEY secure and never share it")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()