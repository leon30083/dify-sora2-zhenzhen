import zipfile
import os

# 删除旧包
if os.path.exists('sora2-video-plugin.difypkg'):
    os.remove('sora2-video-plugin.difypkg')

# 文件列表
files_to_include = [
    'manifest.yaml',
    'main.py',
    'requirements.txt',
    '_assets/icon.svg',
    'provider/sora2.yaml',
    'provider/sora2.py',
    'tools/text_to_video.yaml',
    'tools/text_to_video.py',
    'tools/image_to_video.yaml',
    'tools/image_to_video.py'
]

# 创建新的 zip 包
with zipfile.ZipFile('sora2-video-plugin.difypkg', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file_path in files_to_include:
        if os.path.exists(file_path):
            arcname = file_path.replace(os.sep, '/')
            zipf.write(file_path, arcname)
            print(f'Added: {arcname}')
        else:
            print(f'Missing: {file_path}')

print('')
print('Package created: sora2-video-plugin.difypkg')

# 验证内容
print('')
print('Package contents:')
with zipfile.ZipFile('sora2-video-plugin.difypkg', 'r') as zipf:
    for info in zipf.filelist:
        print(f'  {info.filename}: {info.file_size} bytes')
