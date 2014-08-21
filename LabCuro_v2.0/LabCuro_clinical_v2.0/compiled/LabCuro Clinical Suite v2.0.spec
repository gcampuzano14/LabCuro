# -*- mode: python -*-
a = Analysis(['C:\\Documents and Settings\\gcampuzanozuluaga\\My Documents\\Dropbox\\PC_SHARE\\LabCuro_clinical_v2.0\\src\\labcuro_clinical_v2.pyw'],
             pathex=['C:\\Documents and Settings\\gcampuzanozuluaga\\My Documents\\Dropbox\\PC_SHARE\\LabCuro_clinical_v2.0\\compiled'],
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
          console=False , icon='C:\\Documents and Settings\\gcampuzanozuluaga\\My Documents\\Dropbox\\PC_SHARE\\LabCuro_clinical_v2.0\\src\\bin\\images\\labcuro_icon.ico')
coll = COLLECT(exe,
               Tree('C:\\Documents and Settings\\gcampuzanozuluaga\\My Documents\\Dropbox\\PC_SHARE\\LabCuro_clinical_v2.0\\src\\bin\\images'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'LabCuro Clinical Suite v2.0'))
app = BUNDLE(coll,
             name=os.path.join('dist', 'LabCuro Clinical Suite v2.0.app'))
