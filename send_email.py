import tkinter as tk
import tkinter.filedialog  # 导入filedialog子模块
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders 
import smtplib

# 创建GUI窗口
root = tk.Tk()
root.title("邮件发送工具")

# 创建发件人、收件人、主题、内容、附件的输入控件
tk.Label(root, text="发件人邮箱:").pack()
from_email_entry = tk.Entry(root)
from_email_entry.pack()

tk.Label(root, text="收件人邮箱:").pack()
to_email_entry = tk.Entry(root)
to_email_entry.pack()

tk.Label(root, text="主题:").pack()
subject_entry = tk.Entry(root)
subject_entry.pack()

tk.Label(root, text="邮件内容:").pack()
body_text = tk.Text(root, height=10, width=50)
body_text.pack()

tk.Label(root, text="附件文件路径:").pack()
attachment_entry = tk.Entry(root)
attachment_entry.pack()


tk.Label(root, text="SMTP授权码:").pack()
password_entry = tk.Entry(root, show="*")  # 授权码以密码形式显示
password_entry.pack()


def browse_file():
    file_path = tk.filedialog.askopenfilename()
    attachment_entry.delete(0, tk.END)
    attachment_entry.insert(0, file_path)

def send_email():
    from_email = from_email_entry.get()
    to_email = to_email_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", "end-1c")
    attachment_path = attachment_entry.get()
    password = password_entry.get()

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        filename = attachment_path.split("/")[-1]
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)

    with smtplib.SMTP('smtp.qq.com', 587) as server:  # 替换为所使用的SMTP服务器地址和端口
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

    result_label.config(text="邮件发送成功")

# 创建“浏览”按钮
browse_button = tk.Button(root, text="浏览", command=browse_file)
browse_button.pack()

send_button = tk.Button(root, text="发送邮件", command=send_email)
send_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()