from distutils.core import setup
import py2exe

setup(console=[
               {
                'script':'LabCuro_lab_v2.0.py',
                'icon_resources': [(1, 'bin\images\labcuro_chromatogram.ico')]
                }
               ],
      )