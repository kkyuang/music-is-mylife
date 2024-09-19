import os
from pytubefix import Playlist

import subprocess

class downconv:
    @staticmethod
    def convert_mp3_to_m4a_using_ffmpeg(mp3_path, output_path):
        # ffmpeg 명령어를 subprocess로 실행
        command = [
            'ffmpeg',
            '-i', mp3_path,  # 입력 파일
            '-vn',  # 비디오 스트림을 제외
            '-c:a', 'aac',  # 오디오 코덱: AAC
            '-b:a', '192k',  # 비트레이트 설정 (원하는 비트레이트로 변경 가능)
            output_path  # 출력 파일
        ]

        # subprocess로 ffmpeg 실행
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 오류가 발생했는지 확인
        if process.returncode != 0:
            print(f"Error: {process.stderr.decode('utf-8')}")
        else:
            print("변환 완료!")


    @staticmethod
    def make_alpha_numeric(string):
        return ''.join(char for char in string if char.isalnum())


    @staticmethod
    #유튜브 플레이리스트 다운로드
    def playlistdownload(link):

        yt_playlist = Playlist(link)

        folderName =  downconv.make_alpha_numeric(yt_playlist.title)
        os.mkdir(folderName)

        totalVideoCount = len(yt_playlist.videos)
        print("Total videos in playlist: 🎦", totalVideoCount)

        files = []

        #앨범 순서대로 번호 정렬
        i = 1
        for index, video in enumerate(yt_playlist.videos, start=1):
            print("Downloading:", video.title)
            video_size = video.streams.get_highest_resolution().filesize
            print("Size:", video_size // (1024 ** 2), "🗜 MB")
            files.append(video.streams.get_highest_resolution().download(output_path=folderName, filename_prefix=str(i) + ' ', mp3=True))
            print("Downloaded:", str(i) + ' ' + video.title, "✨ successfully!")
            print("Remaining Videos:", totalVideoCount - index)
            i+=1

        print("All videos downloaded successfully! 🎉")

        return files

    @staticmethod
    #M4A로 변환(아이팟 인식 가능한 파일)
    def convertToM4A(files):
        print(files)
        for f in files:
            print(f)
            downconv.convert_mp3_to_m4a_using_ffmpeg(f, f[0:-3] + 'm4a')

    @staticmethod
    #MP3 파일 삭제
    def removemp3(files):
        for f in files:
            os.remove(f)


    
    
link = input("Enter YouTube Playlist URL: ✨")

files = downconv.playlistdownload(link)

print("M4A 파일로 변환합니다.")
downconv.convertToM4A(files)

print("MP3 파일을 삭제합니다.")
downconv.removemp3(files)