# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# 收集 OpenCV 相关的所有依赖
cv2_bins = collect_all('cv2')[0]
datas = [('shape_predictor_68_face_landmarks.dat', '.')]
datas += collect_all('cv2')[1]

a = Analysis(
    ['blink_calculation_mac.py'],
    pathex=[],
    binaries=cv2_bins,  # 添加 OpenCV 二进制文件
    datas=datas,        # 添加 OpenCV 数据文件
    hiddenimports=['cv2', 'numpy'],  # 确保导入 cv2 和 numpy
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
    console=True,  # 临时设置为 True 以查看错误信息
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='BlinkCalculation.app',
    icon=None,
    bundle_identifier=None,
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': 'True',
        'NSCameraUsageDescription': 'This app needs access to camera to detect eye blinks.',
    },
)