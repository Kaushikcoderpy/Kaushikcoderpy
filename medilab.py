import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score,
    roc_curve, precision_recall_curve
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QScrollArea,
                             QLabel, QLineEdit, QMessageBox, QVBoxLayout, QWidget, QTextEdit, QTabWidget, QGroupBox,QCheckBox)
from PyQt5.Qt import QFont, Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys, random, secrets
from passlib.context import CryptContext
from PyQt5.QtGui import QIcon
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

data = pd.read_csv("archive (1).zip")
class Main(QMainWindow):
    def __init__(self,encryption):
        super().__init__()
        self.setWindowTitle("MEDILAB")
        # Set app icon
        self.setWindowIcon(QIcon("medilab_logo.png"))
        # Create a container widget
        container = QWidget()
        self.layout = QVBoxLayout(container)

        # Add dark mode checkbox
        self.cb = QCheckBox("DARK MODE")
        self.layout.addWidget(self.cb)
        self.cb.stateChanged.connect(self.dark_mode)

        # Tab widget
        self.tab = QTabWidget()
        self.gui = GUI(encryption)
        self.tab.addTab(self.gui, "HEART STROKE PREDICTION")
        helps = HelpWidget()
        self.tab.addTab(helps, "GUIDE")
        self.tab.addTab(AccuracyTab(), "ACCURACY")

        self.layout.addWidget(self.tab)

        # Set container as the central widget
        self.setCentralWidget(container)

    def dark_mode(self):
        if self.cb.isChecked():
            self.setStyleSheet("""
                /* Base dark theme */
                QWidget {
                    background-color: #1e1e1e;
                    color: #f0f0f0;
                    font-family: Segoe UI;
                    font-size: 12px;
                }

                /* Labels - bright with different colors */
                QLabel {
                    font-weight: 500;
                }
                QLabel[class="title"] {
                    color: #ff7f50;  /* Coral */
                    font-size: 16px;
                    font-weight: 600;
                }
                QLabel[class="subtitle"] {
                    color: #2ed573;  /* Green */
                    font-size: 14px;
                }
                QLabel[class="warning"] {
                    color: #eccc68;  /* Yellow */
                }

                /* Buttons - rainbow color palette */
                QPushButton {
                    color: white;
                    font-weight: bold;
                    padding: 8px 16px;
                    border-radius: 6px;
                    min-width: 100px;
                    border: none;
                    /* Default blue */
                    background-color: #007acc;
                }

                /* Alternate button colors */
                QPushButton[color="red"] {
                    background-color: #ff6b81;
                }
                QPushButton[color="orange"] {
                    background-color: #ffa07a;
                }
                QPushButton[color="yellow"] {
                    background-color: #eccc68;
                }
                QPushButton[color="green"] {
                    background-color: #7bed9f;
                }
                QPushButton[color="purple"] {
                    background-color: #9b59b6;
                }

                QPushButton:hover {
                    opacity: 0.9;
                }

                /* Input fields with glow effect */
                QLineEdit, QTextEdit, QPlainTextEdit {
                    background-color: #2e2e2e;
                    color: white;
                    border: 1px solid #555;
                    padding: 8px;
                    border-radius: 5px;
                    selection-background-color: #ff7f50;
                }

                QLineEdit:focus, QTextEdit:focus {
                    border: 1px solid #1e90ff;
                }

                /* Scrollbars with color */
                QScrollBar:vertical {
                    width: 12px;
                    background: #2a2a2a;
                }

                QScrollBar::handle:vertical {
                    background: #ff7f50;
                    min-height: 20px;
                    border-radius: 6px;
                }
                /* Tab widget styling */
                QTabWidget::pane {
                    border-top: 2px solid #ff7f50;
                }

                QTabBar::tab {
                    background: #2a2a2a;
                    color: #f0f0f0;
                    padding: 8px 16px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    border: 1px solid #444;
                    margin-right: 2px;
                }

                QTabBar::tab:selected {
                    background: #1e1e1e;
                    color: #ff7f50;
                    border-bottom: 2px solid #ff7f50;
                }

                /* Checkboxes with color */
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                }

                QCheckBox::indicator:checked {
                    background-color: #7bed9f;
                    border: 1px solid #555;
                }

                /* Custom colored frames */
                QFrame[class="highlight"] {
                    border: 2px solid #1e90ff;
                    border-radius: 5px;
                }
            """)


        else :
            self.setStyleSheet("")
class ModifyData:
    def __init__(self):
        df  = pd.DataFrame(data)
        self.df = df.copy()
        self.clean_data()

    def clean_data(self):
        self.df['ST_Slope'] = self.df['ST_Slope'].map({'Up': 0, 'Flat': 1, 'Down': 2})
        self.df['ExerciseAngina'] = self.df['ExerciseAngina'].map({'Y': 1, 'N': 0})
        self.df['RestingECG'] = self.df['RestingECG'].map({'Normal': 1, 'ST': 2, 'LVH': 3})
        self.df['ChestPainType'] = self.df['ChestPainType'].map({'ASY': 4, 'TA': 3, 'NAP': 2, 'ATA': 1})

        self.df['Sex'] = self.df['Sex'].replace(['nan', 'NaN', 'None', None], np.nan)
        self.df['Sex'] = self.df['Sex'].fillna(self.df['Sex'].mode()[0])
        self.df['Sex'] = self.df['Sex'].map({'M': 1, 'F': 0})

    def get_features_labels(self):
        feature = self.df[['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol',
                            'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina',
                            'Oldpeak', 'ST_Slope']]
        labels = self.df['HeartDisease']
        return feature, labels

    def start_eval_auto(self):
        x, y = self.get_features_labels()

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        trainer = ModelTrainer()
        predictions = trainer.predict(x_test)
        probability = trainer.predict_proba(x_test)

        evaluator = Evaluator(y_test)

        for model_name in predictions:
            evaluator.evaluate(model_name, predictions[model_name], probability[model_name])


class ModelTrainer:
    def __init__(self,target='HeartDisease'):
        df = pd.DataFrame(data)
        modifier = ModifyData()
        if target not in df.columns:
            raise ValueError(f"Target column '{target}' not found in DataFrame. FOUND {df.columns}")
        try :
            y = df[target]
        except Exception as exception :
            QMessageBox.information(None,"INFO",f"{exception}")
        x = modifier.df[['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol',
                'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina',
                'Oldpeak', 'ST_Slope']]
        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)
        self.lr = LogisticRegression(max_iter=1000, random_state=42)
        self.rf = RandomForestClassifier(n_estimators=100, min_samples_split=10,
                                         min_samples_leaf=10, max_features='log2',
                                         max_depth=20)
        self.xgb = XGBClassifier(n_estimators=100, n_jobs=-1, random_state=42)

        self.lr.fit(x_train, y_train)
        self.rf.fit(x_train, y_train)
        self.xgb.fit(x_train, y_train)

    def predict(self,x_test):
        return {
            'lr': self.lr.predict(x_test),
            'rf': self.rf.predict(x_test),
            'xgb': self.xgb.predict(x_test)
        }

    def predict_proba(self, x_test):
        return {
            'LINEAR REGRESSION MODEL': self.lr.predict_proba(x_test)[:, 1],
            'RANDOM FOREST MODEL': self.rf.predict_proba(x_test)[:, 1],
            'GRADIENT BOOSTING MODEL': self.xgb.predict_proba(x_test)[:, 1]
        }


class Evaluator:
    def __init__(self, y_true):
        self.y_true = y_true

    def evaluate(self, name, prediction, y_proba)  :
        print(f"\nmodel = {name.upper()}")
        print("✅ Accuracy:", accuracy_score(self.y_true, prediction))
        print("✅ Precision:", precision_score(self.y_true, prediction))
        print("✅ Recall:", recall_score(self.y_true, prediction))
        print("✅ F1 Score:", f1_score(self.y_true, prediction))
        print("✅ ROC AUC:", roc_auc_score(self.y_true, y_proba))
        print("\n📋 Classification Report:\n", classification_report(self.y_true, prediction))
        print("\n🔍 Confusion Matrix:\n", confusion_matrix(self.y_true, prediction))

    def plot_roc_curve(self, y_proba):
        fpr, tpr, _ = roc_curve(self.y_true, y_proba)
        plt.figure(figsize=(6, 4))
        plt.plot(fpr, tpr, label='ROC Curve (AUC = {:.2f})'.format(roc_auc_score(self.y_true, y_proba)))
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate (Recall)')
        plt.title('ROC Curve')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_pr_curve(self, y_proba):
        prec, rec, _ = precision_recall_curve(self.y_true, y_proba)
        plt.figure(figsize=(6, 4))
        plt.plot(rec, prec, label='PR Curve')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
class GUI(QWidget):
    def __init__(self, encryption):
        super().__init__()
        self.fernet = encryption
        self.data_dict: dict = {}
        self.features = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol',
                         'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina',
                         'Oldpeak', 'ST_Slope']
        self.submit = QPushButton("SUBMIT MY DETAILS")
        self.view_btn = QPushButton("VIEW MY OLD RECORDS")

        # Font size doubled
        font = QFont("Segoe UI", 22)
        self.setFont(font)

        # Scrollable area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.layout = QVBoxLayout(self.content_widget)

        # Button style
        self.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-size: 18px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)

        self.model = ModelTrainer()
        self.layout.addWidget(self.view_btn)
        self.view_btn.clicked.connect(self.view_record)

        self.set_layout()

        # Set scrollable layout as main
        self.scroll.setWidget(self.content_widget)
        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(self.scroll)
        self.setLayout(outer_layout)

    def set_layout(self):
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Heart Stroke Risk Prediction Tool")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin: 10px;")
        self.layout.addWidget(title)

        def add_input(label, placeholder):
            box = QLineEdit()
            box.setPlaceholderText(placeholder)
            self.layout.addWidget(box)
            setattr(self, label, box)

        add_input('age', "1) What is your age?")
        add_input('sex', "2) What is your sex?")
        add_input('chest_pain_type', "3) Type of chest pain experienced?")
        add_input('resting_bp', "4) Resting blood pressure?")
        add_input('cholesterol', "5) Cholesterol level?")
        add_input('fasting_bs', "6) Fasting blood sugar level?")
        add_input('resting_ecg', "7) Resting electrocardiographic results?")
        add_input('max_hr', "8) Maximum heart rate achieved?")
        add_input('exercise_angina', "9) Exercise-induced angina (yes/no)?")
        add_input('oldpeak', "10) ST depression induced by exercise relative to rest?")
        add_input('st_slope', "11) The slope of the peak exercise ST segment?")

        self.submit.clicked.connect(self.validate_inputs)
        self.layout.addWidget(self.submit)

    @staticmethod
    def preprocess_user_input(df):
        df['Sex'] = df['Sex'].map({'M': 1, 'F': 0})
        df['ChestPainType'] = df['ChestPainType'].map({'ATA': 1, 'NAP': 2, 'TA': 3, 'ASY': 4})
        df['RestingECG'] = df['RestingECG'].map({'Normal': 1, 'ST': 2, 'LVH': 3})
        df['ExerciseAngina'] = df['ExerciseAngina'].map({'N': 0, 'Y': 1})
        df['ST_Slope'] = df['ST_Slope'].map({'Up': 0, 'Flat': 1, 'Down': 2})
        return df

    def validate_inputs(self):
        try:
            age = int(self.age.text())
            if age <= 0:
                raise ValueError("Age must be a positive number.")
        except ValueError:
            self.show_error("Please enter a valid, positive number for Age.")
            return False

        try:
            resting_bp = int(self.resting_bp.text())
            if resting_bp <= 0:
                raise ValueError
        except ValueError:
            self.show_error("Please enter a valid, positive number for Resting Blood Pressure.")
            return False

        try:
            cholesterol = int(self.cholesterol.text())
            if cholesterol <= 0:
                raise ValueError
        except ValueError:
            self.show_error("Please enter a valid, positive number for Cholesterol.")
            return False

        try:
            fasting_bs = int(self.fasting_bs.text())
            if fasting_bs < 0:
                raise ValueError
        except ValueError:
            self.show_error("Please enter a valid number (0 or above) for Fasting Blood Sugar.")
            return False

        try:
            max_hr = int(self.max_hr.text())
            if max_hr <= 0:
                raise ValueError
        except ValueError:
            self.show_error("Please enter a valid, positive number for Max Heart Rate.")
            return False

        try:
            oldpeak = float(self.oldpeak.text())
            if oldpeak < 0:
                raise ValueError
        except ValueError:
            self.show_error("Please enter a valid non-negative number for Oldpeak.")
            return False

        # Check categorical fields
        for field in ['sex', 'chest_pain_type', 'resting_ecg', 'exercise_angina', 'st_slope']:
            if not getattr(self, field).text().strip():
                self.show_error(f"{field.replace('_', ' ').title()} field cannot be empty.")
                return False

        self.get_input_data()
        return True

    def show_error(self, message):
        if isinstance(message, bytes):
            message = message.decode(errors="ignore")
        QMessageBox.critical(self, "Validation Error", str(message))

    def get_input_data(self):
        try:
            data_dict = [{
                'Age': int(self.age.text()),
                'Sex': self.sex.text(),
                'ChestPainType': self.chest_pain_type.text(),
                'RestingBP': int(self.resting_bp.text()),
                'Cholesterol': int(self.cholesterol.text()),
                'FastingBS': int(self.fasting_bs.text()),
                'RestingECG': self.resting_ecg.text(),
                'MaxHR': int(self.max_hr.text()),
                'ExerciseAngina': self.exercise_angina.text(),
                'Oldpeak': float(self.oldpeak.text()),
                'ST_Slope': self.st_slope.text()
            }]
        except ValueError:
            QMessageBox.warning(self, "INVALID DATA", "CHECK GUIDE ABOUT HOW TO ENTER DATA")
            return

        self.start_predictions(data_dict)

    def start_predictions(self, data_dict):
        try:
            preprocessed_df: pd.DataFrame = self.preprocess_user_input(pd.DataFrame(data_dict))
            predictions: dict = self.model.predict(preprocessed_df)
            probability: dict = self.model.predict_proba(preprocessed_df)

            python_preds = {k: v.tolist() if hasattr(v, "tolist") else v for k, v in predictions.items()}
            python_probs = {k: v.tolist() if hasattr(v, "tolist") else v for k, v in probability.items()}

            cleaned_dict = [
                {
                    k: (
                        v.decode() if isinstance(v, bytes)
                        else v.item() if hasattr(v, "item")
                        else str(v) if isinstance(v, (bytes, bytearray))
                        else v
                    )
                    for k, v in row.items()
                }
                for row in data_dict
            ]

            serialized_data = json.dumps(cleaned_dict).encode()
            encrypted_data = self.fernet.encrypt(serialized_data)
            encoded_encrypted_data = base64.b64encode(encrypted_data).decode()

            with open("record.json", "w") as file:
                json.dump(
                    {
                        "encrypted_input": encoded_encrypted_data,
                        "predictions": python_preds,
                        "probability": python_probs
                    },
                    file,
                    indent=4
                )

            label1 = QLabel(f"PREDICTION BY MODEL MAX : {max(python_preds.values())} "
                            f"MIN : {min(python_preds.values())}")
            label2 = QLabel(f"PROBABILITY OF HEART STROKE : {python_probs}")

            label1.setStyleSheet("font-size: 20px; color: green; font-weight: bold;")
            label2.setStyleSheet("font-size: 20px; color: #d35400; font-weight: bold;")

            self.layout.addWidget(label1)
            self.layout.addWidget(label2)

        except Exception as ex:
            import traceback
            traceback.print_exc()
            self.show_error(f"An error occurred: {str(ex)}")

    def view_record(self):
        try:
            with open("record.json", "r") as file:
                data_records = json.load(file)
                encoded_encrypted_data = data_records["encrypted_input"]
                encrypted_data = base64.b64decode(encoded_encrypted_data)
                restored_dict = json.loads(self.fernet.decrypt(encrypted_data))

                full_output = {
                    "User Input": restored_dict,
                    "Predictions": data_records["predictions"],
                    "Probabilities": data_records["probability"]
                }

                txt_edit = QTextEdit()
                txt_edit.setText(json.dumps(full_output, indent=4))
                txt_edit.setReadOnly(True)
                txt_edit.setStyleSheet("""
                    background-color: #f4faff;
                    color: #1a1a1a;
                    font-family: Consolas, Courier, monospace;
                    font-size: 18px;
                    border: 2px solid #2980b9;
                    border-radius: 8px;
                    padding: 12px;
                """)
                self.layout.addWidget(txt_edit)

        except FileNotFoundError:
            QMessageBox.critical(self, "ERROR", "Encrypted data file not found!")
        except Exception as e:
            self.show_error(f"Decryption failed: {str(e)}")




class HelpWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("How to Use - Help Guide")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("🩺 Heart Disease Prediction App – Help")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 1. Short summary
        short_label = QLabel("🔹 Quick Summary:")
        short_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(short_label)

        self.short_summary = QTextEdit()
        self.short_summary.setReadOnly(True)
        self.short_summary.setFont(QFont("Segoe UI", 11))
        self.short_summary.setText(
            "Enter your medical details like age, sex, chest pain type, cholesterol level, etc., "
            "and click 'SUBMIT MY DETAILS'. The model will predict if you're at risk for heart disease "
            "and show a confidence score."
            " M : MALE 👨"
            " F : FEMALE 👩"

            " ATA : ATYPICAL ANGINA ❤️‍🩹"
            " NAP : NON-ANGINAL PAIN 💢"
            " TA : TYPICAL ANGINA ❤️"
            " ASY : ASYMPTOMATIC 😐"

            " Normal : NORMAL 💓"
            " ST : ST-T WAVE ABNORMALITY 📉"
            " LVH : LEFT VENTRICULAR HYPERTROPHY 💪"

            " N : NO 🚫"
            " Y : YES ✅"

            " Up : UPSLOPING ⬆️"
            " Flat : FLAT ➖"
            " Down : DOWNSLOPING ⬇️" )

        layout.addWidget(self.short_summary)

        # 2. Detailed guide
        detailed_label = QLabel("📘 Full Guide:")
        detailed_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(detailed_label)

        self.detailed_guide = QTextEdit()
        self.detailed_guide.setReadOnly(True)
        self.detailed_guide.setFont(QFont("Segoe UI", 10))
        self.detailed_guide.setText(
            "Step-by-step instructions:\n\n"
            "1. Launch the app.\n"
            "2. Fill in all the fields:\n"
            "   - Age: Enter your age in years.\n"
            "   - Sex: Type 'M' for male or 'F' for female.\n"
            "   - Chest Pain Type: Choose from 'ATA', 'NAP', 'TA', or 'ASY'.\n"
            "   - Resting Blood Pressure: Normal is around 120 mm Hg.\n"
            "   - Cholesterol: Normal range is 125-200 mg/dL.\n"
            "   - Fasting Blood Sugar: Enter 0 (normal) or 1 (high).\n"
            "   - Resting ECG: Choose from 'Normal', 'ST', or 'LVH'.\n"
            "   - Max Heart Rate Achieved: A number like 150 is typical.\n"
            "   - Exercise Angina: Type 'Y' for yes or 'N' for no.\n"
            "   - Oldpeak: ST depression value like 1.0 or 2.5.\n"
            "   - ST Slope: Choose from 'Up', 'Flat', or 'Down'.\n\n"
            "3. Click the blue 'SUBMIT MY DETAILS' button.\n"
            "4. The model will show:\n"
            "   - The predicted risk (0 = No disease, 1 = Disease).\n"
            "   - The probability or confidence score from the model.\n\n"
            "Tip: If you're not sure about a value, consult your doctor or leave blank and fill later."
        )
        layout.addWidget(self.detailed_guide)

        self.setLayout(layout)
class Security(QMainWindow):
    def __init__(self):
        super().__init__()
        self.locked = True  # Initial state is locked until login
        self.attempts = 0  # Login attempt counter
        self.check_login: bool = False  # Flag for successful login
        self.setWindowTitle("User Authentication")
        layout = QVBoxLayout()
        self.central_widget = QWidget()  # Create a new central widget
        self.central_widget.setLayout(layout)  # Set layout
        self.setCentralWidget(self.central_widget)  # Attach it to the QMainWindow
        # Add Authentication Logo
        self.setWindowIcon(QIcon("logo2.png"))

        layout.addWidget(QLabel("Username"))

        # Password context setup for hashing and verifying passwords
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

        # Widgets for login/account creation
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.reset_key_input = QLineEdit()  # This is for setting/entering the reset key
        self.reset_key_input.setPlaceholderText("Enter a key to reset your password (for new account)")
        self.reset_key_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("background-color: light green; font-weight: bold;")

        self.password_suggest_label = QLabel()  # Label to display suggested password

        self.create_account_btn = QPushButton("Create Account")
        self.create_account_btn.setStyleSheet("background-color: lightblue; font-weight: bold;")

        self.start_app_btn = QPushButton("START APP")
        self.start_app_btn.setEnabled(False)  # Disabled until successful login
        self.start_app_btn.clicked.connect(self.start_app)

        # Widgets for password resetting
        self.username_reset_input = QLineEdit()
        self.username_reset_input.setPlaceholderText("ENTER YOUR USERNAME TO RESET")

        self.reset_key_for_reset_input = QLineEdit()  # This is for entering the reset key during reset process
        self.reset_key_for_reset_input.setPlaceholderText("ENTER RESET KEY")
        self.reset_key_for_reset_input.setEchoMode(QLineEdit.Password)

        self.new_password_input = QLineEdit()  # For entering new password during reset
        self.new_password_input.setPlaceholderText("ENTER THE NEW PASSWORD")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.hide()  # Hidden by default

        self.confirm_reset_btn = QPushButton("RESET PASSWORD NOW")  # Button to confirm new password during reset
        self.confirm_reset_btn.setStyleSheet("background-color: orange; font-weight: bold;")
        self.confirm_reset_btn.clicked.connect(self.reset_successfully)
        self.confirm_reset_btn.hide()  # Hidden by default

        # Main layout
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.reset_key_input)  # Used when creating account
        layout.addWidget(self.login_btn)
        layout.addWidget(self.create_account_btn)
        layout.addWidget(self.start_app_btn)
        layout.addWidget(self.password_suggest_label)

        # Group box for password reset section
        self.reset_group_box = QGroupBox("PASSWORD RESET SECTION")
        self.reset_group_layout = QVBoxLayout()
        self.reset_group_layout.addWidget(QLabel("Reset Username"))
        self.reset_group_layout.addWidget(self.username_reset_input)
        self.reset_group_layout.addWidget(QLabel("Reset Key"))
        self.reset_group_layout.addWidget(self.reset_key_for_reset_input)

        self.initial_reset_btn = QPushButton("INITIATE PASSWORD RESET")  # Button to start reset process
        self.initial_reset_btn.setStyleSheet("background-color: orange; font-weight: bold;")
        self.initial_reset_btn.clicked.connect(self.initiate_password_reset)
        self.reset_group_layout.addWidget(self.initial_reset_btn)

        self.reset_group_box.setLayout(self.reset_group_layout)
        layout.addWidget(self.reset_group_box)
        self.setLayout(layout)

        # Connections for main buttons
        self.create_account_btn.clicked.connect(self.create_account)
        self.login_btn.clicked.connect(self.login_user)
    # Creates a new user account
    def create_account(self):
        username = self.username_input.text().strip()
        self.password = self.password_input.text().strip()
        key = self.reset_key_input.text().strip()

        if not username or not self.password or not key:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out to create an account.")
            return
        if len(self.password) < 12:
            QMessageBox.warning(self, "PASSWORD ERROR", "Password must be at least 12 characters.")
            return
        if len(key) < 10:
            QMessageBox.warning(self, "RESET KEY ERROR", "Reset key must be at least 10 characters.")
            return

        # Create or load salt
        salt = Encryption.get_or_create_salt()
        self.encryption = Encryption(self.password, salt)

        encrypted_username = self.encryption.encrypt(username)
        hashed_password = self.pwd_context.hash(self.password)
        hashed_key = self.pwd_context.hash(key)

        data_user = {
            "username": encrypted_username.decode(),  # Convert to string for saving
            "password": hashed_password,
            "key": hashed_key
        }

        try:
            with open("user_ml.json", "w") as file:
                json.dump(data_user, file, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "ERROR", f"DATA FILES ARE MISSING! {e}")
            return

        QMessageBox.information(self, "Success", "Account created successfully!")
        self.start_app_btn.setEnabled(True)

    # Logs in the user
    def login_user(self):
        try:
            with open("user_ml.json", "r") as file:
                user_credentials = json.load(file)
        except Exception as f:
            QMessageBox.critical(self, "ERROR", f"DATA FILES ARE MISSING {f}")
            return

        username_input = self.username_input.text().strip()
        password_input = self.password_input.text().strip()

        # Derive Fernet key from password + saved salt
        salt = Encryption.get_or_create_salt()
        self.encryption = Encryption(password_input, salt)

        real_username = user_credentials.get("username")
        decrypted_username = self.encryption.decrypt(real_username.encode())
        real_hashed_password = user_credentials.get("password")

        if decrypted_username == username_input and self.pwd_context.verify(password_input, real_hashed_password):
            QMessageBox.information(self, "Login", "Login successful!")
            self.locked = False
            self.start_app_btn.setEnabled(True)
            self.start_app()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
            self.attempts += 1
            if self.attempts >= 3:
                self.lock_out_login()

    # Locks out login functionality temporarily after multiple failed attempts
    def lock_out_login(self):
        self.locked = True
        self.login_btn.setEnabled(False)
        self.create_account_btn.setEnabled(False)
        self.start_app_btn.setEnabled(False)
        QMessageBox.critical(self, "Locked Out", "Too many failed login attempts. Try again in 1 minute.")
        QTimer.singleShot(60000, self.unlock_login)  # Lock for 1 minute (60 seconds)

    # Unlocks login functionality after a lockout period
    def unlock_login(self):
        self.setEnabled(True)  # Re-enable the window if it was disabled
        self.locked = False
        self.login_btn.setEnabled(True)
        self.create_account_btn.setEnabled(True)
        self.start_app_btn.setEnabled(False)  # Keep start app disabled until login
        QMessageBox.information(self, "UNLOCKED", "You can try logging in again (consider resetting password).")
        self.attempts = 0  # Reset attempts

    # Starts the main application window
    def start_app(self):
        # Pass the DataManager instance to the Main app window
        self.new_window = Main(encryption=self.encryption)
        self.new_window.show()
        self.close()  # Close the login window

    # Initiates the password reset process
    def initiate_password_reset(self):
        username = self.username_reset_input.text().strip()
        reset_key = self.reset_key_for_reset_input.text().strip()

        if not username or not reset_key:
            QMessageBox.warning(self, "Input Error", "Please enter both username and reset key.")
            return

        try :
            with open("user_ml.json","r") as file :
                   user_credentials = json.load(file)
        except Exception as g :
            QMessageBox.critical(self,"ERROR",f"DATA FILES ARE MISSING {g}")
        if not user_credentials:
            QMessageBox.warning(self, "Error", "No account found. Please create one first.")
            return

        real_username = user_credentials.get("username")
        real_username = self.encryption.decrypt(real_username)
        stored_hashed_key = user_credentials.get("key")

        if real_username == username and self.pwd_context.verify(reset_key, stored_hashed_key):
            QMessageBox.information(self, "Reset Initiated", "Verification successful. Enter your new password.")

            self.reset_group_layout.removeWidget(self.initial_reset_btn)
            self.initial_reset_btn.deleteLater()  # Delete the button

            self.reset_group_layout.addWidget(self.new_password_input)
            self.new_password_input.show()  # Show new password input

            self.suggest_password()  # Suggest a strong password

            self.reset_group_layout.addWidget(self.confirm_reset_btn)
            self.confirm_reset_btn.show()  # Show confirm reset button
        else:
            QMessageBox.critical(self, "Verification Failed", "Invalid username or reset key.")

    # Resets the user's password after successful key verification
    def reset_successfully(self):
        username = self.username_reset_input.text().strip()
        new_password_text = self.new_password_input.text().strip()
        reset_key = self.reset_key_for_reset_input.text().strip()

        if not new_password_text:
            QMessageBox.warning(self, "Input Error", "Please enter a new password.")
            return

        # Hash the new password and re-hash the key (if user entered it again)
        hashed_new_password = self.pwd_context.hash(new_password_text)
        hashed_reset_key = self.pwd_context.hash(reset_key)

        updated_data = {
            "username": username,
            "password": hashed_new_password,
            "key": hashed_reset_key
        }
        try :
            with open("user_ml.json","w")  as file :
                json.dump(updated_data,file,indent=4)
        except Exception as k :
            QMessageBox.critical(self,"CRITICAL ERROR",f"DATA FILES ARE MISSING! {k}")

        QMessageBox.information(self, "Password Reset", "Your password has been successfully reset!")

        # Clean up reset UI elements
        self.reset_group_layout.removeWidget(self.new_password_input)
        self.new_password_input.hide()
        self.new_password_input.deleteLater()

        self.reset_group_layout.removeWidget(self.confirm_reset_btn)
        self.confirm_reset_btn.hide()
        self.confirm_reset_btn.deleteLater()

        self.password_suggest_label.setText("")  # Clear password suggestion

        # Re-add the initial reset button for next time
        if self.initial_reset_btn not in self.reset_group_layout.children():
            self.reset_group_layout.addWidget(self.initial_reset_btn)
            self.initial_reset_btn.show()

        # Clear input fields
        self.username_reset_input.clear()
        self.reset_key_for_reset_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.reset_key_input.clear()

    # Generates and displays a strong suggested password
    def suggest_password(self):
        letters: str = "abcdefghijklmnopqrstuvwxyz"
        cap_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        symbols = "!@#$%^&*()-_+=[]{}|;:,.<>?/~`"
        nums = "0123456789"
        password_length: int = 16
        all_chars = letters + cap_letters + symbols + nums

        # Ensure at least one of each character type
        password_chars = [
            secrets.choice(letters),
            secrets.choice(cap_letters),
            secrets.choice(nums),
            secrets.choice(symbols)
        ]

        # Fill the rest of the password length with random characters
        for _ in range(password_length - len(password_chars)):
            password_chars.append(secrets.choice(all_chars))

        random.shuffle(password_chars)  # Shuffle to mix character types
        suggested_password = ''.join(password_chars)
        self.password_suggest_label.setText(f"SUGGESTED PASSWORD: {suggested_password}")
class AccuracyTab(QWidget):
    def __init__(self):
        super().__init__()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        inner = QWidget()
        self.vbox = QVBoxLayout(inner)
        scroll.setWidget(inner)

        layout = QVBoxLayout()
        layout.addWidget(scroll)
        self.setLayout(layout)

        self.init_tab()

    def init_tab(self):
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report

        model = ModelTrainer()
        modifier = ModifyData()
        x, y = modifier.get_features_labels()
        _, x_test, _, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        predictions = model.predict(x_test)
        probas = model.predict_proba(x_test)

        name_map = {'lr': 'LINEAR REGRESSION MODEL', 'rf': 'RANDOM FOREST MODEL', 'xgb': 'GRADIENT BOOSTING MODEL'}
        accuracies = []
        names = []

        for name, y_pred in predictions.items():
            y_proba = probas.get(name_map.get(name))
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            auc = roc_auc_score(y_test, y_proba)
            cm = confusion_matrix(y_test, y_pred)
            cr = classification_report(y_test, y_pred)

            accuracies.append(acc)
            names.append(name.upper())

            metrics_text = (
                f"MODEL: {name.upper()}\n"
                f"✅ Accuracy: {acc:.4f}\n"
                f"✅ Precision: {prec:.4f}\n"
                f"✅ Recall: {rec:.4f}\n"
                f"✅ F1 Score: {f1:.4f}\n"
                f"✅ ROC AUC: {auc:.4f}\n"
                f"📋 Classification Report:\n{cr}\n"
                f"🔍 Confusion Matrix:\n{cm}"
            )
            label = QLabel(metrics_text)
            label.setStyleSheet("font-family: Consolas; background: #2e2e2e; color: #f0f0f0; padding: 8px;")
            label.setWordWrap(True)
            self.vbox.addWidget(label)
            self.vbox.addSpacing(10)

        plt.style.use('dark_background')

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(names, accuracies, color=['skyblue', 'lightgreen', 'salmon'])
        ax.set_title("Model Accuracies")
        ax.set_ylabel("Accuracy Score")
        ax.set_ylim(0, 1)
        ax.grid(True)
        canvas = FigureCanvas(fig)
        self.vbox.addWidget(canvas)

        importance_fig, imp_ax = plt.subplots(figsize=(6, 4))
        importance = model.rf.feature_importances_
        features = x.columns
        imp_ax.barh(features, importance, color="goldenrod")
        imp_ax.set_title("Random Forest Feature Importance's")
        imp_ax.set_xlabel("Importance Score")
        importance_canvas = FigureCanvas(importance_fig)
        self.vbox.addWidget(importance_canvas)

class Encryption:
    def __init__(self, password: str, salt: bytes):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.fernet = Fernet(key)

    @staticmethod
    def get_or_create_salt(filepath="salt.bin", length=16) -> bytes:
        import os
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                return f.read()
        else:
            salt = os.urandom(length)
            with open(filepath, "wb") as f:
                f.write(salt)
            return salt

    def encrypt(self, message: str | bytes):
        if isinstance(message, str):
            message = message.encode()
        return self.fernet.encrypt(message)

    def decrypt(self, encrypted_msg: bytes) -> str:
        return self.fernet.decrypt(encrypted_msg).decode()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        form = Security()
        form.show()
        sys.exit(app.exec_())
    except Exception as e :
        print(e)
