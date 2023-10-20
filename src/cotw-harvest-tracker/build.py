import os
import subprocess
from pathlib import Path
import nicegui

cmd = [
    'python',
    '-m', 'PyInstaller',
    'main.py', # your main file with ui.run()
    '--name', 'CotW Harvest Tracker', # name of your app
    '--onefile',
    '--distpath', f'{Path(__file__).parent.parent.parent}/dist'
]
subprocess.call(cmd)