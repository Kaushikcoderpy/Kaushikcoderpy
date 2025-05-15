port datetime
import sys
import pygame
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QApplication, QPushButton, QGridLayout,
                             QMainWindow, QLineEdit, QLabel, QWidget, QRadioButton, QScrollArea)
from zoneinfo import ZoneInfo

class AlarmClock(QMainWindow):
    def __init__(self):
        super().__init__()
        # setting window
        self.setWindowTitle("ALARM CLOCK")
        self.setGeometry(700, 300, 500, 500)
        self.today = datetime.datetime.now().strftime("%d %m %y")
        self.today_time = tuple(map(int, self.today.split(" ")))
        self.remaining_seconds_stopwatch = 0
        # creating labels and buttons,line edits
        self.alarm_time = QLineEdit()
        self.alarm_times: tuple = ()
        self.label = QLabel()
        self.label2 = QLabel()
        self.button = QPushButton("SUBMIT ALARM TIME")
        self.snooze = QPushButton("SNOOZE ALARM OR  STOP ALARM")
        self.radio_button = QRadioButton("DARK MODE")
        self.result = QLabel() #for alarm time
        self.today_day = QLabel()
        self.set_time = QLineEdit("ENTER TIMER  IN (H-M-S)")
        self.st_timer = QPushButton("SET TIMER ")
        self.set_stopwatch = QPushButton("START STOPWATCH")
        self.stop_sw = QPushButton("STOP WATCH")
        self.label3 = QLabel()
        self.history_label = QLabel()
        self.his_button = QPushButton("VIEW  ALARM HISTORY")
        self.am_pm = QLineEdit("CHOOSE AM OR PM")
        # getting present time
        india_tz = ZoneInfo('Asia/Kolkata')
        current_time = datetime.datetime.now(india_tz).strftime("%H-%M-%S")
        self.current_times = tuple(map(int, current_time.split("-")))
        #working with variables layouts timers
        self.remaining_seconds_main = 0
        self.layout = QGridLayout()
        self.timer = QTimer(self)
        self.timer2 = QTimer(self)
        self.timer.setInterval(1000)
        self.timer2.setInterval(1000)
        self.timer3 = QTimer(self)
        self.timer3.setInterval(1000)
        self.check_music_timer = QTimer(self)
        self.timer.timeout.connect(self.simple_countdown)
        self.timer2.timeout.connect(self.set_timer)
        self.timer3.timeout.connect(self.stopwatch)
        self.button.clicked.connect(self.start_countdown)
        self.snooze.clicked.connect(self.stop_alarm)
        self.radio_button.toggled.connect(self.dark_mode_enable)
        self.alarm_time.setPlaceholderText("ENTER YOUR ALARM TIME (H-M-S)")
        self.set_stopwatch.clicked.connect(self.start_stopwatch)
        self.st_timer.clicked.connect(self.start_timer)
        self.stop_sw.clicked.connect(self.stop_stopwatch)
        self.his_button.clicked.connect(self.history_view)
        self.central_widget = QWidget()
        # scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.central_widget)
        # for stopwatch function
        self.sw_hours = 0
        self.sw_minutes = 0
        self.sw_seconds = 0
        #for history view function
        self.history = []
        self.initui()

    def initui(self):
        self.setCentralWidget(self.scroll)
        self.layout.addWidget(self.alarm_time, 0, 0)
        self.layout.addWidget(self.button, 0, 1)
        self.layout.addWidget(self.am_pm,0,2)

        self.layout.addWidget(self.result, 1, 0)
        self.layout.addWidget(self.snooze, 3, 0)
        self.layout.addWidget(self.label, 2, 0)
        self.layout.addWidget(self.radio_button,1,1)
        self.layout.addWidget(self.today_day, 2, 1)
        self.layout.addWidget(self.st_timer, 4, 0)
        self.layout.addWidget(self.set_time, 4, 1)
        self.layout.addWidget(self.label3,5,0)
        self.layout.addWidget(self.label2,5,1)
        self.layout.addWidget(self.stop_sw, 6, 0)
        self.layout.addWidget(self.set_stopwatch, 6,1)
        self.layout.addWidget(self.history_label,7,0)
        self.layout.addWidget(self.his_button,7,1)
        self.central_widget.setLayout(self.layout)

    def get_input(self):
        try:
            text = self.alarm_time.text().strip().split("-")
            self.alarm_times = tuple(map(int, text))
            if not text or len(self.alarm_times) != 3:
                self.label.setText("NO ALARM TIME WAS GIVEN")
        except ValueError:
            self.label.setText("INVALID INPUT")
        except Exception as e :
            self.label.setText(e)

    def return_time_left(self):
        self.get_input()
        india_tz = ZoneInfo('Asia/Kolkata')
        now = datetime.datetime.now(india_tz)

        # Get alarm time input
        try:
            h, m, s = self.alarm_times
        except Exception:
            self.label.setText("INVALID ALARM TIME")
            return 0

        am_pm_text = self.am_pm.text().strip().upper()
        if not am_pm_text:
            self.label.setText("SET EITHER AM OR PM")
            return 0

        # Convert to 24-hour format if needed
        if am_pm_text == "PM" and h != 12:
            h += 12
        if am_pm_text == "AM" and h == 12:
            h = 0

        # Build the alarm datetime for today
        alarm_dt = now.replace(hour=h, minute=m, second=s, microsecond=0)
        if alarm_dt <= now:
            # If alarm time has already passed today, set for tomorrow
            alarm_dt += datetime.timedelta(days=1)

        remaining = (alarm_dt - now).total_seconds()
        self.remaining_seconds_main = int(remaining)
        self.history.append(self.alarm_times)
        return self.remaining_seconds_main



    def start_countdown(self):
        self.timer.stop()  # Stop any previous countdown
        self.remaining_seconds_main = self.return_time_left()
        if self.remaining_seconds_main > 0:
            self.label.setText("ALARM SET!")
            self.timer.start(1000)
        else:
            self.label.setText("ALARM TIME IS IN THE PAST OR INVALID")

    def simple_countdown(self)  :
        if self.remaining_seconds_main > 0:
            self.remaining_seconds_main -= 1
            hrs, rem  = divmod(self.remaining_seconds_main, 3600)
            mins, secs = divmod(rem, 60)
            self.label.setText(f" ALARM {hrs:02}:{mins:02}:{secs:02}")
        else:
            self.timer.stop()
            self.label.setText("ALARM!")
            self.play_alarm()

    def play_alarm(self):
        pygame.mixer.init()
        sound_path = "C://Users//KKAUSHIK//PycharmProjects//PythonProject6//alarmsound.wav.wav"
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        # Start a QTimer to periodically check if music is still playing
        self.check_music_timer = QTimer(self)
        self.check_music_timer.timeout.connect(self.check_music)
        self.check_music_timer.start(500)  # Check every 500 ms

    def check_music(self):
        if not pygame.mixer.music.get_busy():
            self.check_music_timer.stop()

    def stop_alarm(self):
        self.timer.stop()
        self.result.setText("")
        self.label.setText("")
        self.alarm_time.setText("")

    def dark_mode_enable(self):
        self.radio_button.setText("LIGHT MODE")
        if self.radio_button.isChecked():
            self.setStyleSheet("""
                QWidget { background-color: black; color: white; }
                QPushButton {
                    font-size: 30px; font-family: Arial;
                    padding: 12px; margin: 20px; border: 1px solid;
                    background-color: red; color: white;
                }
                QRadioButton {
                    font-size: 20px; font-family: Arial;
                    padding: 10px; margin: 5px; border: 1px solid;
                    color: white;
                }
                QLineEdit {
                    font-size: 32px; padding: 12px;
                    background-color: #222; color: white;
                }
                QLabel {
                    font-size: 32px; padding: 12px;
                    background-color: #222; color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: white; color: black; }
                QPushButton {
                    font-size: 30px; font-family: Arial;
                    padding: 12px; margin: 20px; border: 1px solid;
                    background-color: white; color: black;
                }
                QRadioButton {
                    font-size: 20px; font-family: Arial;
                    padding: 10px; margin: 5px; border: 1px solid;
                    color: black;
                }
                QLineEdit {
                    font-size: 32px; padding: 12px;
                    background-color:white; color: black;
                }
                QLabel {
                    font-size: 32px; padding: 12px;
                    background-color: #222; color: white;
                }
            """)

    def start_timer(self):
        text = self.set_time.text()
        try:
            h, m, s = map(int, text.split("-"))
            self.remaining_seconds_stopwatch = h * 3600 + m * 60 + s
            if self.remaining_seconds_stopwatch > 0:
                self.timer2.start()
        except ValueError:
            self.result.setText("INVALID TIMER FORMAT!")

    def set_timer(self):
        if self.remaining_seconds_stopwatch > 0:
            self.remaining_seconds_stopwatch -= 1
            hrs, rem = divmod(self.remaining_seconds_stopwatch, 3600)
            mins, secs = divmod(rem, 60)
            self.label3.setText(f"TIMER {hrs : 02} HOURS : {mins : 02} MINUTES {secs : 02} SECONDS")
        else:
            self.timer2.stop()
            self.play_alarm()
            self.result.setText("TIMER STOPPED")

    def stop_timer(self):
        self.timer2.stop()
        self.result.setText("")
        self.label.setText("")
        self.alarm_time.setText("")

    def start_stopwatch(self):
        self.stop_alarm()
        self.sw_hours = 0
        self.sw_minutes = 0
        self.sw_seconds = 0
        self.timer3.start()

    def stopwatch(self):
        self.sw_seconds += 1
        if self.sw_seconds == 60:
            self.sw_seconds = 0
            self.sw_minutes += 1
        if self.sw_minutes == 60:
            self.sw_minutes = 0
            self.sw_hours += 1

        self.label2.setText(
            f"STOPWATCH {self.sw_hours:02} HOURS : {self.sw_minutes:02} MINUTES {self.sw_seconds:02} SECONDS"
        )

    def stop_stopwatch(self):
        self.timer3.stop()
    def history_view(self):
        self.history_label.setText("VIEW HISTORY HERE")
        self.history.append(self.current_times)
        if self.alarm_times == () :
            self.history_label.setText("NO ALARM WAS SET")
        else :
            txt = (f"AN ALARM WAS SET TO {self.alarm_times[0]}HOURS {self.alarm_times[1]} MINUTES ON \n"
               f"{self.current_times[0]} HOURS {self.current_times[1]} MINUTES ")
            self.history_label.setText(txt)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AlarmClock()
    window.show()
    sys.exit(app.exec_())
