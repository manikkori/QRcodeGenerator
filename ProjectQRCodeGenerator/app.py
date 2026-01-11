# import qrcode as qr

# img = qr.make("www.instagram.com/yourprofile")

# img.save("instaprofile.png")

from flask import Flask, render_template, request, jsonify
import qrcode
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.json
    # Ab hum 'text' expect kar rahe hain, sirf URL nahi
    text_content = data.get('text')

    if not text_content:
        return jsonify({'error': 'Please enter some text'}), 400

    # QR Code Generate karna
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text_content)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Image processing (Memory buffer)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return jsonify({'image': img_base64})

if __name__ == '__main__':
    app.run(debug=True)