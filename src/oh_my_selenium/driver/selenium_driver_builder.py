import re

from .selenium_driver import SeleniumDriver
from .chrome_selenium_driver import ChromeSeleniumDriver
from .firefox_selenium_driver import FirefoxSeleniumDriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener


class SeleniumDriverBuilder(object):
    CHROME = "chrome"
    FIREFOX = "firefox"

    def __init__(self,):
        super(SeleniumDriverBuilder, self).__init__()
        self.__driver_path = None # Firefox, Chrome
        self.__binary_location = None # Firefox, Chrome
        self.__headless = False # Firefox, Chrome
        self.__disable_gpu = False # Firefox, Chrome
        self.__no_sandbox = False # Chrome
        self.__ignore_certificate_errors = False # Chrome
        self.__test_type = False # Chrome
        self.__log_level = None # Chrome
        self.__mute_audio = False # Firefox
        self.__event_listener = None # Selenium Web Driver

    def __getattr__(self, name):
        bool_attrs = ["__headless",
                      "__disable_gpu",
                      "__no_sandbox",
                      "__ignore_certificate_errors",
                      "__test_type",
                      "__mute_audio",]
        val_attrs = ["__log_level",
                     "__driver_path",
                     "__binary_location",
                     "__event_listener",]

        attr_name = "__%s" % name
        if attr_name in bool_attrs:
            def __():
                self.__dict__["_SeleniumDriverBuilder%s" % attr_name] = True
                return self
            return __

        attr_name = "__%s" % re.sub(r"^no_", "", name)
        if attr_name in bool_attrs:
            def __():
                self.__dict__["_SeleniumDriverBuilder%s" % attr_name] = False
                return self
            return __

        if attr_name in val_attrs:
            def __(val):
                self.__dict__["_SeleniumDriverBuilder%s" % attr_name] = val
                return self
            return __

        raise AttributeError()

    def build(self, browser_type: str,) -> SeleniumDriver:
        driver_wrapper = None
        if browser_type == SeleniumDriverBuilder.CHROME:
            driver_wrapper = ChromeSeleniumDriver(self.__headless,
                                                  self.__disable_gpu,
                                                  self.__no_sandbox,
                                                  self.__ignore_certificate_errors,
                                                  self.__test_type,
                                                  self.__binary_location,
                                                  self.__log_level,
                                                  self.__driver_path)
        elif browser_type == SeleniumDriverBuilder.FIREFOX:
            driver_wrapper = FirefoxSeleniumDriver(self.__headless,
                                                   self.__disable_gpu,
                                                   self.__mute_audio,
                                                   self.__binary_location,
                                                   self.__driver_path)
        else:
            raise NotImplementError(browser_type)

        if isinstance(self.__event_listener, AbstractEventListener):
            driver_wrapper.driver = EventFiringWebDriver(driver_wrapper.driver, self.__event_listener)

        return driver_wrapper

    def chrome(self,) -> ChromeSeleniumDriver:
        return self.build(SeleniumDriverBuilder.CHROME)

    def firefox(self,) -> FirefoxSeleniumDriver:
        return self.build(SeleniumDriverBuilder.FIREFOX)

    def default_headless(self,):
        self.__headless = True
        self.__disable_gpu = True
        self.__mute_audio = True
        self.__no_sandbox = True
        self.__ignore_certificate_errors = True
        self.__test_type = True
        return self
