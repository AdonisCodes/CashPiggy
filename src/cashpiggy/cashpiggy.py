
from dataclasses import dataclass
from enum import Enum
import random
import string
from typing import Optional, List
import requests
from datetime import datetime
from . import urls
import logging
logging.basicConfig(filename='cashpiggy.log', level=logging.INFO)

def generate_random_ip():
    """Generate a random IP address."""

    return ".".join(str(random.randint(0, 255)) for _ in range(4))


APPNAME = "cashpiggy_14" # App Version


class Country(Enum):
    """Enum for supported countries."""

    SOUTH_AFRICA = "ZA"
    UNITED_STATES = "US"
    UNITED_KINGDOM = "GB"
    CANADA = "CA"
    AUSTRALIA = "AU"
    INDIA = "IN"
    NIGERIA = "NG"
    PAKISTAN = "PK"
    PHILIPPINES = "PH"
    KENYA = "KE"
    GHANA = "GH"
    ZIMBABWE = "ZW"
    UGANDA = "UG"
    TANZANIA = "TZ"
    MALAYSIA = "MY"
    SINGAPORE = "SG"
    IRELAND = "IE"
    NEW_ZEALAND = "NZ"
    JAMAICA = "JM"
    TRINIDAD_AND_TOBAGO = "TT"
    BARBADOS = "BB"
    GUYANA = "GY"
    BAHAMAS = "BS"
    BELIZE = "BZ"
    RUSSIA = "RU"
    GERMANY = "DE"
    FRANCE = "FR"
    ITALY = "IT"
    SPAIN = "ES"
    NETHERLANDS = "NL"

class CashPiggyCashoutMethod(Enum):
    """Enum for supported cashout methods."""

    PAYPAL_3 = ("$3%20PayPal%20Cash", 3, 250)
    AMAZON_1 = ("$1%20Amazon%20Card", 1, 600)
    PAYPAL_5 = ("$5%20PayPal%20Cash", 5, 1000)
    PAYPAL_10 = ("$10%20PayPal%20Cash", 10, 1700)
    PAYPAL_30 = ("$30%20PayPal%20Cash", 30, 4500)
    AMAZON_3 = ("$3%20Amazon%20Card", 3, 600)
    AMAZON_5 = ("$5%20Amazon%20Card", 5, 1000)
    AMAZON_10 = ("$10%20Amazon%20Card", 10, 1700)
    AMAZON_30 = ("$30%20Amazon%20Card", 30, 4500)


@dataclass
class CashPiggyAccountReferrals:
    """Dataclass for CashPiggy account referrals."""

    referral_id: str
    ip: str
    first_ref: str
    second_ref: str
    count_first_ref: int
    count_second_ref: int


@dataclass
class CashPiggyCashoutHistory:
    """Dataclass for CashPiggy cashout history."""

    amountindollar: str
    invitecode: str
    points: str
    timestamp: str
    giftstatus: str
    giftcard: str
    email: str
    country: Country
    transactionid: str


@dataclass
class CashPiggyAccount:
    """Dataclass for CashPiggy account."""

    code: str
    ip: str
    email: Optional[str]
    country: Optional[Country]

    def claim_points(self, points: int) -> bool:
        """Claim points for the account.
        
        Args:
            self: The CashPiggy account.
            points (int): The points to claim.

        Returns:
            bool: True if successful, False otherwise.
        """

        logging.info(f'Starting claim_points for {self.email}')
        try:
            response = requests.get(urls.claim_points_url.format(points, self.code))
            if response.status_code == 200:
                logging.info(f'Successful claim_points for {self.email} ✅')
                return True
            else:
                logging.error(f'Failed claim_points for {self.email} ❌')
                return False
        except Exception as e:
            logging.error(f'Error in claim_points for {self.email}: {str(e)} ❌')
            return False
        finally:
            logging.info(f'Finished claim_points for {self.email}')

    def cashout(self, method: CashPiggyCashoutMethod, country: str) -> bool:
        """Cashout points for the account.

        Args:
            self: The CashPiggy account.
            method (CashPiggyCashoutMethod): The cashout method.
            country (str): The country code.

        Returns:
            bool: True if successful, False otherwise.
        """

        cashout_method, dollar, points = method.value
        response = requests.get(urls.cashout_points_url.format(self.code, cashout_method, dollar, points, datetime.now().timestamp(), self.email, APPNAME, country))
        if response.status_code == 200:
            logging.info(f'Successful cashout for {self.email} ✅')
            return True
        else:
            logging.error(f'Failed cashout for {self.email} ❌')
            return False

    def become_referral(self, referral_code: str) -> bool:
        """Become a referral for another account.

        Args:
            self: The CashPiggy account.
            referral_code (str): The referral code.

        Returns:
            bool: True if successful, False otherwise.
        """

        response = requests.get(urls.become_referral_url.format(referral_code, self.code))
        if response.status_code == 200:
            logging.info(f'Successfully became referral for {self.email} ✅')
            return True
        else:
            logging.error(f'Failed becoming referral for {self.email} ❌')
            return False

    def get_referrals(self) -> Optional[CashPiggyAccountReferrals]:
        """Get referrals for the account.

        Args:
            self: The CashPiggy account.

        Returns:
            Optional[CashPiggyAccountReferrals]: The account referrals if successful, None otherwise.
        """

        response = requests.get(urls.retrieve_referrals_url.format(self.code))
        if response.status_code == 200:
            logging.info(f'Successfully retrieved referrals for {self.email} ✅')
            return CashPiggyAccountReferrals(**response.json())
        else:
            logging.error(f'Failed to retrieve referrals for {self.email} ❌')
            return None

    def get_cashout_history(self) -> Optional[List[CashPiggyCashoutHistory]]:
        """Get cashout history for the account.

        Args:
            self: The CashPiggy account.

        Returns:
            Optional[List[CashPiggyCashoutHistory]]: The cashout history if successful, None otherwise.
        """

        response = requests.get(urls.retrieve_rewards_history_url.format(self.code))
        if response.status_code == 200:
            try:
                logging.info(f'Successfully retrieved cashout history for {self.email} ✅')
                return [CashPiggyCashoutHistory(**item) for item in response.json()['data']]
            except Exception as e:
                logging.error(f'Error parsing cashout history for {self.email}: {str(e)} ❌')
                return None
        else:
            logging.error(f'Failed to retrieve cashout history for {self.email} ❌')
            return None

    @staticmethod
    def register(email: str) -> Optional['CashPiggyAccount']:
        """Register a new CashPiggy account.

        Args:
            email (str): The email to register.

        Returns:
            Optional[CashPiggyAccount]: The registered account if successful, None otherwise.
        """

        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        random_ip = generate_random_ip()
        response = requests.get(urls.signup_url.format(random_code, random_ip))
        if response.status_code == 200:
            random_country = random.choice(list(Country))
            logging.info(f'Successfully registered account for {email} ✅')
            return CashPiggyAccount(random_code, random_ip, email, random_country)
        else:
            logging.error(f'Failed to register account for {email} ❌')
            return None
