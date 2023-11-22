from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import datetime

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def generate_certificate(pk_pem, nombre_jugador, player_password):
    """password_utf = player_password.encode('utf-8')
    hashed_password = SHA256.new(password_utf).digest()
    passphrase_str = hashed_password.hex()
    private_key = RSA.import_key(pk_pem, passphrase=passphrase_str)
    
    public_key = private_key.public_key()
    """

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    # Crear un certificado autofirmado
    builder = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, nombre_jugador)]))
        .issuer_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, nombre_jugador)]))
        .public_key(public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        # Puedes agregar más extensiones según tus necesidades
    )

    

    #Firmar el certificado con la clave privada
    certificado = builder.sign(
        private_key=private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    return certificado.public_bytes(encoding=serialization.Encoding.PEM).decode('utf-8')

def verify_certificate(public_key, certificado):
    try:
        certificado_autofirmado = x509.load_pem_x509_certificate(certificado, default_backend())
        public_key.verify(
            certificado_autofirmado.signature,
            certificado_autofirmado.tbs_certificate_bytes,
            padding.PKCS1v15(),
            certificado_autofirmado.signature_hash_algorithm,
        )
        if certificado_autofirmado.not_valid_before < datetime.datetime.utcnow() or datetime.datetime.utcnow() < certificado_autofirmado.not_valid_after:
            print("Certificado no valido")
    except Exception as e:
        print("Certificado no valido")
