from collections import OrderedDict

from voltron.pages.shared.components.banner_section import BannerSection
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class OfferLink(LinkBase):
    _image = 'xpath=.//*[@data-crlat="offerImage"]'
    _no_image = 'xpath=.//*[@data-crlat="noImage"]'

    @property
    def image(self):
        return ComponentBase(self._image, timeout=1, context=self._we)

    def has_image(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._image,
                                                   timeout=0) is not None,
            name=f'Image status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def no_image(self):
        return ComponentBase(self._no_image, timeout=1, context=self._we)

    def has_no_image(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._no_image,
                                                   timeout=0) is not None,
            name=f'No image status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class OfferSlide(ComponentBase):
    _link = 'xpath=.//*[@data-crlat="offerLink"]'
    _link_type = OfferLink

    @property
    def link(self):
        return self._link_type(selector=self._link, context=self._we)


class ArrowButton(ButtonBase):

    def _wait_button_to_be_displayed(self, timeout=0):
        """In order to disable scrolling"""
        pass

    def click(self, scroll_to=False):
        try:
            super().click(scroll_to)
        except VoltronException:
            self._we = self._find_myself()
            super().click(scroll_to)


class OffersSection(BannerSection):
    _item = 'xpath=.//*[@data-crlat="offerSlide"]'
    _list_item_type = OfferSlide
    _slide_container = 'xpath=.//*[@data-crlat="slidecontainer"]'
    _left_arrow = 'xpath=.//*[@data-crlat="lArrow"]'
    _right_arrow = 'xpath=.//*[@data-crlat="rArrow"]'

    @property
    def left_arrow(self):
        return ArrowButton(selector=self._left_arrow, context=self._we)

    @property
    def right_arrow(self):
        return ArrowButton(selector=self._right_arrow, context=self._we)

    def has_left_arrow(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._left_arrow,
                                                   timeout=0) is not None,
            name=f'Left arrow status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_right_arrow(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._right_arrow,
                                                   timeout=0) is not None,
            name=f'Right arrow status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict({items_we.index(item_we): self._list_item_type(web_element=item_we)
                                          for item_we in items_we})
        return items_ordered_dict

    def get_active_offer_number(self):
        container = self._find_element_by_selector(selector=self._slide_container, context=self._we)
        if not container:
            raise VoltronException('Cannot find slide container')

        transform_translate_value = container.get_attribute('style')

        self._logger.debug(f'Element\'s attribute "style" is "{transform_translate_value}"')

        # attribute example - style="transform: translate3d(-100%, 0px, 0px);"
        value = transform_translate_value.replace('transform: translate3d(-', '').split('00%')[0]

        return value
