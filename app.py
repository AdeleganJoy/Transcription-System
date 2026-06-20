from flask import Flask, render_template, request, send_file
import whisper
import os

model = whisper.load_model("turbo")

def transcription(file_path):
    return model.transcribe(file_path)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])  
def transcribe():  
    if request.method == 'POST': 
        file = request.files['file']
        
        if file.filename != '':
            temp_path = os.path.join("/tmp", file.filename)
            file.save(temp_path)
            
            content = transcription(temp_path)
            
            output_filename = "transcription.txt"
            with open(output_filename, "w", encoding="utf-8") as f1:
                f1.write(content["text"])
            
            os.remove(temp_path)
            
            return send_file(
                output_filename,
                as_attachment=True,
                download_name="transcription.txt"
            )
            
    return "No file was uploaded or request failed.", 400

if __name__ == "__main__":
    app.run(debug=True)


