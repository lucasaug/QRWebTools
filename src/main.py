import base64

from io import BytesIO

import qrcode

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_code", methods=["POST"])
def create_code():
    text = request.form["text"]
    if not text:
        return "<div></div>"

    pil_img = qrcode.make(text)

    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG')
    img_io.seek(0)

    base64_img = base64.b64encode(img_io.getvalue()).decode("utf-8")
    return f"""
        <img src='data:image/png;base64, {base64_img}'/>
        <button onclick=
            "window.location.assign('data:application/octet-stream;base64, {base64_img}');"
        >Download image</button>
    """
