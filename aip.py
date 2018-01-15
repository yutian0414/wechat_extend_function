
import requests
import base64
import json
from pydub import AudioSegment
import wave
import io

class BaiduRest:
	api_key='e6BPibfIxqFSvoGb6GLGjpaX'
	secret_key= 'b5b89ab3b51b47975e7c9cae7351bd4c'
	cu_id=app_id='10671400'

	def __init__(self):
		self.token_url="https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
		self.getVoice_url="http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
		self.upvoice_url="http://vop.baidu.com/server_api"
		self.token_str=self.getToken(self.api_key,self.secret_key)

	def getToken(self,api_key,secret_key):
		token_url=self.token_url %(api_key,secret_key)
		r=requests.get(token_url)
		r_str=json.loads(r.text)
		print(r_str)
		return r_str['access_token']

	def getVoice(self,text,filename):
		getVoice_url=self.getVoice_url %(text,self.cu_id,self.token_str)
		voice_data=requests.get(getVoice_url)
		print(voice_data.content)
		fp=open(filename,'wb+')
		fp.write(voice_data.content)
		fp.close()	

#获取语音识别内容，
#  	1.打开原mp3文件，读取原始数据
#	2.将原始数据放到AudioSegment中进行处理
#	3.新建wav格式文件，设置参数，将处理后对数据写入
#	4.读取wav格式文件数据，并设置将发送对url参数
#	5.组合成url，进行post请求。
	def getText(self,filename):

		wav_fp=open(filename,'rb')
		data_f=wav_fp.read()
		wav_fp.close()
		print(type(data_f))
		aud=io.BytesIO(data_f)
		sound=AudioSegment.from_file(aud,format='mp3')
		raw_data=sound._data
		print(type(sound),type(raw_data))

		f=wave.open('input.wav','wb')
		f.setnchannels(1)
		f.setsampwidth(2)
		f.setframerate(16000)
		f.setnframes(1)
		f.writeframes(raw_data)
		f.close

		f_w=open('input.wav','rb')
		data_w=f_w.read()
		f_w.close()

		data={}
		data['format']='wav'
		data['rate']=8000
		data['cuid']=self.cu_id
		data['channel']=1
		data['token']=self.token_str
		data['len']=len(data_w)
		data['speech']=base64.b64encode(data_w).decode('utf-8')
		post_data=json.dumps(data)


		r_data=requests.post(self.upvoice_url,data=bytes(post_data,'utf-8'))
		print(r_data.text)
		try:
			return json.loads(r_data.text)['result'][0]
		except:
			return '语音识别失败'

if __name__ == '__main__':
	api_key='e6BPibfIxqFSvoGb6GLGjpaX'
	app_id='10671400'
	secret_key= 'b5b89ab3b51b47975e7c9cae7351bd4c'

	bdr=BaiduRest('wechact',api_key,secret_key)

	bdr.getVoice('123','out.amr')

	print(bdr.getText('out.amr'))
