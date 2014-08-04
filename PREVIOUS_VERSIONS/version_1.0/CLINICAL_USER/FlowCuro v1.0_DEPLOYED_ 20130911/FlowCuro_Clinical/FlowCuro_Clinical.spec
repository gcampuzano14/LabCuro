# -*- mode: python -*-
a = Analysis(['FlowCuro_Clinical.pyw'],
             pathex=['C:\\Users\\germancz\\Dropbox\\Programming\\Python\\APPS\\pyinstaller-2.0'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'FlowCuro_Clinical.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name=os.path.join('dist', 'FlowCuro_Clinical.exe.app'))
