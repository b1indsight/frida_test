import requests

url = "https://acs-m.lazada.co.id/gw/mtop.lazada.gsearch.appsearch/1.0/?data=%7B%22__original_url__%22%3A%22https%253A%252F%252Fwww.lazada.co.id%252Fbaju-muslim-pria%252F%253Ffrom%253Dlp_category%2526searchFlag%253D1%2526spm%253Da2o4j.category.5.3%22%2C%22adjustID%22%3A%2232761049-ae2e-4d8a-911a-9ff988f11f50%22%2C%22deviceID%22%3A%229dec5be6bc7330c8%7Cfc3af963-623e-4079-8b88-b8d3b9a7d006%22%2C%22firstSearch%22%3A%22true%22%2C%22from%22%3A%22lp_category%22%2C%22latitude%22%3A%220.0%22%2C%22longitude%22%3A%220.0%22%2C%22n%22%3A%2210%22%2C%22page%22%3A%221%22%2C%22rainbow%22%3A%221340%2C151%2C1444%2C2%2C1540%22%2C%22searchFlag%22%3A%221%22%2C%22speed%22%3A%220.0%22%2C%22spm%22%3A%22a2o4j.category.5.3%22%2C%22spm_pre%22%3A%22%22%2C%22spm_url%22%3A%22%22%2C%22sversion%22%3A%226.2%22%2C%22ttid%22%3A%22600000%40lazada_android_7.0.0%22%2C%22url_key%22%3A%22baju-muslim-pria%2F%22%2C%22userID%22%3A%22%22%2C%22utd_id%22%3A%22YoPi8IPL%2BfgDAIUV7VYRmu68%22%2C%22vm%22%3A%22nw%22%7D"

payload={}
headers = {
  'appVersion': '2',
  'x-sgext': 'JAUc%2FGAGxcjvwRCmO%2FIc8PwtzCzFLd8ozy%2FNP80q3y7QLdAt0C3QKNAu0C3QL9Av0C%2FQLNAs0C3QLdAu0C7fLcopySTMKM4pyz%2FMLMwszCzMLMwszCzMLMws3yzfLN8szD%2FMLMws3yzfLd8t3y3fLd8t3y7fLN8u3y3fLN8t3yzfLN8s3yzfLN8%2FmT%2Baed8s33rNL8sszA%3D%3D',
  'X-CID': '9dec5be6bc7330c8|fc3af963-623e-4079-8b88-b8d3b9a7d006',
  'x-i18n-regionID': 'id',
  'x-sign': 'azwfNj002xAAIlNFhihKxXAnjbAiQlNCXFx7dHkJLRl8OxNPphbghnjtg3pFUjLllswz0ZxPETwACJc2A3MXBYF1gtJTUlNCU1JTQl',
  'x-nettype': 'WIFI',
  'x-pv': '6.3',
  'x-nq': 'WIFI',
  'x-apdid-token': 'rsGTV9yoT95IYlsP5ITXoxPZY1+EJDi0WF+CcolTv/8RF6CFgQEAAA==',
  'adid': '32761049-ae2e-4d8a-911a-9ff988f11f50',
  'x-features': '27',
  'x-i18n-language': 'en',
  'x-app-conf-v': '0',
  'x-mini-wua': 'HHnB_B4xPLg5Hif6BH6TOQdqFsuuEn0XZTlzFD2Vdet415wtq4cbsDrM%2BcbiJcrOa6LQXZk%2FAI50f%2FR9LIOps8EdLnBiPh0tHAv2HEU5h7Cr8OBzx3s4unokPWA%2BqTO0DOfTXVaCAm%2F%2BFXCTuqYyzGipASYiwqOBj7KhN%2FpcJtp%2BN7X8%3D',
  'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
  'cache-control': 'no-cache',
  'x-t': '1655804270',
  'Cookie': 'hng=ID|en|IDR|360; t_fv=1654832003934; t_uid=gVsEC1yhuXi9XqRTmrYtoLB01GJkyX1x; cna=hakpG9GrkX8CAWVYp55r+p3d; lzd_cid=0bc727bf-4024-4bdf-dd0e-03d172b62bf0; lzd_sid=1313ad788bb335ff7693b91efd6446f0; _tb_token_=e3319a735e11e; t_sid=BBSJnoA6vxWlsQJRMG28nQhGMaDcdbWb; utm_channel=NA; x5sec=7b22617365727665722d6c617a6164613b32223a223433623566303133643936663438613533343264383939336264663430613263434b656578705547454b6a323475754c7874767a4b44435679624f712b2f2f2f2f2f3842227d; xlly_s=1; _m_h5_tk=f3d07f835d2d857a84ee161aa5dde173_1655813741127; _m_h5_tk_enc=4a33a7c159319eaf90ee93e43afc8a9a; isg=BDY2XbTtSDBtYjxHawPCYJRQjGU4V3qRiB26jqAfIpm049Z9COfKoZyR_6GP0HKp; l=eBPp6m2qL-mslhKkBOfahurza77OSCOYYuPzaNbMiOCPOI5B5r_1W6bjD3Y6C3Mdh6PXR3u1-0XpBeYBY3xonxvt4fpZ6fHmn; tfstk=c1BVBNwhYPgjKWv_9K9ac_yFgSsAwcO9TvxXiyozUxlO4nf0PVKSxdxHvfe9i; _m_h5_tk=485c2f473438974994455cdc806b3bfd_1655805367377; _m_h5_tk_enc=18606542511862622304a6def86a36c2; lzd_sid=13bc703d1bbbefe679dcd810bff64e36',
  'x-bx-version': '6.5.53',
  'f-refer': 'mtop',
  'utdid': 'YoPi8IPL+fgDAIUV7VYRmu68',
  'x-ttid': '600000%40lazada_android_7.0.0',
  'x-app-ver': '7.0.0',
  'x-c-traceid': 'null1655804270502001614331',
  'x-umt': '95QA31VLPEK6%2FQOBYQYafFjmCTzw1Cfl',
  'a-orange-q': 'appKey=23867946&appVersion=7.0.0&clientAppIndexVersion=1120220621172300483&clientVersionIndexVersion=0',
  'x-utdid': 'YoPi8IPL%2BfgDAIUV7VYRmu68',
  'c-launch-info': '0,0,1655804270494,1655804255890,0',
  'x-appkey': '23867946',
  'x-umidtoken': '95QA31VLPEK6/QOBYQYafFjmCTzw1Cfl',
  'x-devid': 'AjWYwize7Ap-z_4SPfJUjN8IJHTgxk1aLJan_BD2weBS',
  'user-agent': 'MTOPSDK%2F3.1.1.7+%28Android%3B9%3BGoogle%3BAOSP+on+IA+Emulator%29',
  'Host': 'acs-m.lazada.co.id'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
