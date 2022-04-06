# One of my favourite websites to go to when I'm designing anything
# is a colour palette website called Flat UI Colors.
# It's a really simple static website that shows a bunch of colours and
# their HEX codes. I can copy the HEX codes and use it in my CSS or any design software.
# On day 76, you learnt about image processing with NumPy. Using this knowledge
# and your developer skills (that means Googling), build a website where a user
# can upload an image and you will tell them what are the top 10 most common colours in that image.
# This is a good example of this functionality:
# copy to clipboard
# https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
# find color
# https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image
# https://towardsdatascience.com/color-identification-in-images-machine-learning-application-b26e770c4c71
import os
import smtplib

import numpy as np
from flask import Flask, render_template, request, url_for
from flask.cli import load_dotenv
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename, redirect
from form import ImageForm, ContactForm
from colorthief import ColorThief
from PIL import Image  # for reading image files

load_dotenv(".env")
email = os.environ.get("email")
password = os.environ.get("password")
sent_email = os.environ.get("sent_email")
SECRET_KEY = os.urandom(32)


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["IMAGE_UPLOADS"] = 'static/img/'
Bootstrap(app)


@app.route("/", methods=["POST", "GET"])
def home():
    colors_example = ['#c3b6b7', '#9f1817', '#995f42', '#a97162', '#565a5d']
    form = ImageForm()
    if form.validate_on_submit():
        all_colors = []
        img = form.image.data
        img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))
        filename = "img/" + secure_filename(img.filename)
        color_thief = ColorThief(img)
        palette = color_thief.get_palette(color_count=5)
        for color in palette:
            all_colors.append((rgb_to_hex(color)))
        return redirect(url_for("color_page", imgcolor=all_colors, img=filename))
    return render_template("index.html", colors=colors_example, form=form)


@app.route("/colors")
def color_page():
    img = request.args.get("img")
    img_color = request.args.getlist("imgcolor")
    return render_template("colors.html", colors=img_color, img=img)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email, to_addrs=sent_email,
                                msg=f"Subject:Message from viewer from Color Palette - {request.form['title']}\n\nName: {request.form['name']}\n"
                                    f"Email: {request.form['email']}\n"
                                    f"Message: {request.form['comments']}")
        return render_template("contact.html", form=form, sent=True)
    return render_template("contact.html", form=form, sent=False)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
