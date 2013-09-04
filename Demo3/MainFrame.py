# coding=gbk
#__author__ = 'generated by py-ui4win'
import string, os, time
import threading

from PyUI import *
from MsgBox import *
from PyFrameBase import *
import UICommon
from CommonUtil import CommonUtils
from PyWin32Utils import PyWin32Util

import DownloadEaz

XP = 1
WIN7 = 2

def PyThreadDownloadEaz(PyClassInstance, ):
    try:
        PyClassInstance.DownloadEazFile()
    except Exception, e:
        PyLog().LogText(str(e))
    PyLog().LogText('PyThreadExecute exit')


class MainFrame(PyFrameBase):
    def __init__(self):
        super(MainFrame, self).__init__()
        self.clsName = self.__class__.__name__
        self.skinFileName = self.__class__.__name__ + '.xml'
        self.progress = 0
        self.os = 0
        self.progress_color = 0
        self.eazfile_size = 0

    def GetSkinFile(self):
        return self.skinFileName

    def GetWindowClassName(self):
        return self.clsName

    def OnExit(self, sendor, wParam, lParam):
        self.ExitApp()

    def OnPrepare(self, sendor, wParam, lParam):
        self.LabelUIDescription = self.PyFindLabel("LabelUIDescription")
        self.LabelUI6 = self.PyFindLabel("LabelUI6")
        self.LabelUI4 = self.PyFindLabel("LabelUI4")
        self.LabelUIOS = self.PyFindLabel("LabelUIOS")
        self.LabelWaiting = self.PyFindLabel("LabelWaiting")
        self.LabelUI5 = self.PyFindLabel("LabelUI5")
        self.LabelUI2 = self.PyFindLabel("LabelUI2")
        self.LabelUI3 = self.PyFindLabel("LabelUI3")
        self.LabelUI12 = self.PyFindLabel("LabelUI12")
        self.LabelUI11 = self.PyFindLabel("LabelUI11")
        self.closebtn = self.PyFindButton("closebtn")
        self.BtnDownloadTooSlow = self.PyFindButton("BtnDownloadTooSlow")
        self.BtnWin7 = self.PyFindButton("BtnWin7")
        self.BtnXP = self.PyFindButton("BtnXP")
        self.ButtonUIReboot = self.PyFindButton("ButtonUIReboot")
        self.adv1 = self.PyFindButton("adv1")
        self.adv2 = self.PyFindButton("adv2")
        self.adv3 = self.PyFindButton("adv3")
        self.adv4 = self.PyFindButton("adv4")
        self.adv5 = self.PyFindButton("adv5")
        self.ProgressDownload = self.PyFindProgress("ProgressDownload")
        self.ContainerUITitle = self.PyFindContainer("ContainerUITitle")
        self.ContainerUIStep2 = self.PyFindContainer("ContainerUIStep2")
        self.ContainerUIStep1 = self.PyFindContainer("ContainerUIStep1")
        self.ContainerUIStep3 = self.PyFindContainer("ContainerUIStep3")
        self.ContainerUIBottom = self.PyFindContainer("ContainerUIBottom")
        self.VerticalLayoutUI1 = self.PyFindVerticalLayout("VerticalLayoutUI1")

        self.ContainerUIStep2.SetVisible(False)
        self.ContainerUIStep3.SetVisible(False)

    def OnCustomTimer(self, wParam, lParam):
        """
        wParam:  时间id
        """
        if wParam == 2:
            if self.progress_color == 0:
                self.ProgressDownload.pControl.SetBorderColor(0xaa00000)
                self.progress_color = 0xaa0000
            else:
                self.ProgressDownload.pControl.SetBorderColor(0)
                self.progress_color = 0

    def show_progress(self):
        self.LabelWaiting.SetText('已经下载( %.1f / %.1f MB)，请耐心等待...'%(float(self.download.get_all_download_bytes())/1024/1024, float(self.eazfile_size)/1024/1024))
        percent = (self.download.get_all_download_bytes()*100)/self.eazfile_size
        if self.percent < percent:
            self.ProgressDownload.SetValue(percent)
            self.percent = percent

    def DownloadEazFile(self):
        try:
            self.percent = 0
            url = ''
            pattern = ''
            if self.os == WIN7:
                url = 'http://pan.baidu.com/share/link?shareid=2475901380&uk=70461429'
                pattern = r'http:\\\\/\\\\/d\.pcs\.baidu\.com\\\\/file\\\\/f477e96d80f27717b821861ab4fa7b45\?fid=.*?&sh=1'
            else:
                url = 'http://pan.baidu.com/share/link?shareid=2423534928&uk=70461429'
                pattern = r'http:\\\\/\\\\/d\.pcs\.baidu\.com\\\\/file\\\\/37c58125068409bf538e3321e5e46d57\?fid=.*?&sh=1'

            self.download = DownloadEaz.EazDownload(url, pattern, self)
            if self.download.get_file_info():
                self.eazfile_size = self.download.file_size
                if self.download.GetDownloadPath() is None:
                    self.LabelWaiting.SetText('磁盘空间太小啦')
                    self.SetTimer(2, 1000)
                    return
                elif self.download.download_file(os.path.join(self.download.GetDownloadPath(),'os.eaz')):
                    if self.os == WIN7:
                        self.LabelUIDescription.SetText('已经准备好安装 Win7 系统到您的计算机')
                    else:
                        self.LabelUIDescription.SetText('已经准备好安装 XP 系统到您的计算机')
                    self.ButtonUIReboot.SetVisible(True)
                    self.ContainerUIStep1.SetVisible(False)
                    self.ContainerUIStep2.SetVisible(False)
                    self.ContainerUIStep3.SetVisible(True)
                    return

            self.LabelWaiting.SetText('镜像下载出错啦')
            #PyWinUtils().SetTimer(self.GetHWnd(), 2, 1000)
            self.SetTimer(2, 1000)
        except Exception, e:
            PyLog().LogText('%s' % e)
            self.LabelWaiting.SetText('镜像下载出错啦')
            #PyWinUtils().SetTimer(self.GetHWnd(), 2, 1000)
            self.SetTimer(2, 1000)

    def OnBtnWin7orBtnXP(self, sendor, sType, wParam, lParam):
        if sendor == "BtnWin7":
            self.os = WIN7
            self.LabelUIOS.SetBkImage('win7.jpg')
            self.LabelUIDescription.SetText('正在下载 Win7 系统到您的计算机...')
        else:
            self.os = XP
            self.LabelUIOS.SetBkImage('xp.jpg')
            self.LabelUIDescription.SetText('正在下载 XP 系统到您的计算机...')
        self.ProgressDownload.SetMaxValue(100)
        self.ProgressDownload.SetValue(self.progress)
        self.LabelWaiting.SetText('开始下载，请耐心等待')

        self.ContainerUIStep1.SetVisible(False)
        self.ContainerUIStep2.SetVisible(True)
        self.ContainerUIStep3.SetVisible(False)

        t = threading.Thread(target=PyThreadDownloadEaz,args=(self,))
        t.start()

    def OnNotify(self, sendor, sType, wParam, lParam):
        if sType == DUI_MSGTYPE_CLICK:
            if sendor == "BtnDownloadTooSlow":
                PyWin32Util.ShellExcute(0, 'open', 'http://www.xiaoniuhui.com/index.php#!/%E5%B0%8F%E5%A6%9E%E4%BC%9A%E8%A3%85%E6%9C%BA', '', '', 1)
            elif sendor == "BtnWin7" or sendor == "BtnXP":
                self.OnBtnWin7orBtnXP(sendor, sType, wParam, lParam)
            elif sendor == "ButtonUIReboot":
                UICommon.ShowMessageBox(self.GetHWnd(), '准备安装', '重启安装部分未实现，请耐心等待...')
            elif sendor == "adv1":
                pass
            elif sendor == "adv2":
                pass
            elif sendor == "adv3":
                pass
            elif sendor == "adv4":
                pass
            elif sendor == "adv5":
                pass

        if sType == DUI_MSGTYPE_ITEMSELECT:
            pass

