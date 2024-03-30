import requests
import random
import string
import json
import hashlib
from faker import Faker

def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def get_mail_domains():
    url = "https://api.mail.tm/domains"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['hydra:member']
        else:
            print("\033[91mLỗi khi lấy danh sách domain mail:\033[0m")
            print(response.text)
            return None
    except Exception as e:
        print("\033[91mĐã xảy ra lỗi:\033[0m", e)
        return None

def create_mail_tm_account():
    fake = Faker()
    mail_domains = get_mail_domains()
    if mail_domains:
        domain = random.choice(mail_domains)['domain']
        username = generate_random_string(10)  # Adjust length as per requirement
        password = 'Kh@ng270308'
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)  # Random birthday between 18 and 45 years old
        first_name = fake.first_name()
        last_name = fake.last_name()
        url = "https://api.mail.tm/accounts"
        headers = {"Content-Type": "application/json"}
        data = {"address": f"{username}@{domain}", "password": password}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                print("\033[92mTạo tài khoản mail thành công\033[0m")
                return f"{username}@{domain}", password, first_name, last_name, birthday
            else:
                print("\033[91mLỗi khi tạo tài khoản mail:\033[0m")
                print(response.text)
                return None, None, None, None, None
        except Exception as e:
            print("\033[91mĐã xảy ra lỗi:\033[0m", e)
            return None, None, None, None, None

def register_facebook_account(email, password, first_name, last_name, birthday):
    api_key = '882a8490361da98702bf97a021ddc14d'
    secret = '62f8ce9f74b12f84c123cc23437a4a32'
    gender = random.choice(['M', 'F'])

    req = {
        'api_key': api_key,
        'attempt_login': True,
        'birthday': birthday.strftime('%Y-%m-%d'),  # Format birthday as 'YYYY-MM-DD'
        'client_country_code': 'EN',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': first_name,
        'format': 'json',
        'gender': gender,
        'lastname': last_name,
        'email': email,
        'locale': 'en_US',
        'method': 'user.register',
        'password': password,
        'reg_instance': generate_random_string(32),
        'return_multiple_errors': True
    }
    sorted_req = sorted(req.items(), key=lambda x: x[0])
    sig = ''.join(f'{k}={v}' for k, v in sorted_req)
    ensig = hashlib.md5((sig + secret).encode()).hexdigest()
    req['sig'] = ensig
    api_url = 'https://b-api.facebook.com/method/user.register'

    reg = _call(api_url, req)
    # Lưu kết quả dưới dạng JSON
    file_name = email.replace('@', '_').replace('.', '_')  # Thay thế "@" và "." bằng "_"
    with open(f"FB_{file_name}.json", "w") as file:
        json.dump(reg, file, indent=4)
    print("\033[96mĐăng ký Facebook thành công:\033[0m")
    print(f"Email: {email}")
    print(f"Password: {password}")

def _call(url, params, post=True):
    headers = {
        'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'
    }
    if post:
        response = requests.post(url, data=params, headers=headers)
    else:
        response = requests.get(url, params=params, headers=headers)
    return response.json()

if __name__ == "__main__":
    for i in range(1, 100001):  # Tạo từ tài khoản thứ 1 đến tài khoản thứ 100000
        email, password, first_name, last_name, birthday = create_mail_tm_account()
        if email and password and first_name and last_name and birthday:
            register_facebook_account(email, password, first_name, last_name, birthday)
