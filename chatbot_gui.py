from rivescript import RiveScript
import tkinter as tk
from tkinter import scrolledtext, font, PhotoImage
import threading
import time
from tkinter import ttk
import random

class TypingAnimation:
    def __init__(self, callback):
        self.callback = callback
        self.active = False
        self.dots = 0

    def start(self):
        self.active = True
        self.animate()

    def stop(self):
        self.active = False

    def animate(self):
        if not self.active:
            return
        self.dots = (self.dots + 1) % 4
        typing_text = "Typing" + "." * self.dots
        self.callback(typing_text)
        self.window.after(400, self.animate)

class ChatbotGUI:
    def __init__(self, brain_dir="./brain"):
        self.bot = RiveScript()
        self.bot.load_directory(brain_dir)
        self.bot.sort_replies()

        self.typing_speed = 10  # Faster typing speed
        self.current_typing_message = ""
        self.typing_position = 0

        self.window = tk.Tk()
        self.window.title("🤖 Chellam - Smart Chatbot")
        self.window.geometry("800x850")
        self.window.minsize(500, 600)
        self.window.configure(bg="#e8eaf6")

        try:
            self.bot_avatar = PhotoImage(file="bot_avatar.png").subsample(4, 4)
            self.user_avatar = PhotoImage(file="user_avatar.png").subsample(4, 4)
        except:
            self.bot_avatar = PhotoImage(width=48, height=48)
            self.user_avatar = PhotoImage(width=48, height=48)

        self.setup_styles()
        self.setup_header()
        self.setup_chat_area()
        self.setup_input_area()
        self.setup_typing_indicator()

        self.typing_animation = TypingAnimation(self.update_typing_indicator)
        self.typing_animation.window = self.window

        self.display_message("Chellam", "Hello! I'm your smart assistant. How can I help you today? 😊", "bot")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Accent.TButton", background="#5e35b1", foreground="white", font=("Segoe UI", 11))
        style.map("Accent.TButton", background=[("active", "#7e57c2")])
        style.configure("Emoji.TButton", font=("Segoe UI Emoji", 14))

    def setup_header(self):
        header = tk.Frame(self.window, bg="#5e35b1", height=70)
        header.pack(fill=tk.X)
        tk.Label(header, text="Chellam AI Assistant", fg="white", bg="#5e35b1",
                 font=("Segoe UI", 18, "bold")).pack(side=tk.LEFT, padx=15)
        tk.Label(header, text="Online", fg="#a5d6a7", bg="#5e35b1",
                 font=("Segoe UI", 10)).pack(side=tk.RIGHT, padx=15)

    def setup_chat_area(self):
        self.chat_frame = tk.Frame(self.window, bg="#e8eaf6")
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, state='disabled', wrap=tk.WORD,
                                                   font=("Segoe UI", 12), bg="#e8eaf6", bd=0)
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        self.chat_area.tag_configure("user", background="#c5cae9", justify="right",
                                     lmargin1=100, lmargin2=20, rmargin=20, spacing3=10)
        self.chat_area.tag_configure("bot", background="#ffffff", justify="left",
                                     lmargin1=20, lmargin2=100, rmargin=20, spacing3=10)

    def setup_input_area(self):
        input_frame = tk.Frame(self.window, bg="#ffffff", padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        self.emoji_button = ttk.Button(input_frame, text="😊", command=self.add_emoji, style="Emoji.TButton")
        self.emoji_button.pack(side=tk.LEFT)

        self.entry = tk.Text(input_frame, height=3, font=("Segoe UI", 13), wrap=tk.WORD,
                             highlightbackground="#bdbdbd", highlightcolor="#5e35b1", highlightthickness=1)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ttk.Button(input_frame, text="Send", command=self.send_message, style="Accent.TButton")
        self.send_button.pack(side=tk.RIGHT)

    def setup_typing_indicator(self):
        self.typing_label = tk.Label(self.window, text="", font=("Segoe UI", 10, "italic"),
                                     fg="#757575", bg="#e8eaf6", anchor=tk.W)
        self.typing_label.pack(fill=tk.X, padx=20, pady=(0, 5))

    def update_typing_indicator(self, text):
        self.typing_label.config(text=text)

    def display_message(self, sender, message, sender_type="user"):
        self.chat_area.configure(state='normal')
        avatar = self.bot_avatar if sender_type == "bot" else self.user_avatar
        self.chat_area.image_create(tk.END, image=avatar)
        self.chat_area.insert(tk.END, "  ")

        if sender_type == "bot":
            self.current_typing_message = message
            self.typing_position = 0
            self.type_next_character()
        else:
            self.chat_area.insert(tk.END, f"{message}\n\n", (sender_type,))
            self.chat_area.configure(state='disabled')
            self.chat_area.see(tk.END)

    def type_next_character(self):
        if self.typing_position < len(self.current_typing_message):
            char = self.current_typing_message[self.typing_position]
            self.chat_area.insert(tk.END, char, ("bot",))
            self.chat_area.see(tk.END)
            self.typing_position += 1
            speed = max(5, self.typing_speed + random.randint(-3, 3))
            self.window.after(speed, self.type_next_character)
        else:
            self.chat_area.insert(tk.END, "\n\n")
            self.chat_area.configure(state='disabled')

    def add_emoji(self):
        emojis = ["😊", "😂", "❤️", "👍", "😍", "🙏", "🤔", "😎"]
        self.entry.insert(tk.END, random.choice(emojis))

    def send_message(self, event=None):
        if event and (event.state == 0 or event.keysym == "Return"):
            self._send_message()
            return "break"

    def _send_message(self):
        user_msg = self.entry.get("1.0", tk.END).strip()
        if not user_msg:
            return
        self.display_message("You", user_msg, "user")
        self.entry.delete("1.0", tk.END)

        if user_msg.lower() in ["quit", "exit", "bye"]:
            self.display_message("Chellam", "Goodbye! Take care 💐", "bot")
            self.window.after(1500, self.window.destroy)
            return

        self.typing_animation.start()
        threading.Thread(target=self.process_message, args=(user_msg,), daemon=True).start()

    def process_message(self, user_msg):
        time.sleep(0.5 + random.random())
        reply = self.bot.reply("localuser", user_msg)
        self.window.after(0, self.typing_animation.stop)
        self.window.after(0, self.update_typing_indicator, "")
        self.window.after(0, self.display_message, "Chellam", reply, "bot")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = ChatbotGUI()
    gui.run()
