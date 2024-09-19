import pandas as pd
from googleapiclient.discovery import build

# 엑셀 파일 불러오기
file_path = 'downloads_list.xlsx'  # 여기에 엑셀 파일 경로를 입력하세요.
df = pd.read_excel(file_path)

# 유튜브 API 설정 (API 키 필요)
API_KEY = 'AIzaSyAMQbHhwszc7Vui2raO6yOyl1bHTGVo6ds'  # 여기에 유튜브 API 키를 입력하세요.
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 유튜브에서 플레이리스트 링크 검색 함수
def search_youtube(artist, album_name):
    query = f'{artist} {album_name} playlist'
    
    # 유튜브 검색 요청
    request = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=1,
        type='playlist'
    )
    response = request.execute()

    # 검색 결과에서 링크 추출
    if response['items']:
        playlist_id = response['items'][0]['id']['playlistId']
        playlist_url = f'https://www.youtube.com/playlist?list={playlist_id}'
        return playlist_url
    return None

# 각 행에 대해 유튜브 검색하여 링크 업데이트
for i, row in df.iterrows():
    artist = row['아티스트']
    album_name = row['앨범명']
    youtube_link = search_youtube(artist, album_name)
    
    if youtube_link:
        df.at[i, '유튜브 링크'] = youtube_link

# 수정된 데이터프레임을 새로운 엑셀 파일로 저장
output_file_path = 'download_links.xlsx'
df.to_excel(output_file_path, index=False)

print(f'업데이트된 엑셀 파일이 {output_file_path}에 저장되었습니다.')
