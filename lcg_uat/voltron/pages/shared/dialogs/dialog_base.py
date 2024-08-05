from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains

import tests
import voltron.environments.constants as vec
from voltron.pages.shared import get_device_properties
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class DialogHeader(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="dTitle"] | .//div'
    _close_button = 'xpath=.//*[@data-uat="popUpCloseButton"]'

    def is_displayed(self, expected_result=True, timeout=1, poll_interval=0.5, name=None, scroll_to=True,
                     bypass_exceptions=(NoSuchElementException, StaleElementReferenceException)) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" displayed status is: {expected_result}'
        self.scroll_to_we() if scroll_to else None
        result = wait_for_result(
            lambda: self._we.is_displayed() and self._find_element_by_selector(selector='xpath=.//*', context=self._we, timeout=0) is not None,
            expected_result=expected_result,
            timeout=timeout,
            poll_interval=poll_interval,
            name=name)
        return result

    @property
    def title_text(self):
        result = wait_for_result(
            lambda: self._get_webelement_text(selector=self._title),
            name='Dialog name not empty',
            timeout=0.8
        )
        title = result if result else self._get_congratulations_dialog_title()
        self._logger.info(f'*** Dialog title is: "{title}"')
        return title

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, timeout=1, context=self._we)

    def has_close_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._close_button, timeout=0) is not None,
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'Close button shown status to be "{expected_result}"'
                               )

    def click_close(self):
        self.close_button.scroll_to_we()
        self.close_button.click()

    @staticmethod
    def _get_congratulations_dialog_title():
        brand = tests.settings.brand
        return vec.dialogs.DIALOG_MANAGER_CONGRATULATIONS_EX if brand == 'bma' or get_device_properties()['type'] == 'desktop' \
            else vec.dialogs.DIALOG_MANAGER_CONGRATULATIONS_EX.title()


class Dialog(ComponentBase):
    _dialog_header = 'xpath=.//*[@data-uat="popUpTitle" or @class="modal-header"]'
    _dialog_header_type = DialogHeader
    _dialog_content = 'xpath=.//*[@data-uat="popUpWindow" or @class="modal-body"][*]'
    _default_action = None
    _selection_content = 'xpath=.//*[@class="event-title"]'

    @property
    def selection_content(self):
        return ButtonBase(selector=self._selection_content, timeout=1, context=self._we)

    @property
    def header_object(self):
        driver = get_driver()
        driver.implicitly_wait(0.7)
        context = self._dialog_header_type(selector=self._dialog_header, context=self._we, timeout=3)
        driver.implicitly_wait(0)
        return context

    def has_header(self, expected_result=True, timeout=3, context=None, bypass_exceptions=(NoSuchElementException, StaleElementReferenceException)):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._dialog_header, timeout=0, context=context) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Header shown status to be {expected_result} for {self.__class__.__name__}',
                               bypass_exceptions=bypass_exceptions)

    def has_content(self, expected_result=True, timeout=3, context=None, bypass_exceptions=(NoSuchElementException, StaleElementReferenceException)):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._dialog_content, timeout=0, context=context) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               bypass_exceptions=bypass_exceptions,
                               name=f'Content shown status to be {expected_result} for {self.__class__.__name__}')

    @property
    def name(self):
        try:
            name = self.header_object.title_text
        except VoltronException:
            name = self.header_object.title_text
        return name

    def has_close_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self.header_object.has_close_button(expected_result=expected_result, timeout=0.5),
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'Dialog "{self.__class__.__name__}" close button shown status to be "{expected_result}"'
                               )
    def wait_dialog_closed(self, timeout=10, **kwargs):

        def check_closed(dialog_we):
            if kwargs.get('dialog_name') and self.has_header(timeout=0, context=dialog_we):
                return kwargs.get('dialog_name') != self.name
            else:
                try:
                    return (not self.has_header(expected_result=False, timeout=0, bypass_exceptions=(), context=dialog_we) and
                            not self.has_content(expected_result=False, timeout=0, bypass_exceptions=(), context=dialog_we))
                except (StaleElementReferenceException, NoSuchElementException):
                    return True

        return wait_for_result(lambda: check_closed(dialog_we=self._we),
                               timeout=timeout,
                               name=f'Dialog "{self.__class__.__name__}" closed')

    def close_dialog(self):
        if tests.settings.brand == 'bma':
            self.header_object.click_close()
        else:
            try:
                self.header_object.click_close()
            except Exception as e:
                self._logger.warning(e)
                self.close_dialog_outside()
        self.wait_dialog_closed()

    def close_dialog_outside(self):
        """
        Method to close a dialog when it doesn't have a closure button
        """
        self.header_object.click()
        ActionChains(get_driver()).move_by_offset(200, 200).click().perform()
        self.wait_dialog_closed()

    def default_action(self, **kwargs):
        try:
            getattr(self, self._default_action)()
        except Exception as e:
            self._logger.warning(f'*** Cannot find "_default_action" for {self.__class__.__name__}. Exception message: {str(e)}')
            self.close_dialog()
        self.wait_dialog_closed(**kwargs)
