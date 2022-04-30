import json
import uuid
import requests
from fastapi import HTTPException, status
from core.config import settings


class WiseService:
    def __init__(self) -> None:
        self.base_url = settings.WISE_BASE_URL
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.WISE_ACCESS_TOKEN}'
        }
        self.profile_id = self.__get_profile_id()

    def __get_profile_id(self) -> str:
        url = self.base_url + "/v1/profiles"
        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 200:
            response = response.json()[0]
            return response["id"]
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Payment provider is not available at the moment")

    def create_quote(self, amount: float):
        url = self.base_url + "/v2/quotes"
        body = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "sourceAmount": amount,
            "profile": self.profile_id
        }
        response = requests.post(url=url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            response = response.json()
            return response["id"]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Payment provider is not available at the moment")

    def create_recipient_account(self, fullname, iban):
        url = self.base_url + "/v1/accounts"
        body = {
            "currency": "EUR",
            "type": "iban",
            "profile": self.profile_id,
            "accountHolderName": fullname,
            "legalType": "PRIVATE",
            "details": {
                "iban": iban
            }
        }
        response = requests.post(url=url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            response = response.json()
            return response["id"]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Payment provider is not available at the moment")

    def create_transfer(self, recipient_id, quote_id):
        url = self.base_url + "/v1/transfers"
        transaction_id = str(uuid.uuid4())
        body = {
            "targetAccount": recipient_id,
            "quoteUuid": quote_id,
            "customerTransactionId": transaction_id,
        }
        response = requests.post(url=url, headers=self.headers, data=json.dumps(body))
        print(response.text, "#"*20, body)
        if response.status_code == 200:
            response = response.json()
            return response["id"]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Payment provider is not available at the moment")

    def fund_transfer(self, transfer_id):
        url = self.base_url + f"/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        body = {
            "type": "BALANCE"
        }
        response = requests.post(url=url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 201:
            response = response.json()
            return response
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Payment provider is not available at the moment")

    def cancel_funds(self, transfer_id):
        url = self.base_url + f"/v1/transfers/{transfer_id}/cancel"
        response = requests.put(url=url, headers=self.headers)

        if response.status_code == 200:
            response = response.json()
            return response["id"]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Payment provider is not available at the moment")
