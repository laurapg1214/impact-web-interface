"""
enforce:

for database functions:
- mysql-connector
- pandas

for pw functions including create account & login:
- hashlib (implements standardized cryptographic hash functions for
securely encoding text & bytes) - using pbkdf2
- maskpass (to mask pw as entered)
- secrets (for token_bytes, 
generating cryptographically-secure 16 byte (128 bit) 
(or whatever length you want) random salt value
secrets is designed for cryptography

for .py


"""