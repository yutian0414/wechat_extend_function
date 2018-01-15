#/usr/bin/env python
#coding=utf8

import random
import hashlib
import requests
import pprint

translate_url=r"http://api.fanyi.baidu.com/api/trans/vip/translate"

class translate:

	appid='20180112000114487'
	secretKey= 'IRGh4Voe7jprWlajjsFe'

	def __init__(self,q,tolang,fromlang='auto'):

		self.fromlang=fromlang
		self.tolang=tolang
		self.q=q

		self.salt=str(random.randint(32768,65536))
		print((self.appid+self.q+self.salt+self.secretKey).encode('utf-8'))
		md5=hashlib.md5()
		md5.update((self.appid+self.q+self.salt+self.secretKey).encode('utf-8'))
		self.sign=md5.hexdigest()
		print(self.sign)
		self.url=translate_url+"?q="+self.q+"&from="+ self.fromlang +"&to="+ self.tolang +\
						"&appid="+ self.appid +"&salt="+ self.salt +"&sign="+ self.sign +""

	def tran_request(self):
		try:
			response=requests.get(self.url)
			pprint.pprint(response.json())
			result=response.json()
			res_txt=result['trans_result'][0]['dst']
			print(res_txt)
			return res_txt
		except Exception as e:
			print(e)
			return('translate fail')