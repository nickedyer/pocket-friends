import os
import PyInstaller.__main__
import pocket_friends

script_dir = os.path.dirname(__file__)

PyInstaller.__main__.run([
    '{0}/pocket_friends/__main__.py'.format(script_dir),
    '--clean',
    '--noconsole',
    '--onefile',
    '--name=pocket_friends_{0}'.format(pocket_friends.__version__),
    '--collect-all=pocket_friends',
    '--icon={0}/pocket_friends/game_files/resources/images/icon/icon.ico'.format(script_dir)
])