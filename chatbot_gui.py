import tkinter as tk
from tkinter import scrolledtext

from chatbot import reply


def send_message() -> None:
    message = message_entry.get().strip()
    if not message:
        return

    conversation.configure(state="normal")
    conversation.insert(tk.END, f"\u0623\u0646\u062a: {message}\n", "user")
    conversation.insert(tk.END, f"Store: {reply(message)}\n\n", "bot")
    conversation.configure(state="disabled")
    conversation.see(tk.END)
    message_entry.delete(0, tk.END)

    if message.lower() in {"\u062e\u0631\u0648\u062c", "exit", "quit"}:
        window.after(500, window.destroy)


window = tk.Tk()
window.title("Store")
window.geometry("620x460+100+100")
window.minsize(480, 320)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

conversation = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    state="disabled",
    font=("Segoe UI", 13),
    padx=12,
    pady=12,
)
conversation.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
conversation.tag_configure("user", justify="right", foreground="#155eef")
conversation.tag_configure("bot", justify="right", foreground="#188038")

input_frame = tk.Frame(window)
input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
input_frame.columnconfigure(0, weight=1)

message_entry = tk.Entry(
    input_frame,
    justify="right",
    font=("Segoe UI", 13),
)
message_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
message_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(
    input_frame,
    text="\u0625\u0631\u0633\u0627\u0644",
    font=("Segoe UI", 11),
    command=send_message,
)
send_button.grid(row=0, column=1)

conversation.configure(state="normal")
conversation.insert(
    tk.END,
    "Store: \u0623\u0647\u0644\u0627 \u0628\u064a\u0643! \u0627\u0643\u062a\u0628 \u0631\u0633\u0627\u0644\u062a\u0643 \u0647\u0646\u0627.\n\n",
    "bot",
)
conversation.configure(state="disabled")
message_entry.focus_set()
window.after(100, message_entry.focus_force)

window.mainloop()
