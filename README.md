# cripto-p1
git reset --hard //este



##########################################################
cifrado simetrico y autenticado
from cryptography.fernet import Fernet

-----Usuario1------ mensaje es el dato a encriptar

key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(ataque)
// te guardas el token y la key. Duda de como guardar la key
-----Usuario2-----
f = Fernet(key)
ataque  = f.decrypt(token)
//consigues el mensaje

##################################################################
try:
    mensaje_desencriptado = fernet.decrypt(mensaje_cifrado)
    print("Mensaje desencriptado:", mensaje_desencriptado.decode('utf-8'))
except Exception as e:
    print("Error: No se pudo desencriptar el mensaje.")