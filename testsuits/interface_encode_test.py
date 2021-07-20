import requests
import json
import base64


def test_load_json():
    with open('demo.json') as f:
        s = json.load(f)
        print(s)


class APIRequest:
    def __init__(self):
        self.my_request = {
            "url": "http://localhost:9999/demo1.txt",
            "method": "GET",
            "headers": None,
            "endcode": "base64"
        }

    def test_send(self):
        self.response = requests.request("GET", self.my_request["url"],
                                    headers=self.my_request["headers"])
        res = base64.b64decode(self.response.text)
        print(res, type(res))
        return json.loads(res)


if __name__ == '__main__':
    test_load_json()
    # print(APIRequest().test_send())
