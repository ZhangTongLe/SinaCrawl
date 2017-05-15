# -*- coding:utf-8 -*-
"""磁盘缓存"""
import hashlib
import os.path, os
import cPickle

class DiskCache:
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir

    def filePath(self, keywords):
        obj = hashlib.md5()
        obj.update(keywords)

        filePath = os.path.join(self.cache_dir, str(obj.hexdigest()))
        return filePath

    def __getitem__(self, keywords):
        filePath = self.filePath(keywords)

        if os.path.exists(filePath):
            with open(filePath, 'rb') as fp:
                return cPickle.load(fp)
        else:
            raise KeyError(keywords+'does not exist')

    def __setitem__(self, keywords, value):
        filePath = self.filePath(keywords)

        with open(filePath, 'wb') as fp:
            fp.write(cPickle.dumps(value))