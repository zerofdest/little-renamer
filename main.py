import os
import subprocess

def main():
    print("请选择重命名方法：")
    print("1. 按名称自动匹配（推荐）")
    print("2. 按集号匹配")
    
    choice = input("请输入选择的方法编号：").strip()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if choice == '1':
        script_path = os.path.join(current_dir, 'method0.py')
        subprocess.call(['python', script_path])
    elif choice == '2':
        script_path = os.path.join(current_dir, 'method1.py')
        subprocess.call(['python', script_path])
    else:
        print("无效选择")

if __name__ == "__main__":
    main()
