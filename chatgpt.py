import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
import openai
openai.api_key = "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"

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

        # Create temperature and max tokens input boxes
        self.temperature_input = QLineEdit("0.7")
        self.temperature_input.setFixedWidth(100)
        self.temperature_label = QLabel("Temperature:")

        self.max_tokens_input = QLineEdit("100")
        self.max_tokens_input.setFixedWidth(100)
        self.max_tokens_label = QLabel("Max Tokens:")

        # Set up layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.chatlog)

        hbox = QHBoxLayout()
        hbox.addWidget(self.temperature_label)
        hbox.addWidget(self.temperature_input)
        hbox.addWidget(self.max_tokens_label)
        hbox.addWidget(self.max_tokens_input)

        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.inputbox)
        hbox.addWidget(self.sendbutton)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # Set up OpenAI API
        self.engine = "davinci"
        self.max_tokens = 100
        self.temperature = 0.7

    def send_message(self):
        # Get user input
        message = self.inputbox.text().strip()
        self.inputbox.clear()

        # Get temperature and max tokens values from input boxes
        self.temperature = float(self.temperature_input.text())
        self.max_tokens = int(self.max_tokens_input.text())

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
    chatbot.setWindowTitle('Chatbot')
    chatbot.setGeometry(100, 100, 800, 600)
    chatbot.show()

    # Run QApplication event loop
    sys.exit(app.exec_())
