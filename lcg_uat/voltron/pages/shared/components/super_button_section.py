from typing import List
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from enum import Enum
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class CTA_ENUM(Enum):
    RIGHT_ALIGNMENT = "generic-right-theme"
    CENTER_ALIGNMENT = "generic-center-theme"


class SuperButtonSection(ComponentBase):
    _cta_alignment = 'xpath=.//*[@class = "generic-center-theme"] | .//*[@class = "generic-right-theme"]'
    _super_button = 'xpath=.//*[@data-crlat="quickLink.section"]'

    @property
    def cta_alignment(self):
        cta_we_class = ComponentBase(selector=self._cta_alignment)._we.get_attribute("class")
        if cta_we_class == CTA_ENUM.CENTER_ALIGNMENT.value:
            return "center"
        if cta_we_class == CTA_ENUM.RIGHT_ALIGNMENT.value:
            return "right"
        return None

    @property
    def super_button(self):
        return SuperButton(selector=self._super_button)

    def has_super_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._super_button,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

class SuperButton(ComponentBase):
    _description = 'xpath=.//*[@data-crlat="description"]'
    _button = 'xpath=.//*[@data-crlat="button"]'

    @property
    def description(self):
        return self._get_webelement_text(selector=self._description, timeout=1)

    @property
    def button(self):
        return ButtonBase(selector=self._button, context=self._we, timeout=3)

    @property
    def theme(self):
        super_button_class = self._we.get_attribute("class")
        if not super_button_class:
            raise VoltronException("Could Not Retrieve Theme Class of Super Button")
        super_button_class_items: List[str] = super_button_class.split("-")
        theme = list(filter(lambda class_items: "theme".lower() in class_items.lower(), super_button_class_items))[0]
        return theme

    def has_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._button,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
