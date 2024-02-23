import base64
import struct
import uuid

from io import BytesIO

import segno

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

    fg_color_hex = request.form["fg-color"]
    bg_color_hex = request.form["bg-color"]

    img_io = BytesIO()
    qrcode = segno.make_qr(text)
    qrcode.save(
        img_io,
        dark=fg_color_hex,
        light=bg_color_hex,
        kind="png",
        scale=5
    )

    base64_img = base64.b64encode(img_io.getvalue()).decode("utf-8")
    data_attr = f"data:application/octet-stream;base64,{base64_img}"

    return f"""
        <img src='data:image/png;base64, {base64_img}'/>
        <a id="button"
            download="{str(uuid.uuid4())}.jpg"
            href="{data_attr}">
            Download image
        </a>
    """
