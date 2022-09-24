import json
import requests

class Client:
    base_url = "https://api.withmono.com/issuing/v1"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response, error, status = "", "", ""

    def __init__(self, secret_key):
        self.headers['mono-sec-key'] = secret_key

    def _request(self, url, payload=None, method=None, base_url=None):        
        url = f'{(base_url or self.base_url)}{url}'
        
        if payload:
            payload = json.dumps(payload)

        try:
            if not method or method == "get":
                res = requests.get(url, headers=self.headers)
                return res.json()

            elif method.casefold() == "post":
                with requests.post(url, data=payload, headers=self.headers) as res:
                    return res.json()

            elif method.casefold() == "put":
                res = requests.put(url, json=payload, headers=self.headers)
                return res.json()

        except Exception as e:
            print(e)
            return e

    def create_holder(self, **kwargs):
        """ 
            Description: Create a user associated to your platform.
            Returns the ID of the created holder
            Params:
                entity: string(default: "INDIVIDUAL")
                first_name: string
                last_name: string
                bvn: string
                city: string
                state: string
                email: string
                address: String
                phone: string
        """

        bvn = kwargs.get('bvn')
        city = kwargs.get('city')
        state = kwargs.get('state')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        address = kwargs.get('address')
        country = kwargs.get('country')
        last_name = kwargs.get('last_name')
        first_name = kwargs.get('first_name')
        entity = kwargs.get('entity', "INDIVIDUAL")
        identity_type = kwargs.get('identity_type')
        identity_number = kwargs.get('identity_number')
        
        payload = {
            "first_name": first_name, 
            "last_name": last_name,
            "bvn": bvn,
            "phone": phone,
            "email": email,
            "entity": entity,
            "address": {
                "lga": city,
                "city": city,
                "state": state,
                "address_line1": address,
            },
        }
        
        # check required fields
        if not all([first_name, last_name, bvn, email, phone, state, city, address]):
            raise ValueError("first_name, last_name, bvn, email, phone, state, city, address are required fields.\n\thelp(client.create_holder) to view detail of required parameters")
        
        url = '/accountholders'
        res = self._request(url, payload=payload, method="post")
        return res

    def create_account(self, **kwargs):
        """
            Create bank account for a particular account holder
            Returns the ID of the created account
            params:
                holder_id: string
                virtual: boolean
                account_type: "deposit" or "collection". Default "deposit"
        """

        holder = kwargs.get('holder_id')
        virtual = kwargs.get('virtual', False)
        account_type = kwargs.get('account_type', 'deposit')

        url = "/bankaccounts" if not virtual else "/virtualaccounts"
        if not holder: raise ValueError("holder_id param is required")
        payload = {"account_holder": holder, "account_type": account_type}

        res = self._request(url, payload=payload, method="post")
        return res
    
    def get_account(self, **kwargs):
        """
            Get detail of a particular bank account.
            Returns a dictionary containing the bank account detail
            params:
                account_id: string
        """

        virtual = kwargs.get('virtual', False)
        account_id = kwargs.get('account_id')

        if not account_id: raise ValueError("account_id is required")

        url = f'/bankaccounts/{account_id}' if not virtual else f'/virtualaccounts/{account_id}'
        res = self._request(url)
        if res.get('status') == 'successful':
            return res['data']

        return res
    
    def get_banks(self):
        """ Return list of all banks """

        url = '/misc/banks'
        return self._request(url, base_url='https://api.withmono.com/v1')

    def get_account_name(self, **kwargs):
        """
            Enquire for names associated with a particular bank account.
            Params:
                bank_code: string
                account_number: string
        """

        bank_code = kwargs.get('bank_code')
        account_number = kwargs.get('account_number')

        if not all([account_number, bank_code]): raise ValueError('bank_code and account_number are required')
        
        url = '/misc/verify/account'
        payload = {
            "bank_code": bank_code,
            "account_number": account_number,
        }
        
        return self._request(url, payload=payload, method='post', base_url='https://api.withmono.com/v1')


    def transfer_internal(self, **kwargs):
        """
            Transfer funds from one bank account to another using issued account_id

            Params:
                amount: string
                from_account_id: string
                to_account_id: string
                reference: string
                narration: string
                meta: key value pair of custom object. e.g {"my_reference": "12345"}

        """

        meta = kwargs.get('meta')
        amount = kwargs.get('amount')
        narration = kwargs.get('narration')
        reference = kwargs.get('reference')
        to_account_id = kwargs.get('to_account_id')
        from_account_id = kwargs.get('from_account_id')

        if not all([amount, narration, reference, to_account_id, from_account_id]):
            raise ValueError('amount, narration, reference, to_account_id, from_account_id are required fields')

        payload = {
            "meta": meta,
            "amount": amount,
            "narration": narration,
            "reference": reference,
            "account_id": to_account_id,
        }

        url = f'/bankaccounts/{from_account_id}/transfer'
        return self._request(url, payload=payload, method='post')
    

    def transfer(self, **kwargs):
        """
            Transfer funds from one bank account to another via the beneficiary bank account number and bank code.

            Params:
                amount: string
                to_bank_code: string -> This field expects the beneficiary bank code
                from_account_id: string
                to_account_number: string -> Beneficiary account number
                to_account_id: string
                reference: string
                narration: string
                meta: key value pair of custom object. e.g {"my_reference": "12345"}

        """

        meta = kwargs.get('meta')
        amount = kwargs.get('amount')
        narration = kwargs.get('narration')
        reference = kwargs.get('reference')
        to_bank_code = kwargs.get('to_bank_code')
        to_account_id = kwargs.get('to_account_id')
        from_account_id = kwargs.get('from_account_id')
        to_account_number = kwargs.get('to_account_number')

        if not all([amount, narration, reference, to_bank_code, to_account_number]):
            raise ValueError('amount, narration, reference, to_account_id, from_account_id are required fields')

        payload = {
            "meta": meta,
            "amount": str(amount),
            "narration": narration,
            "reference": reference,
            "bank_code": to_bank_code,
            "account_number": to_account_number,
        }

        url = f'/bankaccounts/{from_account_id}/transfer'
        return self._request(url, payload=payload, method='post')
