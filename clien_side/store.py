from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox,QFileDialog
from PyQt5.uic import loadUi
import sys,cv2,os,base64,json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests
import numpy as np
class Store(QMainWindow):
    global file_name
    file_name = None
    global list_for_tag
    list_for_tag=[]
    
    def __init__(self):
        global addr
        super().__init__()
        loadUi(r"Menu.ui", self)
        self.show_tags=''
        self.submit.clicked.connect(self.create_store)
        # self.tags.textChanged.connect(self.onChanged)
        self.tags.returnPressed.connect(self.onChanged)
        self.upload.clicked.connect(self.upload_logo)
        self.delete_2.clicked.connect(self.delete)
        self.getlist.clicked.connect(self.get_list_data)
    def get_list_data(self):
    	name=self.Name.text()
    	if len(name)==0:
    		self.name_check.show()
    		self.name_check.setText('required*')
    	else:
    		self.name_check.hide()
    		api_data_json_form = {
	            "name": name,
	            }
    		addr ="http://127.0.0.1:8000/"
	    	test_url = addr + "GetStorelist/"
	    	api_data_encoded = urlencode(api_data_json_form).encode("utf-8")
	    	responce_from_server = requests.get(url=test_url, params=api_data_encoded)
	    	responce_json = responce_from_server.json()
	    	buffer = base64.b64decode(responce_json["img"].encode("utf-8"))
	    	img_org = np.frombuffer(buffer, dtype=np.uint8).reshape(responce_json["shape"])
	    	print(responce_json["data"])
	    	cv2.imshow('logo',img_org)
	    	cv2.waitKey(0)
	    	self.Name.setText('')
    def delete(self):
    	name=self.Name.text()
    	if len(name)==0:
    		self.name_check.show()
    		self.name_check.setText('required*')
    	else:
    		self.name_check.hide()
    		api_data_json_form = {
	            "name": name,
	            }
    		addr ="http://127.0.0.1:8000/"
	    	test_url = addr + "DeleteStore/"
	    	api_data_encoded = urlencode(api_data_json_form).encode("utf-8")
	    	responce_from_server = Request(test_url, api_data_encoded)
	    	responce_from_server = urlopen(responce_from_server)
	    	responce_decode = responce_from_server.read().decode("utf-8")
	    	responce_json_form = json.loads(responce_decode)
	    	print(responce_json_form)
	    	self.Name.setText('')

    def onChanged(self):
    	if self.tags!='':
    		if len(list_for_tag)<4:
    			self.tags_check.hide()
	    		self.show_tags=str(self.show_tags)+ ' '+str(self.tags.text())
		    	list_for_tag.append(self.tags.text())
		    	self.tags.setText('')
		    	self.tags_list.setText(self.show_tags)
    		elif len(list_for_tag)==0:
		    	self.tags_check.show()
		    	self.tags_check.setText('required*')
    def upload_logo(self):
                options = QFileDialog.Options()
                self.file_name_select, _ = QFileDialog.getOpenFileName(
                    self,
                    "QFileDialog.getOpenFileName()",
                    "",
                    "Images (*.png *.jpeg *.jpg",
                    options=options,
                )

                if self.file_name_select != "":
                    self.logo_image = cv2.imread(self.file_name_select)
                    self.logo_name = os.path.split(self.file_name_select)[-1]
                    self.file_.setText(self.logo_name)
    def create_store(self):
    	global list_for_tag
    	name=self.Name.text()
    	description=self.description.toPlainText()

    	# tags=self.tags.text()
    	if len(name)>20:
    		self.name_check.show()
    		self.name_check.setText('name required upto 20 character')
    	elif len(name)==0:
    		self.name_check.show()
    		self.name_check.setText('required*')
    	elif self.file_.text()=="":
    		self.name_check.hide()
	    	self.file_.setText('required*')
    	elif len(list_for_tag)==0:
	    	self.name_check.hide()
	    	# self.file_.hide()
    		self.tags_list.setText('required')
    	else:
    		self.file_.show()
    		self.name_check.hide()
	    	# self.name_check.hide()
	    	img_b64 = base64.b64encode(self.logo_image)
	    	api_data_json_form = {
	            "logo": img_b64,
	            "shape": self.logo_image.shape,
	            "name": name,
	            "description":description,
	            'tags':self.show_tags
	            }
	    	addr ="http://127.0.0.1:8000/"
	    	test_url = addr + "CreateStore/"
	    	api_data_encoded = urlencode(api_data_json_form).encode("utf-8")
	    	responce_from_server = Request(test_url, api_data_encoded)
	    	responce_from_server = urlopen(responce_from_server)
	    	responce_decode = responce_from_server.read().decode("utf-8")
	    	responce_json_form = json.loads(responce_decode)
	    	self.Name.setText('')
	    	self.description.setPlainText('')
	    	self.file_.setText('')
	    	self.tags_list=''
	    	list_for_tag=[]
	    	
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Store()
    widget.show()
    sys.exit(app.exec_())