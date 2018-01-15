#主要功能命令
function_code={
		"stock":'gp',
		"sound_identify":'yy',
		"translate":'fy',
		'image_text_identify':'ii'
}

#关心股票数据

stock_of_care=[
			{'sz002295':'精艺股份'},
			{'sz002195':'二三四五'},
			{'sz002681':'奋达科技'},
			{'sz000050':"深天马Ａ"},
			{'sz002211':"宏达新材"},
			{'sz002351':"漫步者"},
			{'sz002609':"捷顺科技"},
			{'sh603005':"晶方科技"},
			{"sz000785":"武汉中商"}
]

#大盘数据

stock_main=[
	
	{'sh000001':'shanghai'},
	{'sz399001':'shenzheng'}
]


#翻译语言对照
lang={
	
		'auto': '自动检测',
		'zh':   '中文',
		'en':   '英语',
		'yue':  '粤语',
		'wyw':  '文言文',
		'jp':   '日语',
		'kor':  '韩语',
		'fra':  '法语',
		'spa':  '西班牙语',
		'th':   '泰语',
		'ara':  '阿拉伯语',
		'ru':   '俄语',
		'pt':	'葡萄牙语',
		'de':	'德语',
		'it':	'意大利语',
		'el':	'希腊语',
		'nl':	'荷兰语',
		'pl':	'波兰语',
		'bul':	'保加利亚语',
		'est':	'爱沙尼亚语',
		'dan':	'丹麦语',
		'fin':	'芬兰语',
		'cs':	'捷克语',
		'rom':	'罗马尼亚语',
		'slo':	'斯洛文尼亚语',
		'swe':	'瑞典语',
		'hu':	'匈牙利语',
		'cht':	'繁体中文',
		'vie':	'越南语',

}
#打开语音识别命令
open_yy=False  
#打开翻译命令
open_trans=False
#打开图片识别功能
open_image_identify=False

#默认从自动翻译到英文
trans_to='en'
trans_from='auto'
uuid=''

#百度帐号应用相关认证信息
API_KEY='vt9vGGzbV9sIdbSkXdlq5bZn'
APP_ID='10685094'
SECRET_KEY='0T8yNycZEWMHZnpVAzA9gL3CaS0Q4gZv'

#常用命令
OPEN_FUNC=['open','o']
CLOSE_FUNC=['close','c']
HELP_FUNC=['help','h']

#朋友nickname表
friends_nickname_list=[]
#聊天室nickname表
chatrooms_nickname_list=[]
#公众号nickname表
mps_nickname_list=[]
