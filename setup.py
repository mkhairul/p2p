from distutils.core import setup
import py2exe

setup(name="mka_clientServer", console = ["client.py", "server.py"])