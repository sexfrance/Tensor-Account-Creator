import tls_client 
import random
import time
import re
import toml
import ctypes
import threading
import string
import base64
import json
import html

from solver.sync_solver import get_turnstile_token
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
from logmagix import Logger, Home

with open('input/config.toml') as f:
    config = toml.load(f)

DEBUG = config['dev'].get('Debug', False)
log = Logger()

def debug(func_or_message, *args, **kwargs) -> callable:
    if callable(func_or_message):
        @wraps(func_or_message)
        def wrapper(*args, **kwargs):
            result = func_or_message(*args, **kwargs)
            if DEBUG:
                log.debug(f"{func_or_message.__name__} returned: {result}")
            return result
        return wrapper
    else:
        if DEBUG:
            log.debug(f"Debug: {func_or_message}")

def debug_response(response) -> None:
    debug(response.headers)
    debug(response.text)
    debug(response.status_code)

def decode_jwt_payload(token: str) -> dict:
    try:
        payload = token.split('.')[1]
        payload += '=' * (-len(payload) % 4)
        decoded = base64.b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        log.failure(f"Failed to decode JWT: {e}")
        return None

class Miscellaneous:
    @debug
    def get_proxies(self) -> dict:
        try:
            if config['dev'].get('Proxyless', False):
                return None
                
            with open('input/proxies.txt') as f:
                proxies = [line.strip() for line in f if line.strip()]
                if not proxies:
                    log.warning("No proxies available. Running in proxyless mode.")
                    return None
                
                proxy_choice = random.choice(proxies)
                proxy_dict = {
                    "http": f"http://{proxy_choice}",
                    "https": f"http://{proxy_choice}"
                }
                log.debug(f"Using proxy: {proxy_choice}")
                return proxy_dict
        except FileNotFoundError:
            log.failure("Proxy file not found. Running in proxyless mode.")
            return None

    @debug 
    def generate_email(self, domain: str = "bune.pw") -> str:
        username = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=20))}"
        email = f"{username}@{domain}"
        return email
    
    @debug 
    def randomize_user_agent(self) -> str:
        platforms = [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 10.0; WOW64",
            "Macintosh; Intel Mac OS X 10_15_7",
            "Macintosh; Intel Mac OS X 11_2_3",
            "X11; Linux x86_64",
            "X11; Linux i686",
            "X11; Ubuntu; Linux x86_64",
        ]
        
        browsers = [
            ("Chrome", f"{random.randint(90, 140)}.0.{random.randint(1000, 4999)}.0"),
            ("Firefox", f"{random.randint(80, 115)}.0"),
            ("Safari", f"{random.randint(13, 16)}.{random.randint(0, 3)}"),
            ("Edge", f"{random.randint(90, 140)}.0.{random.randint(1000, 4999)}.0"),
        ]
        
        webkit_version = f"{random.randint(500, 600)}.{random.randint(0, 99)}"
        platform = random.choice(platforms)
        browser_name, browser_version = random.choice(browsers)
        
        if browser_name == "Safari":
            user_agent = (
                f"Mozilla/5.0 ({platform}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                f"Version/{browser_version} Safari/{webkit_version}"
            )
        elif browser_name == "Firefox":
            user_agent = f"Mozilla/5.0 ({platform}; rv:{browser_version}) Gecko/20100101 Firefox/{browser_version}"
        else:
            user_agent = (
                f"Mozilla/5.0 ({platform}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                f"{browser_name}/{browser_version} Safari/{webkit_version}"
            )
        
        return user_agent

    @debug
    def extract_source_id(self, url: str) -> str | None:
        if not url:
            return None
        try:
            match = re.search(r'source_id=([^&\s]+)', url)
            return match.group(1) if match else None
        except Exception as e:
            log.failure(f"Failed to extract source ID: {e}")
            return None


    class Title:
        def __init__(self) -> None:
            self.running = False
            self.is_windows = hasattr(ctypes, 'windll')

        def start_title_updates(self, total, start_time) -> None:
            self.running = True
            def updater():
                while self.running:
                    self.update_title(total, start_time)
                    time.sleep(0.5)
            threading.Thread(target=updater, daemon=True).start()

        def stop_title_updates(self) -> None:
            self.running = False

        def update_title(self, total, start_time) -> None:
            try:
                if not self.is_windows:
                    return  # Skip title updates on non-Windows systems
                    
                elapsed_time = round(time.time() - start_time, 2)
                title = f'discord.cyberious.xyz | Total: {total} | Time Elapsed: {elapsed_time}s'
                sanitized_title = ''.join(c if c.isprintable() else '?' for c in title)
                ctypes.windll.kernel32.SetConsoleTitleW(sanitized_title)
            except Exception as e:
                log.debug(f"Failed to update console title: {e}")

class AccountCreator:
    def __init__(self, proxy_dict: dict = None) -> None:
        self.session = tls_client.Session("chrome_131", random_tls_extension_order=True)
        self.session.headers = {
        'accept': '*/*',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'connection': 'keep-alive',
        'content-type': 'application/json',
        'host': 'api.tensor.art',
        'origin': 'https://tensor.art',
        'referer': 'https://tensor.art/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'x-device-id': 'GuftawFyAyB3Vp2HXm1pU',
        'x-request-package-id': '3000',
        'x-request-package-sign-version': '0.0.1',
        'x-request-sign': 'Mjg2YTE4ZmE2ZDBlNGVjMTRkNWEzZjYwYTU5YmNlNGNhZmVhNDZjZGVjNDdjN2E1YzRkMTU1ZTlmYTI0YzU0Yg==',
        'x-request-sign-type': 'HMAC_SHA256',
        'x-request-sign-version': 'v1',
        'x-request-timestamp': '1738362103831',
        }
        self.session.proxies = proxy_dict

    @debug
    def create_account(self, email: str, affiliate_code: str = None) -> bool:
        try:
            json_data = {
                'email': email,
                'type': 'EMAIL',
            }

            if affiliate_code:
                json_data['returnUrl'] = f'https://tensor.art/?source_id={affiliate_code}'

                self.session.cookies.update({
                'ta_invite_code': affiliate_code,
                })
            
            else:
                json_data['returnUrl'] = 'https://tensor.art/'

            result = get_turnstile_token(
                url="https://tensor.art/",
                sitekey="0x4AAAAAAAS1_AKN3XKlym8v",
                invisible=False,
                debug=DEBUG
            )

            self.session.headers["x-captcha-token"] = result.get("turnstile_value")

            response = self.session.post('https://api.tensor.art/user-web/v1/signin', json=json_data)
            
            debug_response(response)

            self.session.headers.pop("x-captcha-token")

            if response.status_code == 200 and response.json().get("code") == "0":
                return True
            else:
                log.failure(f"Failed to register account: {response.text}, {response.status_code}")
       
        except Exception as e:
            log.failure(f"Failed to create account: {e}")
        
    @debug
    def verify_email(self, url: str) -> str:
        response = self.session.get(url, allow_redirects=False)
        debug_response(response)

        if response.status_code == 302 and response.cookies.get("ta_token_prod"):
            authorization = response.cookies.get('ta_token_prod')

            self.session.headers.update({"authorization": f"Bearer {authorization}"})
            return authorization
        else:
            log.failure(f"Failed to verify email: {response.text}, {response.status_code}")
    
    @debug
    def create_image(self) -> bool:
        debug("Creating image...")
        json_data = {
            'params': {
                'baseModel': {
                    'modelId': '619225630271212879',
                    'modelFileId': '619225630270164304',
                },
                'sdxl': {
                    'refiner': False,
                },
                'models': [],
                'embeddingModels': [],
                'sdVae': 'Automatic',
                'prompt': 'a girl',
                'negativePrompt': 'EasyNegative',
                'height': 768,
                'width': 512,
                'imageCount': 1,
                'steps': 20,
                'images': [],
                'cfgScale': 7,
                'seed': '-1',
                'clipSkip': 2,
                'etaNoiseSeedDelta': 31337,
                'v1Clip': False,
                'guidance': 3.5,
                'samplerName': 'Euler a',
            },
            'credits': 0.8,
            'taskType': 'TXT2IMG',
            'isRemix': False,
            'captchaType': 'CLOUDFLARE_TURNSTILE',
        }

        self.session.headers.update({'x-request-sign': 'OGFhYmI4MTFhNjFiZWU5YzVmNWJiZTVhYjVkMzhhNTc4ZDM5YjdiOThiNjNjY2JiZDlkMGZmNzgxZmRkODQzNA==','x-request-timestamp': '1738413533660','referer': 'https://tensor.art/settings/profile'})

        debug(f"Request headers: {self.session.headers}")
        debug(f"Request cookies: {self.session.cookies.get_dict()}")

        self.session.headers.pop("x-device-id")
        result = get_turnstile_token(
                url="https://tensor.art/",
                sitekey="0x4AAAAAAAS1_AKN3XKlym8v",
                invisible=False,
                debug=DEBUG
            )

        self.session.headers["x-captcha-token"] = result.get("turnstile_value")

        response = self.session.post('https://api.tensor.art/works/v1/works/task', json=json_data)
        
        debug_response(response)

        if response.status_code == 200 and response.json().get("code") == "0":
            return True
        else:
            log.failure(f"Failed to create image: {response.text}, {response.status_code}")
            return False

class EmailHandler:
    def __init__(self, proxy_dict: dict = None) -> None:
        self.session = tls_client.Session(random_tls_extension_order=True)
        self.session.proxies = proxy_dict

    @debug
    def check_mailbox(self, email: str, max_retries: int = 5) -> list | None:
        debug(f"Checking mailbox for {email}")
        
        for attempt in range(max_retries):
            try:
                json_data = {
                    'email': email,
                    'take': 10,
                    'skip': 0,
                }
                response = self.session.post(f'https://bune.pw/api/inbox', json=json_data)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    log.failure(f"Failed to check mailbox: {response.text}, {response.status_code}")
                    debug(response.json(), response.status_code)
                    break
            except Exception as e:
                log.failure(f"Error checking mailbox: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                break
        return None

    @debug
    def fetch_message(self, email: str, id: int, max_retries: int = 5) -> dict | None:
        debug(f"Fetching mailbox message for {email}")
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(f'https://bune.pw/api/inbox/message/{id}')
                
                if response.status_code == 200:
                    return response.json()
                else:
                    log.failure(f"Failed to fetch message: {response.text}, {response.status_code}")
                    break
            except Exception as e:
                log.failure(f"Error fetching message: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                break
        return None

    @debug
    def get_mail_id(self, email: str) -> str | None:
        attempt = 0
        debug(f"Getting verification message id for {email}")
        while attempt < 10: 
            messages = self.check_mailbox(email)
            if messages and messages.get('messages'):
                for message in messages['messages']:
                    subject = message.get("subject", "")
                    if 'Sign in to Tensor.Art' in subject:
                        debug(message)
                        return message.get("id")
            attempt += 1
            time.sleep(1.5)
        debug(f"No verification message found after {attempt} attempts")
        return None 

    @debug
    def get_verification_url(self, email: str) -> str | None:
        debug(f"Getting verification link for {email}")
        try:
            mail_id = self.get_mail_id(email)
            if not mail_id:
                log.failure("No mail ID found")
                return None
                
            message = self.fetch_message(email, mail_id)
            if not message or 'html' not in message:
                log.failure("No message content found")
                return None
                
            login_url_match = re.search(r'https://api\.tensor\.art/user-web/signin/auth/callback\?[^"\'<>\s]+', message['html'])
            if not login_url_match:
                log.failure("No verification URL found in message")
                return None
                
            # Decode HTML entities in the URL
            return html.unescape(login_url_match.group(0))
            
        except Exception as e:
            log.failure(f"Error getting verification URL: {str(e)}")
            return None

def create_account() -> bool:
    try:
        account_start_time = time.time()

        Misc = Miscellaneous()
        proxies = Misc.get_proxies()
        Email_Handler = EmailHandler(proxies)
        Account_Generator = AccountCreator(proxies)
        
        email = Misc.generate_email()
        affiliate_url = config['data'].get('Affiliate_Link', None)
        affiliate = Misc.extract_source_id(affiliate_url)

        log.info(f"Starting a new account creation process for {email[:10]}...")
        
        if not Account_Generator.create_account(email, affiliate):
            log.failure("Failed to create account")
            return False
            
        log.info("Verification email sent successfully. Retrieving URL...")
        url = Email_Handler.get_verification_url(email)
        
        auth_token = Account_Generator.verify_email(url)

        if auth_token:
            log.info("Successfully verified email.")
        else:
            return False
        

        decoded_payload = decode_jwt_payload(auth_token)
        user_id = decoded_payload.get('userId')


        with open("output/accounts.txt", "a") as f:
            f.write(f"{email}:{user_id}\n")
        
        with open("output/full_account_capture.txt", "a") as f:
            f.write(f"{user_id}:{email}:{auth_token}\n")
                    
        log.message("Tensor.Art", f"Account created successfully: {email[:10]}... | {user_id}", account_start_time, time.time())
        
        if affiliate:
            if Account_Generator.create_image():
                log.info("Affiliate code successfully validated!")
                return True
        else:
            return True
               
        return False
        
    except Exception as e:
        log.failure(f"Error during account creation process: {str(e)}")
        return False

def main() -> None:
    try:
        start_time = time.time()
        
        # Initialize basic classes
        Misc = Miscellaneous()
        Banner = Home("Tensor Generator", align="center", credits="discord.cyberious.xyz")
        
        # Display Banner
        Banner.display()

        total = 0
        thread_count = config['dev'].get('Threads', 1)

        # Start updating the title
        title_updater = Misc.Title()
        title_updater.start_title_updates(total, start_time)
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            while True:
                futures = [
                    executor.submit(create_account)
                    for _ in range(thread_count)]                
                for future in as_completed(futures):                    
                    try:
                        if future.result():
                            total += 1
                    except Exception as e:
                        log.failure(f"Thread error: {e}")

    except KeyboardInterrupt:
        log.info("Process interrupted by user. Exiting...")
    except Exception as e:
        log.failure(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()