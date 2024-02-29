---

# CashPiggy PyPI Package Documentation

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

```python
account = cashpiggy.CashPiggyAccount.register("your_email@example.com")
```

This method returns a `CashPiggyAccount` object representing the newly created account. If the registration fails, it returns `None`.

### Claiming Points

You can claim points using the `claim_points` method of the `CashPiggyAccount` class:

```python
success = account.claim_points(100)
```

This method takes the number of points to claim as an argument and returns `True` if the claim is successful, otherwise `False`.

### Cashout

To cash out your earnings, you can use the `cashout` method of the `CashPiggyAccount` class:

```python
success = account.cashout(cashpiggy.CashPiggyCashoutMethod.PAYPAL_5, "US")
```

This method takes the cashout method (`CashPiggyCashoutMethod` enum) and the country code as arguments and returns `True` if the cashout is successful, otherwise `False`.

### Getting Referrals

You can retrieve information about your referrals using the `get_referrals` method of the `CashPiggyAccount` class:

```python
referrals = account.get_referrals()
```

This method returns a `CashPiggyAccountReferrals` object containing information about your referrals.

### Getting Cashout History

You can retrieve your cashout history using the `get_cashout_history` method of the `CashPiggyAccount` class:

```python
cashout_history = account.get_cashout_history()
```

This method returns a list of `CashPiggyCashoutHistory` objects representing your cashout history.

### Logging

The package uses logging to track the execution flow and any errors encountered during the process. You can configure the logging level and output destination as needed.

## Conclusion

The CashPiggy package provides a convenient way to interact with CashPiggy's services programmatically, allowing users to create accounts, claim points, cash out earnings, and retrieve account information easily.

---

This documentation provides an overview of the package, installation instructions, and usage examples for its main functionalities. Users can refer to this documentation to effectively utilize the `cashpiggy` package in their Python projects.
