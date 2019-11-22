import base64

image_file = 'history_graph.png'
html_path = '/var/www/html/index.nginx-debian.html'

with open(image_file, 'rb') as image:
    data_uri = base64.b64encode(image.read()).decode('utf-8')

img_tag = f"""<img src="data:image/png;base64,{data_uri}">"""
head = """<head></head>"""
body = f"""<body>{img_tag}</body>"""
html_content = f"""<html>{head}{body}</html>"""
with open(html_path, 'w') as html_file:
    html_file.write(html_content)

if __name__ == "__main__":
    import webbrowser
    webbrowser.open(html_path)
