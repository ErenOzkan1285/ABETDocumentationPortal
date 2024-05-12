import os
import pytest
import pandas as pd
from flaskbitirme import app

class TestFileUpload:
    @classmethod
    def setup_class(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_upload_excel_file_unauthorized(self):
        file_path = os.path.join(os.path.dirname(__file__), 'samplerecords-odtuclass.xlsx')
        with open(file_path, 'rb') as excel_file:
            response = self.client.post('/upload', data={'file': (excel_file, 'samplerecords-odtuclass.xlsx')})
            assert response.status_code == 401, "Unauthorized"

    def test_upload_excel_file_authorized(self):
        file_path_excel = os.path.join(os.path.dirname(__file__), 'samplerecords-odtuclass.xlsx')
        
        with self.client.session_transaction() as session:
            # Simulate login
            response1 = self.client.post("/", data={"email": 'me@metu.edu.tr', "password": '1234'})
            assert response1.status_code == 302, "Logged in and redirected."

            # Upload Excel file
            with open(file_path_excel, 'rb') as excel_file:
                response2 = self.client.post('/upload', data={'file': (excel_file, 'samplerecords-odtuclass.xlsx')})
                assert response2.status_code == 200, "Excel file upload successfull."
    
    def test_upload_non_excel_file_authorized(self):
        file_path_pdf = os.path.join(os.path.dirname(__file__), 'test.pdf')

        with self.client.session_transaction() as session:
            # Simulate login
            response1 = self.client.post("/", data={"email": 'me@metu.edu.tr', "password": '1234'})
            assert response1.status_code == 302, "Logged in and redirected."

            # Upload PDF file (non-Excel)
            with open(file_path_pdf, 'rb') as pdf_file:
                response3 = self.client.post('/upload', data={'file': (pdf_file, 'test.pdf')})
                assert response3.status_code == 400 , "PDF file is not supported."
                

    

if __name__ == '__main__':
    pytest.main()
