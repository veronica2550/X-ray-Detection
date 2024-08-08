import os
import shutil
import cv2
import numpy as np


def process_video(video_path):

    # 출력 폴더가 존재하지 않으면 생성
    frames_dir = "video_2_frame"
    frames_dir_yolo = "frame_2_yolo"
    
    # 폴더가 존재하면 전체 데이터 삭제
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
        shutil.rmtree(frames_dir_yolo)
    
    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
        os.makedirs(frames_dir_yolo)

    # 동영상 캡처 객체 생성
    cap = cv2.VideoCapture(video_path)

    # 동영상 파일 열기 확인
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
    else:
        # 첫 번째 프레임 읽기
        ret, previous_frame = cap.read()
        
        if not ret:
            print("Error: Could not read the first frame.")
        else:
            previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
            
            frame_number = 0
            last_saved_frame = None
            saved = False

            # 프레임 간격 설정 (예: 10프레임마다 처리)
            frame_interval = 10

            # 이전 프레임이 존재할 때까지 반복
            while True:
                # 프레임 건너뛰기
                for _ in range(frame_interval - 1):
                    ret = cap.grab()
                    if not ret:
                        break

                ret, current_frame = cap.retrieve()
                if not ret:
                    break

                # 현재 프레임을 그레이스케일로 변환
                current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
                
                if last_saved_frame is None:
                    # 첫 번째 비교에서는 프레임을 저장하고 초기화
                    frame_filename = os.path.join(frames_dir, f'frame_{frame_number}.jpg')
                    cv2.imwrite(frame_filename, current_frame)
                    print(f'Saved initial frame: {frame_filename}')
                    last_saved_frame = current_gray.copy()
                    saved = True
                else:
                    # 현재 프레임과 마지막 저장된 프레임의 차이 계산
                    difference = cv2.absdiff(last_saved_frame, current_gray)
                    _, difference = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
                    
                    if np.sum(difference) == 0 and not saved:
                        # 동일한 프레임이 발견되었고 이전에 저장하지 않은 경우
                        frame_filename = os.path.join(frames_dir, f'frame_{frame_number}.jpg')
                        cv2.imwrite(frame_filename, current_frame)
                        print(f'Saved identical frame: {frame_filename}')
                        saved = True
                    elif np.sum(difference) != 0:
                        # 다른 프레임이 나타났을 때
                        saved = False
                        last_saved_frame = current_gray.copy()
                
                # 프레임 번호 증가 (설정한 간격만큼 증가)
                frame_number += frame_interval

            # 동영상 캡처 객체 해제
            cap.release()
            print("Processing complete.")
            return frames_dir
