# -*- mode: python -*-
a = Analysis(['D:\\Dropbox\\Programming\\Python\\PY_APPS_COLLABORATIVE\\LabCuro\\LabCuro_v2.0\\LabCuro_clinical_v2.0\\src\\labcuro_clinical_v2.pyw'],
             pathex=['D:\\Dropbox\\Programming\\Python\\PY_APPS_COLLABORATIVE\\LabCuro\\LabCuro_v2.0\\LabCuro_clinical_v2.0\\compiled'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\LabCuro Clinical Suite v2.0', 'LabCuro Clinical Suite v2.0.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='D:\\Dropbox\\Programming\\Python\\PY_APPS_COLLABORATIVE\\LabCuro\\LabCuro_v2.0\\LabCuro_clinical_v2.0\\src\\bin\\images\\labcuro_icon.ico')
coll = COLLECT(exe,
               Tree('D:\\Dropbox\\Programming\\Python\\PY_APPS_COLLABORATIVE\\LabCuro\\LabCuro_v2.0\\LabCuro_clinical_v2.0\\src\\bin\\images'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'LabCuro Clinical Suite v2.0'))
app = BUNDLE(coll,
             name=os.path.join('dist', 'LabCuro Clinical Suite v2.0.app'))
