from distutils.core import setup
from datetime import datetime
import py2exe


setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console = [
        {
            'script':'proxy.py',
            'icon_resources':[(0,'icon.ico')],
            'dest_base' : 'trackmania_proxy_{}'.format(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
        }
    ],
    zipfile = None,
)