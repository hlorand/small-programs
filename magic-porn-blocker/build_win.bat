
REM requirements: install pyinstaller and add Python installation folder and /Scripts subfolder to Windows PATH

pip install elevate
pip install python_hosts

pyinstaller --onefile --add-data "block.py;." --add-data "mpb_logo.png;." program.py
