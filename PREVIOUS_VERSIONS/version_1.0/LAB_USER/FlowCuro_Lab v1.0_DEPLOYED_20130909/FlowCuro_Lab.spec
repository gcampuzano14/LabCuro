# -*- mode: python -*-
a = Analysis(['FlowCuro_Lab.py'],
             pathex=['C:\\Users\\germancz\\Dropbox\\Programming\\Python\\APPS\\pyinstaller'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'FlowCuro_Lab.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
