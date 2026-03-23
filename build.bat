@echo off
echo ========================================
echo 字幕繁简转换工具 - 打包脚本
echo ========================================
echo.

echo 正在清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

echo.
echo 正在创建spec文件...
echo # -*- mode: python ; coding: utf-8 -*- > SubtitleConverter.spec
echo. >> SubtitleConverter.spec
echo block_cipher = None >> SubtitleConverter.spec
echo. >> SubtitleConverter.spec
echo a = Analysis( >> SubtitleConverter.spec
echo     ['subtitle_converter.py'], >> SubtitleConverter.spec
echo     pathex=[], >> SubtitleConverter.spec
echo     binaries=[], >> SubtitleConverter.spec
echo     datas=[], >> SubtitleConverter.spec
echo     hiddenimports=['tkinter', 'tkinterdnd2', 'opencc'], >> SubtitleConverter.spec
echo     hookspath=[], >> SubtitleConverter.spec
echo     hooksconfig={}, >> SubtitleConverter.spec
echo     runtime_hooks=[], >> SubtitleConverter.spec
echo     excludes=[], >> SubtitleConverter.spec
echo     win_no_prefer_redirects=False, >> SubtitleConverter.spec
echo     win_private_assemblies=False, >> SubtitleConverter.spec
echo     cipher=block_cipher, >> SubtitleConverter.spec
echo     noarchive=False, >> SubtitleConverter.spec
echo ^) >> SubtitleConverter.spec
echo. >> SubtitleConverter.spec
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher) >> SubtitleConverter.spec
echo. >> SubtitleConverter.spec
echo exe = EXE( >> SubtitleConverter.spec
echo     pyz, >> SubtitleConverter.spec
echo     a.scripts, >> SubtitleConverter.spec
echo     a.binaries, >> SubtitleConverter.spec
echo     a.zipfiles, >> SubtitleConverter.spec
echo     a.datas, >> SubtitleConverter.spec
echo     [], >> SubtitleConverter.spec
echo     name='SubtitleConverter', >> SubtitleConverter.spec
echo     debug=False, >> SubtitleConverter.spec
echo     bootloader_ignore_signals=False, >> SubtitleConverter.spec
echo     strip=False, >> SubtitleConverter.spec
echo     upx=True, >> SubtitleConverter.spec
echo     upx_exclude=[], >> SubtitleConverter.spec
echo     runtime_tmpdir=None, >> SubtitleConverter.spec
echo     console=False, >> SubtitleConverter.spec
echo     disable_windowed_traceback=False, >> SubtitleConverter.spec
echo     argv_emulation=False, >> SubtitleConverter.spec
echo     target_arch=None, >> SubtitleConverter.spec
echo     codesign_identity=None, >> SubtitleConverter.spec
echo     entitlements_file=None, >> SubtitleConverter.spec
echo     version='version_info.txt', >> SubtitleConverter.spec
echo     icon=None, >> SubtitleConverter.spec
echo ^) >> SubtitleConverter.spec

echo.
echo 正在打包exe文件...
pyinstaller SubtitleConverter.spec --clean

echo.
echo ========================================
echo 打包完成！
echo.
echo 输出文件: dist\SubtitleConverter.exe
echo ========================================
echo.
pause
