import PyPDF2 
import textract
import re
import csv

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



################################### PARTE PARA EL REGISTRO ###################################


global global_registro
global_registro = "" #INICIALIZAMOS LA VARIABLE REGISTRO. SI ES UN " ENTONCES SE USAR LA ANTERIOR

def set_global_registro(registro):
	global global_registro
	global_registro = registro


def limpiar_array_registro(array_registro):

	global global_registro

	aux_array_registro = []

	print(array_registro)

	if len(array_registro) == 0 :
		return []

	for i in range(0, len(array_registro)):
		if array_registro[i] != '"' and array_registro[i] != ' ':
			aux_array_registro.append(array_registro[i])

	if aux_array_registro == []:
		return global_registro

	else :
		global_registro = "" #reiniciamos global_registro
		for i in range(0, len(aux_array_registro)):
			if aux_array_registro[i].find('2020-11-19')>-1 :
				break
			global_registro = global_registro + aux_array_registro[i]

	return global_registro



################################### PARTE PARA EL REGISTRO ###################################

################################### PARTE PARA EL TITULAR ###################################


global global_titular
global_titular = "" #INICIALIZAMOS LA VARIABLE REGISTRO. SI ES UN " ENTONCES SE USAR LA ANTERIOR

def set_global_titular(titular):
	global global_titular
	global_titular = titular


################################### PARTE PARA EL TITULAR ###################################



### TAREAS LIMPIAR EL REGISTRO DE UN INMUEBLE


class Inmueble:
	def __init__(self, parametros, pagina):

		global global_registro
		global global_titular
		

		self.error = False
		self.pagina = pagina
		print(pagina)
		self.registro = ''
		array_registro = []

		if len(parametros) < 5:
			self.error = True
			self.municipio =  ""
			self.distinto =  ""
			self.titular =  ""
			self.titulo = ""
			self.tipo = ""
			self.templo = ""


		else :
			
			#SACAMOS ORDEN Y REGISTRO
			for i in range(0, len(parametros)-1):

				if parametros[i].isdigit() == True or parametros[i].find(' bis')>0:
					
					pivote_orden = i
					self.orden = parametros[i]
					break
			
			#NO FUNCIONA YA QUE LOS REGISTROS LOS PUEDE PASAR AL FINAL DE LA PAGINA Y NO HAY MANERA DE LOCALIZAR
				else :
					array_registro.append(parametros[i]) #TENEMOS QUE LIMPIAR EL REGISTRO

			#NO FUNCIONA YA QUE LOS REGISTROS LOS PUEDE PASAR AL FINAL DE LA PAGINA Y NO HAY MANERA DE LOCALIZAR
			#self.registro = limpiar_array_registro(array_registro) 
			self.registro = ""

			
			parametros = parametros[pivote_orden+1:]
			#FIN SACAMOS ORDEN Y REGISTRO (primer parametro ahora en parametros es municipio o siguientes si acaba en espacio)
			
			# LIMPIAMOS PARAMETROS PARA QUE NO SE JUNTE EL SI CON EL ANTERIOR
			for i in range(1, len(parametros)):
				
				if (parametros[i].strip() == 'SI' or parametros[i].strip() == 'NO'):
					parametros[i-1] = parametros[i-1].strip()
					parametros[i] = parametros[i].strip()

			linea_formateada = []
			aux = ''

			for i in range(0, len(parametros)):

				if parametros[i] != '' and parametros[i][-1] != " " and parametros[i][-1] != "-":

					if aux == '' :

						linea_formateada.append(parametros[i])

					else :

						linea_formateada.append(aux + parametros[i])
						aux = ''

				else :

					aux = aux + parametros[i]

			#ASIGNAMOS DATOS AL INMUEBLE

			self.municipio = linea_formateada[0]
			self.distinto = linea_formateada[-1]
			self.titular = linea_formateada[-2].strip()
			self.titulo = ""
			self.tipo = ""
			self.templo = "NO"


			if len(linea_formateada) == 6:
				self.titulo = linea_formateada[1]
				self.tipo = linea_formateada[2]
				self.templo = linea_formateada[3]


			if len(linea_formateada) == 4:
				self.tipo = linea_formateada[1]


			if len(linea_formateada) == 5:

				if linea_formateada[2] == 'SI' or linea_formateada[2] == 'NO' or linea_formateada[2] == 'sólo consta parcela':
					self.tipo = linea_formateada[1]
					self.templo = linea_formateada[2]

				else :
					self.titulo = linea_formateada[1]
					self.tipo = linea_formateada[2]

			if self.titular == '"' :
				self.titular = global_titular
			else :
				global_titular = self.titular

	def imprimir(self):
		print('o: ',self.orden, ' - m: ', self.municipio, ' - tit: ',  self.titulo,  ' - tip: ', self.tipo,  ' - tem: ', self.templo,  ' - tir: ', self.titular,  ' - dis: ', self.distinto, ' -pag: ', self.pagina)
		

	def parametros(self):
		return [self.orden,self.municipio,self.titulo,self.tipo,self.templo,self.titular,self.distinto,self.pagina]
		


#Write a for-loop to open many files (leave a comment if you'd like to learn how).

name = 'inmatriculaciones_limpio_removed'
filename = name + '.pdf'

#open allows you to read the file.

pdfFileObj = open(filename,'rb')

#The pdfReader variable is a readable object that will be parsed.
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#Discerning the number of pages will allow us to parse through all the pages.

#num_pages = pdfReader.numPages #NO LO NECESITAMOS
count = 0 # 0 - 1614 PAGINA EN LA QUE SE COMIENZA (HAY QUE RESTAR 1)
particion = 5204 #5204 - 1570 NUMERO DE PAGINAS PARA EXTRAER LA INFORMACION
num_pages = count + particion
text = ""

#The while loop will read each page.
while count < num_pages:
	pageObj = pdfReader.getPage(count) 
	count +=1
	text += pageObj.extractText()




#This if statement exists to check if the above library returned words. It's done because PyPDF2 cannot read scanned files.

if text != "":
	text = text

#If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.

else:
	text = textract.process(fileurl, method='tesseract', language='spa')

#Now we have a text variable that contains all the text derived from our PDF file. Type print(text) to see what it contains. It likely contains a lot of spaces, possibly junk such as '\n,' etc.
#Now, we will clean our text variable and return it as a list of keywords.


pagina = count-particion+1
palabra = text.split('\n')
palabra_empiece = palabra.index('Total')
palabra = palabra[palabra_empiece+1:]


linea = []
inmuebles = []


#print(palabra)

for i in range(1, len(palabra)):

	palabra[i] = palabra[i].replace('€','')

	#if palabra[i].find('16 FEB. 2021 13:10:46 Entrada: 88947') >  -1 or palabra[i].find('16 FEB. 2021 13:12:33 Entrada: 88949') > -1:
	if palabra[i].find('16 FEB. 2021') >  -1:
		pagina = pagina +1

	#if palabra[i] == 'SI' or palabra[i] == 'NO' and i>0: #EVITAMOS QUE LA ANTERIOR SE JUNTE
	#	linea[-1] = linea[-1].strip()
		
	if palabra[i] == "1" and (palabra[i-1] == 'SI' or palabra[i-1] == 'NO') and len(linea) >= 5: #hemos llegado al fin de linea para evitar la pagina 1614 ponemos lo de len

		print(linea)
		inmuebles.append(Inmueble(linea, pagina))
		linea = []

	else : # no hemos llegado al fin de linea

		linea.append(palabra[i])



lista_inmuebles = []
for inmueble in inmuebles :
	lista_inmuebles.append(inmueble.parametros())



with open(name + '.csv', 'w', newline='') as file:
	writer = csv.writer(file,quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
	#writer = csv.writer(file,delimiter=';')
	writer.writerows(lista_inmuebles)
