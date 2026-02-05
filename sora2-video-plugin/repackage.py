import zipfile
import os

# 删除旧包
if os.path.exists('sora2-video-plugin.difypkg'):
    os.remove('sora2-video-plugin.difypkg')

# 创建新的 zip 包
with zipfile.ZipFile('sora2-video-plugin.difypkg', 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 添加 manifest.yaml
    zipf.write('manifest.yaml', 'manifest.yaml')

    # 添加 provider 目录文件
    for root, dirs, files in os.walk('provider'):
        for file in files:
            if '__pycache__' in root or file.endswith('.pyc'):
                continue
            file_path = os.path.join(root, file)
            arcname = file_path.replace(os.sep, '/')  # 转换为正斜杠
            zipf.write(file_path, arcname)

    # 添加 tools 目录文件
    for root, dirs, files in os.walk('tools'):
        for file in files:
            if '__pycache__' in root or file.endswith('.pyc'):
                continue
            file_path = os.path.join(root, file)
            arcname = file_path.replace(os.sep, '/')  # 转换为正斜杠
            zipf.write(file_path, arcname)

print('Package created: sora2-video-plugin.difypkg')

# 验证内容
print('')
print('Package contents:')
with zipfile.ZipFile('sora2-video-plugin.difypkg', 'r') as zipf:
    for info in zipf.filelist:
        print(f'  {info.filename}')
