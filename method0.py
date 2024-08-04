import os
import difflib

def find_best_match(subtitle, videos):
    matches = difflib.get_close_matches(subtitle, videos, n=3, cutoff=0.1)
    return matches[0] if matches else None

def preview_rename_log(rename_pairs):
    print("预览重命名日志：")
    for index, (origin, new) in enumerate(rename_pairs):
        print(f"{index + 1}. {origin} -> {new}")

def main():
    path = input("请输入包含视频与字幕文件的路径：")

    if not os.path.exists(path):
        print("路径不存在，请重新输入。")
        return

    mkv_files = [f for f in os.listdir(path) if f.endswith('.mkv')]
    ass_files = [f for f in os.listdir(path) if f.endswith('.ass')]

    if not ass_files:
        ass_files = [f for f in os.listdir(path) if f.endswith('.ssa')]

    if not mkv_files or not ass_files:
        print("路径中没有找到.mkv或或字幕文件(.ass或.ssa)。")
        return
    
    rename_pairs = []

    for ass_file in ass_files:
        base_ass_name = os.path.splitext(ass_file)[0]
        mkv_file = find_best_match(base_ass_name, mkv_files)
        if mkv_file:
            new_ext = '.ass' if ass_file.endswith('.ass') else '.ssa'
            new_name = os.path.splitext(mkv_file)[0] + new_ext
            rename_pairs.append((ass_file, new_name))

    if not rename_pairs:
        print("没有找到匹配的文件。")
        return


    while True:
        # 预览重命名日志
        preview_rename_log(rename_pairs)
        
        confirm = input("是否确认重命名？(Y/N)，或者第 k 个文件不重命名（输入 k）：").strip().upper()
        
        if confirm == 'N':
            print("操作已取消")
            return
        elif confirm == 'Y':
            # 执行重命名
            for old_name, new_name in rename_pairs:
                os.rename(os.path.join(path, old_name), os.path.join(path, new_name))
                print("重命名完成")
                return
        elif confirm.isdigit():
            k = int(confirm) - 1
            if 0 <= k < len(rename_pairs):
                rename_pairs.pop(k)
            else:
                print("无效输入，文件序号超出范围")
        else:
            print("无效输入，请输入Y、N或跳过的文件序号")


if __name__ == "__main__":
    main()
