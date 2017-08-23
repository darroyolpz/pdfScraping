import PyPDF2, glob, os, csv
import pandas as pd

# Create the empty dataframe
Header = ['Component', 'Value1', 'Value2', 'Value3', 'Value4']
df = pd.DataFrame(columns = Header)

# Motor function ------------------------------------------
# Key values to be change for every component
Component = 'Motor'
aStart = ['Tipo de motor', 'Potencia nominal', 'Velocidad (nominal)', 'Tensión']
aEnd = ['IEC-tamaño', 'kW', 'RPM', 'V']

# Open file and read it
fileName = 'HOTEL CANALEJAS'
pdfFileObj = open(fileName + '.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# Get the total number of pages
number_of_pages = pdfReader.getNumPages()
print('Number of pages:', number_of_pages)

for pageNumber in range(number_of_pages):
	nextPage = False
	print('Page number: ', pageNumber)
	pageObj = pdfReader.getPage(pageNumber)
	pageContent = pageObj.extractText()
	pageContent.strip()
	# Create an empty list
	values = []

	# Actual loop looking up the values
	for wordStart, wordEnd in zip (aStart, aEnd):
		# Assumption 1: Words are ordered sequentially
		# Assumption 2: Both start and end word are in the same line
		print('Words to look up: ', wordStart, ', ', wordEnd)
		if wordStart not in pageContent:
			print('Start missing:', wordStart, 'at page', pageNumber)
			print('Next page: ', pageNumber + 1)
			print('\n')
			nextPage = True
		elif wordStart in pageContent:
			# Start position
			posStart = pageContent.index(wordStart) + len(wordStart)
			# New content for start
			newContent = pageContent[posStart:]
			newContent = newContent.strip()
			# End position
			posEnd = newContent.index(wordEnd)
			# New content for end
			unitFeature = newContent[:posEnd]
			unitFeature = unitFeature.strip()
			values.append(unitFeature)
			# Trim for next look up
			pageContent = newContent[posEnd:]
			nextPage == False

	if nextPage == False:
		# Fill the dataframe with the values
		df = df.append({'Component': Component, 'Value1': values[0], 'Value2': values[1],
						'Value3': values[2], 'Value4': values[3]}, ignore_index = True)
		print(df)
		print('\n')

# Export to csv or Excel. This is the very last step, once the dataframe is completed
try:
	df.to_csv('New.csv', index = False)
	print('Done bro!')
except:
	print('Please close the file')
