# 最小限度请求
# 
import frida, sys
import time
import json
import requests
import urllib.parse

def get_res(page):
    url = "https://acs-m.lazada.sg/gw/mtop.lazada.gsearch.appsearch/1.0/?data={}"

    js_code = """
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
                    
                    var mtopConfig = Java.use('mtopsdk.mtop.global.MtopConfig').$new();
                    console.log(mtopConfig.ttid.value);
                    

                    var C26958b = Java.use("mtopsdk.security.b").$new();
                    C26958b.a(mtopConfig);
                    var r = C26958b.a(hashMap1, hashMap2, str, str2, z);
                    console.log(r)
                    console.log(hashMap1)
                    console.log(hashMap2)
                    result = '{'+'"x_sign":"'+r.get("x-sign")+'",'+'"x_mini_wua":"'+r.get("x-mini-wua")+'",'+'"x_umt":"'+r.get("x-umt")+'",'+'"x_sgext":"'+r.get("x-sgext")+ '",' + '"x_devid":"' + mtopConfig.deviceId.value + '"}';
                }catch(e){
                    console.log(e)
                }
            });
            return result;
        }
    }
    """

    def on_message(message, data):
        if message['type'] == 'send':
            print("[*] {0}".format(message['payload']))
        else:
            print(message)

    session = frida.get_device('socket').attach('Lazada')
    # 在目标进程里创建脚本
    script = session.create_script(js_code)
    # 注册消息回调
    script.on('message', on_message)
    print('[*] Start attach')
    # 加载创建好的javascript脚本
    script.load()
    now = str(int(time.time()))
    # now = '1654151812'
    print(now)
    utd_id = script.exports.getutdid()
    print(utd_id)
    deviceID = script.exports.getdeviceid()
    print(deviceID)
    data = """{{"__original_url__":"https%3A%2F%2Fwww.lazada.sg%2Fshop-disposable-diapers%2F%3Fpos%3D7%26acm%3D201711220.1003.1.2873589%26scm%3D1003.1.201711220.OTHER_8757_2873589%26from%3Dlp_category%26searchFlag%3D1%26spm%3Da2o42.category.6.2_7","acm":"201711220.1003.1.2873589","adjustID":"32761049-ae2e-4d8a-911a-9ff988f11f50","deviceID":"{deviceID}","firstSearch":"true","from":"lp_category","latitude":"0.0","longitude":"0.0","n":"100","page":"{page}","rainbow":"1340,151,1444,1446,2,1540","scm":"1003.1.201711220.OTHER_8757_2873589","searchFlag":"1","speed":"35.31","spm":"a2o42.category.6.2_7","spm_pre":"a2o42.category.5.7","sversion":"6.2","ttid":"600000@lazada_android_7.0.0","sort":"order", "url_key":"shop-disposable-diapers/","userID":"","utd_id":"{utd_id}","vm":"nw"}}""".format(utd_id=utd_id, deviceID=deviceID, page=page)
    print(data)
    sign_dict = script.exports.getsign(now, data, utd_id, deviceID)
    sign_dict = json.loads(sign_dict)
    print(sign_dict)

    payload={}
    headers = {
    'appVersion': '2',
    'x-sgext': urllib.parse.quote(sign_dict['x_sgext']),
    'x-sign': urllib.parse.quote(sign_dict['x_sign']),
    'x-pv': '6.3',
    'x-features': '27',
    'x-mini-wua': urllib.parse.quote(sign_dict['x_mini_wua']),
    'x-t': now,
    'x-ttid': '600000%40lazada_android_7.0.0',
    'x-app-ver': '7.0.0',
    'x-umt': urllib.parse.quote(sign_dict['x_umt']),
    'x-utdid': urllib.parse.quote(utd_id),
    'x-appkey': '23867946',
    #   'x-devid': deviceID,
    'user-agent': 'MTOPSDK%2F3.1.1.7+%28Android%3B9%3BGoogle%3BAOSP+on+IA+Emulator%29',
    'Host': 'acs-m.lazada.sg'
    }

    url = url.format(urllib.parse.quote(data))
    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        print(f'request error {e}')
        return ''

    if response.ok:
        return response.json()
    else:
        return ''
    

def main():
    max_page = 999
    current_page = 1
    while current_page <= max_page:
        time.sleep(30)
        res = get_res(current_page)
        tmp = res.get('data', {}).get('mainInfo', {}).get('totalResults', '')
        if tmp.isdigit():
            max_page = int(tmp) // 100 + 1
        print(f'current page is {current_page}')
        res['current_page'] = current_page
        print(res)
        current_page += 1

if __name__ == '__main__':
    main()