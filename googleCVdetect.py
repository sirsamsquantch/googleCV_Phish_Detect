import io, os, urllib, re, sys, argparse
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

project = [full path to project.json]
urlscanKey = [urlscan api key]

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = project

keywords = {'MICROSOFT', 'ACCOUNT', 'DOCUMENT', 'ACCESS', 'GMAIL', 'O365', 'AOL', 'PASSWORD', 'PROVIDER'}
phrases = {'YOUR EMAIL PROVIDER', 'LOGIN WITH OTHER', 'OTHER EMAIL', 'WORK OR SCHOOL ACCOUNT', 'SIGN AND APPROVE DOCUMENTS', 'DOWNLOAD ATTACHMENT', 'USE YOUR MICROSOFT ACCOUNT', 'LOGIN WITH YAHOO', 'LOGIN WITH AOL','LOG IN TO VIEW DOCUMENT', 'ADOBE ID', 'RECEIVING EMAIL'}
foundText = []
foundPhrase = []

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url')

for x, y in enumerate(sys.argv):
	if sys.argv[x] == '-u' or sys.argv == '--url':
		url = sys.argv[x+1]

# url = raw_input('URL: ')
url = 'http://api.screenshotmachine.com/?key='+urlscanKey+'&dimension=800xfull&cacheLimit=0&format=gif&url='+url
urllib.urlretrieve(url, 'screenshot.png')

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'screenshot.png')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

textResponse = client.text_detection(image=image)
texts = textResponse.text_annotations

logoResponse = client.logo_detection(image=image)
logos = logoResponse.logo_annotations

labelResponse = client.label_detection(image=image)
labels = labelResponse.label_annotations

if len(logos) > 0:
	print('******* Logos *******')
	for logo in logos:
		print(logo.description)
else:
	print ('No logos found on page.')
	
# print('Labels: ')
# for label in labels:
	# print(label.description)

if len(texts) > 0:
	print('******* Text *******')
	for text in texts:
		# print(text.description)
		textDescription = text.description.upper()
		foundText.append(textDescription.encode('ascii', 'ignore'))
		
	for x, y in enumerate(foundText): # Get rid of all new line chars in foundText
		foundText[x] = re.sub('\n', ' ', foundText[x])

	print (foundText)
else:
	print ('No text on page.')

if len(foundText) > 0:
	for phrase in phrases:
		if phrase in foundText[0]:
			foundPhrase.append(phrase)	

	keywordMatch = list(set(foundText) & set(keywords))

	print ('***************************')
	print ("Threat Keywords Found:")
	for match in keywordMatch:
		print (match)
		
	print ('***************************')
	print ("Threat Phrases Found:")
	for match in foundPhrase:
		print (match)
print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])