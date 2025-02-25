import argparse
import re

def convert_partition(input_file, output_file):
    """Partition 파일을 NEXUS 형식으로 변환하는 함수"""

    # NEXUS 파일 헤더
    nexus_header = """#NEXUS

begin sets;
"""

    # 데이터 읽기 및 변환
    partition_lines = []
    with open(input_file, "r") as infile:
        for line in infile:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # 빈 줄이나 주석 건너뛰기
            
            # 정규식을 사용하여 이름과 범위 추출
            match = re.match(r"DNA, ([\w.]+) = (\d+)-(\d+)", line)
            if match:
                name, start, end = match.groups()
                start, end = int(start), int(end)
                partition_lines.append(f"    charset {name}_1 = {start}-{end}\\3;")
                partition_lines.append(f"    charset {name}_2 = {start+1}-{end}\\3;")
                partition_lines.append(f"    charset {name}_3 = {start+2}-{end}\\3;")

    # NEXUS 파일 저장
    with open(output_file, "w") as outfile:
        outfile.write(nexus_header)
        outfile.write("\n".join(partition_lines))
        outfile.write("\nend;\n")

    print(f"✅ NEXUS 파일이 '{output_file}' 로 생성되었습니다!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Partition 파일을 NEXUS 형식으로 변환")
    parser.add_argument("-i", "--input", required=True, help="입력 파일 (예: partition.txt)")
    parser.add_argument("-o", "--output", required=True, help="출력 파일 (예: partition.nex)")

    args = parser.parse_args()

    convert_partition(args.input, args.output)