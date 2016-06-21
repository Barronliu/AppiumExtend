# -*- coding:utf-8 -*-

import robot
from AppiumLibrary import *
import sys, time, re, os

reload(sys)
sys.setdefaultencoding('utf8')

class AppiumExtend(AppiumLibrary):

    ROBOT_LIBRARY_SCOPE = 'Global'
    localTime = time.strftime("%Y-%m-%d", time.localtime())

    def __init__(self):
        AppiumLibrary.__init__(self)

    def clear_until_no_error(self, locator, message="", timeout=None):
        """Try clear `text` in text field identified by `locator` until no error occurred.
        
        Fails if `timeout` expires before the clear success.
        
        Examples:
        | Clear Until No Error |               |                |     |
        | Clear Until No Error | name=username | clear username | 10s |
        """
        if not message:
            message = "Clear text field '%s'" % (locator)
        self._wait_until_no_error_fixed(timeout, True, message, self.clear_text, locator)
        
    def input_until_no_error(self, locator, text, message="", timeout=None): 
        """Try types the given `text` into text field identified by `locator` until no error occurred.
        
        Fails if `timeout` expires before the input success.
        
        Examples:
        | Input Until No Error | class=android.widget.Button | username |                |     |
        | Input Until No Error | class=android.widget.Button | username | input username | 10s |
        """
        if not message:
            message = "Typing text '%s' into text field '%s'" % (text, locator)
        self._wait_until_no_error_fixed(timeout, True, message, self.input_text, locator, text)
    
    def click_until_no_error(self, locator, message="", timeout=None):
        """Try click element identified by `locator` until no error occurred.
        
        Fails if `timeout` expires before the click success.
        
        Examples:
        | Click Until No Error | name=Login |           |     |
        | Click Until No Error | name=Login | click btn | 10s |
        """
        if not message:
            message = "Clicking element '%s'" % locator
        self._wait_until_no_error_fixed(timeout, True, message, self.click_element, locator)
    
    def click_nth_element(self, locator, nth=1):
        """Click the nth element identified by `locator`.
        
        Examples:
        | #Click the 2th element |                             |    |
        | Click Nth Element      | class=android.widget.Button |  2 |
        | #Click last element    |                             |    |
        | Click Nth Element      | class=android.widget.Button | -1 |
        """
        try:
            nth = int(nth)
        except ValueError, e:
            raise ValueError(u"'%s' is not a number" % (nth))
        if nth == 0:
            raise ValueError(u"'nth' must not equal 0")
        elements = self.get_elements(locator)
        self._info("Clicking %dth element '%s'" % (nth, locator))
        if nth > 0:
            elements[nth-1].click()
        elif nth < 0:
            elements[nth].click()
            
    def click_nth_until_no_error(self, locator, nth=1, message="", timeout=None):
        """Click the nth element identified by `locator` until no error occurred.
        
        Fails if `timeout` expires before the click success.
        
        Examples:
        | #Click the 2th element   |                             |    |                |     |
        | Click Nth Until No Error | class=android.widget.Button |  2 |                |     |
        | #Click last element      |                             |    |                |     |
        | Click Nth Until No Error | class=android.widget.Button | -1 | click last btn | 10s |
        """
        if not message:
            message = "Clicking %sth element '%s'" % (nth, locator)
        self._wait_until_no_error_fixed(timeout, True, message, self.click_nth_element, locator, nth)

    def click_until_element_exists(self, locator, wait_locator, message="", timeout=None):
        """Click element identified by `locator` until element identified by `wait_locator` appear.
        
        Fails if `timeout` expires before element identified by `wait_locator` appear.
        
        Examples:
        | Click Until Element Exists | name=first | name=twice |                                    |     |
        | Click Until Element Exists | name=first | name=twice | Click 'first' until 'twice' appear | 10s |
        """
        if not message:
            message = "Clicking element '%s' until element '%s' appear" % (locator, wait_locator)
        def click_if_not_exists():
            try:
                self.click_element(locator)
            except:
                pass
            self.page_should_contain_element(wait_locator)
        self._wait_until_no_error_fixed(timeout, True, message, click_if_not_exists)
    
    def click_nth_until_element_exists(self, locator, nth, wait_locator, message="", timeout=None):
        """Click the nth element identified by `locator` until element identified by `wait_locator` appear.
        
        Fails if `timeout` expires before element identified by `wait_locator` appear.
        
        Examples:
        | Click Nth Until Element Exists | name=test1 |  2 | name=test2 |                                         |     |
        | Click Nth Until Element Exists | name=test1 | -1 | name=test2 | Click last 'test1' until 'test2' appear | 10s |
        """
        if not message:
            message = "Clicking %sth element '%s' until element '%s' appear" % (nth, locator, wait_locator)
        def click_nth_if_not_exists():
            try:
                self.click_nth_element(locator, nth)
            except:
                pass
            self.page_should_contain_element(wait_locator)
        self._wait_until_no_error_fixed(timeout, True, message, click_nth_if_not_exists)
        
    def scroll_continue_no_error(self, locator_list, message=""):
        """Scrolls from one element to another.
        
        Do not raise error if any step failed.
        
        Examples
        | Scroll Continue No Error | name=first,name=twice,name=third |                            |
        | Scroll Continue No Error | name=first,name=twice,name=third | Scroll first->twice->third |
        """
        if not isinstance(locator_list, list):
            _locator_list = self._convert_to_list(locator_list)
        if not message:
            message = "Scrolling [%s]" % ("->".join(_locator_list))
        flag = True
        for index in range(len(_locator_list)-1, 0, -1):
            try:
                self.scroll(_locator_list[index-1], _locator_list[index])
            except:
                flag = False
                continue
        if flag:
            self._info(u"%s ==> PASS." % (message))
        else:
            self._info(u"%s ==> NOT ALL PASS." % (message))
            
    def click_if_exists_in_time(self, locator, message="", timeout=None):
        """Try click element identified by `locator` in setting time.
        
        Ignore if `timeout` expires before the click success.
        
        Examples:
        | Click If Exists In Time | name=skip |                                    |     |
        | Click If Exists In Time | name=skip | click skip, no error if click fail | 10s |
        """
        if not message:
            message = "Clicking element '%s'" % locator
        return self._wait_until_no_error_fixed(timeout, False, message, self.click_element, locator)
        
    def double_click_until_no_error(self, locator, message="", timeout=None):  
        """Try double click element identified by `locator` until no error occurred.
        
        Fails if `timeout` expires before the click success.
        
        Examples:
        | Double Click Until No Error | name=Login |                         |     |
        | Double Click Until No Error | name=Login | double click login link | 10s |
        """
        if not message:
            message = "Double clicking element '%s'" % locator
        self._wait_until_no_error_fixed(timeout, True, message, self.double_click_element, locator)
    
    def is_element_present(self, locator):
        """Check the element identified by `locator` is exist or not. 
        
        Return True if locator element present, False if locator element not present.
        
        Examples:
        | ${isPresent}= | Is Element Present | name=Login |
        """
        return self._is_element_present(locator)
    
    def get_element_attribute_in_time(self, locator, attribute, message="", timeout=None):
        """Get element attribute using given attribute: name, value,... by `locator` until no error occurred.
        
        Fails if `timeout` expires before the click success.
        
        Examples:
        | Get Element Attribute In Time | id=com.xx/id/what | text |                  |     |
        | Get Element Attribute In Time | id=com.xx/id/what | text | get element name | 10s |
        """
        if not message:
            message = "Element locator '%s' did not match any elements." % locator
        return self._wait_until_no_error_fixed(timeout, True, message, self.get_element_attribute, locator, attribute)
    
    def get_element_count(self, locator, fail_on_error=True):
        """Count elements found by `locator`.
        
        Examples:
        | ${count}= | Get Element Count | class=android.widget.Button |
        """
        return len(self.get_elements(locator, fail_on_error=fail_on_error))

    def get_element_count_in_time(self, locator, message="", timeout=None):
        """Count elements found by `locator` until result is not 0.
        
        Return 0 if `timeout` expires.
        
        Examples:
        | ${count}= | Get Element Count In Time | class=android.widget.Button |              |     |
        | ${count}= | Get Element Count In Time | class=android.widget.Button | count button | 10s |
        """
        return self._wait_until_not_value(timeout, 0, False, message, self.get_element_count, locator)
    
    def page_should_contain_text_in_time(self, text, message="", timeout=None):
        """Verifies text is not found on the current page in setting time.
        
        Fails if `timeout` expires before find page contain text.
        
        Examples:
        | Page Should Contain Text In Time | hello world |            |     |
        | Page Should Contain Text In Time | hello world | check page | 10s |
        """
        if not message:
            message = "Page should have contained text '%s'" % (text)
        self._wait_until_no_error_fixed(timeout, True, message, self.page_should_contain, text, 'NONE')

    def page_should_contain_element_in_time(self, locator, message="", timeout=None):
        """Verifies element identified by `locator` is not found on the current page in setting time.
        
        Fails if `timeout` expires before find page contain locator element.
        
        Examples:
        | Page Should Contain Element In Time | name=Login |                          |     |
        | Page Should Contain Element In Time | name=Login | check login button exist | 10s |
        """
        if not message:
            message = "Page should have contained element '%s'" % (locator)
        self._wait_until_no_error_fixed(timeout, True, message, self.page_should_contain_element, locator, 'NONE')
    
    def wait_until_page_contains_elements(self, locator_list, message="", timeout=None):
        """Waits until any element specified with `locator_list` appears on current page.
        
        Return appear locator if found.
        Fails if `timeout` expires before the element appears.
        
        Examples:
        | Wait Until Page Contains Elements | name=unlogin, name=login          |                            |                       |     |
        | ${appear_locator}=                | Wait Until Page Contains Elements | [name=unlogin, name=login] | wait elements appears | 10s |
        """
        if not isinstance(locator_list, list):
            _locator_list = self._convert_to_list(locator_list)
        message_info = "Wait Page contains %s" % (" or ".join(["'"+i+"'" for i in _locator_list]))
        if not message:
            message = message_info
        self._info(u"%s." % (message_info))
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else 15
        maxtime = time.time() + timeout
        while True:
            for locator in _locator_list:
                if self._is_element_present(locator):
                    self._info(u"%s ==> PASS." % (message))
                    return locator
            else:
                if time.time() > maxtime:
                    raise AssertionError(u"%s ==> FAIL." % (message))
                    time.sleep(0.5)  
                continue
            break
            
    def _convert_to_list(self, str_list):
        if str_list.startswith('[') and str_list.endswith(']'):
            str_list = str_list[1:-1]
        return [i.strip() for i in str_list.split(',')]
            
    def _wait_until_no_error_fixed(self, timeout, fail_raise_error, message, wait_func, *args):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else 15
        maxtime = time.time() + timeout
        while True:
            try:
                res = wait_func(*args)
            except Exception, e:
                timeout_error = True
            else:
                timeout_error = False
            if not timeout_error:
                self._info(u"%s ==> PASS." % (message))
                return res
            if time.time() > maxtime:
                if not fail_raise_error:
                    self._info(u"%s ==> NOT PASS." % (message))
                    return False
                else:
                    raise AssertionError(u"%s ==> FAIL." % (message))
                    break
            time.sleep(0.5)
    
    def _wait_until_not_value(self, timeout, value, fail_raise_error, message, wait_func, *args):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else 20
        maxtime = time.time() + timeout
        while True:
            res = wait_func(*args)
            if res != value:
                if message:
                    self._info(u"%s ==> %s." % (message, res))
                return res
            if time.time() > maxtime:
                if not fail_raise_error:
                    if message:
                        self._info(u"%s ==> %s." % (message, res))
                    return res
                if message:
                    raise AssertionError(u"%s ==> %s." % (message, res))
                else:
                    raise AssertionError(u"Return ==> %s." % res)
                break
            time.sleep(0.5)
