import os
import glob
import re

def extract_poc_info():
    """
    提取所有.poc文件中的 id、name、severity 字段
    """
    # 获取当前目录下所有.poc文件
    poc_files = glob.glob("*.poc")
    
    if not poc_files:
        print("当前目录下没有找到.poc文件")
        return []
    
    extracted_info = []
    
    for poc_file in poc_files:
        try:
            # 初始化字段值
            poc_id = ""
            poc_name = ""
            severity = ""
            
            # 打开并读取文件内容
            with open(poc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 使用正则表达式提取字段
                # 提取 id
                id_match = re.search(r'##\s*id:\s*(.+)', content, re.IGNORECASE)
                if id_match:
                    poc_id = id_match.group(1).strip()
                
                # 提取 name
                name_match = re.search(r'##\s*name:\s*(.+)', content, re.IGNORECASE)
                if name_match:
                    poc_name = name_match.group(1).strip()
                
                # 提取 severity
                severity_match = re.search(r'##\s*severity:\s*(.+)', content, re.IGNORECASE)
                if severity_match:
                    severity = severity_match.group(1).strip()
                
                # 如果至少有一个字段被提取到，就保存
                if poc_id or poc_name or severity:
                    extracted_info.append({
                        'file': poc_file,
                        'id': poc_id,
                        'name': poc_name,
                        'severity': severity
                    })
                    print(f"✓ 已提取: {poc_file}")
                else:
                    print(f"⚠ 未找到目标字段: {poc_file}")
                    
        except UnicodeDecodeError:
            # 如果UTF-8解码失败，尝试其他编码
            try:
                with open(poc_file, 'r', encoding='gbk') as f:
                    content = f.read()
                    
                    id_match = re.search(r'##\s*id:\s*(.+)', content, re.IGNORECASE)
                    if id_match:
                        poc_id = id_match.group(1).strip()
                    
                    name_match = re.search(r'##\s*name:\s*(.+)', content, re.IGNORECASE)
                    if name_match:
                        poc_name = name_match.group(1).strip()
                    
                    severity_match = re.search(r'##\s*severity:\s*(.+)', content, re.IGNORECASE)
                    if severity_match:
                        severity = severity_match.group(1).strip()
                    
                    if poc_id or poc_name or severity:
                        extracted_info.append({
                            'file': poc_file,
                            'id': poc_id,
                            'name': poc_name,
                            'severity': severity
                        })
                        print(f"✓ 已提取: {poc_file}")
                    else:
                        print(f"⚠ 未找到目标字段: {poc_file}")
                        
            except Exception as e:
                print(f"✗ 读取文件 {poc_file} 时出错: {e}")
                
        except Exception as e:
            print(f"✗ 处理文件 {poc_file} 时出错: {e}")
    
    return extracted_info

def save_to_txt(extracted_info, filename='poc_info.txt'):
    """
    将提取的信息保存到txt文件
    """
    with open(filename, 'w', encoding='utf-8') as f:
        # 写入标题
        f.write("="*80 + "\n")
        f.write("POC文件信息提取结果\n")
        f.write(f"生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        if not extracted_info:
            f.write("未找到任何包含目标字段的POC文件\n")
            return
        
        # 统计信息
        total_files = len(extracted_info)
        f.write(f"共提取 {total_files} 个POC文件的信息\n")
        f.write("-"*80 + "\n\n")
        
        # 逐条写入详细信息
        for idx, info in enumerate(extracted_info, 1):
            f.write(f"【{idx}】文件名: {info['file']}\n")
            f.write(f"## id: {info['id'] if info['id'] else '未找到'}\n")
            f.write(f"## name: {info['name'] if info['name'] else '未找到'}\n")
            f.write(f"## severity: {info['severity'] if info['severity'] else '未找到'}\n")
            f.write("\n" + "-"*80 + "\n\n")
        
        # 添加汇总信息
        f.write("\n" + "="*80 + "\n")
        f.write("汇总信息:\n")
        f.write(f"总文件数: {total_files}\n")
        
        # 按严重程度统计
        severity_count = {}
        for info in extracted_info:
            if info['severity']:
                sev = info['severity'].lower()
                severity_count[sev] = severity_count.get(sev, 0) + 1
        
        if severity_count:
            f.write("\n按严重程度统计:\n")
            for sev, count in sorted(severity_count.items()):
                f.write(f"  - {sev}: {count}个\n")

def save_to_csv(extracted_info, filename='poc_info.csv'):
    """
    可选：将提取的信息保存为CSV格式，方便Excel打开
    """
    import csv
    
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['文件名', 'ID', '名称', '严重程度'])
        
        for info in extracted_info:
            writer.writerow([
                info['file'],
                info['id'],
                info['name'],
                info['severity']
            ])
    
    print(f"CSV格式已保存到: {filename}")

def print_summary(extracted_info):
    """
    在控制台打印摘要信息
    """
    print("\n" + "="*80)
    print("提取完成！")
    print(f"共处理了 {len(extracted_info)} 个包含目标字段的POC文件")
    print("="*80)
    
    if extracted_info:
        print("\n前5个文件的摘要信息:")
        for idx, info in enumerate(extracted_info[:5], 1):
            print(f"\n{idx}. {info['file']}")
            print(f"   ID: {info['id']}")
            print(f"   Name: {info['name'][:60]}{'...' if len(info['name']) > 60 else ''}")
            print(f"   Severity: {info['severity']}")
        
        if len(extracted_info) > 5:
            print(f"\n... 还有 {len(extracted_info) - 5} 个文件，详见输出文件")
    
    # 统计严重程度分布
    severity_stats = {}
    for info in extracted_info:
        sev = info['severity'] if info['severity'] else '未知'
        severity_stats[sev] = severity_stats.get(sev, 0) + 1
    
    if severity_stats:
        print("\n严重程度分布:")
        for sev, count in sorted(severity_stats.items()):
            print(f"  {sev}: {count}个")

def main():
    """
    主函数
    """
    print("开始扫描并提取POC文件信息...")
    print("正在提取字段: ## id, ## name, ## severity")
    print("-"*80)
    
    # 提取信息
    extracted_info = extract_poc_info()
    
    if not extracted_info:
        print("\n未找到任何包含目标字段的POC文件")
        return
    
    # 保存为txt文件
    txt_filename = 'poc_extracted_info.txt'
    save_to_txt(extracted_info, txt_filename)
    print(f"\n✓ TXT格式已保存到: {txt_filename}")
    
    # 可选：同时保存为CSV格式
    csv_filename = 'poc_extracted_info.csv'
    save_to_csv(extracted_info, csv_filename)
    print(f"✓ CSV格式已保存到: {csv_filename}")
    
    # 打印摘要
    print_summary(extracted_info)
    
    # 如果只想保存为TXT，注释掉CSV部分即可

if __name__ == "__main__":
    main()