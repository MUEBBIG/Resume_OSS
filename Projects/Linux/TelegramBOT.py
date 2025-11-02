import asyncio               # 비동기 I/O를 위한 asyncio 모듈 (백그라운드 태스크 실행 등에 사용)
import time                  # 시간 측정을 위한 모듈 (녹화 시간 체크 등에 사용)
import RPi.GPIO as GPIO      # 라즈베리파이 GPIO 핀 제어 모듈
import cv2                   # OpenCV - 비디오 촬영 및 저장을 위한 라이브러리
import logging               # 로깅 설정 모듈 (디버깅 시 로그 출력에 사용됨)
from telegram import Update  # Telegram Bot API 사용을 위한 모듈
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes  # Telegram Bot 명령어 처리 프레임워크
from typing import Optional  # Optional 타입 힌트 제공을 위한 typing 모듈

# Telegram Bot API 인증 토큰
TOKEN = "8170323752:AAEoO49JtFJM0TL0jP_md5bFxSpkvqe1FuE"

# 로그 출력 형식과 레벨을 설정
logging.basicConfig(
    format="%(asctime)s -%(name)s -%(levelname)s -%(message)s",
    level=logging.WARNING
)


# 동영상 촬영 함수 (움직임 감지 시 호출됨)
def capture_video() -> Optional[str]:
    # 녹화된 영상을 저장할 경로 설정
    video_path = "/tmp/capture.mp4"

    # 카메라 장치 열기 (디바이스 0번, V4L2 backend 사용)
    camera = cv2.VideoCapture(0, cv2.CAP_V4L)

    # 카메라 오픈 실패 시 None 반환
    if not camera.isOpened():
        return None

    # 해상도와 FPS 설정
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # 가로 해상도 설정
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)  # 세로 해상도 설정
    camera.set(cv2.CAP_PROP_FPS, 10)            # 초당 프레임 수 설정

    # mp4v 코덱 설정 (OpenCV에서 mp4 파일을 저장할 때 사용)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # 비디오 라이터 객체 생성 (파일명, 코덱, FPS, 해상도)
    writer = cv2.VideoWriter(video_path, fourcc, 10, (640, 360))

    # 현재 시간 저장 → 녹화 시간 측정용
    start_time = time.time()

    # 10초 동안 프레임을 읽어서 파일에 저장
    while time.time() - start_time < 10:
        ret, frame = camera.read()   # 카메라에서 프레임 읽기
        if not ret:                  # 읽기 실패 시 종료
            break
        writer.write(frame)         # 프레임을 비디오 파일에 저장

    # 사용한 리소스 해제
    writer.release()
    camera.release()

    # 저장된 파일 경로 반환
    return video_path


# 상태 플래그 변수 (전역 변수로 상태 관리)
monitoring = False      # 도둑 잡기 모드 실행 여부
capturing = False       # 현재 비디오 촬영 중 여부
exit_requested = False  # 프로그램 종료 요청 여부


# PIR 센서 감시용 비동기 루프 함수
# (백그라운드에서 지속적으로 PIR 센서를 감시)
async def pir_monitor(chat_id: int, application):
    global monitoring, capturing, exit_requested

    # GPIO 핀 번호 설정 (BCM 기준)
    led = 6          # LED를 연결한 GPIO 번호
    pir_sensor = 18  # PIR 센서를 연결한 GPIO 번호

    # GPIO 초기화 설정
    GPIO.setwarnings(False)       # 경고 메시지 비활성화
    GPIO.setmode(GPIO.BCM)        # 핀 번호를 BCM 모드로 설정

    # 핀의 입출력 모드 설정
    GPIO.setup(led, GPIO.OUT)     # LED 핀을 출력 모드로 설정
    GPIO.setup(pir_sensor, GPIO.IN)  # PIR 센서 핀을 입력 모드로 설정

    try:
        # 메인 감시 루프
        while not exit_requested:
            # /exit 명령이 오면 exit_requested = True → 루프 종료

            if monitoring:
                # 도둑 감지 모드가 활성화된 경우

                # PIR 센서에 움직임 감지 && 현재 촬영 중이 아닐 때
                if GPIO.input(pir_sensor) == 1 and not capturing:
                    capturing = True              # 촬영 중 상태로 전환
                    GPIO.output(led, GPIO.HIGH)   # LED ON

                    # 텔레그램으로 감지 메시지 전송
                    await application.bot.send_message(
                        chat_id=chat_id, text="움직임 감지! 10초간 동영상을 촬영합니다."
                    )

                    # 비디오 촬영 실행
                    video_path = capture_video()
                    if video_path:
                        with open(video_path, "rb") as vid:
                            # 텔레그램으로 비디오 전송
                            await application.bot.send_video(chat_id=chat_id, video=vid)
                    else:
                        # 에러 메시지 전송
                        await application.bot.send_message(
                            chat_id=chat_id, text="카메라를 사용할 수 없습니다."
                        )

                    # 촬영 후 LED 끄기
                    GPIO.output(led, GPIO.LOW)

                    # 10초 쿨타임 동안 다시 촬영 금지  #
                    # await asyncio.sleep(10)     # 잘못된 코드 (제거)

                    # 촬영 완료 후 상태 초기화
                    capturing = False

            # 센서 폴링 주기 (0.3초마다 확인)
            await asyncio.sleep(0.3)
    finally:
        # 프로그램 종료 시 GPIO 핀 정리
        GPIO.cleanup()


# /start 명령 핸들러 : 도둑 잡기 모드 시작
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global monitoring
    if monitoring:
        await update.message.reply_text("이미 도둑 잡기 모드가 실행 중입니다.")
        return

    # 도둑 잡기 모드 ON
    monitoring = True

    # 사용자에게 알림 전송
    await update.message.reply_text("도둑 잡기 모드를 실행합니다. (/stop 명령으로 해제 가능)")

    # 감시 루프를 백그라운드 태스크로 실행
    context.application.create_task(
        pir_monitor(update.effective_chat.id, context.application)
    )


# /stop 명령 핸들러 : 도둑 잡기 모드 종료
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global monitoring
    if not monitoring:
        await update.message.reply_text("현재 도둑 잡기 모드 실행 중이 아닙니다.")
        return

    # 모니터링 종료
    monitoring = False
    await update.message.reply_text("도둑 잡기 모드를 해제합니다. (/start 명령으로 실행 가능)")


# /exit 명령 핸들러 : 프로그램 완전 종료 + GPIO 정리
async def exit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global exit_requested, monitoring

    # 종료 요청 및 모니터링 중단
    exit_requested = True
    monitoring = False

    # 사용자에게 알림
    await update.message.reply_text("도둑 잡기 프로그램을 종료하고 GPIO를 정리합니다.")

    # GPIO 핀 초기화
    GPIO.cleanup()


# main 함수 - Telegram 봇 실행
def main() -> None:
    # Telegram 봇 앱 생성
    app = ApplicationBuilder().token(TOKEN).build()

    # 명령어 핸들러 등록
    app.add_handler(CommandHandler("start", start))        # /start → 도둑 잡기 모드 (모니터링) 시작
    app.add_handler(CommandHandler("stop", stop))          # /stop  → 도둑 잡기 모드 (모니터링) 종료
    app.add_handler(CommandHandler("exit", exit_command))  # /exit  → 프로그램 종료 및 GPIO 정리

    # 봇 폴링 시작 (계속해서 명령을 기다림)
    app.run_polling()


# Python 프로그램의 진입점
if __name__ == "__main__":
    main()
