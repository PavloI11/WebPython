#!/usr/bin/env python3
import cgi

print("Content-type: text/html\n")

form = cgi.FieldStorage()

field1 = form.getvalue('field1', 'Not specified')
field2 = form.getvalue('field2', 'Not specified')
checkbox1 = 'checkbox1' in form
checkbox2 = 'checkbox2' in form
dropdown = form.getvalue('dropdown', 'Not selected')
radio = form.getvalue('radio', 'Not selected')

print("""
<!DOCTYPE html>
<html>
<head>
    <title>Form Results</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>Form Results:</h1>
        <div class="result">
            <strong>First field (input):</strong> {field1}
        </div>
        <div class="result">
            <strong>Second field (input):</strong> {field2}
        </div>
        <div class="result">
            <strong>First checkbox:</strong> {'Selected' if checkbox1 else 'Not selected'}
        </div>
        <div class="result">
            <strong>Second checkbox:</strong> {'Selected' if checkbox2 else 'Not selected'}
        </div>
        <div class="result">
            <strong>Dropdown selection:</strong> {dropdown}
        </div>
        <div class="result">
            <strong>Radio selection:</strong> {radio}
        </div>
    </div>
</body>
</html>
""")
