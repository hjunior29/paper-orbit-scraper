#!/usr/bin/env python3

import base64
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization

def generate_public_key():
    """Generate public key from private key and return as base64"""
    load_dotenv()
    
    private_key_b64 = os.getenv('PRIVATE_KEY')
    if not private_key_b64:
        raise ValueError("PRIVATE_KEY not found in .env file")
    
    # Load private key
    private_key_pem = base64.b64decode(private_key_b64)
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)
    
    # Extract public key
    public_key = private_key.public_key()
    
    # Serialize public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Encode to base64
    public_key_b64 = base64.b64encode(public_key_pem).decode('utf-8')
    
    return public_key_b64

def main():
    print("🔑 Public Key Generator")
    print("=" * 40)
    
    try:
        public_key_b64 = generate_public_key()
        
        print("✅ Public key generated successfully!")
        print("=" * 60)
        print("PUBLIC KEY (base64):")
        print("=" * 60)
        print(public_key_b64)
        print("=" * 60)
        
        print("\n📝 Add this to your .env file:")
        print(f"PUBLIC_KEY={public_key_b64}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()