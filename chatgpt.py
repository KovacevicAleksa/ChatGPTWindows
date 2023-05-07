import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt
import openai
#!!!ADD YOUR API_KEY FREE FROM https://platform.openai.com/account/api-keys!!!
openai.api_key = "YOUR API_KEY"

class Chatbot(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create UI elements
        self.chatlog = QTextEdit()
        self.chatlog.setReadOnly(True)
        self.inputbox = QLineEdit()
        self.inputbox.returnPressed.connect(self.send_message)
        self.sendbutton = QPushButton("Send")
        self.sendbutton.clicked.connect(self.send_message)

        # Create temperature and max tokens input sliders
        self.temperature_slider = QSlider(Qt.Horizontal)
        self.temperature_slider.setMinimum(1)
        self.temperature_slider.setMaximum(100)
        self.temperature_slider.setTickPosition(QSlider.TicksBelow)
        self.temperature_slider.setTickInterval(5)
        self.temperature_slider.setValue(70)
        self.temperature_slider.valueChanged.connect(self.on_temperature_slider_value_changed)

        self.max_tokens_slider = QSlider(Qt.Horizontal)
        self.max_tokens_slider.setMinimum(1)
        self.max_tokens_slider.setMaximum(500)
        self.max_tokens_slider.setTickPosition(QSlider.TicksBelow)
        self.max_tokens_slider.setTickInterval(10)
        self.max_tokens_slider.setValue(100)
        self.max_tokens_slider.valueChanged.connect(self.on_max_tokens_slider_value_changed)

        # Create labels for sliders
        self.temperature_label = QLabel("Temperature: {:.2f}".format(self.temperature_slider.value() / 100))
        self.max_tokens_label = QLabel("Max Tokens: {}".format(self.max_tokens_slider.value()))

        # Set up layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.chatlog)

        hbox = QHBoxLayout()
        hbox.addWidget(self.temperature_label)
        hbox.addWidget(self.temperature_slider)
        hbox.addWidget(self.max_tokens_label)
        hbox.addWidget(self.max_tokens_slider)

        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.inputbox)
        hbox.addWidget(self.sendbutton)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # Set up OpenAI API
        self.engine = "davinci"
        self.max_tokens = self.max_tokens_slider.value()
        self.temperature = self.temperature_slider.value() / 100

    def on_temperature_slider_value_changed(self, value):
        self.temperature_label.setText("Temperature: {:.2f}".format(value / 100))
        self.temperature = value / 100

    def on_max_tokens_slider_value_changed(self, value):
        self.max_tokens_label.setText("Max Tokens: {}".format(value))
        self.max_tokens = value

    def send_message(self):
        # Get user input
        message = self.inputbox.text().strip()
        self.inputbox.clear()

        # Generate response from OpenAI API
        response = openai.Completion.create(
            engine=self.engine,
            prompt=message,
            max_tokens=self.max_tokens,
            n=1,
            stop=None,
            temperature=self.temperature
        )
        response_text = response.choices[0].text.strip()

        # Display response in chat log
        self.chatlog.append("You: " + message)
        self.chatlog.append("ChatGPT: " + response_text)

if __name__ == '__main__':
    # Create QApplication and Chatbot instance
    app = QApplication(sys.argv)
    chatbot = Chatbot()

    # Set window properties and show
    chatbot.setWindowTitle('CHATBOT V1.1.0')
    chatbot.setGeometry(100, 100, 800, 600)
    chatbot.show()

    # Run QApplication event loop
    sys.exit(app.exec_())
