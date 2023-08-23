# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path, WindowsPath
from PyQt5 import QtGui

class Tesseract():
    def __init__(self):
        self.tesseract = 'TESSDATA_PREFIX=tessdata tesseract/build/bin/tesseract'

    def command(self, filename, output_file):
        return [self.tesseract, str(filename), output_file.stem]

    def OCR(self, data):
        if type(data) is str or type(data) is WindowsPath:
            return self.OCR_file(data)
        if type(data) is QtGui.QPixmap:
            imagefile = Path('__temp__.png')
            data.save(str(imagefile))
            output = self.OCR_file(imagefile)
            imagefile.unlink()
            return output

    def OCR_file(self, filename):
        output_file = Path('__temp__.txt')
        # cmd = [self.tesseract, str(filename), output_file.stem]
        cmd = self.tesseract + ' ' + str(filename) + ' ' + output_file.stem
        startupinfo = None
        import os
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        # returncode = subprocess.Popen(cmd, startupinfo=startupinfo)
        returncode = subprocess.Popen(cmd, shell=True, encoding='utf-8', startupinfo=startupinfo)
        returncode.wait()
        
        try:
            with open(output_file, 'r', encoding='utf-8') as file:
                output = file.readline()
            output_file.unlink()
            return output
        except:
            return ''
