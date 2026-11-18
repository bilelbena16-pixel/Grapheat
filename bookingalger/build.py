# Génère index.html (PWA) à partir de app.html
import pathlib
d = pathlib.Path(__file__).parent
body = (d / "app.html").read_text(encoding="utf-8")
head = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#F1F4F6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="BookingAlger">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="img/icon-192.png">
<link rel="apple-touch-icon" href="img/icon-180.png">
</head>
<body>
"""
(d / "index.html").write_text(head + body + "\n</body>\n</html>\n", encoding="utf-8")
print("index.html OK")
