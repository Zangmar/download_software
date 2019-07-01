from flask import Flask, render_template,request
import os
from Config import global_config
import logging

app = Flask(__name__)

#日志级别
logging.basicConfig(level=logging.INFO)
#日志文件位置
handler = logging.FileHandler('Config/app.log', encoding='UTF-8')
#日志格式
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
#设置日志格式
handler.setFormatter(logging_format)
#为全局的日志工具对象添加日志记录器
app.logger.addHandler(handler)



#遍历软件名称,拼接url
def search_path(download_type):
    name_list=[]
    target_path = ""
    dct_dict = {}
    for  path  in os.listdir(global_config.getconfig('file_root')):
        if "_" in path and path.split("_")[1] == download_type:
            target_path = path
            break

    # 返回导航目录名称如：办公软件_work，导航目录下的文件名称，多级目录拼接的字典
    if target_path:
        target_root = os.path.join(global_config.getconfig('file_root'),target_path)
        for path, dirs, fs in os.walk(target_root):
            for i in fs:
                pat=os.path.join(path, i)
                p1,p2 = os.path.split(pat)
                name_path = p1.split(target_path)[1]+os.path.join("/")
                name = p2
                dct_dict[name] = name_path
            for f in fs:
                name_list.append((f))
    return target_path,name_list,dct_dict

# 返回导航名+关键字：[('办公软件','work')]
def search_download_type():
    type_list=[]
    for path in os.listdir(global_config.getconfig('file_root')):
        abs_path = os.path.join(global_config.getconfig('file_root'),path)
        if os.path.isdir(abs_path) and "_" in path:
            cn_name,en_name = path.split("_")
            type_list.append((cn_name,en_name))
    return type_list


# 返回备注字典
def remark():
    dct = {}
    if not os.path.isdir(global_config.getconfig('readme_path')):
        os.makedirs(global_config.getconfig('readme_path'))
    path = os.path.join(global_config.getconfig('readme_path'), "readme.txt").replace("\\", "/")
    if not os.path.exists(path):
        f = open(path,"w")
        f.close()
    with open(path, 'r', encoding='utf-8') as f:
        remarks = f.readlines()
    for i in remarks:
        software_name, remarks = i.split(" ")
        dct[software_name] = remarks
    return dct



@app.route('/',methods=['GET'])
def download():
    try:
        dct=remark()
        download_type = request.args.get("download_type","work")
        dir_names = search_download_type()
        sub_root, file_names, dct_dict = search_path(download_type)
        return render_template('index.html',dir_names=dir_names,sub_root=sub_root,names=file_names,baseurl=global_config.getconfig('nginx_root'),dct=dct,dct_dict=dct_dict,download_type=download_type)
    except Exception as e:
        app.logger.exception('%s', e)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port='8080',debug=True)

