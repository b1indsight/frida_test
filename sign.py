# GET /get_sign_data获取json {task_file: "", data: ""}
# sign 之后 POST /upload_sign 正文部分为json {status: "", result:{"task_file": "", "data": "", "sign": {}}}

import httpx
import frida
import json
import time
import base64
import logging
from urllib.parse import quote, unquote

logging.basicConfig(filename="lazada_sign.log", encoding="utf-8")

class frida_sign:
    JS_CODE = """
    rpc.exports = {
        getutdid: function(){
            var result = null;
            Java.perform(function () {
                try{
                let GlobalAppRuntimeInfo = Java.use("anet.channel.GlobalAppRuntimeInfo");
                result = GlobalAppRuntimeInfo.getUtdid();

                }catch(e){
                    console.log(e)
                }
            });
            return result;
        },
        getdeviceid: function(){
            var devices_id = Java.use('com.lazada.android.search.f');
            return devices_id.b();
        },
        getsign: function(timestamp,data,utdid,deviceID){
            console.log("start getsign")
            var result = null;
            Java.perform(function () {
                try{
                    var HashMap = Java.use('java.util.HashMap')
                    var hashMap1 = HashMap.$new();
                    hashMap1.put("appKey", "23867946")
                    hashMap1.put("deviceId", null)
                    hashMap1.put("utdid",utdid)
                    hashMap1.put("x-features", "27")
                    hashMap1.put("ttid", "600000@lazada_android_7.0.0")
                    hashMap1.put("v", "1.0")
                    hashMap1.put("sid", null)
                    hashMap1.put("t", timestamp)
                    hashMap1.put("api", "mtop.lazada.gsearch.appsearch")
                    hashMap1.put("data", data)
                    hashMap1.put("uid", null)

                    var hashMap2 = HashMap.$new();
                    hashMap2.put("pageName","")
                    hashMap2.put("pageId","")

                    var str = "23867946"
                    var str2 = null
                    var z = false
                    
                    var mtopConfig = Java.use('com.lazada.android.compat.network.a').a().getMtopConfig();                                                                 
                
                    var C26958b = Java.use("mtopsdk.security.b").$new();                                                
                    C26958b.a(mtopConfig);                            
                    var r = C26958b.a(hashMap1, hashMap2, str, str2, z);
                    result = '{'+'"x_sign":"'+r.get("x-sign")+'",'+'"x_mini_wua":"'+r.get("x-mini-wua")+'",'+'"x_umt":"'+r.get("x-umt")+'",'+'"x_sgext":"'+r.get("x-sgext")+ '"}';
                }catch(e){
                    console.log(e)
                }
            });
            return result;
        }
    }
    """
    _instance = None
    _session = None
    _script = None

    def __new__(cls):
        if cls._instance is None:
            cls._init(cls)
        if cls._script is None or cls._script.is_destroyed:
            cls._init(cls)
        return cls._instance

    def get_sign(self, data:dict):
        if not data:
            return {}, {}
        timestamp = str(int(time.time()))
        utd_id = self._script.exports.getutdid()
        device_id = self._script.exports.getdeviceid()
        data['utd_id'] = utd_id
        data['deviceID'] = device_id
        data = json.dumps(data, separators=(',', ':'))
        sign_dict = self._script.exports.getsign(timestamp, data, utd_id, device_id)
        sign_dict = json.loads(sign_dict)
        sign_dict['utd_id'] = utd_id
        sign_dict['x_t'] = timestamp
        return data, sign_dict

    @staticmethod
    def _on_message(message, data):
        if message['type'] == 'send':
            logging.info("[*] {0}".format(message['payload']))
        else:
            logging.info(message)

    @staticmethod
    def _init(cls):
        cls._instance = super().__new__(cls)
        cls._instance._session = frida.get_device('socket').attach('Lazada')
        cls._instance._script = cls._instance._session.create_script(cls.JS_CODE)
        cls._instance._script.on('message', cls._on_message)
        cls._instance._script.load()
    

def get_data():
    api_url = "https://spservice.nint.jp/lazada/get_sign_data"
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(b'lazada:lazada_pwd').decode()
    }
    try:
        r = httpx.get(api_url, headers=headers)
    except Exception as e:
        logging.error(f"get sign data failed error: {e}", exc_info=True)
        return None
    if r.is_success:
        return r.json()
    else:
        return None

def upload_data(data):
    api_url = "https://spservice.nint.jp/lazada/upload_sign"
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(b'lazada:lazada_pwd').decode()
    }
    for _ in range(0, 3):
        try:
            r = httpx.post(api_url, headers=headers, json=data)
            if r.is_success and r.json().get('status', 'failed') == 'success':
                return
        except Exception as e:
            logging.error(f"post signed failed error: {e}", exc_info=True)
            continue

def _sign(data):
    try:
        tmp, sign = frida_sign().get_sign(data)
        res = {
            "data": quote(tmp),
            "sign": sign
        }
        return res
    except Exception as e:
        logging.error(f"get sign failed error: {e}", exc_info=True)


def main():
    while True:
        data = get_data()
        if data:
            task_file = data.get("task_file", '')
            tmp = _sign(data.get("data", '{}'))
            tmp['task_file'] = task_file
            tmp['category'] = data.get("category", '')
            tmp['proxy'] = data.get("proxy", '{}')
            upload_data(tmp)
        time.sleep(10)


if __name__ == "__main__":
    main()
