import bcrypt

# Contraseña original
contraseña = "hola"

# Generar el hash de la contraseña
hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

print("Hash generado:", hashed_password.decode('utf-8'))
# Verificación de la contraseña
if bcrypt.checkpw(contraseña.encode('utf-8'), hashed_password):
    print("La contraseña es correcta")
else:
    print("La contraseña es incorrecta")