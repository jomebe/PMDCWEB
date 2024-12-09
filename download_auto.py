import os
import zipfile
import shutil
import win32com.client
import time

# 사용자 바탕화면 경로
desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
# Documents의 기본 경로
documents = os.path.join(os.environ["USERPROFILE"], "Documents")
# 다운로드 폴더 경로
downloads = os.path.join(documents, "Downloads")
# cta.zip 파일 경로 (다운로드 후 이동될 위치)
zip_path = os.path.join(downloads, "cta.zip")
# download_auto.py 파일 경로
download_auto_path = os.path.join(downloads, "download_auto.py")
# 압축 해제 대상 폴더
extract_folder = os.path.join(documents, "cta")
# 최종 exe 파일 경로
exe_relative_path = os.path.join("dhw", "dhw", "RMAKSWHA.exe")
exe_full_path = os.path.join(extract_folder, exe_relative_path)
# 아이콘 파일 경로
icon_path = os.path.join(downloads, "gamelogo.ico")

# 압축 해제 함수
def extract_zip(zip_file, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
    print(f"압축 해제 완료: {dest_folder}")

# 바로가기 생성 함수
def create_shortcut(target, shortcut_path, icon_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target
    # 아이콘 경로와 인덱스를 명시적으로 지정
    shortcut.IconLocation = f"{icon_path}, 0"  # 아이콘 경로와 인덱스 설정
    shortcut.Save()
    print(f"바로가기 생성 완료: {shortcut_path}")

# 파일 삭제 함수
def delete_files(*file_paths):
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"파일 삭제 완료: {file_path}")
            else:
                print(f"파일이 존재하지 않습니다: {file_path}")
        except Exception as e:
            print(f"파일 삭제 중 오류 발생: {file_path}, 오류: {e}")

# cta 폴더 삭제 함수
def delete_cta_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"cta 폴더 삭제 완료: {folder_path}")
    else:
        print(f"cta 폴더가 존재하지 않습니다: {folder_path}")

# 작업 시작
try:
    # cta 폴더 삭제
    delete_cta_folder(extract_folder)
    
    # 압축 파일 확인
    if not os.path.exists(zip_path):
        print(f"압축 파일이 없습니다: {zip_path}")
    else:
        # 압축 해제
        extract_zip(zip_path, extract_folder)
        # exe 파일 확인
        if os.path.exists(exe_full_path):
            shortcut_path = os.path.join(desktop, "CTA.lnk")
            create_shortcut(exe_full_path, shortcut_path, icon_path)
        else:
            print(f"exe 파일을 찾을 수 없습니다: {exe_full_path}")
        
        # 작업 완료 후 불필요한 파일 삭제
        delete_files(zip_path, download_auto_path)
        
        # 3초 뒤에 아이콘 파일 삭제
        time.sleep(3)
        delete_files(icon_path)

except Exception as e:
    print(f"오류 발생: {e}")

# 콘솔 창을 유지
input("Press Enter to exit...")
