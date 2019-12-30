# oh-my-selenium

## Intro

## Usage

### 1st Layer: Webdriver is Out of Box for You
```python
from oh_my_selenium.driver import SeleniumDriverBuilder


with SeleniumDriverBuilder().driver_path("./chrome_driver").chrome() as driver:
    driver.get("http://site.com")
    driver.find_element_by_css_selector("#username").send_keys("hi,guy")
```

### 2nd Layer: Component Oriented Development
```python
from oh_my_selenium.driver import SeleniumDriverBuilder
from oh_my_selenium.core import declarative_component


with SeleniumDriverBuilder().driver_path("./chrome_driver").chrome() as driver:
    Component = declarative_component(driver)
    driver.get("http://site.com")
    Component("#username").value("hi,guy")

    class Dialog(Component):
        __selector__ = ".dialog"          # set css selector by `__selector__` field
        username = Component(".username") # bind child component by field
	message = Component(".message")   
        submit = Componnent(".submit")

        def submit(self, username, message,):
            self.username.value(username)
            self.message.value(message)
            self.submit.click()

   dialog = Dialog()
   dialog.submit("guy", "hi")
``` 

### 3th Layer: Page Object Pattern  Development
```python
import time

from oh_my_selenium.driver import SeleniumDriverBuilder
from oh_my_selenium.stereotype import declarative_page


with SeleniumDriverBuilder().driver_path("./chrome_driver").chrome() as driver:
    app, Page, Component = declarative_page(driver)

    class Login(Page):
        __route__ = "sign.com"
        username = Component(".username")
        password = Component(".password")
        login = Component(".login")
  
        def index(self,):
            self.username.value("fsjohnhuang")
            self.password.value("123")
            self.login.click()

            time.sleep(1)
            if self.page_source.count("Authencation Invalid").count() > 0:
                print("Anthentication Invalid")
                app.exit() # exit the application
            else:
                # assume it would redirect to http://main.com when authentication is success.
                app.refresh() # becase selenium can't detect the change of url by browser own redirection, so we have to refresh current page to notify selenium.

    class Main(Page):
        __route__ = "main.com"
        dialog = Dialog()
        logout = Component(".person").find("a").last()
        
	def index(self,):
            dialog.submit("guy", "hi")
            logout.click()
    
    app.request("http://sign.com")
```

## Author
[@fsjohnhuang](fsjohnhuang@hotmail.com)

## License
Copyright © 2019 [@fsjohnhuang](fsjohnhuang@hotmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
