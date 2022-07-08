# Uncrackable
Generador de contraseñas indecifrables a partir de una contraseña fácil de recordar. Es más simple recordar una contraseña y con ello 
generar Contraseñas Fuertes. Con los mismos parametros, siempre generaremos las mismas palabras.

Para esto, utilizando la función 'getUncrackablePasswords' permite a partir de una contraseña fácil de recordar, una cantidad infinita de contraseñas fuertes. 
Con los mismos parámetros, siempre se generan las misma contraseñas fuertes, esto permite poder guardar la fácil y siempre generar las 
contraseñas fuertes para su uso diario.

## Ejemplos de Uso:

```Python
uncrkPwd = getUncrackablePasswords

passwd = uncrkPwd('contraseñaFacil123', out_json=True)
print(passwd)
pwd_dict = json.loads(passwd)
print('Pwd-01 len:', len(pwd_dict['pwd-01']))
# Output: Obtenemos 1 contraseña con la palabara "ContraseñaFacil123"
# {
#   "pwd-01": "{Mi&?h2~0ccWPWVj.g#.yn"
# }
# Pwd-01 len: 22

passwd = uncrkPwd('contraseñaFacil123', 3, out_json=True)
print(passwd)
# Output: Obtenemos 3 palabras con longitudes entre 20 y 32 por defecto, todas a raiz de la misma contraseña.
# {
#   "pwd-01": "{Mi&?h2~0ccWPWVj.g#.yn",
#   "pwd-02": "=?a#BY}A6oyMG}}KKd4IJ?a*y2QD?",
#   "pwd-03": "&JYEn.jQ{im$GnnbbAHe4EBVL"
# }

passwd = uncrkPwd('contraseñaFacil123', qty=3, length=24, out_json=True)
print(passwd)
# Output: Obtenemos 3 palabras con longitud 24, todas a raiz de la misma contraseña.
# {
#   "pwd-01": "={Mi&?h2~0ccWPWVj.g#.ynk",
#   "pwd-02": "=?a#BY}A6oyMG}}KKd4IJ?a*",
#   "pwd-03": "y2QD?N&JYEn.jQ{im$GnnbbA"
# }

passwd = uncrkPwd('contraseñaFacil123', punc=False, length=32, out_json=True)
print(passwd)
# Es posible quitar: lower=False, upper=False, digits=False
# y añadir caracteres extras con charset='¡¿¬' por ejemplo.
# Output: Obtenemos una contraseña de longitud 32 pero sin signos de puntuación:
# {
#   "pwd-01": "FxQj3Gj9z8eeYTYXk6h16wnkFGd1IZyH"
# }

passwd = uncrkPwd('contraseña facil 123', only='0123456789ABCDEF', length=32, out_json=True)
print(passwd)
# Output: Obtenemos una contraseña de longitud 32 pero solamente con los caracteres dados:
# {
#   "pwd-01": "419093CDE66CC9C936558216BB85B7C2"
# }
```
