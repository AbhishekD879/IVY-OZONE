from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.dialogs.dialog_base import DialogHeader
from voltron.utils.waiters import wait_for_result


class CouponItem(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="couponName" or @data-crlat="item-title"]'
    _coupon_dialog = 'xpath=.//*[@id="onboarding-overlay"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=2)

    @property
    def coupon_dialog(self):
        return DialogHeader(selector=self._coupon_dialog,timeout=2)


class CouponItemDesktop(CouponItem):
    _name = 'xpath=.//*[@data-crlat="couponName"]'


class SportsCouponsAccordionsList(Accordion):
    _name = 'xpath=./preceding::header[1]'
    _item = 'xpath=.//*[@data-crlat="couponItem"]'
    _list_item_type = CouponItem

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=2)

    def _wait_active(self, timeout=5):
        wait_for_result(lambda: self._find_elements_by_selector(selector=self._item, context=self._we, timeout=0),
                        name='Coupons to be loaded',
                        timeout=timeout)


class CouponsCategories(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="couponContainer"]'
    _list_item_type = SportsCouponsAccordionsList


class CouponsEventGroup(EventGroup):
    pass


class CouponsAccordionList(AccordionsList):
    _list_item_type = CouponsEventGroup


class CouponsTabContent(TabContent):
    _coupons_categories_locators = 'xpath=.//*[@class="heuristic-container"]'
    _accordions_list_type = CouponsCategories
    _bet_filter_link = 'xpath=.//*[@data-crlat="betFilterLink"]'
    _verify_spinner = True

    @property
    def bet_filter_link(self):
        return ComponentBase(selector=self._bet_filter_link, timeout=1)

    @property
    def coupons_categories(self):
        return CouponsAccordionList(selector=self._coupons_categories_locators)
