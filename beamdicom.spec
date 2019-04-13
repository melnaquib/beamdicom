# -*- mode: python -*-

block_cipher = None

a = Analysis(['app.py', , 'dist/obf/app.py'],
             pathex=['C:\\work\\code\\beamdicom'],
             binaries=[],
             datas=[('C:\\work\\opt\\py\\Anaconda3\\Library\\plugins\\platforms\\*.dll', 'platforms') ,('C:\\work\\opt\\py\\Anaconda3\\Library\\qml\\' ,'.'),
			 ('C:\\work\\opt\\py\\Anaconda3\\Library\\bin\\Qt5Quick.dll','.'),
			 ('c:\\work\\code\\beamdicom\\logo.ico\\','.')],
             hiddenimports=[beamdicom],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.scripts[0] = 'app', 'dist/obf/app.py', 'PYSOURCE'
for i in range(len(a.pure)):
    if a.pure[i][1].startswith(a.pathex[0]):
        a.pure[i] = a.pure[i][0], a.pure[i][1].replace(a.pathex[0], os.path.abspath('dist/obf'), a.pure[i][2]

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
