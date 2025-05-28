import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QPushButton, QLabel, QLineEdit,
                             QGridLayout, QCheckBox, QRadioButton, QVBoxLayout, QTextEdit, QMessageBox, QTableWidget,
                             QTableWidgetItem,qApp,QGroupBox)
from PyQt5.QtCore import  QTimer,Qt
import sys
import  datetime
from datetime import timedelta
import random
from passlib.context import CryptContext
import secrets
import pandas as pd

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab = QTabWidget()
        self.setCentralWidget(self.tab)
        self.tab.setWindowTitle("HABIT TRACKER")
        self.settings = Settings()
        self.ui = UI()
        self.visual = Table()
        self.tab.addTab(self.ui, "HABITS")
        self.tab.addTab(self.settings,"SETTINGS")
        self.tab.addTab(self.visual,"DATA IN TABLE")
        self.notif = Notification()
        self.tab.addTab(self.notif,"SET NOTIFICATIONS")


class MyHabit(QWidget):
    def __init__(self):
        super().__init__()
        self.description_count = QLineEdit()
        self.description_count.setPlaceholderText("ENTER HOW MANY HABITS YOU WANT DESCRIPTION FOR")
        self.choice = QLineEdit()
        self.line_edits = [] #for delete habits function
        self.quotes = [
            "The only moment that truly matters is now. Don’t let your dreams be delayed by the weight of later.",
            "Small habits make a big difference. Stay consistent!",
            "Discipline is the bridge between goals and accomplishment.",
            "Don’t watch the clock; do what it does. Keep going.",
            "You don’t have to be extreme, just consistent.",
            "Success is the sum of small efforts, repeated day in and day out.",
            "Wake up with determination. Go to bed with satisfaction."
        ]

        # Pick a random based
        index = random.randrange(7)
        self.motivation = QLabel(self.quotes[index].upper())
        #data
        self.data = DataManager()
        self.habit_count = QLineEdit()
        self.habit_count.setPlaceholderText("ENTER HOW MANY HABITS DO YOU HAVE")
        self.my_habits : set = set()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.motivation)
        self.layout.addWidget(self.habit_count)
        self.submit = QPushButton("SUBMIT")
        self.submit.clicked.connect(self.add_habits)
        self.layout.addWidget(self.submit)
        self.done = QPushButton("DONE")
        self.done.clicked.connect(self.save_habits)
        self.del_hab_count = QLineEdit()
        self.del_hab_count.setPlaceholderText("ENTER HOW MANY HABITS YOU WANT TO REMOVE")
        self.delete = QPushButton("DELETE")
        self.delete.clicked.connect(self.create_delete_habits_ui)
        self.del_permanently = QPushButton("DELETE HABITS")
        self.layout.addWidget(self.delete)
        self.layout.addWidget(self.del_hab_count)
        self.setLayout(self.layout)
        self.habits_set : set = set()
        self.set_desc = QPushButton("SET DESCRIPTION")
        self.submit_desc_count = QPushButton("SUBMIT DESCRIPTION COUNT")
        self.submit_desc_count.clicked.connect(self.set_desc_func)
    def add_habits(self):
        try:
            habit_count = int(self.habit_count.text())
            if habit_count :
                for _ in range(habit_count):
                    habit_input = QLineEdit()
                    habit_input.setPlaceholderText("ENTER HABIT")
                    self.habits_set.add(habit_input)
                    self.layout.addWidget(habit_input)
                self.layout.addWidget(self.done)
            else :
                QMessageBox.information(self,"INVALID COUNT","PLEASE ENTER COUNT")
        except ValueError:
            QMessageBox.warning(self,"COUNT MUST BE A INTEGER")
    def save_habits(self):
        self.my_habits.clear()
        data_total : list  = []
        if self.habits_set :
            for habit in self.habits_set:
                name = habit.text().strip()
                if name:
                    self.my_habits.add(name)
                    data : dict = {"habit_name": name, "started on": str(datetime.datetime.now().date())}
                    data_total.append(data)
        print("Saved habits:", self.my_habits)
        self.data.create_json_for_store(data_total,filename="habits.json")
        self.done.setEnabled(False)
        self.submit.setEnabled(False)

        # Remove and delete widgets properly
        for line_edit in self.habits_set:
            self.layout.removeWidget(line_edit)
            line_edit.deleteLater()  # Properly delete the widget

        self.habits_set.clear()  # Clear the list after deletion
        self.choice.setPlaceholderText("DO YOU WANT TO ADD ANY DESCRIPTION?(Y/N)")
        self.layout.addWidget(self.choice)
        self.layout.addWidget(self.set_desc)
        self.set_desc.clicked.connect(self.set_description)
    def set_description(self):
        if self.choice.text().upper() == "Y" or self.choice.text().upper() == "YES" :
            self.layout.removeWidget(self.choice)
            self.choice.deleteLater()
            self.layout.addWidget(self.description_count)
            self.layout.addWidget(self.submit_desc_count)
    def set_desc_func(self) :
        count = int(self.description_count.text())
        self.description_count.setEnabled(False)
        self.layout.removeWidget(self.description_count)
        self.description_count.deleteLater()
        if not count:
            QMessageBox.warning(self, "YOU DID NOT GAVE HABIT DESCRIPTION COUNT")
            return
        if count == 0:
            QMessageBox.warning(self, "COUNT MUST BE GREATER THAN 0")
            return

        line_edits = []
        if count > 0 :
            for i in range(count):
                le = QLineEdit()
                le.setPlaceholderText("ENTER DESCRIPTION (FORMAT : HABIT NAME <space> DESCRIPTION")
                line_edits.append(le)
                self.layout.addWidget(le)
                self.set_desc.setEnabled(False)
                self.layout.removeWidget(self.set_desc)
                self.set_desc.deleteLater()
                def adding_desc() :
                    for led in line_edits : #led = line-edits
                        le.setEnabled(False)
                        self.layout.removeWidget(led)
                        le.deleteLater()
                    hab_descriptions = []
                    for j in range(len(line_edits)) :
                        hab_descriptions.append(line_edits[j].text())
                    old_data = self.data.load_habits_from_file(filename="habits.json")
                    my_habs = []
                    for l in range(len(old_data)) :
                        my_habs.append(old_data[l]['habit_name'])
                    #adding description
                    for m,hab in enumerate(hab_descriptions) :
                        if hab.startswith(hab_descriptions[m]) :
                            old_data[m]['DESCRIPTION'] = hab_descriptions[m].split(' ',1)[1]
                    self.data.create_json_for_store(data=old_data,filename="habits.json")
                
                    
            btn = QPushButton("SUBMIT DESCRIPTIONS")
            self.layout.addWidget(btn)
            btn.clicked.connect(adding_desc)


    def create_delete_habits_ui(self) :
        line_edits : list = []
        habits : set = set(self.data.load_habits_from_file())
        if not habits :
            habits : set = set(self.my_habits)
        count = int(self.del_hab_count.text())

        if count :
            if habits :
                line_edits = []
                for i in range(count) :
                    line_edit = QLineEdit()
                    line_edit.setPlaceholderText("ENTER THE HABIT TO BE DELETED")
                    line_edits.append(line_edit)
                    self.layout.addWidget(line_edit)

                self.layout.addWidget(self.del_permanently)

        else :
            QMessageBox.information(self,"YOU DONT HAVE ANY HABITS YET")
        def delete_habs() :
            self.del_permanently.setEnabled(False)
            self.layout.removeWidget(self.del_permanently)
            self.del_permanently.deleteLater()
            habs : list[str] = []
            if line_edits :
                for j in range(len(line_edits)) :
                    habs.append(str(line_edits[j].text().lower()))
            if habs :
                for hab in habs :
                    if hab in habits :
                        habits.remove(hab)
                        QMessageBox.information(self,f"SUCCESSFULLY DELETED,YOUR HABITS : {habits}")
                        self.data.create_json_for_store(data=habits,filename="habits.json")
                        for le in line_edits:
                            le.setEnabled(False)
                            self.layout.removeWidget(le)
                            le.deleteLater()
            else :
                for le in line_edits:
                    print(le.text())
                QMessageBox.information(self,"FAILED TO DELETE")

        self.del_permanently.clicked.connect(delete_habs)


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.call_count = 0
        self.today_days : list = []
        self.all_cb  : list = []
        self.habits = MyHabit()
        self.evaluation = QPushButton('EVALUATE MY XP')
        self.layout = QVBoxLayout()
        self.sub_tabs = QTabWidget()
        self.sub_tabs.addTab(self.habits, "ENTER HABITS")
        self.view_tab = QWidget()
        self.view_layout = QGridLayout()
        self.start = QPushButton("GENERATE UI")
        self.start.clicked.connect(self.create_ui)
        self.view_layout.addWidget(self.start, 8, 0)
        self.view_tab.setLayout(self.view_layout)
        self.sub_tabs.addTab(self.view_tab, "SHOW UI")
        self.done = QPushButton("DONE")
         #data
        self.data = DataManager()
        self.layout.addWidget(self.sub_tabs)
        self.setLayout(self.layout)
        #handling dates and days
        self.now = datetime.datetime.now().strftime("%I-%M-%S")
        self.now_date : datetime.date = datetime.datetime.now().date()
        self.now_day = datetime.datetime.now().strftime("%A")
        self.warning = QLabel("Please select a habit to delete")
        self.gen_7 = QPushButton("GENERATE NEXT 7 DAYS UI")
    def create_ui(self):
        days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
        habits = list(self.habits.my_habits)
        index = days.index(self.now_day.upper())
        self.today_days = [day.upper() for day in days if day == self.now_day.upper()]
        if habits :
            data_hab = list(habits)
        else :
            data_hab  : list = self.data.load_habits_from_file()
        for i in range(1, len(days)):
            if  i + index  < len(days) :
                self.today_days.append(days[index + i])

        for j in range(0, index):
            if 0 <=  j < index:
                self.today_days.append(days[j])
            if len(days) == len(self.today_days):
                break
        for j in range(len(self.today_days)):
            label = QLabel(f"{self.today_days[j]}")
            self.view_layout.addWidget(label, 0, j + 1)

        for i in range(len(data_hab)):
            habit = QLabel(data_hab[i])
            self.view_layout.addWidget(habit,  i + 1 , 0)
        self.all_cb = []
        for i in range(len(data_hab)):  # each habit
            column = []
            for j in range(len(days)):  # each day
                checkbox = QCheckBox(f"{self.now_date + timedelta(days=j)} {data_hab[i]}")
                column.append(checkbox)
                checkbox.setChecked(False)
                self.view_layout.addWidget(checkbox, i + 1, j + 1)  # row: habit index, col: day index
            self.view_layout.addWidget(self.done,6,0)
            self.all_cb.append(column)
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        for column in self.all_cb:
            for cb in column :
                if not  cb.text().startswith(today) :
                    cb.setEnabled(False)


        def check():
            done = []
            not_done = []
            for k, row_copy in enumerate(self.all_cb):
                for cbs in row_copy :
                    if cbs.isChecked():
                        print(f"On {self.today_days[k]}, you completed: {cbs.text()}")
                        done.append(cbs.text())
                        self.done.setEnabled(False)
                    else:
                        not_done.append(cbs.text())
            user_xp = len(done) * 20
            user_stats = {
                "completed_habits": done,
                "pending_habits": not_done,
                "xp": user_xp
            }
            self.data.create_json_for_store(data=user_stats, filename="user_stats.json")
        self.done.clicked.connect(check)
        self.layout.addWidget(self.gen_7)
        self.gen_7.clicked.connect(self.generate_next7_ui)
        self.start.setEnabled(False)

    def generate_next7_ui(self):
        # Clear the view_layout (the grid layout that shows checkboxes)
        for i in reversed(range(self.view_layout.count())):
            widget = self.view_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Handle persistent call count
        self.call_count += 1

        # Load habits
        habits = list(self.habits.my_habits)
        if not habits:
            habits = self.data.load_habits_from_file()

        self.all_cb = []  # Reset checkbox matrix

        # Calculate the next 7 dates from today, shifted by call count
        next_7_dates = [self.now_date + timedelta(days=i + 7 * self.call_count) for i in range(7)]

        # Get corresponding day names (e.g., Monday, Tuesday, etc.)
        next7_days = [date.strftime("%A") for date in next_7_dates]

        # Add day labels (top row headers)
        for j, day in enumerate(next7_days):
            label = QLabel(f"{day}\n{next_7_dates[j].strftime('%b %d')}")
            self.view_layout.addWidget(label, 0, j + 1)

        # Add habit labels (first column) and checkboxes
        for i, habit_name in enumerate(habits):
            habit_label = QLabel(habit_name)
            self.view_layout.addWidget(habit_label, i + 1, 0)
            column = []
            for j in range(7):
                checkbox = QCheckBox(f"{next_7_dates[j]} {habit_name}")
                checkbox.setChecked(False)
                self.view_layout.addWidget(checkbox, i + 1, j + 1)
                column.append(checkbox)
            self.all_cb.append(column)

        today = datetime.datetime.now().strftime("%d-%m-%Y")
        for column in self.all_cb:
            for cb in column:
                if not cb.text().startswith(today):
                    cb.setEnabled(False)

        # Add back the generate button
        self.view_layout.addWidget(self.gen_7)
        self.view_layout.addWidget(self.evaluation)
        self.evaluation.clicked.connect(self.eval_xp)
    def eval_xp(self):
        try:
            with open("user_stats.json", "r") as file:
                user_stats = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            user_stats = {}
        if not user_stats :
            done = []
            not_done = []
            for k, row_copy in enumerate(self.all_cb):
                for cbs in row_copy:
                    if cbs.isChecked():
                        done.append(cbs.text())
                        self.done.setEnabled(False)
                    else:
                        not_done.append(cbs.text())
            user_xp = len(done) * 20
            user_stats = {
                "completed_habits": done,
                "pending_habits": not_done,
                "xp": user_xp
            }
            self.data.create_json_for_store(data=user_stats, filename="user_stats.json")
        else :

            done : list= user_stats.get("completed_habits",[])
            pending  : list = user_stats.get("pending_habits",[])
            xp  : int = user_stats.get("xp",0)
            for k, row_copy in enumerate(self.all_cb):
                for cbs in row_copy:
                    if cbs.isChecked():
                        print(f"On {self.today_days[k]}, you completed: {cbs.text()}")
                        done.append(cbs.text())
                        self.done.setEnabled(False)
                    else:
                        pending.append(cbs.text())
            latest_xp : int = xp + len(done) * 20
            user_stats = {
                "completed_habits": done,
                "pending_habits": pending,
                "xp": latest_xp
            }
            self.data.create_json_for_store(data=user_stats, filename="user_stats.json")

class Table(QWidget) :
    def __init__(self):
        super().__init__()
        self.gen_table = QPushButton("GENERATE TABLE")
        self.radio_btn = QRadioButton("DARK MODE")

        self.table = QTableWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.radio_btn)
        self.layout.addWidget(self.gen_table)
        self.layout.addWidget(self.table)
        self.gen_table.clicked.connect(self.view_habs_as_table)
        self.radio_btn.toggled.connect(self.dark_mode_enable)
        self.setLayout(self.layout)
    @staticmethod
    def process_data(data,status):
        split_rows = [line.split(' ',1) for line in data]
        df = pd.DataFrame(split_rows,columns=['DATE','HABIT'])
        df['STATUS'] = status
        return df

    def view_habs_as_table(self):
        try:
            with open("user_stats.json", "r") as file:
                user_stats = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            user_stats = {}
        if not user_stats :
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            print("no data to show")
        else :
            completed = user_stats.get("completed_habits",[])
            incompleted = user_stats.get("pending_habits",[])
            df_done = self.process_data(data=completed,status="DONE")
            df_pending = self.process_data(data=incompleted,status="INCOMPLETE")
            df = pd.concat([df_done,df_pending],ignore_index=True)
            self.table.setRowCount(len(df))
            self.table.setColumnCount(len(df.columns))
            self.table.setHorizontalHeaderLabels(df.columns)

            for i in range(len(df)) :
                for j in range(len(df.columns)) :
                    item = QTableWidgetItem(str(df.iat[i,j]))
                    item.setFlags(item.flags() & ~ Qt.ItemIsEditable)
                    self.table.setItem(i,j,item)

    def dark_mode_enable(self):
        app: QApplication = qApp

        # Access radio button from the Settings tab
        if self.radio_btn.isChecked():
            self.radio_btn.setText("LIGHT MODE")
            app.setStyleSheet(""" 
                QWidget { background-color: #E3F2FD; color: #212121; font-weight : bold ;}
                QPushButton {
                    font-size: 30px; font-family: Arial;
                    padding: 12px; margin: 20px; border-radius: 10px;
                    background-color: #BBDEFB; color: #0D47A1;font-weight : bold ;
                }
                QRadioButton {
                    font-size: 20px; padding: 10px; color: #0D47A1;font-weight : bold ;
                }
                QLineEdit {
                    font-size: 24px; padding: 10px;
                    background-color: #FFFFFF; color: #0D47A1;
                    border: 2px solid #90CAF9;font-weight : bold ;
                }
                QLabel {
                    font-size: 24px; padding: 8px;
                    color: #01579B ;font-weight : bold ;
                }
            """)
        else:
            self.radio_btn.setText("DARK MODE")
            app.setStyleSheet("""
                QWidget { background-color: #121212; color: #E0E0E0; font-weight : bold ;}
                QPushButton {
                    font-size: 30px; font-family: Arial;
                    padding: 12px; margin: 20px; border-radius: 10px;
                    background-color: #1E88E5; color: #FFFFFF;font-weight : bold ;
                }
                QRadioButton {
                    font-size: 20px; padding: 10px; color: #BBDEFB;font-weight : bold ;
                }
                QLineEdit {
                    font-size: 24px; padding: 10px;
                    background-color: #263238; color: #FFFFFF;font-weight : bold ;
                    border: 2px solid #1E88E5;
                }
                QLabel {
                    font-size: 24px; padding: 8px;
                    color: #81D4FA;font-weight : bold ;
                }
            """)

class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = UI()
        self.tabs = QTabWidget()
        self.streak_input = QLineEdit()
        self.streak_input.setPlaceholderText("ENTER THE HABIT NAME TO CALCULATE STREAK")
        # HABIT SETTINGS TAB
        self.habits_tab = QWidget()
        self.habits_txt = QTextEdit()
        self.show_hab = QPushButton("SHOW MY HABITS")
        self.show_hab.clicked.connect(self.show_habits_handler)
        self.eval = QPushButton("GET MY RANK")
        self.eval.clicked.connect(self.give_user_rank)
        self.rank = QLabel("YOUR RANK IS DISPLAYED HERE")
        self.habits_layout = QVBoxLayout()
        self.habits_layout.addWidget(self.streak_input)
        self.habits_layout.addWidget(self.rank)
        self.habits_layout.addWidget(self.show_hab)
        self.habits_layout.addWidget(self.habits_txt)
        self.habits_layout.addWidget(self.eval)

        self.streak = QPushButton("CALCULATE STREAK")
        self.streak.clicked.connect(self.handle_streak)
        self.habits_layout.addWidget(self.streak)
        self.habits_tab.setLayout(self.habits_layout)
         #data
        self.data = DataManager()
        # GUIDE TAB
        self.guide_tab = QWidget()
        self.guide_text = QTextEdit()
        self.guide_text.setReadOnly(True)
        self.guide_text.setText("""
## HOW TO USE THE HABIT TRACKER

THIS HABIT TRACKER IS A PYQT5-BASED APPLICATION THAT ALLOWS YOU TO MANAGE AND TRACK YOUR HABITS. HERE'S A BREAKDOWN OF HOW TO USE IT:

### 1. SETTING UP HABITS

1.  **OPEN THE APPLICATION:** RUN THE PYTHON SCRIPT. A WINDOW WITH TABS LABELED "HABITS", "SETTINGS", AND "DATA IN TABLE" WILL APPEAR.
2.  **NAVIGATE TO THE "HABITS" TAB:** THIS IS WHERE YOU'LL SET UP YOUR HABITS.
3.  **ENTER HABIT COUNT:** IN THE "ENTER HOW MANY HABITS DO YOU HAVE" FIELD, TYPE THE NUMBER OF HABITS YOU WANT TO TRACK AND CLICK "SUBMIT".
4.  **ENTER HABITS:** FOR EACH HABIT, A NEW TEXT FIELD WILL APPEAR. TYPE IN THE NAME OF THE HABIT AND CLICK "DONE".
5.  **(OPTIONAL) ADD DESCRIPTIONS:** AFTER ADDING HABITS, YOU'LL BE PROMPTED TO ADD DESCRIPTIONS. TYPE "Y" OR "YES" IN THE "DO YOU WANT TO ADD ANY DESCRIPTION?(Y/N)" FIELD AND CLICK THE "SET DESCRIPTION" BUTTON.
6.  **ENTER DESCRIPTION COUNT:** ENTER HOW MANY HABITS YOU WANT TO ADD DESCRIPTIONS FOR.
7.  **ENTER DESCRIPTIONS:** ENTER EACH DESCRIPTION IN THE FORMAT "HABIT NAME DESCRIPTION".
8.  **SUBMIT DESCRIPTIONS:** CLICK THE "SUBMIT DESCRIPTIONS" BUTTON.
9.  **(OPTIONAL) DELETE HABITS:** TO DELETE HABITS, ENTER THE NUMBER OF HABITS YOU WANT TO REMOVE IN THE "ENTER HOW MANY HABITS YOU WANT TO REMOVE" FIELD AND CLICK "DELETE". ENTER THE NAME OF EACH HABIT YOU WISH TO DELETE AND CLICK "DELETE HABITS".

### 2. TRACKING HABITS

1.  **NAVIGATE TO THE "SHOW UI" TAB:** GO TO THE "HABITS" TAB AND SELECT THE SUB-TAB "SHOW UI". THIS TAB DISPLAYS YOUR HABITS AND A CHECKBOX FOR EACH DAY OF THE WEEK.
2.  **GENERATE UI:** CLICK THE "GENERATE UI" BUTTON TO DISPLAY THE UI WITH YOUR HABITS AND CHECKBOXES FOR EACH DAY. CHECKBOXES FOR PAST DATES ARE DISABLED.
3.  **MARK HABITS AS DONE:** CHECK THE BOXES FOR THE HABITS YOU COMPLETED ON THE CURRENT DAY.
4.  **SAVE PROGRESS:** CLICK THE "DONE" BUTTON TO SAVE YOUR PROGRESS.
5.  **GENERATE NEXT 7 DAYS UI:** TO GENERATE THE UI FOR THE NEXT 7 DAYS, CLICK THE "GENERATE NEXT 7 DAYS UI" BUTTON. YOU CAN GENERATE MULTIPLE SETS OF 7 DAYS.
6.  **EVALUATE XP:** CLICK THE "EVALUATE MY XP" BUTTON TO CALCULATE YOUR EXPERIENCE POINTS (XP) BASED ON COMPLETED HABITS. EACH COMPLETED HABIT IS WORTH 20 XP.

### 3. VIEWING DATA

1.  **NAVIGATE TO THE "DATA IN TABLE" TAB:** THIS TAB SHOWS YOUR HABIT DATA IN A TABLE FORMAT.
2.  **GENERATE TABLE:** CLICK THE "GENERATE TABLE" BUTTON TO DISPLAY THE DATA. THE TABLE SHOWS THE DATE, HABIT, AND STATUS (DONE OR INCOMPLETE) OF EACH TRACKED HABIT.

### 4. SETTINGS

1.  **DARK MODE:** IN THE "DATA IN TABLE" TAB, YOU CAN TOGGLE DARK MODE BY CLICKING THE "DARK MODE" RADIO BUTTON. THIS CHANGES THE APPLICATION'S COLOR SCHEME.

        """)
        self.guide_layout = QVBoxLayout()
        self.guide_layout.addWidget(self.guide_text)
        self.guide_tab.setLayout(self.guide_layout)

        self.tabs.addTab(self.habits_tab, "HABIT SETTINGS")
        self.tabs.addTab(self.guide_tab, "ABOUT / GUIDE")
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def handle_streak(self):
        hab = self.streak_input.text().strip().lower()  # Normalize input
        try:
            with open("user_stats.json", "r") as file:
                user_stats = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            user_stats = {}

        done = user_stats.get("completed_habits", [])

        # Check for exact habit match at the end of the string (case-insensitive)
        found = any(habit.lower().endswith(f" {hab}") for habit in done)
        if found:
            self.calculate_streak(hab)
        else:
            self.streak_input.setText("THE HABIT YOU GAVE WAS NOT IN YOUR HABITS")

    def give_user_rank(self):
        try:
            with open("user_stats.json", "r") as file:
                user_stats = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            user_stats = {}

        xp = user_stats.get('xp', 0)

        if xp < 100:
            rank = "📄 Just Getting Started"
        elif 1000 > xp > 100:
            rank = "🥉 Habit Novice"
        elif xp < 5000:
            rank = "🧪 Routine Explorer"
        elif xp < 15000:
            rank = "🔥 Discipline Rookie"
        elif xp < 30000:
            rank = "⚡ Consistency Knight"
        elif xp < 50000:
            rank = "🚀 Momentum Master"
        elif xp < 100000:
            rank = "💎 Habit Hero"
        else:
            rank = "👑 Habits Master"
        self.rank.setText(rank)
    def show_habits_handler(self):
        habits : list = self.data.load_habits_from_file(filename="habits.json")
        if habits:
            self.habits_txt.setText(f"YOUR HABITS ARE {habits}")
        else:
            self.habits_txt.setText("No habits found.")
        self.habits_txt.setReadOnly(True)
    def calculate_streak(self, entry: str = "code"):
        streak = 0
        today = datetime.datetime.now().date()
        try:
            with open("user_stats.json", "r") as file:
                user_stats = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            user_stats = {}
        done = set(h.lower() for h in user_stats.get("completed_habits", []))  # Normalize to lower case
        entry = entry.lower()
        for i in range(len(done)):
            check_day = today - datetime.timedelta(days=i)
            check_str = f"{check_day} {entry}"
            print(f"Checking: {check_str}")
            if check_str in done:
                streak += 1
            else:
                break
        user_stats["streak"] = streak
        self.data.create_json_for_store(data=user_stats)
        print("Final streak:", streak)
class Security(QWidget):
    def __init__(self):

        self.new_password = QLineEdit()
        self.group = QGroupBox("PASSWORD RESETTING SECTION")
        super().__init__()
        self.new_window : Main = Main()
        self.locked = True
        self.attempts = 0
        self.username_reset = QLineEdit()
        self.username_reset.setPlaceholderText("ENTER YOUR USERNAME TO RESET")
        self.reset = QLineEdit()
        self.reset.setPlaceholderText("ENTER RESET KEY")
        self.check_login  : bool = False
        self.setWindowTitle("User  Authentication")

        # Password context setup
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
        #data
        self.data = DataManager()
        # Widgets
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.Password)

        self.key = QLineEdit()
        self.key.setPlaceholderText("Enter a key to reset your password")
        self.key.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("background-color: light green; font-weight: bold;")
        self.password_suggest = QLabel()
        self.create_account_btn = QPushButton("Create Account")
        self.create_account_btn.setStyleSheet("background-color: lightblue; font-weight: bold;")
        self.start = QPushButton("START APP")
        self.start.setEnabled(False)
        self.reset = QLineEdit()
        self.reset.setPlaceholderText("ENTER YOUR RESET KEY")
        self.reset.setEchoMode(QLineEdit.Password)
        self.reset_now = QPushButton("RESET PASSWORD")
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)
        layout.addWidget(self.key)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.create_account_btn)
        layout.addWidget(self.start)
        layout.addWidget(self.password_suggest)
        self.setLayout(layout)
        self.group_layout = QVBoxLayout()
        self.group_layout.addWidget(QLabel("Reset Username"))
        self.group_layout.addWidget(self.username_reset)
        self.group_layout.addWidget(QLabel("Reset Key"))
        self.group_layout.addWidget(self.reset)
        layout.addWidget(self.group)
        self.group.setLayout(self.group_layout)
        # Add a button to trigger password reset
        self.reset_btn = QPushButton("Reset Password")
        self.reset_btn.setStyleSheet("background-color: orange; font-weight: bold;")
        layout.addWidget(self.reset_btn)
        self.reset_btn.clicked.connect(self.reset_password)

        # Connections
        self.create_account_btn.clicked.connect(self.create_account)
        self.login_btn.clicked.connect(self.login_user)
    def create_account(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        key = self.key.text().strip()

        if not username or not password or not key:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return

        hashed_password = self.pwd_context.hash(password)
        hashed_key = self.pwd_context.hash(key)

        data = {
            "username": username,
            "password": hashed_password,
            "key": hashed_key
        }

        self.data.create_json_for_store(data=data,filename="users.json")
        QMessageBox.information(self, "Success", "Account created successfully!")
    def login_user(self):
        try:
            with open("users.json", "r") as file:
                user_credentials = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            QMessageBox.warning(self, "Error", "No account found. Please create one.")
            return

        username_input = self.username.text().strip()
        password_input = self.password.text().strip()

        real_username = user_credentials.get("username")
        real_hashed_password = user_credentials.get("password")
        if real_username == username_input and self.pwd_context.verify(password_input, real_hashed_password):
            QMessageBox.information(self, "Login", "Login successful!")
            self.locked = False
            self.start.setEnabled(True)
            self.start_app()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
            self.attempts += 1
            if self.attempts >= 1:
                self.lock_out_login()

    def lockout(self, seconds : int =60000):
        self.setEnabled(False)
        timer =  QTimer()
        timer.singleShot(seconds,self.unlock)
    def start_app(self):
        self.new_window = Main()
        self.new_window.show()
        self.close()
    def lock_out_login(self):
        self.locked = True
        self.login_btn.setEnabled(False)
        self.create_account_btn.setEnabled(False)
        self.start.setEnabled(False)
        QMessageBox.critical(self, "Locked Out", "Too many failed login attempts. Try again in 1 minute.")
        self.lockout()
    def unlock(self):
        self.setEnabled(True)
        self.locked = False
        self.login_btn.setEnabled(True)
        self.create_account_btn.setEnabled(True)
        self.start.setEnabled(True)
        QMessageBox.information(self,"UNLOCKED","YOU CAN TRY NOW (BETTER TO RESET PASSWORD)")
    def reset_password(self):
        username = self.username_reset.text()
        reset = self.reset.text()
        print(username,reset)
        if not reset or  not username :
            QMessageBox.warning(self,"ERROR","YOU DID NOT ENTER USERNAME OR RESET KEY")
            return
        try:
            with open("users.json", "r") as file:
                user_credentials = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            QMessageBox.warning(self, "Error", "No account found. Please create one.")
            return
        if self.reset_now in self.group_layout :
            self.group_layout.removeWidget(self.reset_now)
            self.reset_now.deleteLater()
        real_username = user_credentials.get("username")
        key = user_credentials.get("key")
        print(real_username,key)
        if real_username == username and self.pwd_context.verify(reset, key):
            self.new_password = QLineEdit()
            self.new_password.setPlaceholderText("ENTER THE PASSWORD")
            self.new_password.setEchoMode(QLineEdit.Password)
            self.group_layout.addWidget(self.new_password)
            self.suggest_password()
            self.group_layout.removeWidget(self.reset_btn)

            self.group_layout.addWidget(self.reset_now)
            self.reset_now.clicked.connect(self.reset_successfully)
            self.reset_now.setStyleSheet("background-color: orange; font-weight: bold;")
    def reset_successfully(self):
        username = self.username_reset.text()
        new_password_txt  = self.new_password.text()
        reset = self.reset.text()
        data = {
            "username": username,
            "password": self.pwd_context.hash(new_password_txt),
            "key": self.pwd_context.hash(reset)
        }
        self.data.create_json_for_store(data=data,filename="users.json")
        if self.new_password in self.group_layout.children():  # Check if it's still in the layout
            self.group_layout.removeWidget(self.new_password)
            self.new_password.deleteLater()

        if self.reset_now in self.group_layout.children():  # Check if it's still in the layout
            self.group_layout.removeWidget(self.reset_now)
            self.reset_now.deleteLater()

            # Re-add the original reset_btn if it's not already there
        if self.reset_btn not in self.group_layout.children():
            self.group_layout.addWidget(self.reset_btn)

            # Clear the password suggestion label
        self.password_suggest.setText("")

        # Re-enable the main security window, as reset is complete
        self.setEnabled(True)


    def suggest_password(self):

        letters  : str = "qwertyupasdfghjkmnbvcxz"
        cap_letters = "QWERTYUPKJHGFDSAZXCVBNM"
        symbols = "@#£_&-+()/?!;:'~`|×}{=^¢$¥€%✓[]"
        nums = "23456789"
        password_length : int  = 16
        all_chars = letters + cap_letters + symbols + nums

        password_box = [secrets.choice(letters), secrets.choice(cap_letters), secrets.choice(nums),
                            secrets.choice(symbols)]
        random.shuffle(password_box)
        remaining = password_length - 4
        password = ""
        for k in range(remaining):
            password_letter = secrets.choice(all_chars)
            password += password_letter
            password_box.append(password_letter)
        random.shuffle(password_box)
        password = ''.join(password_box)
        self.password_suggest.setText(f"SUGGESTED PASSWORD : {password}")
class Notification(QWidget):
    def __init__(self):
        super().__init__()
        self.notif_inputs = []
        self.data = DataManager()
        self.notif_timer = QTimer()
        self.notif_timer.timeout.connect(self.check_notifications)

        # Main layout
        self.layout = QVBoxLayout()

        # Create buttons
        self.generate_btn = QPushButton("CREATE NOTIFICATION TIME UI")
        self.save_btn = QPushButton("SAVE NOTIFICATION TIMES")

        # Connect buttons
        self.generate_btn.clicked.connect(self.create_notif_time_ui)
        self.save_btn.clicked.connect(self.save_notif_time)

        # Add buttons to layout
        self.layout.addWidget(self.generate_btn)
        self.layout.addWidget(self.save_btn)

        # Set layout
        self.setLayout(self.layout)

    def create_notif_time_ui(self):
        self.notif_inputs.clear()
        info = self.data.load_habits_from_file(filename="habits.json")

        for habit in info:
            notif_input = QLineEdit()
            habit_name = habit.get("habit_name", "UNKNOWN")
            notif_input.setPlaceholderText(f"{habit_name} NOTIFICATION TIME (e.g. 18:30)")
            self.notif_inputs.append(notif_input)
            self.layout.addWidget(notif_input)

    def save_notif_time(self):
        info = self.data.load_habits_from_file(filename="habits.json")
        for i in range(len(self.notif_inputs)):
            input_text = self.notif_inputs[i].text().strip()
            if not input_text:
                continue
            try:
                # Validate input time format
                parts = input_text.split(' ')
                if len(parts) != 2:
                    QMessageBox.warning(self,"INVALID FORMAT")
                habit_name, time_str = parts
                datetime.datetime.strptime(time_str, "%H:%M")

                # Match habit and save time
                for habit in info:
                    if habit["habit_name"].lower() == habit_name.lower():
                        habit["NOTIFICATION"] = time_str
                        break
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", f"Invalid format: {input_text}. Use HABIT_NAME HH:MM")

        self.data.create_json_for_store(data=info, filename="habits.json")
        QMessageBox.information(self, "Saved", "Notification times saved.")
        self.notif_timer.start(1200000)  # Check every 120 seconds

    def check_notifications(self):
        now = datetime.datetime.now().strftime("%H:%M")
        try:
            with open("habits.json", "r") as file:
                habits = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        for habit in habits:
            notif_time = habit.get("NOTIFICATION", "")
            if notif_time and now >= notif_time:
                QMessageBox.warning(self, "Reminder", f"⏰ Time to: {habit['habit_name'].upper()}")
                # Optional: prevent repeated warnings by clearing the time or updating a flag

class DataManager :
    def __init__(self):
        pass

    @staticmethod
    def create_json_for_store(data, filename="users.json"):
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    @staticmethod
    def load_habits_from_file(filename="habits.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                return list(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return list()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Security()
    window.suggest_password()
    window.show()
    sys.exit(app.exec_())
