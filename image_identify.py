import requests
import base64
from config import API_KEY,APP_ID,SECRET_KEY
import pprint
import json

class image_identify:


	def __init__(self):

		self.image=''
		self.token=None

	def get_token(self):

		token_url='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ API_KEY +'&client_secret='+SECRET_KEY
		response=requests.get(token_url)
		self.token=json.loads(response.text)['access_token']
		print(self.token)

	def identify(self,image,detect_direction=False,):	

		if not self.token:
			self.get_token()
		identify_url='https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token='+self.token
		with open(image,'rb') as f:
			data_f=base64.b64encode(f.read()).decode('utf-8')
		data={	'image':data_f,
				'detect_direction':detect_direction
				}
		response=requests.post(identify_url,data=data,headers={'Content-Type':'application/x-www-form-urlencoded'})
		pprint.pprint(response.json())
		identify_text=[word.get('words','') for word in response.json()['words_result']]
		return(identify_text)


if __name__ == '__main__':
	im_id=image_identify()
	# im_id.get_token()
	result=im_id.identify('1.jpg')
	print(result)
