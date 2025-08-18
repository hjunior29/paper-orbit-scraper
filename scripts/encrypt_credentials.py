
import base64
import json
import os
import urllib.parse
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def load_public_key_from_private():
    load_dotenv()
    
    private_key_b64 = os.getenv('PRIVATE_KEY')
    if not private_key_b64:
        raise ValueError("PRIVATE_KEY not found in .env file")
    
    private_key_pem = base64.b64decode(private_key_b64)
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)
    
    public_key = private_key.public_key()
    return public_key

def encrypt_credentials(email: str, password: str) -> str:
    public_key = load_public_key_from_private()
    
    credentials = {
        "email": email,
        "password": password
    }
    
    credentials_json = json.dumps(credentials)
    credentials_bytes = credentials_json.encode('utf-8')
    
    encrypted_bytes = public_key.encrypt(
        credentials_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    encrypted_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
    return encrypted_b64

def main():
    print("🔐 Kindle Credentials Encryptor")
    print("=" * 40)
    
    try:
        email = input("Amazon account email: ").strip()
        password = input("Amazon account password: ").strip()
        
        if not email or not password:
            print("❌ Email and password are required!")
            return
        
        print("\n🔄 Encrypting credentials...")
        encrypted_data = encrypt_credentials(email, password)
        
        encrypted_url_encoded = urllib.parse.quote(encrypted_data, safe='')
        
        print("\n✅ Credentials encrypted successfully!")
        print("=" * 60)
        print("ORIGINAL ENCRYPTED DATA:")
        print("=" * 60)
        print(encrypted_data)
        print("=" * 60)
        print("\nURL ENCODED ENCRYPTED DATA (copy to Postman):")
        print("=" * 60)
        print(encrypted_url_encoded)
        print("=" * 60)
        
        print(f"\n📝 To use in Postman:")
        print(f"   'encrypted' parameter: {encrypted_url_encoded}")
        print(f"   'email' and 'password' parameters: leave blank")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()