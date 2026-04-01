from flask import Flask, render_template, request
import qrcode
import io
import base64
import urllib.parse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code_b64 = None
    
    if request.method == 'POST':
        raw_text = request.form.get('data')
        
        if raw_text:
            safe_text = urllib.parse.quote(raw_text)
            
            # This automatically detects your live PythonAnywhere URL!
            qr_data = f"{request.host_url}view?msg={safe_text}"
            
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buf = io.BytesIO()
            img.save(buf, format='PNG')
            image_stream = buf.getvalue()
            qr_code_b64 = base64.b64encode(image_stream).decode('utf-8')

    return render_template('index.html', qr_code=qr_code_b64)

@app.route('/view')
def view_message():
    scanned_message = request.args.get('msg', 'No message found.')
    return render_template('view.html', message=scanned_message)

if __name__ == '__main__':
    app.run(debug=True)