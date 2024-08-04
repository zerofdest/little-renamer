import os

def generate_rename_log(mkv_files_raw, ass_files):
    rename_log = []
    for i, ass_file in enumerate(ass_files):
        mkv_file = mkv_files_raw[i]
        new_ext = '.ass' if ass_file.endswith('.ass') else '.ssa'
        new_ass_name = os.path.splitext(mkv_file)[0] + new_ext
        rename_log.append((ass_file, new_ass_name))
    return rename_log

def preview_rename_log(rename_log):
    print("预览重命名日志：")
    for index, (origin, new) in enumerate(rename_log):
        print(f"{index + 1}. {origin} -> {new}")

def renamer(directory, begin_serial_number):
    # 检查目录是否存在
    if not os.path.isdir(directory):
        print(f"错误: 目录 '{directory}' 不存在")
        return
    
    # 检查 begin_serial_number 是否为两位数
    if not begin_serial_number.isdigit() or len(begin_serial_number) != 2:
        print(f"错误: 起始集数'{begin_serial_number}'格式错误，请输入两位数（例如'01'）")
        return
        
    # 获取目录下的所有文件
    files = os.listdir(directory)
    
    # 过滤出 .mkv 和 .ass 文件，并分别排序
    mkv_files = sorted([f for f in files if f.endswith('.mkv')])
    ass_files = sorted([f for f in files if f.endswith('.ass')])

    if not ass_files:
        ass_files = [f for f in os.listdir(directory) if f.endswith('.ssa')]

    if not mkv_files or not ass_files:
        print("路径中没有找到.mkv或或字幕文件(.ass或.ssa)。")
        return
    
    # 检索第一个包含起始序号的 .mkv 文件
    start_index = None
    for index, mkv_file in enumerate(mkv_files):
        if begin_serial_number in mkv_file:
            start_index = index
            break
    
    if start_index is None:
        print(f"错误: 找不到包含 '{begin_serial_number}' 的 .mkv 文件")
        return
    
    # 获取包含起始序号的 .mkv 文件及其之后总计 n 个 .mkv 文件组成新的列表 mkv_files_raw
    n = len(ass_files)
    mkv_files_raw = mkv_files[start_index:start_index + n]

    # 检查是否有足够的 .mkv 文件匹配 .ass 文件
    if len(mkv_files_raw) < n:
        print(f"错误: 从 {begin_serial_number} 开始的 .mkv 文件不足以匹配所有 .ass 文件")
        return

    # 生成初始的重命名日志
    rename_log = generate_rename_log(mkv_files_raw, ass_files)
    
    while True:
        # 预览重命名日志
        preview_rename_log(rename_log)
        
        # 询问用户是否确认重命名，或者从第 k 个文件开始不重命名
        confirm = input("是否确认重命名？(Y/N)，或者输入开始跳过的文件序号：").strip().upper()
        
        if confirm == 'N':
            print("操作已取消")
            return
        elif confirm == 'Y':
            # 执行重命名
            for ass_file, new_ass_name in rename_log:
                os.rename(os.path.join(directory, ass_file), os.path.join(directory, new_ass_name))
            print("重命名完成")
            return
        elif confirm.isdigit():
            k = int(confirm)
            if 1 <= k <= n:
                # 生成新的重命名日志，只包括前 k-1 个文件
                rename_log = generate_rename_log(mkv_files_raw[:k-1], ass_files[:k-1])
            else:
                print("无效输入，文件序号超出范围")
        else:
            print("无效输入，请输入Y、N或跳过的文件序号")

if __name__ == "__main__":
    # 用户输入路径
    directory = input("请输入包含字幕文件和视频文件的路径（请确保字幕文件只包含正片）：")
    begin_serial_number = input("请输入起始集数（例如'01'）：")
    renamer(directory, begin_serial_number)
