import frida

js_get_hashmap_mtop_global = """
rpc.exports = {
    myfunc11: function(){
    	var result = null;
        Java.perform(function () {
            try{
                var HashMap = Java.use('java.util.HashMap');
                const str = Java.use('java.lang.String');
                var hashMap1 = HashMap.$new();
                var devices_id = Java.use('com.lazada.android.search.f');
                console.log(devices_id.b())
                
                var headers = Java.use('com.taobao.weex.WXEnvironment');
                console.log("x-devid = " + headers.getApplication());
                var app;
                var TelephonyManager = Java.use('android.telephony.TelephonyManager');
                Java.choose('android.app.Application', {
                    "onMatch":function(instance){
                        var devid = instance
                        
                    },
                    "onComplete":function(){
                    }
                });

                headers = Java.use('com.alibaba.wireless.security.open.securityguardaccsadapter.usertrack.UserTrackUFWrapper');
                
                

                var mtopConfig;
                Java.choose('mtopsdk.mtop.global.MtopConfig',{
                    "onMatch":function(instance){
                         mtopConfig = instance;
                    },
                    "onComplete":function(){
                    }
                })
                var devid = mtopConfig.deviceId.value;
                result = mtopConfig.sign;
            }catch(e){
                console.log(e)
            }
        });
        return result;
    },
    myfunc12: function(){
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
    }
}
"""

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


session = frida.get_usb_device().attach('Lazada')
# 在目标进程里创建脚本
script = session.create_script(js_get_hashmap_mtop_global)
# 注册消息回调
script.on('message', on_message)
print('[*] Start attach')
# 加载创建好的javascript脚本
script.load()

utdid =  script.exports.myfunc12()
print(utdid)