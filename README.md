# The Unofficial python wrapper around mono.co APIs

Mono helps businesses to access high-quality financial data and direct bank payments, with this package you can have a pythonic access to mono's APIs.

## Getting Started

### Installation

```bash
    pip install mono_client
```

### Setup, Inialize the package using your mono test or live secret_key

```python
    from mono_client import Client
    client = Client(secret_key='secret')
```

### Usage

#### Now, lets create an account holder, then generate a bank account for our user and transfer funds.

- Create an account holder on mono

```python
    res = client.create_holder(
        bvn='12345',
        city='Abuja',
        state='Abuja',
        last_name='Doe',
        first_name='Jane',
        phone='+2347000000000',
        email='mail@abdull.dev',
        address='Abuja, Nigeria',
    )

    # example response

    {
        "status": "success",
        "message": "Account holder created successfully",
        "data": {
            "id": "61a73645c2d313658ce82d44"
        }
    }
```

#### We have holder, now lets generate a bank account for our user.

- Create a bank account

pass the parameter `virtual=True` to make a virtual bank account.

```python
    res = client.create_account(holder_id='61a73645c2d313658ce82d44', virtual=True)

    # example response
    {
        "status": "successful",
        "message": "Virtual account generation is processing",
        "data": {
            "id": "62decea1063a19fcba1234"
        }
    }
```

At this point you should be able to transfer money to this account (if you used live credentials in the setup).

#### Transfer funds from one user account to another (internal)

- Internal Transfer

```python
    res = client.transfer_internal(
        amount='1000',
        reference='reference',
        narration='funds transfer',
        to_account_id='62decea1063a19fcba1234',
        from_account_id='54decea1063a19fcba2434',
        meta={"my_reference": "12345"}, # optional dict. e.g {"my_reference": "12345"}
    )

    # example response
    {
        "status": "successful",
        "message": "Transfer is processing",
        "data": {
            "id": "62f0c405dcf59e51e408daf9"
        }
    }
```

#### Transfer funds from user account to an external bank account

- Transfer

```python
    res = client.transfer(
        amount='1000',
        narration='narration',
        reference='reference',
        from_account_id='62decea1063a19fcba1234',
        to_bank_code='211', # bank code, e.g Stanbic IBTC is 211
        to_account_number='0000000000', # Account number for the stated bank_code
        meta={"my_reference": "12345"}, # optional dict. e.g {"my_reference": "12345"}
    )

    # example response
    {
        "status": "successful",
        "message": "Transfer is processing",
        "data": {
            "id": "62f0c405dcf59e51e408daf9"
        }
    }
```

#### Retrieve a bank account

- Get Account detail

```python
    res = client.get_account(account_id=account_id, virtual=True)
```

#### Get list of banks

- Retrieve banks

```python
    res = client.get_banks()

    # example response
    {
        "status": "successful",
        "data": [
            {
                "name": "Access Bank",
                "code": "044"
            },
            {
                "name": "Citi Bank",
                "code": "023"
            }
            ...
            ...
        ]
    }
```

#### Docs

##### Learn how to use each function

```python
    help(client.transfer)
```

##### View all available functions

```python
    dir(client)
```

## Authors

Abdulrasheed Ibrahim
[@CodePharaoh](https://twitter.com/Aiibrahim3)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
