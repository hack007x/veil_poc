import os
import glob

def find_poc_files_with_timeout():
    """
    查找当前目录下所有.poc文件中包含 '#@ timeout: 20' 或 '#@ timeout: 30' 字段的文件
    """
    # 获取当前目录下所有.poc文件
    poc_files = glob.glob("*.poc")
    
    if not poc_files:
        print("当前目录下没有找到.poc文件")
        return
    
    # 定义要查找的timeout值
    timeout_values = ['20', '30']
    matching_files = {
        '20': [],
        '30': [],
        'both': []
    }
    
    # 遍历每个.poc文件
    for poc_file in poc_files:
        try:
            # 打开并读取文件内容
            with open(poc_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                has_timeout_20 = '#@ timeout: 20' in content
                has_timeout_30 = '#@ timeout: 30' in content
                
                if has_timeout_20 and has_timeout_30:
                    matching_files['both'].append(poc_file)
                elif has_timeout_20:
                    matching_files['20'].append(poc_file)
                elif has_timeout_30:
                    matching_files['30'].append(poc_file)
                    
        except Exception as e:
            print(f"读取文件 {poc_file} 时出错: {e}")
    
    # 输出结果
    total_count = len(matching_files['20']) + len(matching_files['30']) + len(matching_files['both'])
    
    if total_count > 0:
        print(f"找到 {total_count} 个包含 timeout 字段的.poc文件:")
        print("=" * 60)
        
        if matching_files['20']:
            print(f"\n⏱️  包含 '#@ timeout: 20' 的文件 ({len(matching_files['20'])}个):")
            for file in matching_files['20']:
                print(f"   ✓ {file}")
        
        if matching_files['30']:
            print(f"\n⏱️  包含 '#@ timeout: 30' 的文件 ({len(matching_files['30'])}个):")
            for file in matching_files['30']:
                print(f"   ✓ {file}")
        
        if matching_files['both']:
            print(f"\n🔄 同时包含两种 timeout 的文件 ({len(matching_files['both'])}个):")
            for file in matching_files['both']:
                print(f"   ✓ {file}")
    else:
        print("未找到包含 '#@ timeout: 20' 或 '#@ timeout: 30' 的.poc文件")

def find_poc_files_with_timeout_detailed():
    """
    详细版本：显示更多信息，包括文件路径和匹配的行
    """
    poc_files = glob.glob("*.poc")
    
    if not poc_files:
        print("当前目录下没有找到.poc文件")
        return
    
    matching_files = []
    timeout_values = ['20', '30']
    
    for poc_file in poc_files:
        try:
            with open(poc_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
                # 检查每一行
                matching_lines = []
                has_timeout_20 = False
                has_timeout_30 = False
                
                for line_num, line in enumerate(lines, 1):
                    if '#@ timeout: 20' in line:
                        matching_lines.append((line_num, line.strip(), '20'))
                        has_timeout_20 = True
                    elif '#@ timeout: 30' in line:
                        matching_lines.append((line_num, line.strip(), '30'))
                        has_timeout_30 = True
                
                if matching_lines:
                    matching_files.append({
                        'filename': poc_file,
                        'matches': matching_lines,
                        'has_20': has_timeout_20,
                        'has_30': has_timeout_30
                    })
                    
        except Exception as e:
            print(f"读取文件 {poc_file} 时出错: {e}")
    
    # 输出结果
    if matching_files:
        print(f"找到 {len(matching_files)} 个包含 timeout 字段的.poc文件:")
        print("=" * 60)
        
        for match_info in matching_files:
            # 根据包含的timeout类型显示不同图标
            if match_info['has_20'] and match_info['has_30']:
                icon = "🔄"
                timeout_type = "同时包含 timeout:20 和 timeout:30"
            elif match_info['has_20']:
                icon = "⏱️"
                timeout_type = "包含 timeout:20"
            else:
                icon = "⏰"
                timeout_type = "包含 timeout:30"
                
            print(f"\n{icon} 文件: {match_info['filename']} ({timeout_type})")
            print(f"   匹配位置:")
            for line_num, line, timeout_val in match_info['matches']:
                print(f"     第 {line_num} 行: {line}")
    else:
        print("未找到包含 '#@ timeout: 20' 或 '#@ timeout: 30' 的.poc文件")

def find_poc_files_custom_timeout(*timeout_values):
    """
    自定义版本：可以查找任意指定的timeout值
    
    参数:
        *timeout_values: 要查找的timeout值，如 20, 30, 60 等
    """
    if not timeout_values:
        print("请指定要查找的timeout值，如: find_poc_files_custom_timeout(20, 30, 60)")
        return
    
    poc_files = glob.glob("*.poc")
    
    if not poc_files:
        print("当前目录下没有找到.poc文件")
        return
    
    # 初始化结果字典
    matching_files = {}
    for value in timeout_values:
        matching_files[str(value)] = []
    
    matching_files['multiple'] = []  # 包含多个不同timeout的文件
    
    for poc_file in poc_files:
        try:
            with open(poc_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                found_values = []
                for value in timeout_values:
                    search_pattern = f'#@ timeout: {value}'
                    if search_pattern in content:
                        matching_files[str(value)].append(poc_file)
                        found_values.append(value)
                
                if len(found_values) > 1:
                    matching_files['multiple'].append({
                        'file': poc_file,
                        'values': found_values
                    })
                    
        except Exception as e:
            print(f"读取文件 {poc_file} 时出错: {e}")
    
    # 输出结果
    total_count = sum(len(matching_files[str(v)]) for v in timeout_values)
    
    if total_count > 0:
        print(f"查找 timeout 值为 {', '.join(map(str, timeout_values))} 的文件:")
        print("=" * 60)
        
        for value in timeout_values:
            if matching_files[str(value)]:
                print(f"\n🔍 包含 '#@ timeout: {value}' 的文件 ({len(matching_files[str(value)])}个):")
                for file in matching_files[str(value)]:
                    print(f"   ✓ {file}")
        
        if matching_files['multiple']:
            print(f"\n🔄 包含多个不同 timeout 值的文件:")
            for item in matching_files['multiple']:
                print(f"   ✓ {item['file']} (包含: {', '.join(map(str, item['values']))})")
    else:
        print(f"未找到包含 timeout 值为 {', '.join(map(str, timeout_values))} 的.poc文件")

if __name__ == "__main__":
    print("🔍 开始查找包含 '#@ timeout: 20' 或 '#@ timeout: 30' 的.poc文件...\n")
    
    # 使用简单版本
    find_poc_files_with_timeout()
    
    print("\n" + "="*60 + "\n")
    
    # 使用详细版本（显示具体行号）
    find_poc_files_with_timeout_detailed()
    
    print("\n" + "="*60 + "\n")
    
    # 使用自定义版本示例（可以指定任意timeout值）
    print("自定义版本示例 - 查找 timeout: 20, 30, 60:")
    find_poc_files_custom_timeout(20, 30, 60)