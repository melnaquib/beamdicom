# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\work\\code\\beamdicom'],
             binaries=[],
             datas=[('C:\\Users\\Abdulrahman\\Anaconda3\\Library\\plugins\\platforms\\*.dll', 'platforms') ,('C:\\Users\\Abdulrahman\\Anaconda3\\Library\\qml\\' ,'.'),
			 ('C:\\Users\\Abdulrahman\\Anaconda3\\Library\\bin\\Qt5Quick.dll','.'),
			 ('c:\\work\\code\\beamdicom\\logo.ico\\','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
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
          name='beamdicom',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='beamdicom')