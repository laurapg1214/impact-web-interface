"""
enforce:

for database.py
- mysql-connector
- pandas

for passwords.py
- maskpass (to mask pw as entered)
- base64 (encrypt)
- secrets (for token_bytes, 
generating cryptographically-secure 16 byte (128 bit) 
(or whatever length you want) random salt value
secrets is designed for cryptography
- hashlib (implements standardized cryptographic hash functions for
securely encoding text & bytes) - using sha256

"""