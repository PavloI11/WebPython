#!/usr/bin/env python3
import cgi

# Встановлюємо заголовок для виводу
print("Content-type: text/html\n")

# Отримуємо дані з форми, які надіслані через POST
form = cgi.FieldStorage()

first_name = form.getvalue('first_name', 'Not specified')
last_name = form.getvalue('last_name', 'Not specified')
email = form.getvalue('email', 'Not specified')
gender = form.getvalue('gender', 'Not specified')
country = form.getvalue('country', 'Not specified')
subscribe = 'subscribe' in form

# Виводимо дані на сторінці результатів
print(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Form Results</title>
</head>
<body>
    <h1>Form Results:</h1>
    <p><strong>First Name:</strong> {first_name}</p>
    <p><strong>Last Name:</strong> {last_name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Gender:</strong> {gender}</p>
    <p><strong>Country:</strong> {country}</p>
    <p><strong>Subscribe to Newsletter:</strong> {subscribe}</p>
    <p><a href="/your_form_page.html">Back to Form</a></p>
</body>
</html>
""")
