# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/ui/form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QButtonGroup, QFileDialog, QMessageBox
from pipeline import Pipeline
from .record import RecordWindow
from .inference import InferenceWindow
from .demo import ExerciseDemoWindow


class FormWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(900, 650)

        self.MainWindow.setWindowIcon(QtGui.QIcon('favicon.png'))

        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setContentsMargins(24, 24, 24, 24)
        self.verticalLayout_4.setSpacing(16)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.dataTypeLayout = QtWidgets.QVBoxLayout()
        self.dataTypeLayout.setObjectName("dataTypeLayout")
        self.dataTypeLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.dataTypeLabel.setFont(font)
        self.dataTypeLabel.setObjectName("dataTypeLabel")
        self.dataTypeLayout.addWidget(self.dataTypeLabel)
        self.dataTypeRadioButtonLayout = QtWidgets.QHBoxLayout()

        self.dataTypeRadioButtonLayout.setObjectName(
            "dataTypeRadioButtonLayout"
        )
        self.dataTypeRadioButtonGroup = QButtonGroup(self.centralwidget)

        self.liveFeedRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.liveFeedRadioButton.setFont(font)
        self.liveFeedRadioButton.setObjectName("liveFeedRadioButton")
        self.dataTypeRadioButtonLayout.addWidget(self.liveFeedRadioButton)
        self.dataTypeRadioButtonGroup.addButton(self.liveFeedRadioButton)

        self.kimoreRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.kimoreRadioButton.setFont(font)
        self.kimoreRadioButton.setObjectName("kimoreRadioButton")
        self.dataTypeRadioButtonLayout.addWidget(self.kimoreRadioButton)
        self.dataTypeRadioButtonGroup.addButton(self.kimoreRadioButton)

        self.labKinectRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labKinectRadioButton.setFont(font)
        self.labKinectRadioButton.setObjectName("labKinectRadioButton")
        self.dataTypeRadioButtonLayout.addWidget(self.labKinectRadioButton)
        self.dataTypeRadioButtonGroup.addButton(self.labKinectRadioButton)

        self.dataTypeLayout.addLayout(self.dataTypeRadioButtonLayout)
        self.verticalLayout_4.addLayout(self.dataTypeLayout)

        self.selectDataFileWidget = QtWidgets.QWidget(self.centralwidget)
        self.selectDataFileWidget.setEnabled(True)
        self.selectDataFileWidget.setObjectName("selectDataFileWidget")
        self.chooseFileWidget = QtWidgets.QHBoxLayout(
            self.selectDataFileWidget
        )
        self.chooseFileWidget.setContentsMargins(0, -1, 0, -1)
        self.chooseFileWidget.setObjectName("chooseFileWidget")
        self.specifyPathLabel = QtWidgets.QLabel(self.selectDataFileWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.specifyPathLabel.setFont(font)
        self.specifyPathLabel.setObjectName("specifyPathLabel")
        self.chooseFileWidget.addWidget(self.specifyPathLabel)
        self.specifyPathButton = QtWidgets.QPushButton(
            self.selectDataFileWidget
        )
        self.specifyPathButton.setStyleSheet(
            """
            border-width: 5px;
            border-color: #000000;
            border-radius: 5px;
            background: #DD5353;
            color: #FEFEFE;
            padding: 10px 20px;
            font-size: 12px;
            font-weight: bold;
            """
        )
        font = QtGui.QFont()
        font.setPointSize(14)
        self.specifyPathButton.setFont(font)
        self.specifyPathButton.setObjectName("specifyPathButton")
        self.chooseFileWidget.addWidget(self.specifyPathButton)
        self.verticalLayout_4.addWidget(self.selectDataFileWidget)

        self.modelTypeLayout = QtWidgets.QVBoxLayout()
        self.modelTypeLayout.setObjectName("modelTypeLayout")
        self.modelTypeLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.modelTypeLabel.setFont(font)
        self.modelTypeLabel.setObjectName("modelTypeLabel")
        self.modelTypeLayout.addWidget(self.modelTypeLabel)
        self.modelTypeRadioButtonLayout = QtWidgets.QHBoxLayout()
        self.modelTypeRadioButtonLayout.setObjectName(
            "modelTypeRadioButtonLayout"
        )
        self.msg3dRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.msg3dRadioButton.setFont(font)
        self.msg3dRadioButton.setObjectName("msg3dRadioButton")
        self.modelTypeRadioButtonLayout.addWidget(self.msg3dRadioButton)
        self.stgcnRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stgcnRadioButton.setFont(font)
        self.stgcnRadioButton.setObjectName("stgcnRadioButton")
        self.modelTypeRadioButtonLayout.addWidget(self.stgcnRadioButton)
        self.modelTypeLayout.addLayout(self.modelTypeRadioButtonLayout)
        self.verticalLayout_4.addLayout(self.modelTypeLayout)

        self.exerciseTypeLayout = QtWidgets.QVBoxLayout()
        self.exerciseTypeLayout.setObjectName("exerciseTypeLayout")
        self.exerciseTypeLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.exerciseTypeLabel.setFont(font)
        self.exerciseTypeLabel.setObjectName("exerciseTypeLabel")
        self.exerciseTypeLayout.addWidget(self.exerciseTypeLabel)
        self.exerciseTypeComboBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.exerciseTypeComboBox.sizePolicy().hasHeightForWidth()
        )
        self.exerciseTypeComboBox.setSizePolicy(sizePolicy)
        self.exerciseTypeComboBox.setObjectName("exerciseTypeComboBox")
        self.exerciseTypeLayout.addWidget(self.exerciseTypeComboBox)
        self.verticalLayout_4.addLayout(self.exerciseTypeLayout)

        # id name and age fields
        self.IdNameAgeLayout = QtWidgets.QHBoxLayout()
        self.IdNameAgeLayout.setObjectName("IdNameAgeLayout")
        self.patientIdLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.patientIdLabel.setFont(font)
        self.patientIdLabel.setObjectName("patientIdLabel")
        self.IdNameAgeLayout.addWidget(self.patientIdLabel)
        self.patientIdField = QtWidgets.QLineEdit(self.centralwidget)
        self.patientIdField.setObjectName("patientIdField")
        self.IdNameAgeLayout.addWidget(self.patientIdField)
        self.patientNameLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.patientNameLabel.setFont(font)
        self.patientNameLabel.setObjectName("patientNameLabel")
        self.IdNameAgeLayout.addWidget(self.patientNameLabel)
        self.patientNameField = QtWidgets.QLineEdit(self.centralwidget)
        self.patientNameField.setObjectName("patientNameField")
        self.IdNameAgeLayout.addWidget(self.patientNameField)
        self.patientAgeLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.patientAgeLabel.setFont(font)
        self.patientAgeLabel.setObjectName("patientAgeLabel")
        self.IdNameAgeLayout.addWidget(self.patientAgeLabel)
        self.patientAgeField = QtWidgets.QLineEdit(self.centralwidget)
        self.patientAgeField.setObjectName("patientAgeField")
        self.IdNameAgeLayout.addWidget(self.patientAgeField)
        self.verticalLayout_4.addLayout(self.IdNameAgeLayout)
        # end of id name and age fields

        self.visualizeDataCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.visualizeDataCheckBox.setFont(font)
        self.visualizeDataCheckBox.setObjectName("visualizeDataCheckBox")
        self.verticalLayout_4.addWidget(self.visualizeDataCheckBox)

        self.getScorePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.getScorePushButton.setStyleSheet(
            """
            border-width: 5px;
            border-color: #000000;
            border-radius: 5px;
            background: #DD5353;
            color: #FEFEFE;
            padding: 10px 20px;
            font-size: 12px;
            font-weight: bold;
            """
        )
        self.getScorePushButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.getScorePushButton.sizePolicy().hasHeightForWidth()
        )
        self.getScorePushButton.setSizePolicy(sizePolicy)
        self.getScorePushButton.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.getScorePushButton.setFont(font)
        self.getScorePushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.getScorePushButton.setObjectName("getScorePushButton")
        self.verticalLayout_4.addWidget(
            self.getScorePushButton, 0, QtCore.Qt.AlignHCenter
        )

        self.MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 809, 20))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        #####styling##### 
        #input feilds
        self.MainWindow.setStyleSheet(
            """            
            background-color: #5F8D4E;
            border-radius: 10px;
            color: #FFFFFF;
            font-family: Arial, Helvetica, sans-serif;
            """
        )
        self.patientIdField.setStyleSheet(
            """
            background-color: #FFFFFF;
            color: #282A3A;
            border-style: solid;
            border-width: 0.2px;
            border-radius: 2px;
            padding: 5px 5px;
            font-weight: bold;
            border color: #D6E4E5; 
            """
        )
        self.patientNameField.setStyleSheet(
            """
            background-color: #FFFFFF;
            color: #282A3A;
            border-style: solid;
            border-width: 0.2px;
            border-radius: 2px;
            padding: 5px 5px;
            font-weight: bold;
            border color: #D6E4E5; 
            """
        )
        self.patientAgeField.setStyleSheet(
            """
            background-color: #FFFFFF;
            color: #282A3A;
            border-style: solid;
            border-width: 0.2px;
            border-radius: 2px;
            padding: 5px 5px;
            font-weight: bold;
            border color: #D6E4E5; 
            """
        )

        #exercise type combobox
        self.exerciseTypeComboBox.setStyleSheet(
            """
            background-color: #FFFFFF;
            color: #282A3A;
            border-style: solid;
            border-width: 0.2px;
            border-radius: 2px;
            padding: 2px 2px;
            font-weight: bold;
            border color: #D6E4E5; 
            """
        )

        # child inference window setup
        self.inferenceWindowContainer = QtWidgets.QMainWindow(
            parent=self.MainWindow  # need to set the parent as current window
        )

        # child record window setup
        self.recordWindowContainer = QtWidgets.QMainWindow()
        self.recordWindow = RecordWindow(self)
        self.recordWindow.setupUi(self.recordWindowContainer)

        self.inferenceWindow = InferenceWindow(self, self.recordWindow)
        self.inferenceWindow.setupUi(self.inferenceWindowContainer)

        self.exerciseDemoWindowContainer = QtWidgets.QMainWindow()
        self.exerciseDemoWindow = ExerciseDemoWindow(self.recordWindow)
        self.exerciseDemoWindow.setupUi(self.exerciseDemoWindowContainer)


        # combo box intialization
        self.exerciseTypeComboBox.addItems(
            ["Exercise Type {0}".format(i) for i in range(1, 6)]
        )

        # event handler for when live feed radio button is selected
        self.liveFeedRadioButton.toggled.connect(
            self.toggleSelectDataFileWidget
        )

        # event handler for choose data file button click
        self.specifyPathButton.clicked.connect(
            self.handleSpecifyPathButtonClick
        )

        # init form state
        self.state = dict()

        # event handler for get score button click
        self.getScorePushButton.clicked.connect(self.handleGetScoreButtonClick)

        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def show_error_messagebox():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
    
        # setting message for Message Box
        msg.setText("Please enter patient info to proceed")
        
        # setting Message box window title
        msg.setWindowTitle("Erorr Message")
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)
        
    def set_patient_info(self):
        temp_file = open("temp_patient_info_file.txt", "w")
        filename = self.patientIdField.text()+"_"+self.patientNameField.text()+"_"+self.patientAgeField.text()+"_"+self.exerciseTypeComboBox.currentText()
        print(filename)
        temp_file.write(filename)
        temp_file.close()

    def handleGetScoreButtonClick(self):
        if self.liveFeedRadioButton.isChecked()==True and self.msg3dRadioButton.isChecked()==True:
            self.state["datatype"] = None

            if self.kimoreRadioButton.isChecked():
                self.state["datatype"] = "kimore"
            elif self.liveFeedRadioButton.isChecked():
                self.state["datatype"] = "live-feed"
            elif self.labKinectRadioButton.isChecked():
                self.state["datatype"] = "lab-kinect-mat"

            self.state["modelType"] = None

            if self.msg3dRadioButton.isChecked():
                self.state["modelType"] = "msg3d"
            elif self.stgcnRadioButton.isChecked():
                self.state["modelType"] = "stgcn"

            self.state["exerciseType"] = self.exerciseTypeComboBox.currentText()
            self.state["shouldVisualize"] = self.visualizeDataCheckBox.isChecked()
            
            if self.liveFeedRadioButton.isChecked():
                # transfer current state to the record screen
                self.exerciseDemoWindow.set_state(self.state)
                self.exerciseDemoWindow.set_exercise_type(
                    self.state["exerciseType"]
                )
                
                #error check if patient info field is empty
                if self.patientIdField.text()!="" and self.patientNameField.text()!="" and self.patientAgeField.text()!="":
                    self.set_patient_info()
                    # cannot run pipeline here, need to show demo screen
                    self.MainWindow.hide()
                    self.exerciseDemoWindowContainer.show()
                else:
                    self.msg = QMessageBox()
                    self.msg.setIcon(QMessageBox.Critical)
        
                    # setting message for Message Box
                    self.msg.setText("Please enter patient info to proceed.")
                    
                    # setting Message box window title
                    self.msg.setWindowTitle("Erorr Message")
                    
                    # declaring buttons on Message Box
                    self.msg.setStandardButtons(QMessageBox.Ok)
                    self.msg.show() 
            else:
                # the business logic class
                pipeline = Pipeline()
                result = pipeline.run(**self.state)
                animation, scores = result
                # keep the animation in a persistent variable otherwise it won't play
                self.animation = animation
                # scores is a 2D tensor -> [[CF, PO]]
                scores = scores.cpu().numpy()

                self.inferenceWindow.set_data_type(self.state["datatype"])
                self.inferenceWindow.set_exercise_type(self.state["exerciseType"])
                self.inferenceWindow.set_score_and_suggestions_label(scores)
                self.MainWindow.hide()
                self.inferenceWindowContainer.show()
        else:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
        
            # setting message for Message Box
            self.msg.setText("Please select 'Live Feed' and 'MSG3D' to proceed.")
                    
            # setting Message box window title
            self.msg.setWindowTitle("Erorr Message")
                    
            # declaring buttons on Message Box
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show() 

    def handleSpecifyPathButtonClick(self):
        caption = "Choose the data files"
        filetypes = "Custom files (*.*)"

        if self.kimoreRadioButton.isChecked():
            caption = "Choose the .skeleton/.npy/.npz files"
            filetypes = "Skeleton files (*.skeleton);;Numpy Files (*.npy)"
        elif self.labKinectRadioButton.isChecked():
            caption = "Choose the lab kinect MAT files (.mat files)"
            filetypes = "MAT files (*.mat)"

        filename = QFileDialog.getOpenFileName(
            self.centralwidget, caption, ".", filetypes
        )
        self.state["selectedDataFile"] = filename[0]

    def toggleSelectDataFileWidget(self):
        if not self.liveFeedRadioButton.isChecked():
            self.selectDataFileWidget.setDisabled(False)
            self.specifyPathButton.setStyleSheet(
                """
                border-width: 5px;
                border-color: #000000;
                border-radius: 5px;
                background: #DD5353;
                color: #FEFEFE;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                """
            )

        else:
            self.selectDataFileWidget.setDisabled(True)
            self.specifyPathButton.setStyleSheet(
                """
                border-width: 5px;
                border-color: #000000;
                border-radius: 5px;
                background: #575757;
                color: #FEFEFE;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                """
            )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Intelligent Rehabilitation Assistant")
        )
        self.dataTypeLabel.setText(
            _translate("MainWindow", "Choose the type of data")
        )
        self.liveFeedRadioButton.setText(_translate("MainWindow", "Live Feed"))
        self.kimoreRadioButton.setText(_translate("MainWindow", "Kimore"))
        self.labKinectRadioButton.setText(
            _translate("MainWindow", "Lab Kinect (MAT format)")
        )
        self.modelTypeLabel.setText(
            _translate("MainWindow", "Choose the model to use for inference")
        )
        self.msg3dRadioButton.setText(_translate("MainWindow", "MSG3D"))
        self.stgcnRadioButton.setText(_translate("MainWindow", "STGCN"))
        self.exerciseTypeLabel.setText(
            _translate("MainWindow", "Choose the type of exercise")
        )
        self.visualizeDataCheckBox.setText(
            _translate("MainWindow", "Visualize data?")
        )
        self.getScorePushButton.setText(_translate("MainWindow", "Next"))
        self.specifyPathLabel.setText(
            _translate("MainWindow", "Specify the path to the data file")
        )
        self.specifyPathButton.setText(
            _translate("MainWindow", "Choose File...")
        )
        self.patientIdLabel.setText(_translate("MainWindow", "Patient ID"))
        self.patientNameLabel.setText(_translate("MainWindow", "Patient name"))
        self.patientAgeLabel.setText(_translate("MainWindow", "Patient age"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = FormWindow(None)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
