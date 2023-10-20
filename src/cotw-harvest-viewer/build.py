import os
import subprocess
from pathlib import Path
import nicegui

cmd = [
    'python',
    '-m', 'PyInstaller',
    'main.py', # your main file with ui.run()
    '--name', 'CotW Harvest Viewer', # name of your app
    '--onefile',
    '--noconsole', # prevent console appearing, only use with ui.run(native=True, ...)
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',
    '--distpath', f'{Path(__file__).parent.parent.parent}/dist'
]
subprocess.call(cmd)