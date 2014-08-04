# -*- mode: python -*-
a = Analysis(['D:\\Dropbox\\Programming\\Python\\PY_APPS_COLLABORATIVE\\LabCuro\\LabCuro_v2.0\\LabCuro_lab_v2.0\\src\\LabCuro_lab_v2.0.py'],
             pathex=['D:\\Dropbox\\Programming\\Python\\PY_APPS_COLLABORATIVE\\LabCuro\\LabCuro_v2.0\\LabCuro_lab_v2.0\\compiled'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\LabCuro Laboratory Suite v2.0', 'LabCuro Laboratory Suite v2.0.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='D:\\Dropbox\\Programming\\Python\\PY_APPS_COLLABORATIVE\\LabCuro\\LabCuro_v2.0\\LabCuro_lab_v2.0\\src\\bin\\images\\labcuro_chromatogram.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'LabCuro Laboratory Suite v2.0'))
