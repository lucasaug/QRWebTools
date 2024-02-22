import base64
import struct
import uuid

from io import BytesIO

import qrcode

from qrcode.image.styledpil import StyledPilImage

from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer

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

    fg_color_hex = request.form["fg-color"][1:]
    bg_color_hex = request.form["bg-color"][1:]

    fg_color = struct.unpack("BBB", bytes.fromhex(fg_color_hex))
    bg_color = struct.unpack("BBB", bytes.fromhex(bg_color_hex))
    print(fg_color)
    print(bg_color)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    pil_img = qr.make_image(fill_color="red", back_color="purple")

    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG')
    img_io.seek(0)

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
