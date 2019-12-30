from .selenium_driver import SeleniumDriver

from selenium  import webdriver
from selenium.webdriver.chrome.options import Options

class ChromeSeleniumDriver(SeleniumDriver):
    __headless = False
    __disable_gpu = False
    __no_sandbox = False
    __ignore_certificate_errors = False
    __test_type = False
    __binary_location = None # chrome or chromium executable file path
    # INFO = 0
    # WARNING = 1
    # LOG_ERROR = 2
    # LOG_FATAL = 3
    # default is 0
    __log_level = 0
    __driver_path = None # webdriver file path


    def __init__(self,
                 headless,
                 disable_gpu,
                 no_sandbox,
                 ignore_certificate_errors,
                 test_type,
                 binary_location,
                 log_level,
                 driver_path):
        super(ChromeSeleniumDriver, self).__init__()
        self.__headless = headless
        self.__disable_gpu = disable_gpu
        self.__no_sandbox = no_sandbox
        self.__ignore_certificate_errors = ignore_certificate_errors
        self.__test_type = test_type
        self.__binary_location = binary_location
        self.__log_level = 0 if log_level is None else log_level
        self.__driver_path = driver_path

        chrome_options = Options()
        if self.__headless:
            chrome_options.add_argument('--headless')
        if self.__disable_gpu:
            chrome_options.add_argument('--disable-gpu')
        if self.__no_sandbox:
            chrome_options.add_argument('--no-sandbox')
        if self.__ignore_certificate_errors:
            chrome_options.add_argument('--ignore-certificate-errors')
        if self.__test_type:
            chrome_options.add_argument('--test-type')
        if self.__binary_location:
            chrome_options.binary_location = self.__binary_location

        chrome_options.add_argument('--log-level=%s' % self.__log_level)
        opts = {"chrome_options": chrome_options,}
        if self.__driver_path:
            opts["executable_path"] = self.__driver_path

        self.driver = webdriver.Chrome(**opts)
