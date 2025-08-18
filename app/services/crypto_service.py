import base64
import os
import logging
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CryptoService:
    def __init__(self):
        self.private_key = self._load_private_key()
    
    def _load_private_key(self):
        try:
            private_key_b64 = os.getenv('PRIVATE_KEY')
            if not private_key_b64:
                raise ValueError("PRIVATE_KEY not found in environment variables")
            
            private_key_pem = base64.b64decode(private_key_b64)
            
            private_key = serialization.load_pem_private_key(
                private_key_pem,
                password=None,
            )
            
            logger.info("RSA private key loaded successfully")
            return private_key
            
        except Exception as e:
            logger.error(f"Error loading private key: {e}")
            raise
    
    def decrypt_credentials(self, encrypted_data: str) -> Dict[str, str]:
        try:
            logger.info(f"Starting data decryption: {encrypted_data}")

            encrypted_bytes = base64.b64decode(encrypted_data)
            
            decrypted_bytes = self.private_key.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            decrypted_str = decrypted_bytes.decode('utf-8')
            credentials = json.loads(decrypted_str)
            
            logger.info("Credentials decrypted successfully")
            
            if 'email' not in credentials or 'password' not in credentials:
                raise ValueError("Decrypted data does not contain email and password")
            
            return credentials
            
        except Exception as e:
            logger.error(f"Error decrypting credentials: {e}")
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def is_encrypted_format(self, data: str) -> bool:
        try:
            base64.b64decode(data)
            return len(data) > 100
        except:
            return False