#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'RicterZheng@gmail.com'

import os,sys
import tornado.web
from tornado import template
import tornado.ioloop

class BaseHandler(tornado.web.RequestHandler):
    """
        每个Handler的基类
    """
    downloadPath = str(os.getcwd()) + "/static/download/"

    #这个字典是根据节目时间区分节目名称
    fmData = {
        '06' : "FM97.5/新闻麻辣烫",
        '12' : "FM97.5/传说那些事",
        '14' : "FM97.5/娱乐香饽饽",
        '20' : "FM97.5/信不信由你"
    }


    def render(self, templateData):
        self.write(templateData)

    def getFile(self):
        list = os.listdir(self.downloadPath)
        return [line for line in list][:-28] #取前28，倒序

class MainHandler(BaseHandler):
    def get(self):
        """
            处理get请求
        """
        fileList, fileInfoList = self.getFile(), []
        for fileName in fileList:
            fileDataList = fileName.split('-')
            """
                eg.
                -------------
                fileName = '975-2013.06.04-12.00.mp3'
                fileDataList[0] = '975'
                fileDataList[1] = '2013.06.04'
                fileDataList[2] = '12.00.mp3'
            """
            fileSize = os.path.getsize(self.downloadPath + fileName)
            fileLong = fileSize * 8 / 63 / 60 / 1024
            fileSize = fileSize / 1024 / 1024
            fileInfoList.append([
                self.fmData[fileDataList[2].split('.')[0]], #节目名称
                fileDataList[1]                           , #节目时间
                fileSize                                  , #文件大小
                fileLong                                    #文件时长
            ]) 

        """
            fileInfoList是一个二元列表（姑且先这么叫）
            其里面的列表保存各个文件信息，然后传递倒模板
        """
        return self.render(
            loaderTemplate.load("index.html").generate(
                title = u"FM广播录音",
                fileInfoList = fileInfoList 
            )
        )

settings = {"static_path" : os.path.join(os.path.dirname(__file__), "static".decode('utf-8'))}
application = tornado.web.Application([
    (r"/", MainHandler)
], **settings)

loaderTemplate = template.Loader("template")

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
