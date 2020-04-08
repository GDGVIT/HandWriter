# -*- mode: python -*-

block_cipher = None


a = Analysis(['/home/zeus/HandwritingParser/src/main/python/main.py'],
             pathex=['/home/zeus/HandwritingParser/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=['pkg_resources.py2_warn', 'six', 'cv2', 'PIL', 'PIL.Image'],
             hookspath=['/home/zeus/HandwritingParser/env/lib/python3.6/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/home/zeus/HandwritingParser/target/PyInstaller/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='HandWriter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='HandWriter')
