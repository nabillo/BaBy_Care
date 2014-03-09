'''
Created on Mar 6, 2014

@author: nabillo
'''

from BaBy_Care import app
app.run(
		host="0.0.0.0",
		port=int(app.config['PORT']))
