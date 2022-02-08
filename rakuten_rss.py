"""楽天RSS用モジュール
"""
from lib.ddeclient import DDEClient
import pandas as pd
import numpy as np
import time 

 


def rss(item,k):
	


	dde_ware = []
	indexes = pd.read_csv("TOPIX_weight_jp.csv")
	


	indexes["コード"] = pd.to_numeric(indexes["コード"], errors='coerce')


	indexes_code = indexes["コード"].astype(int)

	
	for i,j in enumerate(indexes_code):
		indexes_code[i] = str(j) + ".T"
	indexes_code = np.array(indexes_code)
	indexes_code = indexes_code.flatten()

	

	for i,j in indexes.iterrows():
		#l = j.replace("%", "")
		indexes.at[i, "TOPIXに占める個別銘柄のウェイト"] = indexes.loc[i, "TOPIXに占める個別銘柄のウェイト"].replace("%", "")	

	
	count = 0
	calc = 0
	issures = []
	for i,j in enumerate(indexes_code, start = k): #.Tは転置
		count += 1
		dde = DDEClient("rss", indexes_code[i])
		dde_ware.append(dde)
			
		try: # if i != 1461 and i != 420: # if i != 2166 and i != 1956 and i != 1461 and i != 420
			calc += float(dde.request(item).decode("sjis")) * float(indexes["TOPIXに占める個別銘柄のウェイト"][i] )* 0.01
		except Exception:
			string = "fileX"
			try:
				name = dde.request("銘柄コード").decode("sjis")
				name.replace(".T", "")
			except:
				name = str(indexes["コード"][i]) + ".T"
			#print(name)
			f = open(string, "a")
			f.write(name + " ") 
			pass	
		else:
			pass	
		finally:
			del dde
			if count >= 126:
				break
			if k == 2142 and count == 40:
				break 

			
			

	pocket = [calc, dde_ware, indexes["TOPIXに占める個別銘柄のウェイト"]]
	
	
	return pocket
	

def rss2(item,k, dde_ware, weights):
	calc = 0
	count = 0
	for i,j in enumerate(dde_ware): #.Tは転置
		dde = dde_ware[i]
			#print(str(i)+ dde.request("銘柄名称").decode("sjis"))
		try: # if i != 1461 and i != 420: # if i != 2166 and i != 1956 and i != 1461 and i != 420
			calc += float(dde.request(item).decode("sjis")) * float(weights[i] )* 0.01
		except Exception:
			pass
			# del dde
		count += 1
		if count >= 126:
			break
			#issures.append(np.array(jasd["発行済株式数"][i]))
			#res += float(dde.request(item).decode("sjis")) * float(np.array(jasd["発行済株式数"][i])) #strip()		
		else:
			continue
	return calc


def rss_dict(code, *args):
	"""
	楽天RSSから辞書形式で情報を取り出す(複数の詳細情報問い合わせ可）
	Parameters
	----------
	code : str
	args : *str
	Returns
	-------
	dict
	Examples
	----------
	>>>rss_dict('9502.T', '始値','銘柄名称','現在値')
	{'始値': '1739.50', '現在値': '1661.50', '銘柄名称': '中部電力'}
	"""

	dde = DDEClient("rss", str(code))

	
	values ={}
	element = []

	res = {}
	try:
		for item in args:
			res[item] = dde.request(item).decode('sjis').strip()
	except:
		print('fail: code@', code)
		res = {}
	finally:
		dde.__del__()
	return res

def fetch_open(code):
	""" 始値を返す（SQ計算用に関数切り出し,入力int）
	Parameters
	----------
	code : int
	Examples
	---------
	>>> fetch_open(9551)
	50050
	"""

	return float(rss(str(code) + '.T', '始値'))