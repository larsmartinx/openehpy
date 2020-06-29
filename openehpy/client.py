import requests
import pandas

class server_connection:
    def __init__(self, EHRStoreURL, responseEncoding = 'utf-8-sig',headers = None, verifySSLConnection = True):
        self.EHRStoreURL = EHRStoreURL
        self.responseEncoding = responseEncoding
        self.verifySSLConnection = verifySSLConnection
        self.headers = headers

    def query(self, query):
        response = requests.post(
          self.EHRStoreURL + '/openehr/v1/query/aql/',
          json = { 'q': query },
          verify = self.verifySSLConnection,
          headers = self.headers
          )
        response.encoding = self.responseEncoding
        return self.ResultsetAsDataFrame(response.json()) if response.ok else response

    def ResultsetAsDataFrame(self, resultset):
        columnNames = []
        for column in resultset['columns']:
            columnNames.append(column['name'])
        return pandas.DataFrame(resultset['rows'], columns=columnNames) if 'rows' in resultset else resultset