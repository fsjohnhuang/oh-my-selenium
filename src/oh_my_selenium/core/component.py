from pprint import pprint

from typing import Callable, Any
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from ..driver import SeleniumDriver


def declarative_component(selenium_driver: SeleniumDriver):
    ComponentType = None
    class ComponentMetaclass(type):
        def __new__(cls, name, bases, attrs):
            if not "selector" in attrs.keys():
                attrs["selector"] = None

            attrs["__components__"] = dict()
            if name == "Component":
                return type.__new__(cls, name, bases, attrs)

            components = dict()
            if "__selector__" in attrs.keys():
                attrs["selector"] = attrs.pop("__selector__")
                for k, v in attrs.items():
                    if isinstance(v, ComponentType):
                        components[k] = v

            attrs["__components__"] = components

            return type.__new__(cls, name, bases, attrs)

    class Component(object, metaclass=ComponentMetaclass):
        __driver__ = selenium_driver

        def __init__(self, selector=None, **kargs):
            super(Component, self).__init__()
            self.this = kargs.get("this") # List[WebElement]
            if self.this is not None and not isinstance(self.this, list):
                self.this = [self.this]
            if selector is not None:
                self.selector = selector
            self.parent = kargs.get("parent") # Component

            # initialize child components
            for k, v in self.__components__.items():
                v.erase(ComponentType(self.selector))

        def __len__(self,):
            return len(self.bind().this)

        def __getitem__(self, n):
            if isinstance(n, int):
                return self.bind().this[n]
            if isinstance(n, slice):
                return self.bind().this[n.start:n.stop]

        def __getattr__(self, name):
            return getattr(self.bind().this[0], name)

        def __iter__(self,) -> ComponentType:
            self.__cursor = 0
            return self.bind()

        def __next__(self,) -> ComponentType:
            if self.__cursor == len(self.this):
                raise StopIteration()
            else:
                i = self.__cursor
                self.__cursor += 1
                return self.copy(this=self.this[i])

        def bind(self, rebind=False) -> ComponentType:
            if self.this is None or rebind:
                if self.parent is None:
                    self.this = self.__driver__.find_elements(By.CSS_SELECTOR, self.selector)
                else:
                    # get the children of the first web element only.
                    we_parent = self.parent.bind().this[0]
                    self.this = we_parent.find_elements(By.CSS_SELECTOR, self.selector)

            if len(self.this) == 0:
                raise Exception("Element Not Found(parent:%s, selector:%s)" % (None if self.parent is None else self.parent.selector, self.selector))

            return self

        def copy(self, **kargs) -> ComponentType:
            selector = kargs.get("selector", self.selector)
            opts = {
                "parent": kargs.get("parent", self.parent),
                "this": kargs.get("this", self.this),
            }
            return self.__class__(selector, **opts)

        def first(self,) -> ComponentType:
            if self.this is None:
                return self.copy(selector=self.selector + ":first-child")
            else:
                return self.copy(this=self.bind().this[0])

        def last(self,) -> ComponentType:
            if self.this is None:
                return self.copy(selector=self.selector + ":last-child")
            else:
                return self.copy(this=self.bind().this[-1])

        def reverse(self,) -> ComponentType:
            self.bind().this.reverse()
            return self

        def find(self, selector) -> ComponentType:
            return Component(selector, parent = self)

        def value(self, v=None):
            if v is None:
                return self.bind().this[0].get_attribute("value")
            else:
                self.bind().this[0].clear()
                self.bind().this[0].send_keys(v)
                return self

        def text(self, v=None):
            if v is None:
                return self.bind().this[0].text
            else:
                self.bind().this[0].text = v
                return self

        def execute_script(self, script, *args):
            if len(args) == 0:
                args = [self.bind().this[0]]
            else:
                args = map(lambda x: x.bind().this[0] if isinstance(x, ComponentType) else x, args)

            return self.__driver__.execute_script(script, *args)

        def script_click(self,):
            self.execute_script("arguments[0].click()")

        def erase(self, parent=None):
            self.this = None
            self.parent = parent
            for k, v in self.__components__.items():
                v.erase(ComponentType(self.selector))

    ComponentType = Component
    return Component
