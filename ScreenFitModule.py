import winreg
import wmi
import win32api, win32con

class monitor:
    def __init__(self):
        PATH = "SYSTEM\\ControlSet001\\Enum\\"
        m = wmi.WMI()
        # 获取屏幕信息
        monitors = m.Win32_DesktopMonitor()
        for m in monitors:
            subPath = m.PNPDeviceID  #
            # 可能有多个注册表
            if subPath == None:
                continue
            # 这个路径这里就是你的显示器在注册表中的路径，比如我现在的电脑是在HKEY_LOCAL_MACHINE下面的路径：
            # \SYSTEM\ControlSet001\Enum\DISPLAY\CMN1604\1&8713bca&0&UID0\Device Parameters
            infoPath = PATH + subPath + "\\Device Parameters"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, infoPath)
            # 屏幕信息按照一定的规则保存（EDID）
            value = winreg.QueryValueEx(key, "EDID")[0]
            winreg.CloseKey(key)

            # 屏幕实际尺寸
            self.width, self.height = value[21], value[22]
            # 推荐屏幕分辨率
            self.widthResolutionRecommend = value[56] + (value[58] >> 4) * 256
            self.heightResolutionRecommend = value[59] + (value[61] >> 4) * 256
            # 实际屏幕分辨率
            self.widthResolution = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得屏幕分辨率X轴
            self.heightResolution = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) # 获得屏幕分辨率Y轴
            # 屏幕像素密度（Pixels Per Inch）
            self.widthDensity = self.widthResolution / (self.width / 2.54)
            self.heightDensity = self.heightResolution / (self.height / 2.54)

    def show_info(self):
        print("屏幕宽度：", self.width, " (厘米)")
        print("屏幕高度：", self.height, " (厘米)")
        print("水平分辩率: ", self.widthResolution, " (像素)")
        print("垂直分辩率: ", self.heightResolution, " (像素)")
        # 保留小数点固定位数的两种方法
        print("水平像素密度: ", round(self.widthDensity, 2), " (PPI)")
        print("垂直像素密度: ", "%2.f" % self.heightDensity, " (PPI)")

    # 把毫米转换成像素
    def mm_to_px(self, mm):
        return mm * self.heightDensity / 25.4

# mnt = monitor()
# mnt.show_info()
# mm = 7.65
# print(mnt.mm_to_px(mm))
