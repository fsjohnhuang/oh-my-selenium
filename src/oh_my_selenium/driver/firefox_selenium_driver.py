from .selenium_driver import SeleniumDriver

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options


class FirefoxSeleniumDriver(SeleniumDriver):
    __headless = False
    __disable_gpu = False
    __mute_audio = False # without audio
    __binary_location = None # firefox executable file path
    __driver_path = None # webdriver file path

    def __init__(self,
                 headless,
                 disable_gpu,
                 mute_audio,
                 binary_location,
                 driver_path,):
        super(FirefoxSeleniumDriver, self).__init__()
        self.__headless = headless
        self.__disable_gpu = disable_gpu
        self.__mute_audio = mute_audio
        self.__binary_location = binary_location
        self.__driver_path = driver_path

        firefox_options = Options()
        if self.__headless:
            firefox_options.add_argument('--headless')
        if self.__disable_gpu:
            firefox_options.add_argument('--disable-gpu')
        if self.__mute_audio:
            firefox_options.add_argument('--mute-audio')

        opts = {"firefox_options": firefox_options}
        if self.__driver_path:
            opts["executable_path"] = self.__driver_path
        if self.__binary_location:
            opts["firefox_binary"] = FirefoxBinary(self.__binary_location)

        self.driver = webdriver.Firefox(**opts)

    def __getattr__(self, name):
        return getattr(self.driver, name)
