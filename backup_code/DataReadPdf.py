# coding=utf-8 #

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os
from os import path
import codecs

class DataReadPdf:
    def __init__(self,rootdir):
        self.rootdir = rootdir
        self.readpath=self.rootdir+"Data_read/"
        self.savepath=self.rootdir+"Data_save/"
    def read_pdf(self,filename):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(self.readpath+filename, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return text

    def save_text(self,text,filename):
        with codecs.open(self.savepath + filename[:-3]+"txt","w","utf-8") as f:
            print('opentext:' + filename[:-3])
            f.write(text)

    def traversal(self):
        for parent, dirnames, filenames in os.walk(self.readpath):
            for filename in filenames:
                #filenameFull = os.path.join(filename)
                print(filename)
                if (filename.endswith('pdf') or filename.endswith('PDF')):
                    text = self.read_pdf(filename)
                    self.save_text(
                        text.replace(u'\xa9', u'').replace(u'\xa0', u'').replace(u'\xad', u'').replace(u'\u037e', u''),
                        filename)

