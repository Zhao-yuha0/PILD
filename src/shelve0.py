# coding:utf-8
import daemon
import shelve
import os

def saveFile(url, content, taskName, taskId):
    fileName = taskName + '_' + str(taskId)
    filePath = 'store/' + fileName

    os.chdir('/root/demo/project/store')
    if not os.path.exists(fileName + '.dat'):
        os.mknod(fileName+ '.dat')

    data = shelve.open(fileName)
    data[url] = content
    data.close()

    os.chdir('/root/demo/project')


def readFile(taskName, taskId, url):

    os.chdir('/root/demo/project/store')

    fileName = taskName + '_' + str(taskId)
    filePath = 'store/' + fileName
    with shelve.open(fileName) as data:
        res = data[url]
    return res


