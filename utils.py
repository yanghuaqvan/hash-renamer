import os
import sys
import hashlib
from PyQt5.QtCore import QThread, pyqtSignal

class RenameThread(QThread):

    processSignal = pyqtSignal(int) #0-100
    stateSignal = pyqtSignal(int) #0-idle 1-process

    def __init__(self, path, method, parent=None):
        super(RenameThread, self).__init__(parent)
        self.path = path
        self.method = method

    def run(self):
        self.stateSignal.emit(1)
        file_list = os.listdir(self.path)
        file_cnt = len(file_list)
        for i,file in enumerate(file_list,start=1):
            target_file = os.path.join(self.path, file)
            if(os.path.isfile(target_file)):
                filename, file_extension = os.path.splitext(file)
                sum = hash(target_file, self.method)
                sum_path = os.path.join(self.path,sum + file_extension)
                if os.path.isfile(sum_path) and (sum_path!=target_file):
                    os.remove(target_file)
                else:
                    os.rename(target_file, sum_path)
            self.processSignal.emit(int(i/file_cnt*100))
        self.stateSignal.emit(0)

def hash(file, method):
    if not os.path.isdir(file):
        f = open(file, 'rb')
        sum = ""
        if method == "sha1":
            sum = hashlib.sha1(f.read()).hexdigest()
        elif method == "sha224":
            sum = hashlib.sha224(f.read()).hexdigest()
        elif method == "sha256":
            sum = hashlib.sha256(f.read()).hexdigest()
        elif method == "sha384":
            sum = hashlib.sha384(f.read()).hexdigest()
        elif method == "sha512":
            sum = hashlib.sha512(f.read()).hexdigest()
        elif method == "md5":
            sum = hashlib.md5(f.read()).hexdigest()
        f.close()
        return sum
    else:
        return "dir"