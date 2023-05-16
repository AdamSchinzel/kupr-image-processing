from flask import Flask, request
import os 

import analyze

app = Flask(__name__)
base_dir = os.path.dirname(os.path.realpath(__file__))

@app.route('/analyze', methods=['POST'])
def upload_file():
  f = request.files['file']  
  filename1 = base_dir + '/uploads/uploaded_file.jpg'
  filename2 = base_dir + '/images/' + request.values['ref']
  if not os.path.exists(filename2):
    return { 'error': 'ref not found' }
  f.save(filename1)
  match = analyze.analyze(filename1, filename2)
  return { 'match': match }
  
