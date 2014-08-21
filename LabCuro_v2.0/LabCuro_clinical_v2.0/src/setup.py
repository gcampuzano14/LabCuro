from distutils.core import setup
import py2exe

setup(console=[
               {
                'script':'labcuro_clinical_v2.pyw',
                'icon_resources': [(1, 'bin\images\labcuro_icon.ico')]
                }
               ],
      )