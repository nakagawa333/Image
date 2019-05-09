from flask import Flask,render_template,request,send_file
from flask_sqlalchemy import SQLAlchemy
import secrets
from io import BytesIO
import urllib.request
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class FileContents(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	data = db.Column(db.LargeBinary) ##画像を保存

	def __repr__(self):
		return "FileContents(id = '{0}',name='{1}',data='{2}')".format(self.id,self.name,self.data)
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/upload",methods=["POST"])
def upload():
	file = request.files['inputFile']

	newfile = FileContents(name=file.filename,data=file.read())
	db.session.add(newfile)
	db.session.commit()
	return file.filename

def save_picture(form_picture):
	return "hello"

@app.route("/download")
def download():
	file_data = FileContents.query.filter_by(id=1).first()
	return send_file(BytesIO(file_data.data),attachment_filename="filename.pdf",as_attachment=True)

if __name__ == "__main__":
	app.run(debug=True)