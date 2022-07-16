# Tested in: Python 3.8.8
# By: LawlietJH
# Uncrackable v1.0.0
# Descripción: Generador de contraseñas indecifrables a partir de una contraseña fácil de recordar
#              Es más simple recordar una contraseña y con ello generar Contraseñas Fuertes.
#              Con los mismos parametros, siempre generaremos las mismas palabras.
#
# Idea General: La idea de esto es que sea una capa intermediaria en el uso de una contraseña.
#               Memorizas la contraseña fácil (o la almacenas), cuando quieras utilizarla la pasas
#               por la función getUncrackablePasswords (siempre con sus mismos parametros) y finalmente
#               la utilizas. Solo añade una capa de seguridad.
#
# Info Extra: Es posible obtener a partir de una misma palabra, infinitas contraseñas complejas, siempre en el mismo orden.

import string
import json

#=======================================================================
__author__  = 'LawlietJH'          # Desarrollador
__title__   = 'Uncrackable'        # Título
__version__ = 'v1.0.0'             # Versión
#=======================================================================

class Splitmix64:	# Pseudo-random number generator (PRNG). From: https://github.com/LawlietJH/Utils
	
	def __init__(self, seed=0):
		
		self.MASK64 = (1 << 64) - 1
		self.seed  = seed
		self.state = self.seed & self.MASK64
		
		self.use = '''
		\r Clase: Splitmix64       # Pseudo-random number generator. By: LawlietJH
		\r |
		\r + Descripción: 
		\r |    
		\r |    Splitmix64 es el algoritmo generador de números pseudoaleatorios
		\r |    predeterminado en Java y está incluido/disponible en muchos otros
		\r |    idiomas. Utiliza un algoritmo bastante simple que, aunque se
		\r |    considera pobre para fines criptográficos, es muy rápido de
		\r |    calcular y es "suficientemente bueno" para muchas necesidades de
		\r |    números aleatorios. Pasa varias pruebas de "aptitud" PRNG bastante
		\r |    rigurosas que fallan algunos algoritmos más complejos.
		\r |    
		\r |    Splitmix64 no se recomienda para requisitos exigentes de números
		\r |    aleatorios, pero a menudo se usa para calcular estados iniciales
		\r |    para otros generadores de números pseudoaleatorios más complejos.
		\r |    
		\r |    El splitmix64 "estándar" mantiene una variable de estado de 64
		\r |    bits y devuelve 64 bits de datos aleatorios con cada llamada.
		\r |    
		\r + Ejemplo de uso: 
		\r |    
		\r |    # Se debe generar un objeto de la clase Splitmix64
		\r |    splitmix64 = Splitmix64()
		\r |    
		\r |    # Seleccionamos una semilla
		\r |    splitmix64.seed = 1234567
		\r |    
		\r |    # Para obtener el primer número pseudo-aleatorio
		\r |    splitmix64.nextInt()
		\r |    
		\r |    # Salida: 6457827717110365317
		\r |    
		\r |    # Para obtener el número con un valor entre 0 y 1:
		\r |    splitmix64.nextFloat()
		\r |    
		\r |    # Para obtener el valor entero con un rango entre 0 y 5:
		\r |    splitmix64.nextIntInRange(5)			# Método 1
		\r |    splitmix64.nextIntInRange(0, 5)			# Método 2
		\r |    splitmix64.nextIntInRange((0, 5))		# Método 3
		\r |    
		\r |    # Salida (Posibles): 0, 1, 2, 3 o 4
		\r |    
		\r |    # Para obtener el valor entero con un rango entre 2 y 5:
		\r |    splitmix64.nextIntInRange(2, 5)			# Método 1
		\r |    splitmix64.nextIntInRange([2, 5])		# Método 2
		\r |    
		\r |    # Salida (Posibles): 2, 3 o 4
		\r |    
		\r |    # Es posible hacer lo mismo pero obteniendo valores flotantes
		\r |    splitmix64.nextFloatInRange(2, 5)
		\r |    
		\r |    # Salida (Posibles): Desde 2.0 hasta 5.0
		\r |    
		\r |    # Para reiniciar la semilla
		\r |    splitmix64.reset()
		\r |    
		\r |    # Es posible seleccionar otra semilla, y comenzará de nuevo
		\r |    splitmix64.semilla = 7654321
		\r \\
		'''
	
	def asc2Bin(self, text):
		if not text.__class__ == bytes:
			text = [ord(x) for x in text]
		bins = [bin(x)[2:].zfill(8 if len(bin(x)[2:]) <= 8 else 16) for x in text]
		return bins
	
	def bin2Asc(self, binary):
		
		if binary.__class__ == int:
			binary = str(binary)
		
		if binary.__class__ == str:
			
			bin_lis = []
			byte = ''
			
			for i, b in enumerate(binary):
				if i % 8 == 0 and not i == 0:
					bin_lis.append(byte)
					byte = b
				else:
					byte += b
			
			if len(byte): bin_lis.append(byte)
			
			binary = bin_lis
		
		nums = []
		
		for b in binary:
			
			b = int(b)
			
			if b == 0:
				nums.append(0)
				continue
			
			i = 0
			c = 0
			k = int(math.log10(b))+1
			
			for j in range(k):
				i = ((b%10)*(2**j))   
				b = b//10
				c = c+i
			
			nums.append(c)
		
		asc = ''.join([chr(n) for n in nums])
		
		return asc
	
	def bin2Dec(self, binary):
		try:
			decimal = int(binary, 2)
		except:
			decimal = int(str(binary), 2)
		return decimal
	
	def dec2Bin(self, decimal, raw=False):
		binary = bin(decimal)
		if not raw:
			binary = str(binary)[2:]
			lbin = (len(binary)//8) + (1 if len(binary)%8 > 0 else 0)
			binary = binary.zfill(lbin*8)
		return binary
	
	@property
	def seed_text(self):
		binary = self.dec2Bin(self.seedv)
		ascii_ = self.bin2Asc(binary)
		return ascii_
	
	@property
	def seed(self):
		return self.seedv
	
	@seed.setter
	def seed(self, num):
		if num.__class__ == str:
			num = ''.join(self.asc2Bin(num))
			num = self.bin2Dec(num)
		self.seedv = num
		self.state = num & self.MASK64
	
	def reset(self):
		self.state = self.seedv & self.MASK64
	
	def nextInt(self):
		'return random int between 0 and 2**64'
		z = self.state = (self.state + 0x9e3779b97f4a7c15) & self.MASK64
		z = ((z ^ (z >> 30)) * 0xbf58476d1ce4e5b9) & self.MASK64
		z = ((z ^ (z >> 27)) * 0x94d049bb133111eb) & self.MASK64
		number = (z ^ (z >> 31)) & self.MASK64
		return number
	
	def nextFloat(self):
		'return random float between 0 and 1'
		return self.nextInt() / (1 << 64)
	
	def nextFloatInRange(self, ini, end=None):
		
		if end == None:
			end = ini
			ini = None
		else:
			if not ini.__class__ == int:
				msg = f'The value {ini} is invalid.'
				raise TypeError(msg)
			elif not end.__class__ == int:
				msg = f'The value {end} is invalid.'
				raise TypeError(msg)
		
		if end.__class__ in (tuple, list) and len(end) == 2:
			ini = end[0]
			end = end[1]
			if ini > end:
				temp = ini
				ini = end
				end = temp
			dif = end - ini
			return (self.nextFloat() * (dif)) + ini
		elif end.__class__ == int:
			if ini.__class__ == int:
				if ini > end:
					temp = ini
					ini = end
					end = temp
				dif = end - ini
				return (self.nextFloat() * (dif)) + ini
			else:
				return (self.nextFloat() * (end))
		else:
			msg = f'The value {end} is invalid.'
			raise TypeError(msg)
	
	def nextIntInRange(self, ini, end=None):
		return int(self.nextFloatInRange(ini, end))



def getUncrackablePasswords(passwd, qty=1, length=(20, 32),
	lower=True, upper=True, digits=True, punc=True,
	charset='', only='', out_json=False):
	
	assert length.__class__ in [list, tuple, int], \
	'Se esperaban 2 valores "(start, end)" para el '
	f'rango de longitud de contraseña, no \'{length}\''
	
	if only.__class__ == str and not only == '':
		pwd_chrs = only
	else:
		pwd_chrs  = charset
		pwd_chrs += string.ascii_lowercase if lower  else ''
		pwd_chrs += string.ascii_uppercase if upper  else ''
		pwd_chrs += string.digits          if digits else ''
		pwd_chrs += '!@#$%&*+-/=?^_`{|}~.' if punc   else ''
	
	pwd_chrs  = ''.join(sorted(list(set(pwd_chrs))))
	pwd_chrs_l = len(pwd_chrs)
	
	SM64 = Splitmix64(passwd)
	
	out = { f'pwd-{n:02}':'' for n in range(1, qty+1) }
	
	for n in range(1, len(out)+1):
		
		pwd_num = f'pwd-{n:02}'
		
		if length.__class__ == int:
			pwd_len = length
		else:
			pwd_len = SM64.nextIntInRange(*length)
		
		for x in range(pwd_len):
			value = SM64.nextIntInRange(pwd_chrs_l)
			out[pwd_num] += pwd_chrs[int(value)]
	
	if out_json:
		out = json.dumps(out, indent=4)
	
	return out
