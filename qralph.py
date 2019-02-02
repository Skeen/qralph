import os
import sys
import requests
from flask import Flask
app = Flask(__name__)

ralph_conf = {}

def required_option(varname, default=None):
    value = os.environ.get(varname, default)
    if value is None:
        app.logger.critical('Required variable not set! (%s)', varname)
        sys.exit(1)
    ralph_conf[varname] = value

required_option('RALPH_URL')
required_option('RALPH_USERNAME', 'ralph')
required_option('RALPH_PASSWORD', 'ralph')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get-token')
def get_token():
    # Authentification:
    #    curl -H "Content-Type: application/json" -X POST https://<YOUR-RALPH-URL>/api-token-auth/ -d '{"username": "<YOUR-USERNAME>", "password": "<YOUR-PASSWORD>"}'
    #    {"token":"79ee13720dbf474399dde532daad558aaeb131c3"}
    url = ralph_conf['RALPH_URL'] + "/api-token-auth/"
    payload = {
        "username": ralph_conf['RALPH_USERNAME'],
        "password": ralph_conf['RALPH_PASSWORD'],
    }
    response = requests.post(url, json=payload)
    return response.text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

#
#
#
#Lookup asset:
#    http://localhost/api/back-office-assets/?sn=QR-1
#    Check 'count'
#
#Add asset:
#    POST http://localhost/api/back-office-assets/
#
#    Error on non-unique sn
#
#    {
#        "tags": "",
#        "remarks": "",
#        "hostname": "",
#        "sn": "QR-3",
#        "barcode": "",
#        "niw": "",
#        "required_support": false,
#        "order_no": "",
#        "invoice_no": "",
#        "invoice_date": null,
#        "price": null,
#        "provider": "",
#        "depreciation_rate": 0,
#        "force_depreciation": false,
#        "depreciation_end_date": null,
#        "buyout_date": null,
#        "task_url": "",
#        "location": "",
#        "purchase_order": "",
#        "loan_end_date": null,
#        "status": 1,
#        "imei": "",
#        "parent": null,
#        "service_env": null,
#        "configuration_path": null,
#        "model": 1,
#        "budget_info": null,
#        "property_of": null,
#        "region": 1,
#        "warehouse": 1,
#        "owner": null,
#        "user": null,
#        "office_infrastructure": null
#    }
