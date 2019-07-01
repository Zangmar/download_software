# -*- coding: UTF-8 -*-
# author:liujiayu

# -*- coding: UTF-8 -*-
# author:liujiayu


import os
import configparser


# 封装一个路径，直接输入文件名称filename就可以获得filename的路径
def getPath(filename):
    return os.path.join(os.path.dirname(__file__) + "/", filename)


class Config(object):

    def __init__(self, filename, section):
        """
        :param filename: 文件名称
        :param section: 属于文件中的第几个section，这是整形
        """
        self.section = section
        # 实例化一个configparser对象
        self.cf = configparser.ConfigParser()
        # 读取文件的内容
        self.cf.read(getPath(filename), encoding="utf-8")

    def getconfig(self, avg):
        """
        获得想要属性的内容
        :param avg: 属性名称
        :return: 属性的值
        """
        parameter = self.cf.get(self.cf.sections()[self.section], avg)
        return parameter


#实例化Config，想要config.ini文件，第1个section的内容
global_config = Config("config.ini",0)




