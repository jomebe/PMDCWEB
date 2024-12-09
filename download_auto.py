import os
import zipfile
import shutil

# 사용자 바탕화면 경로
desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
# Documents의 기본 경로
documents = os.path.join(os.environ["USERPROFILE"], "Documents")
# 다운로드 폴더 경로
downloads = os.path.join(documents, "Downloads")
# cta.zip 파일 경로 (다운로드 후 이동될 위치)
zip_path = os.path.join(downloads, "cta.zip")
# 압축 해제 대상 폴더
extract_folder = os.path.join(documents, "cta")

# 압축 해제 함수
def extract_zip(zip_file, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # 폴더가 없으면 생성
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)  # 압축 해제
    print(f"압축 해제 완료: {dest_folder}")

# 파일 삭제 함수
def delete_files(*file_paths):
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)  # 파일 삭제
                print(f"파일 삭제 완료: {file_path}")
            else:
                print(f"파일이 존재하지 않습니다: {file_path}")
        except Exception as e:
            print(f"파일 삭제 중 오류 발생: {file_path}, 오류: {e}")

# 작업 시작
try:
    # cta 폴더 삭제 (이미 존재하면 제거)
    if os.path.exists(extract_folder):
        shutil.rmtree(extract_folder)  # 폴더와 내용 전체 삭제
        print(f"기존 cta 폴더 삭제 완료: {extract_folder}")
    
    # 압축 파일 확인
    if not os.path.exists(zip_path):
        print(f"압축 파일이 없습니다: {zip_path}")
    else:
        # 압축 해제
        extract_zip(zip_path, extract_folder)
        # 작업 완료 후 불필요한 파일 삭제
        delete_files(zip_path)
        print(f"모든 작업이 완료되었습니다!")
except Exception as e:
    print(f"오류 발생: {e}")

# 콘솔 창을 유지
input("Press Enter to exit...")
