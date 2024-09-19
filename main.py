import downconv

import pandas as pd


#엑셀 파일 읽어오기
df = pd.read_excel('download_links.xlsx')

# 각 행을 딕셔너리로 변환한 리스트로 변환
records_list = df.to_dict('records')

# 변환된 리스트 출력 (확인용)
for record in records_list:
    print(record)