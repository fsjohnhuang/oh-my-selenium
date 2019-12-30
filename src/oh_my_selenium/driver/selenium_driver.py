from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener


SeleniumDriverType = None
class SeleniumDriver(object):
    driver = None

    def __init__(self,):
        super(SeleniumDriver, self).__init__()

    def __getattr__(self, name):
        return getattr(self.driver, name)

    def __enter__(self, ):
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        self.driver.quit()

    # replace or append event listener??
    def add_event_listener(self, listener: AbstractEventListener) -> SeleniumDriverType:
        self.driver = EventFiringWebDriver(self.driver, listener)
        return self

SeleniumDriverType = SeleniumDriver
