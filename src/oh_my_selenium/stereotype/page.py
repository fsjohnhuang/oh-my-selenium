from typing import Tuple, Any, Union, Callable
from selenium.webdriver.support.events import AbstractEventListener

from ..driver import SeleniumDriver
from ..core import declarative_component


def declarative_page(selenium_driver: SeleniumDriver) -> Tuple[Any, Any, Any]:
    Component = declarative_component(selenium_driver)

    PageType = None
    RouterType = None

    class Router(object):
        __driver__ = selenium_driver
        redirects = None
        routes = None
        status_handlers = {}

        def __init__(self,):
            super(Router, self).__init__()
            self.routes = {}
            self.redirects = {}

        def route(self, route: str, page_type: PageType) -> RouterType:
            self.routes[route] = page_type
            return self

        def redirect(self, src_route: str, dst_route: str) -> RouterType:
            self.redirects[src_route] = dst_route
            return self

        def status(self, status: Union[int, str], handler: Callable[[Any], None]) -> RouterType:
            self.status_handlers[status] = handler
            return self

        def request(self, url: str) -> RouterType:
            self.__driver__.get(url)
            return self

        def refresh(self, ) -> RouterType:
            self.__driver__.get(self.__driver__.current_url)
            return self


    RouterType = Router
    router = Router()

    class RouterEventListener(AbstractEventListener):
        __router__ = router
        def __init__(self,):
            super(RouterEventListener, self).__init__()

        def after_navigate_to(self, url, driver):
            print(url)
            print(driver.current_url)
            for route, page_type in self.__router__.routes.items():
                if driver.current_url.count(route):
                    return page_type().index()

        def after_navigate_refresh(self, url, driver):
            print(url)
            print(driver.current_url)
            for route, page_type in self.__router__.routes.items():
                if driver.current_url.count(route):
                    return page_type().index()


    selenium_driver.add_event_listener(RouterEventListener())

    class PageMetaclass(type):
        def __new__(cls, name, bases, attrs):
            if name == "Page":
                return type.__new__(cls, name, bases, attrs)

            router = None
            components = dict()
            if "__route__" in attrs.keys():
                attrs["route"] = attrs["__route__"]
                for k, v in attrs.items():
                    if isinstance(v, Component):
                        components[k] = v

                for base in bases:
                    if base == PageType:
                        router = base.__router__
                        break

            attrs["__components__"] = components
            page_type = type.__new__(cls, name, bases, attrs)
            if router is not None:
                router.route(attrs["route"], page_type)

            return page_type

    class Page(object, metaclass=PageMetaclass):
        __router__ = router
        __driver__ = selenium_driver

        def __init__(self,):
            super(Page, self).__init__()
            # initialize components
            for k, v in self.__components__.items():
                v.erase()

        def page_source(self,):
            return self.__driver__.page_source

        def current_url(self,):
            return self.__driver__.current_url

    PageType = Page
    return (router, Page, Component,)
