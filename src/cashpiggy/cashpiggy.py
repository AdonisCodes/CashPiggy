
from dataclasses import dataclass
from enum import Enum
import random
import string
from typing import Optional, List
import requests
from datetime import datetime
import logging
logging.basicConfig(filename='cashpiggy.log', level=logging.INFO)

def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


APPNAME = "cashpiggy_14"


class Country(Enum):
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
    referral_id: str
    ip: str
    first_ref: str
    second_ref: str
    count_first_ref: int
    count_second_ref: int


@dataclass
class CashPiggyCashoutHistory:
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
    code: str
    ip: str
    email: Optional[str]
    country: Optional[Country]
    claim_points_url: str = "https://djkmhg4jm0.execute-api.us-east-2.amazonaws.com/default/surveys_adjustpoints?points={}&uniquecode={}&desc=free_bonus"

    def claim_points(self, points: int) -> bool:
        logging.info(f'Starting claim_points for {self.email}')
        try:
            response = requests.get(self.claim_points_url.format(points, self.code))
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
        cashout_method, dollar, points = method.value
        response = requests.get(f"https://69ppjn70tj.execute-api.us-east-2.amazonaws.com/default/rewardHistoryInsertData?ic={self.code}&cn={cashout_method}&dollar={dollar}&points={points}&time={datetime.now().timestamp}&pemail={self.email}&appname={APPNAME}&country={country}")
        if response.status_code == 200:
            logging.info(f'Successful cashout for {self.email} ✅')
            return True
        else:
            logging.error(f'Failed cashout for {self.email} ❌')
            return False

    def become_referral(self, referral_code: str) -> bool:
        response = requests.get(f"https://eighth-vehicle-107008.appspot.com/_ah/api/handlert/v1/object/{referral_code}/{self.code}")
        if response.status_code == 200:
            logging.info(f'Successfully became referral for {self.email} ✅')
            return True
        else:
            logging.error(f'Failed becoming referral for {self.email} ❌')
            return False

    def get_referrals(self) -> Optional[CashPiggyAccountReferrals]:
        response = requests.get(f"https://eighth-vehicle-107008.appspot.com/_ah/api/handlert/v1/retrieveRef/{self.code}")
        if response.status_code == 200:
            logging.info(f'Successfully retrieved referrals for {self.email} ✅')
            return CashPiggyAccountReferrals(**response.json())
        else:
            logging.error(f'Failed to retrieve referrals for {self.email} ❌')
            return None

    def get_cashout_history(self) -> Optional[List[CashPiggyCashoutHistory]]:
        response = requests.get(f"https://oqdyz05zj9.execute-api.us-east-2.amazonaws.com/default/rewardHistoryGetData?invitecode={self.code}")
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
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        random_ip = generate_random_ip()
        response = requests.get(f"https://eighth-vehicle-107008.appspot.com/_ah/api/handlert/v1/cn_insertRef/{random_code}/{random_ip}")
        if response.status_code == 200:
            random_country = random.choice(list(Country))
            logging.info(f'Successfully registered account for {email} ✅')
            return CashPiggyAccount(random_code, random_ip, email, random_country)
        else:
            logging.error(f'Failed to register account for {email} ❌')
            return None# Example where we do a pyramid scheme referrals


master_referral = CashPiggyAccount.register("business@simonferns.com")
print(master_referral)
if not master_referral:
    print("Failed to register")
    exit()

for i in range(10):
    account = CashPiggyAccount.register(f"business+{i}@simonferns.com")
    if account:
        if i > 0:
            account.become_referral(master_referral.code)
        with open("accounts.txt", "a") as f:
            f.write(f"{account.code} {account.ip} {account.email} {account.country}\n")
    else:
        print("Failed to register")
