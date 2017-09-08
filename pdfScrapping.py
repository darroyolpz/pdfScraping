import PyPDF2, glob, os, csv, sys
import pandas as pd

# Function to extract the pageContent ---------------------
def extractContent(pageNumber):
	pageObj = pdfReader.getPage(pageNumber)
	pageContent = pageObj.extractText()
	pageContent.strip()
	return pageContent
# ---------------------------------------------------------

# Function to get word index -----------------------------
def indexFunction(word, content):
	contentLen = len(content)
	wordLen = len(word)
	for i in range(contentLen):
		new_word = content[i:(i+wordLen)]
		if new_word == word:
			return(i)
			break
# ---------------------------------------------------------

# Function for pages, DV size and Line --------------------
def dvFunction():
	lookUp = 'Resumen de la unidad no.'
	for pageNumber in range(number_of_pages):
		pageContent = extractContent(pageNumber)
		if lookUp in pageContent:
			aPageStart.append(pageNumber)

	for pageNumber in aPageStart:
		# DV size
		wordStart = 'Danvent'
		wordEnd = 'Orden no.'
		pageContent = extractContent(pageNumber)
		posStart = pageContent.index(wordStart) + len(wordStart)
		newContent = pageContent[posStart:]
		if wordEnd in newContent:
			posEnd = indexFunction(wordEnd, newContent)
			print('Not found')
		elif wordEnd not in newContent:
			posEnd = newContent.index('Proyecto')
		unitFeature = newContent[:posEnd]
		unitFeature = unitFeature.strip()
		aDVSize.append(unitFeature)

		# Line
		wordStart = 'no.'
		wordEnd = 'Danvent'
		posStart = pageContent.index(wordStart) + len(wordStart)
		newContent = pageContent[posStart:]
		if wordEnd in newContent:
			posEnd = indexFunction(wordEnd, newContent)
			print('Not found')
		unitFeature = newContent[:posEnd]
		unitFeature = unitFeature.strip()
		aDVLine.append(unitFeature)

	aPageEnd = aPageStart[1:]
	aPageEnd.append(number_of_pages)
	# Sanity check
	w = len(aDVLine)
	x = len(aDVSize)
	y = len(aPageStart)
	z = len(aPageEnd)
	if (w == x == y == z):
		print('dvFunction OK')
		return aDVLine, aDVSize, aPageStart, aPageEnd
	elif not (w == x == y == z):
		print('Error in the lenght of the arrays in the dvFunction')
		sys.exit()
# ---------------------------------------------------------

# Function to get the starting pages list -----------------
def lookup(extList, Component, aWordStart, aWordEnd, aWordEndOp):
	inner = []
	for dvSize, dvLine, startPage, endPage in zip(aDVSize, aDVLine, aPageStart, aPageEnd):
		for pageNumber in range(startPage, endPage):
			print(fileName)
			print('Page number:', pageNumber)
			pageContent = extractContent(pageNumber)
			n = 1
			while (n>0):
				for wordStart, wordEnd, wordEndOp in zip(aWordStart, aWordEnd, aWordEndOp):
					if aWordStart.index(wordStart) == len(inner):
						print('Words to look up: ', wordStart, ', ', wordEnd)
						if wordStart not in pageContent:
							print('Start missing:', wordStart, 'at page', pageNumber)
							print('Next page: ', pageNumber + 1)
							print('\n')
							n -= 1
						elif wordStart in pageContent:						
							print(wordStart, 'found in page', pageNumber)		
							posStart = indexFunction(wordStart, pageContent) + len(wordStart)
							#posStart = pageContent.index(wordStart) + len(wordStart)
							print('posStart:', posStart)
							newContent = pageContent[posStart:]
							try:
								posEnd = indexFunction(wordEnd, newContent)
								#posEnd = newContent.index(wordEnd)
							except:
								posEnd = indexFunction(wordEndOp, newContent)
							if posEnd == None:
								print('posEnd not found')
								n -= 1
								break
							print('posEnd:', posEnd)
							unitFeature = newContent[:posEnd]
							if len(unitFeature) > 100:
								inner =[]
								n -= 1
								continue
							unitFeature = unitFeature.strip()
							print(unitFeature)
							inner.append(unitFeature)
							pageContent = newContent[posEnd:]
							n = pageContent.count(wordStart)
							print(n)
							print(inner)				
								
					if len(inner) == len(aWordStart):
						inner.insert(0, fileName)
						inner.insert(1, dvLine)
						inner.insert(2, dvSize)
						inner.insert(3, Component)
						extList.append(inner)
						print('This is the extList')
						print(extList)
						inner = []
					elif aWordStart.index(wordStart) != len(inner):
						n -= 1
						continue
	# With this we get a list of list with all the items
	return extList
# ---------------------------------------------------------

# Function to get the starting pages list -----------------
def lookup_count(extList, Component, aWordStart):
	inner = []
	for dvSize, dvLine, startPage, endPage in zip(aDVSize, aDVLine, aPageStart, aPageEnd):
		for pageNumber in range(startPage, endPage):
			print('Page number:', pageNumber)
			pageContent = extractContent(pageNumber)
			n = 1
			while (n>0):
				for wordStart in aWordStart:
					unitFeature = 0
					if aWordStart.index(wordStart) == len(inner):
						print('Words to look up:', wordStart)
						if wordStart not in pageContent:
							print('Start missing:', wordStart, 'at page', pageNumber)
							print('Next page: ', pageNumber + 1)
							print('\n')
							n -= 1
						elif wordStart in pageContent:						
							print(wordStart, 'found in page', pageNumber)		
							posStart = indexFunction(wordStart, pageContent) + len(wordStart)
							print('posStart:', posStart)
							newContent = pageContent[posStart:]
							unitFeature = unitFeature + 1
							print(unitFeature)
							inner.append(unitFeature)
							pageContent = newContent
							n = pageContent.count(wordStart)
							print(inner)				
								
					if len(inner) == len(aWordStart):
						inner.insert(0, fileName)
						inner.insert(1, dvLine)
						inner.insert(2, dvSize)
						inner.insert(3, Component)
						extList.append(inner)
						print('This is the extList')
						print(extList)
						inner = []
					elif aWordStart.index(wordStart) != len(inner):
						n -= 1
						continue
	# With this we get a list of list with all the items
	return extList
# ---------------------------------------------------------

# Function to get the starting pages list -----------------
def lookup_config(extList, Component, aWordStart):
	inner = []
	unitFeature = 0
	for dvSize, dvLine, startPage, endPage in zip(aDVSize, aDVLine, aPageStart, aPageEnd):
		for pageNumber in range(startPage, endPage):
			print('Page number:', pageNumber)
			pageContent = extractContent(pageNumber)
			for wordStart in aWordStart:
				unitFeature = 0
				if aWordStart.index(wordStart) == len(inner):
					print('Words to look up:', wordStart)
					if wordStart not in pageContent:
						print('Start missing:', wordStart, 'at page', pageNumber)
						print('Next page: ', pageNumber + 1)
						print('\n')
					elif wordStart in pageContent:						
						print(wordStart, 'found in page', pageNumber)		
						unitFeature = 1
						inner.append(unitFeature)			
							
				if len(inner) == len(aWordStart):
					inner.insert(0, fileName)
					inner.insert(1, dvLine)
					inner.insert(2, dvSize)
					inner.insert(3, Component)
					extList.append(inner)
					print('This is the extList')
					print(extList)
					inner = []
					unitFeature = 0

	# With this we get a list of list with all the items
	return extList
# ---------------------------------------------------------

# EC function ---------------------------------------------
def ecFunction(extList):
	Component = 'Motor'
	aWordStart = ['Tipo de motor', 'Potencia nominal', 'Velocidad (nominal)']
	aWordEnd = ['IEC-tamaño', 'Velocidad (nominal)', 'RPM']
	aWordEndOp = ['IEC-tamaño', 'Velocidad (nominal)', 'RPM']
	extList = lookup(extList, Component, aWordStart, aWordEnd, aWordEndOp)
	print('motorFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# AC function ---------------------------------------------
def acFunction(extList):
	Component = 'Motor'
	aWordStart = ['Tipos de motor', 'Potencia total', 'Velocidad (nominal)']
	aWordEnd = ['IEC-tamaño', 'Velocidad (nominal)', 'RPM']
	aWordEndOp = ['IEC-tamaño', 'Velocidad (nominal)', 'RPM']
	extList = lookup(extList, Component, aWordStart, aWordEnd, aWordEndOp)
	print('motorFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Impeller function ---------------------------------------
def impellerFunction(extList):
	Component = 'Impeller'
	aWordStart = ['Ventilador tipo']
	aWordEnd = ['Descripción del ventilador']
	aWordEndOp = ['Descripción del ventilador']
	extList = lookup(extList, Component, aWordStart, aWordEnd, aWordEndOp)
	print('impellerFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Filters function ----------------------------------------
def filtersFunction(extList):
	Component = 'Filters'
	aWordStart = ['Clase de filtro', 'Longitud del filtro']
	aWordEnd = ['Dimensión', 'mm']
	aWordEndOp = ['Dimensión', 'mm']
	extList = lookup(extList, Component, aWordStart, aWordEnd, aWordEndOp)
	print('filtersFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Rotary function -----------------------------------------
def rotFunction(extList):
	Component = 'Rotary HE'
	aWordStart = ['Tipo de intercambiador de calor', 'Eficiencia (Espacio entre aletas)', 'Descripción']
	aWordEnd = ['(', 'Diámetro', 'Motor']
	aWordEndOp = ['Eficiencia', 'Diámetro', 'Motor']
	extList = lookup(extList, Component, aWordStart, aWordEnd, aWordEndOp)
	for i in extList:
		try:
			if len(i[5]) > 50:
				extList.remove(i)
		except:
			continue
	print('rotFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Plate function ------------------------------------------
def plateFunction(extList):
	Component = 'Plate HE'
	aWordStart = ['Modelo de intercambiador de calor']
	aWordEnd = ['Distancia']
	aWordEndOp = ['Distancia']
	extList = lookup(extList, Component, aWordStart, aWordEnd, aWordEndOp)
	print('plateFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# By-pass function ----------------------------------------
def bypassFunction(extList):
	Component = 'By-pass Dampers'
	aWordStart = ['de bypass']
	extList = lookup_count(extList, Component, aWordStart)
	print('controlFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Dampers function ----------------------------------------
def dampersFunction(extList):
	Component = 'Dampers'
	aWordStart = ['Lamas de las compuertas']
	extList = lookup_count(extList, Component, aWordStart)
	print('dampersFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Sound function ------------------------------------------
def soundFunction(extList):
	Component = 'Sound att.'
	aWordStart = ['Material del silenciador']
	aWordEnd = ['Banda de frecuencia']
	aWordEndOp = ['Banda de frecuencia']
	extList = lookup(extList, Component, aWordStart, aWordEnd, aWordEndOp)
	print('soundFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Config function -----------------------------------------
def configFunction(extList):
	Component = 'Double Height'
	aWordStart = ['La unidad de extracción consiste en']
	extList = lookup_count(extList, Component, aWordStart)
	print('configFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Control function ----------------------------------------
def controlFunction(extList):
	Component = 'Control'
	aWordStart = ['Sistema de control integrado']
	extList = lookup_count(extList, Component, aWordStart)
	print('controlFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Export to csv -------------------------------------------
def createDataframe(extList):
	Header = ['Filename', 'Line', 'DV', 'Component',
			'Value1', 'Value2', 'Value3', 'Value4']
	df = pd.DataFrame(columns = Header)
	# Loop through the list
	for i in extList:
		n = len(i)
		# Fill the dataframe with the values
		if n == 5:
			df = df.append({'Filename': i[0], 'Line': i[1], 'DV': i[2],
							'Component': i[3], 'Value1': i[4]}, ignore_index = True)
		elif n == 6:
			df = df.append({'Filename': i[0], 'Line': i[1], 'DV': i[2],
							'Component': i[3], 'Value1': i[4], 'Value2': i[5]},
							ignore_index = True)
		elif n == 7:
			df = df.append({'Filename': i[0], 'Line': i[1], 'DV': i[2],
							'Component': i[3], 'Value1': i[4], 'Value2': i[5],
							'Value3': i[6]}, ignore_index = True)
		elif n == 8:
			df = df.append({'Filename': i[0], 'Line': i[1], 'DV': i[2],
							'Component': i[3], 'Value1': i[4], 'Value2': i[5],
							'Value3': i[6], 'Value4': i[7]}, ignore_index = True)
	return df
# ---------------------------------------------------------

# To Excel ------------------------------------------------
def toExcel(df):
	# Export to csv
	try:
		writer = pd.ExcelWriter('ordersSummary.xlsx')
		df.to_excel(writer, index = False)
		print('Done bro!')
	except:
		writer = pd.ExcelWriter('newOrdersSummary.xlsx')
		df.to_excel(writer, index = False)
		print('New newOrdersSummary.xlsx has been created')
		print('Done bro!')
# ---------------------------------------------------------

# DoTheMagic ----------------------------------------------
def doTheMagic(extList):	
	extList = dampersFunction(extList)
	extList = bypassFunction(extList)
	extList = filtersFunction(extList)
	extList = configFunction(extList)
	extList = controlFunction(extList)
	extList = ecFunction(extList)
	extList = acFunction(extList)
	extList = impellerFunction(extList)
	extList = rotFunction(extList)
	extList = plateFunction(extList)
	extList = soundFunction(extList)
# ---------------------------------------------------------	

# Main ----------------------------------------------------
# Open file and read it
path = os.path.dirname(os.path.realpath(__file__))
num_files = len(glob.glob1(path,'*.pdf'))

extList = []

for fileName in glob.glob('*.pdf'):
	# Initialize ----------------------------------------------
	aPageStart = []
	aPageEnd = []
	aDVSize = []
	aDVLine = []
	aPageStart = []	
	# ---------------------------------------------------------
	fileName = fileName[:-4]
	pdfFileObj = open(fileName + '.pdf', 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	number_of_pages = pdfReader.getNumPages()
	print('Number of pages:', number_of_pages)
	aDVLine, aDVSize, aPageStart, aPageEnd = dvFunction()
	doTheMagic(extList)
	pdfFileObj.close()

df = createDataframe(extList)
toExcel(df)
