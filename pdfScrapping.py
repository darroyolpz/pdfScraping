# Release date: 27-11-2017

import PyPDF2, glob, os, csv, sys
import pandas as pd
import csv

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
	#lookUp = 'Resumen de la unidad no.' # For old format
	lookUp = 'Unit no.:' # For new format
	for pageNumber in range(number_of_pages):
		pageContent = extractContent(pageNumber)
		if lookUp in pageContent:
			aPageStart.append(pageNumber)

	for pageNumber in aPageStart:
		# DV size
		wordStart = 'Danvent' # For new format
		#wordEnd = 'Orden no.' # For old format
		wordEnd = 'Peso'
		pageContent = extractContent(pageNumber)
		posStart = pageContent.index(wordStart) + len(wordStart)
		newContent = pageContent[posStart:]
		if wordEnd in newContent:
			posEnd = indexFunction(wordEnd, newContent)
			print('Not found')
		elif wordEnd not in newContent:
			posEnd = newContent.index('Proyecto')
		unitFeature = newContent[:posEnd]
		unitFeature = unitFeature.replace(' ', '')	

		# Check for longer text when DV with roof and from 100 on
		if len(unitFeature)>5:
			unitFeature = unitFeature[0:5]
			last_val = unitFeature[-1:]
			if (last_val.isalpha()) or last_val == '-':
				unitFeature = unitFeature[0:4]
		print(unitFeature)
		print('\n')
		unitFeature = unitFeature.replace(' ', '')
		
		aDVSize.append(unitFeature)

		# Line
		#wordStart = 'no.' # For old format
		wordStart = 'Unit no.:' # For new format
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
def lookup(extList, Component, aWordStart, aWordEnd):
	inner = []
	for dvSize, dvLine, startPage, endPage in zip(aDVSize, aDVLine, aPageStart, aPageEnd):
		for pageNumber in range(startPage, endPage):
			print(fileName)
			print('Page number:', pageNumber)
			pageContent = extractContent(pageNumber)
			n = 1
			while (n>0):
				for wordStart, wordEnd in zip(aWordStart, aWordEnd):
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
							print('posStart:', posStart)
							newContent = pageContent[posStart:]
							posEnd = indexFunction(wordEnd, newContent)
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
							unitFeature = unitFeature.replace(' ', '')
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

			for wordStart in aWordStart:
				unitFeature = 0
				print('Words to look up:', wordStart)
				if wordStart not in pageContent:
					print('Start missing:', wordStart, 'at page', pageNumber)
					print('Next page: ', pageNumber + 1)
					print('\n')
				elif wordStart in pageContent:						
					print(wordStart, 'found in page', pageNumber)		
					posStart = indexFunction(wordStart, pageContent) + len(wordStart)
					print('posStart:', posStart)
					newContent = pageContent[posStart:]
					unitFeature = unitFeature + 1
					print(unitFeature)
					inner.append(unitFeature)
					pageContent = newContent
					print(inner)				
						
					# Everytime the word is found, place it in the inner list
					inner.insert(0, fileName)
					inner.insert(1, dvLine)
					inner.insert(2, dvSize)
					inner.insert(3, Component)
					extList.append(inner)
					print('This is the extList')
					print(extList)
					# Reset the inner list
					inner = []

	# With this we get a list of list with all the items
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

# Filters function ----------------------------------------
def filtersFunction(extList):
	Component = 'Filters'
	aWordStart = ['Clase de filtro', 'Longitud del filtro']
	aWordEnd = ['Dimensión', 'mm']
	extList = lookup(extList, Component, aWordStart, aWordEnd)

	# Naming the filters for dic
	for i in extList:
		try:
			# Check that it is a filter
			type = i[3]
			if type == Component:
				# Check that actually is a G4 or M5, F6, etc.
				bg = i[4][0]
				if (bg == 'F') or (bg == 'G') or (bg == 'M'):
					i.append(i[5])
					i[5] = i[4]
					i[4] = i[2]
		except:
			continue
	print('filtersFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# EC and AC function --------------------------------------
def ecacFunction(extList):
	Component = 'Motor'
	aWordStart = ['Tipo de motor', 'Potencia nominal', 'Velocidad (nominal)']
	aWordEnd = ['IEC-tamaño', 'Velocidad (nominal)', 'RPM']
	extList = lookup(extList, Component, aWordStart, aWordEnd)

	# IE3 poles function
	for i in extList:
		type = i[4]
		# Remove element if it's a IE4 motor
		if type == 'IE4,PM-Motor':
			extList.pop(extList.index(i))		
		elif type == 'IE3':
			per = 0.09
			try:
				rpm = int(i[6])
				print(rpm)
				print(rpm)
				if (rpm >= 1000 * (1 - per)) and (rpm <= 1000 * (1 + per)):
					i[6] = '6P'
				elif (rpm >= 1500 * (1 - per)) and (rpm <= 1500 * (1 + per)):
					i[6] = '4P'
				elif (rpm >= 3000 * (1 - per)) and (rpm <= 3000 * (1 + per)):
					i[6] = '2P'
				print(i[6])
				print('\n')
			except:
				continue
	print('motorFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Several EC or AC function -------------------------------
def ecacsFunction(extList):
	Component = 'Motor'
	aWordStart = ['Tipos de motor', 'Potencia total', 'Velocidad (nominal)']
	aWordEnd = ['IEC-tamaño', 'Velocidad (nominal)', 'RPM']
	extList = lookup(extList, Component, aWordStart, aWordEnd)

	# Handling two or more motors
	for i in extList:
		try:
			type = i[3]
			if type == Component:
				val = i[5]
				n = int(val[1]) - 1
				wordStart = 'x'
				wordEnd = ')'
				posStart = val.index(wordStart) + len(wordStart)
				newContent = val[posStart:]
				posEnd = indexFunction(wordEnd, newContent)
				unitFeature = newContent[:posEnd]
				unitFeature = unitFeature.replace(' ', '')
				i[5] = unitFeature
				for j in range(n):
					extList.append(i)
		except:
			continue

	# IE3 poles function
	for i in extList:
		type = i[4]
		# Remove element if it's a IE4 motor
		if type == 'IE4,PM-Motor':
			extList.pop(extList.index(i))		
		elif type == 'IE3':
			per = 0.09
			try:
				rpm = int(i[6])
				print(rpm)
				print(rpm)
				if (rpm >= 1000 * (1 - per)) and (rpm <= 1000 * (1 + per)):
					i[6] = '6P'
				elif (rpm >= 1500 * (1 - per)) and (rpm <= 1500 * (1 + per)):
					i[6] = '4P'
				elif (rpm >= 3000 * (1 - per)) and (rpm <= 3000 * (1 + per)):
					i[6] = '2P'
				print(i[6])
				print('\n')
			except:
				continue
	print('motorFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Single PM function --------------------------------------
def pmFunction(extList):
	Component = 'Motor'
	aWordStart = ['Tipo de motor', 'Potencia nominal', 'Velocidad, calculada']
	aWordEnd = [',', 'Velocidad, calculada', 'RPM']
	extList = lookup(extList, Component, aWordStart, aWordEnd)
	print('pmFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Several PM function -------------------------------------
def pmsFunction(extList):
	Component = 'Motor'
	aWordStart = ['Tipos de motor', 'Potencia total', 'Velocidad, calculada']
	aWordEnd = [',', 'Velocidad, calculada', 'RPM']
	extList = lookup(extList, Component, aWordStart, aWordEnd)
	# Handling two or more motors
	for i in extList:
		try:
			type = i[3]
			if type == Component:
				val = i[5]
				n = int(val[1]) - 1
				wordStart = 'x'
				wordEnd = ')'
				posStart = val.index(wordStart) + len(wordStart)
				newContent = val[posStart:]
				posEnd = indexFunction(wordEnd, newContent)
				unitFeature = newContent[:posEnd]
				unitFeature = unitFeature.replace(' ', '')
				i[5] = unitFeature
				for j in range(n):
					extList.append(i)
		except:
			continue
	print('pmsFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Impeller function ---------------------------------------
def impellerFunction(extList):
	Component = 'Impeller'
	aWordStart = ['Ventilador tipo']
	aWordEnd = ['Descripción del ventilador']
	extList = lookup(extList, Component, aWordStart, aWordEnd)

	# Handling when there are two or more impellers
	for i in extList:
		try:
			type = i[3]
			if type == Component:
				val = i[4]
				wordStart = 'x'
				if wordStart in val:
					n = int(val[2]) - 1
					posStart = val.index(wordStart) + len(wordStart)
					unitFeature = val[posStart:]
					unitFeature = unitFeature.strip()
					i[4] = unitFeature
					for j in range(n):
						extList.append(i)
		except:
			continue

	# Removing the size in the begining
	for i in extList:
		try:
			type = i[3]
			if type == Component:
				val = i[4]
				wordStart = '-'
				posStart = val.index(wordStart) + len(wordStart)
				unitFeature = val[posStart:]
				unitFeature = unitFeature.strip()
				i[4] = unitFeature
		except:
			continue

	# Removing the pro ending
	for i in extList:
		try:
			type = i[3]
			if type == Component:
				val = i[4]
				if len(val) > 5:
					val = val[:5]
				i[4] = val
		except:
			continue
	print('impellerFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Inverter function ---------------------------------------
def inverterFunction(extList):
	Component = 'Inverter'
	aWordStart = ['., [', 'A', 'Variador de frecuencia IP']
	aWordEnd = [']', 'us', 'montado']
	extList = lookup(extList, Component, aWordStart, aWordEnd)

	# Handling two or more inverters
	for i in extList:
		try:
			type = i[3]
			if type == Component:
				# Swap the position of num_inverters[5] and IP[6]
				i[5], i[6] = i[6], i[5]
				# Check how many inverters are in that motor
				num_inverters = int(i[6]) - 1
				# Remove the num_inverters to clean the item
				i.pop(6)
				# Add as many inverters as stated in the datasheet
				for j in range(num_inverters):
					extList.append(i)
		except:
			continue

	print('inverterFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Inverter for PM or several motors -----------------------
def inverterPMFunction(extList):
	Component = 'Inverter'
	aWordStart = ['de fábrica.  (', ')', 'Variador de frecuencia IP']
	aWordEnd = [' Amp', 'us', 'montado']
	extList = lookup(extList, Component, aWordStart, aWordEnd)

	# Handling two or more inverters
	for i in extList:
		try:
			type = i[3]
			if type == Component:
				# Swap the position of num_inverters[5] and IP[6]
				i[5], i[6] = i[6], i[5]
				# Check how many inverters are in that motor
				num_inverters = int(i[6]) - 1
				# Remove the num_inverters to clean the item
				i.pop(6)
				# Add as many inverters as stated in the datasheet
				for j in range(num_inverters):
					extList.append(i)
		except:
			continue

	print('inverterPMFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# For purchasing purpose ------------------------------------------------------
# Rotary function -----------------------------------------
def rotFunction(extList):
	Component = 'Rotary HE'
	aWordStart = ['Tipo de intercambiador de calor', 'Eficiencia (Espacio entre aletas)', 'Descripción']
	aWordEnd = ['(', 'Diámetro', 'Motor']
	extList = lookup(extList, Component, aWordStart, aWordEnd)
	for i in extList:
		try:
			type = i[3]
			if type == Component:
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
	extList = lookup(extList, Component, aWordStart, aWordEnd)
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
	extList = lookup(extList, Component, aWordStart, aWordEnd)
	print('soundFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Electrical Heater ---------------------------------------
def electricalFunction(extList):
	Component = 'Electrical Heater'
	aWordStart = ['Número de pasos', 'Potencia nominalkW', 'Tensión V']
	aWordEnd = ['Pasos', 'Tensión', 'Corriente']
	extList = lookup(extList, Component, aWordStart, aWordEnd)
	print('electricalFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------

# Absolute filters H10 ------------------------------------
def absFiltersFunction(extList):
	Component = 'Abs. Filters'
	aWordStart = ['absol']
	extList = lookup_count(extList, Component, aWordStart)
	print('absFiltersFunction OK')
	print('\n')
	return extList
# ---------------------------------------------------------


# -----------------------------------------------------------------------------

# Dataframe with dict -------------------------------------
def df_dict(extList):
	Header = ['Filename', 'Line', 'DV', 'Component',
			'Value1', 'Value2', 'Value3', 'Value4',
			'Description', 'Item no', 'Price']
	df = pd.DataFrame(columns = Header)

	# Create dictionary -----------------------------------
	reader = csv.reader(open('csvDB.csv'), delimiter=';')
	db = {}
	for row in reader:
	    key = row[0]
	    db[key] = row[1:]
	# -----------------------------------------------------
	
	# Loop through the list
	for i in extList:
		n = len(i)
		description_dict = '-'.join(i[4:n])
		try:
			item_no_dict = db[description_dict][0]
			price_dict = db[description_dict][1]
			# Fill the dataframe with the values
			if n == 5:
				df = df.append({'Filename': i[0], 'Line': i[1], 'DV': i[2],
								'Component': i[3], 'Value1': i[4], 
								'Description': description_dict,
								'Item no': item_no_dict, 'Price': price_dict}, ignore_index = True)
			elif n == 6:
				df = df.append({'Filename': i[0], 'Line': i[1], 'DV': i[2],
								'Component': i[3], 'Value1': i[4], 'Value2': i[5],
								'Description': description_dict,
								'Item no': item_no_dict, 'Price': price_dict}, ignore_index = True)
			elif n == 7:
				df = df.append({'Filename': i[0], 'Line': i[1], 'DV': i[2],
								'Component': i[3], 'Value1': i[4], 'Value2': i[5],
								'Value3': i[6], 'Description': description_dict,
								'Item no': item_no_dict, 'Price': price_dict}, ignore_index = True)
			elif n == 8:
				df = df.append({'Filename': i[0], 'Line': i[1], 'DV': i[2],
								'Component': i[3], 'Value1': i[4], 'Value2': i[5],
								'Value3': i[6], 'Value4': i[7], 
								'Description': description_dict,
								'Item no': item_no_dict, 'Price': price_dict}, ignore_index = True)
		except:
			# When the item is not found, place it without using dictionary
			if n == 5:
				df = df.append({'Filename': i[0], 'Line': i[1], 'DV': i[2],
								'Component': i[3], 'Value1': i[4]}, ignore_index = True)
			elif n == 6:
				df = df.append({'Filename': i[0], 'Line': i[1], 'DV': i[2],
								'Component': i[3], 'Value1': i[4], 'Value2': i[5]}, ignore_index = True)
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

# Dataframe WITHOUT dict ----------------------------------
def df_no_dict(extList):
	Header = ['Filename', 'Line', 'DV', 'Component',
			'Value1', 'Value2', 'Value3', 'Value4',
			'Description', 'Item no', 'Price']
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
							'Component': i[3], 'Value1': i[4], 'Value2': i[5]}, ignore_index = True)
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
def toExcel(df, name):
	# Export to Excel
	writer = pd.ExcelWriter(name)		
	df.to_excel(writer, index = False)
	print('Done bro!')
# ---------------------------------------------------------

# DoTheMagic ----------------------------------------------
def doTheMagic(extList, newList):
	extList = filtersFunction(extList)
	extList = ecacFunction(extList)
	extList = ecacsFunction(extList)
	extList = pmFunction(extList)
	extList = pmsFunction(extList)
	extList = impellerFunction(extList)
	extList = inverterFunction(extList)
	extList = inverterPMFunction(extList)

	newList = configFunction(newList)
	newList = controlFunction(newList)

	newList = absFiltersFunction(newList)
# ---------------------------------------------------------

# ForPurchasing -------------------------------------------
# Use the no_dict function to print
def purchasing(extList, newList):
	extList = filtersFunction(extList)
	extList = ecacFunction(extList)
	extList = ecacsFunction(extList)
	extList = pmFunction(extList)
	extList = pmsFunction(extList)
	extList = impellerFunction(extList)
	extList = inverterFunction(extList)
	extList = inverterPMFunction(extList)

	newList = configFunction(newList)
	newList = controlFunction(newList)

	newList = dampersFunction(newList)
	newList = bypassFunction(newList)
	newList = rotFunction(newList)
	newList = plateFunction(newList)
	newList = soundFunction(newList)
	newList = electricalFunction(newList)
	newList = absFiltersFunction(newList)
# ---------------------------------------------------------

# TestTheMagic --------------------------------------------
def testTheMagic(extList, newList):
	extList = inverterFunction(extList)
	extList = filtersFunction(extList)
	newList = configFunction(newList)	
# ---------------------------------------------------------		

# Main ----------------------------------------------------
# Open file and read it
path = os.path.dirname(os.path.realpath(__file__))
num_files = len(glob.glob1(path,'*.pdf'))

extList = []
newList = []

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
	doTheMagic(extList, newList)
	#testTheMagic(extList, newList)
	pdfFileObj.close()

# With dictionary
name = 'ordersSummary.xlsx'
df = df_dict(extList)
toExcel(df, name)

# Without dictionary, for the config and control
name = 'configSummary.xlsx'
df1 = df_no_dict(newList)
df1 = df1.drop_duplicates()
toExcel (df1, name)