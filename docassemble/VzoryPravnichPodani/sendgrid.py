# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from docassemble.base.util import get_config
import sendgrid
import json


def odeslat_email (email,nazev):
    sg = SendGridAPIClient(get_config('ecomailKey'))
    data = {
      "personalizations": [
        {
          "to": [
            {
              "email": email
            }
          ],
          "subject": ""
        }
      ],
      "template_id": "d66b9437-1c63-4167-aed6-f30c65d09a02",

      "from": {
        "email": "servis@frankbold.com"
      },
      "content": [
        {
          "type": "text/plain",
          "value": ""
        }
      ],
      "custom_args": [
       {
        "title":  "Vzor – "+nazev
       }
      ]
    }
    response = sg.client.mail.send.post(request_body=data)
    return
