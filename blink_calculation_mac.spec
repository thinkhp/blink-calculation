# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['blink_calculation_mac.py'],
    pathex=['/opt/miniconda3/envs/blinkcalculation/lib/python3.9/site-packages/'],
    binaries=[],
    datas=[('shape_predictor_68_face_landmarks.dat', '.')],  # 添加数据文件
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BlinkCalculation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为False来隐藏终端窗口
    # icon='app.icns',  # 如果有图标文件的话
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file='entitlements.plist',  # 添加授权文件
)

# 创建更详细的 Info.plist
info_plist = {
    'CFBundleDisplayName': 'BlinkCalculation',
    'CFBundleShortVersionString': '1.0.0',
    'CFBundleVersion': '1.0.0',
    'CFBundleIdentifier': 'com.yourdomain.blinkcalculation',
    'NSHighResolutionCapable': True,
    'NSCameraUsageDescription': 'This app needs access to camera to detect eye blinks.',
    'NSMicrophoneUsageDescription': 'This app needs access to microphone.',
    'LSMinimumSystemVersion': '10.13.0',
    'NSRequiresAquaSystemAppearance': False,
    'LSApplicationCategoryType': 'public.app-category.utilities',
    'NSPrincipalClass': 'NSApplication',
    'NSAppleEventsUsageDescription': 'This app needs to control other applications.',
    'CFBundleDocumentTypes': [],
    'UTExportedTypeDeclarations': []
}

app = BUNDLE(
    exe,
    name='BlinkCalculation.app',
    # icon='app.icns',  # 如果有图标文件的话
    bundle_identifier='com.yourdomain.blinkcalculation',
    info_plist=info_plist,
)
