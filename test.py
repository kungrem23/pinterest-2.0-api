import smtplib


print('start')
email = 'tekhno.strelka@mail.ru'
password = 'cCeTMHz7BTvLefbJcJ2K'
smtp_server = 'smtp.mail.ru'
smtp_port = 465
server = smtplib.SMTP_SSL(smtp_server, smtp_port)
# server.starttls()
server.login(email, password)
recipient = 'demabrothers@gmail.com'
server.sendmail(email, recipient, 'Subject: test\ntest bebra email')
server.quit()
print('finish')