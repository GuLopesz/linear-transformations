import subprocess
import sys

subprocess.Popen([sys.executable, "square.py"])
subprocess.Popen([sys.executable, "cube.py"])
#arquivo para rodar as duas janelas do matplot ao mesmo tempo