import itchat
import requests
from bs4 import BeautifulSoup as Soup
import config
import image
import qrcode
import time
from aip import BaiduRest
from translate import translate
import pprint
import json
from image_identify import image_identify


def login(id):
	while True:
		status=itchat.check_login(id)
		print(config.uuid,status)
		if status in ['200','201']:
			print('Already login')
			time.sleep(10)
		elif status in ['400','408','0']:
			print('Need to login')
			try:
				itchat.auto_login(hotReload=True)
				itchat.send_msg('login successfully!',toUserName='filehelper')
				config.uuid=itchat.get_QRuuid()
				get_friend_list()
				get_chart_room_list()
				get_mp_list()
				itchat.run()

			except:
				time.sleep(10)


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):

	pprint.pprint(msg)

	if msg['ToUserName']=='filehelper':
		try:
			msg=msg['Text'].split(' ')
			if len(msg)==1:
				raise("message length is not enough")
			else:
				pass
		except Exception as e:
			print("message format error "+str(e))
			itchat.send_msg("message format error",toUserName='filehelper')

		if msg[0].lower() in config.function_code.values():
			msg=[x.lower() for x in msg]


			if msg[0] ==config.function_code['sound_identify']:
				if msg[1] in config.OPEN_FUNC:
					config.open_yy=True
					itchat.send_msg('open sound identify successfully',toUserName='filehelper')
				elif msg[1] in config.CLOSE_FUNC:
					config.open_yy=False
					itchat.send_msg('close sound identify successfully',toUserName='filehelper')
				else:
					pass



			elif msg[0]==config.function_code['stock']:
				if msg[1] in config.HELP_FUNC:
					itchat.send_msg('you can input "all" for all stock you care or 0 for main stock or number from 1 to '+str(len(config.stock_care)+1)+'for specific stock')
				elif msg[1] in ['all']+[str(e) for e in range(len(config.stock_care)+1)]:
					result=get_data(msg[1])
					re_text=''
					for i in result:
						re_text=re_text+i+'\n'	
					itchat.send_msg(re_text,toUserName='filehelper')
				else:
					itchat.send_msg('stock code error',toUserName='filehelper')



			elif msg[0]==config.function_code['translate']:
				if msg[1] in config.OPEN_FUNC:
					config.open_trans=True
					itchat.send_msg('open translate successfully',toUserName='filehelper')
				elif msg[1] in config.CLOSE_FUNC:
					config.open_trans=False
					itchat.send_msg('close translate successfully',toUserName='filehelper')
				elif msg[1] in config.HELP_FUNC:
					itchat.send_msg(str(config.lang),toUserName='filehelper')
				elif msg[1] in config.lang:
					if len(msg)==2:
						config.trans_to=msg[1]
						config.trans_from='auto'
						itchat.send_msg('Set translate from '+ config.trans_from +' to '+config.trans_to+' successfully',toUserName='filehelper')
					elif msg[2].lower() in config.lang:
						config.trans_from=msg[1]
						config.trans_to=msg[2]
						itchat.send_msg('Set translate from '+ config.trans_from +' to '+config.trans_to+' successfully',toUserName='filehelper')
					else:
						itchat.send_msg("langue set error",toUserName='filehelper')
				else:
					itchat.send_msg("langue set error",toUserName='filehelper')


			elif msg[0]==config.function_code['image_text_identify']:
				if msg[1] in config.OPEN_FUNC:
					config.open_image_identify=True
					itchat.send_msg('open image identify successfully',toUserName='filehelper')
				elif msg[1] in config.CLOSE_FUNC:
					config.open_image_identify=False
					itchat.send_msg('close image identify successfully',toUserName='filehelper')
				else:
					pass



		else:
			itchat.send_msg('message function_code error'+str([e+',' for e in config.function_code.values()]),toUserName="filehelper")
	elif msg['User']['NickName']=='雨田':
		if config.open_trans:
			print(msg['Text'],config.trans_to,config.trans_from)
			trans=translate(q=msg['Text'],tolang=config.trans_to,fromlang=config.trans_from)
			trans_result=trans.tran_request()
			pprint.pprint(trans_result)
			itchat.send_msg(trans_result,msg['FromUserName'])
		else:
			pass
	else:
		pass


@itchat.msg_register(itchat.content.RECORDING)
def treat_recording(msg):
	if config.open_yy:
		pprint.pprint(msg)
		msg.download(msg.FileName)
		bdyuyin=BaiduRest()
		re_text=bdyuyin.getText(msg.FileName)
		pprint.pprint(re_text)
		print(msg['FromUserName'])
		if re_text!='语音识别失败':
			re_text="语音识别内容:\n"+re_text
		itchat.send_msg(re_text,toUserName=msg['FromUserName'])
	else:
		pass

@itchat.msg_register(itchat.content.PICTURE)
def treat_imaeg(msg):
	pprint.pprint(msg)
	if config.open_image_identify and msg['ToUserName']=='filehelper':
		msg.download(msg.FileName)
		img_identify=image_identify()
		result=img_identify.identify(msg.FileName)
		print(result)
		re_text=''
		for re in result:
			re_text=re_text+re+'\n'
		itchat.send_msg(re_text,'filehelper')



def get_data(msg=None):
	gethtml={}
	sockid={}
	if msg=='0':
		sockid= config.stock_care
	elif msg in [str(x+1) for x in range(len(config.stock_of_main))]:
		sockid=[config.stock_of_main[int(msg)-1]]
	elif msg=='all':
		sockid=config.stock_of_main
	else:
		return ['not found']

	for i in sockid:
		for key,value in i.items():
			gethtml[value]=requests.get('http://gu.qq.com/'+ key )

	return paserhtml(gethtml)



def paserhtml(html):
	text=[]
	for i,h in html.items():
		page=h.text
		soup=Soup(page,'lxml')
		s=soup.find('div',class_='item-2')
		pprint.pprint(s)
		text.append(i[0]+' '+s.get_text().replace('%',"").replace("+","#").replace('-','_')+'  '+i[1])
	return text

def get_friend_list():
	config.friends_nickname_list=[i['NickName'] for i in itchat.get_friends()]
	print(config.friends_nickname_list)

def get_chart_room_list():
	config.chatrooms_nickname_list=[i['NickName'] for i in itchat.get_chatrooms()]
	print(config.chatrooms_nickname_list)

def get_mp_list():
	config.mps_nickname_list=[i['NickName'] for i in itchat.get_mps()]
	print(config.mps_nickname_list)


if __name__ == '__main__':

	login(config.uuid)
