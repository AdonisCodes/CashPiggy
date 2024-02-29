---
## Overview
CashPiggy is a Python package designed to provide easy access to CashPiggy's services through a set of classes and methods. CashPiggy is a platform that allows users to earn rewards by participating in surveys and referrals.

## Installation
You can install the CashPiggy package via pip. Open your terminal and run the following command:
```bash
pip install cashpiggy
```

## Usage

### Importing the Package
You can import the CashPiggy package in your Python script or interactive session using the following import statement:
```python
import cashpiggy
```

### Creating an Account
To create a CashPiggy account, you can use the `register` method of the `CashPiggyAccount` class:
This method returns a `CashPiggyAccount` object representing the newly created account. If the registration fails, it returns `None`.
```python
account = cashpiggy.CashPiggyAccount.register("your_email@example.com")
```

### Claiming Points
You can claim points using the `claim_points` method of the `CashPiggyAccount` class:
Note, that you should only claim 10 points per day, as that is the limit they give as a daily bonus. But you can experiment!
This method takes the number of points to claim as an argument and returns `True` if the claim is successful, otherwise `False`.
```python
success = account.claim_points(100)
```

### Cashout
To cash out your earnings, you can use the `cashout` method of the `CashPiggyAccount` class:
This method takes the cashout method (`CashPiggyCashoutMethod` enum) and the country code as arguments and returns `True` if the cashout is successful, otherwise `False`.
```python
success = account.cashout(cashpiggy.CashPiggyCashoutMethod.PAYPAL_5, "US")
```


### Getting Referrals
You can retrieve information about your referrals using the `get_referrals` method of the `CashPiggyAccount` class:
This method returns a `CashPiggyAccountReferrals` object containing information about your referrals.
```python
referrals = account.get_referrals()
```

### Becoming Referral
You can also become a referral to another account using the `become_referral` method of the `CashPiggyAccount` class:
This method returns a `Boolean` which will be true if it worked, or false if it failed.
```python
success = account.become_referral("other_account_id")
```


### Getting Cashout History
You can retrieve your cashout history using the `get_cashout_history` method of the `CashPiggyAccount` class:
This method returns a list of `CashPiggyCashoutHistory` objects representing your cashout history.
```python
cashout_history = account.get_cashout_history()
```


### Logging
The package uses logging to track the execution flow and any errors encountered during the process. You can configure the logging level and output destination as needed.
Logs are saved in the root folder as cashpiggy.log as it improves debugging for both you & me!


### Contribution
Just make a pull-request with a well described description & I will review to see if the pr is worth it.
If you want your pr to be validated from the get-go, make an issue first so that We can see if the problem/feature will be worth it.
Hope you have fun hacking/coding!
