from collections import OrderedDict

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, retry_if_exception_type

from voltron.pages.coral.components.right_column_widgets.offers_widget_section import CoralOffersWidgetSection
from voltron.pages.shared import get_cms_config
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.right_column_widgets.favourites_widget_section import FavoritesWidgetSection
from voltron.pages.shared.components.right_column_widgets.in_play_widget import InPlayWidget
from voltron.pages.shared.components.right_column_widgets.mini_games_widget import MiniGamesWidget
from voltron.pages.shared.components.right_column_widgets.next_races_widget import NextRacesWidget
from voltron.pages.shared.components.right_column_widgets.right_column_item_widget import RightColumnItem
from voltron.pages.shared.contents.bet_receipt.bet_receipt import BetReceiptDesktop
from voltron.pages.shared.contents.betslip.betslip_desktop import BetSlipDesktop
from voltron.pages.shared.contents.in_shop import InShop
from voltron.pages.shared.contents.my_bets.bet_history.bet_history import BetHistoryDesktop
from voltron.pages.shared.contents.my_bets.cashout import CashoutDesktop
from voltron.pages.shared.contents.my_bets.open_bets.open_bets import OpenBetsDesktop
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class RightColumn(ComponentBase):
    _item = 'xpath=.//*[contains(@data-crlat, "widgetAccordion")]'
    _widget_accordion = 'xpath=.//*[@data-crlat="accordion"]'
    _betslip_widget_controller = 'xpath=.//*[contains(@data-crlat, "slideContent")]'
    _bet_receipt = 'xpath=.//*[@data-crlat="betslipReceipt"]'
    _list_item_type = RightColumnItem
    _offer_image = 'xpath=.//*[@data-crlat="offerImage"]'

    _slide_content_betslip = BetSlipDesktop
    _slide_content_cashout = CashoutDesktop
    _slide_content_open_bets = OpenBetsDesktop
    _slide_content_bet_history = BetHistoryDesktop
    _slide_content_inshop_bets = InShop

    widget_attributes = {'widgetAccordion.betslip': BetSlipDesktop,
                         'widgetAccordion.favourites': FavoritesWidgetSection,
                         'widgetAccordion.offers': CoralOffersWidgetSection,
                         'widgetAccordion.mini-games': MiniGamesWidget,
                         'widgetAccordion.in-play': InPlayWidget,
                         'widgetAccordion.next-races': NextRacesWidget,
                         'widgetAccordion.stream': InPlayWidget}

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._item,
                                           bypass_exceptions=(NoSuchElementException,))
        except StaleElementReferenceException:
            self._we = self._find_myself()

    def _controller_attributes(self):
        return {'slideContent.betslip': self._slide_content_betslip,
                'slideContent.cashOut': self._slide_content_cashout,
                'slideContent.1': self._slide_content_cashout,
                'slideContent.openBets': self._slide_content_open_bets,
                'slideContent.2': self._slide_content_open_bets,
                'slideContent.betHistory': self._slide_content_bet_history,
                'slideContent.3': self._slide_content_bet_history,
                'slideContent.inshopBets': self._slide_content_inshop_bets,
                'slideContent.4': self._slide_content_inshop_bets}

    def _get_widget_item_type(self, widget):
        widget_attributes = self.widget_attributes
        controller_attributes = self._controller_attributes()

        data_crlat_attribute = widget.get_attribute('data-crlat')
        if data_crlat_attribute in widget_attributes:
            if data_crlat_attribute == 'widgetAccordion.betslip':
                controller = self._find_element_by_selector(selector=self._betslip_widget_controller, context=widget, timeout=1)
                if controller:
                    controller_attribute = controller.get_attribute('data-crlat')
                    if controller_attribute in controller_attributes:
                        # now controller_attribute is the same for betslip and betreceipt
                        if wait_for_result(lambda: self._find_element_by_selector(selector=self._bet_receipt,
                                                                                  context=widget, timeout=0) is not None,
                                           name=f'Widget status to be "True"',
                                           expected_result=True,
                                           timeout=1):
                            widget_type = BetReceiptDesktop
                        else:
                            widget_type = controller_attributes[controller_attribute]
                        self._logger.debug('*** Recognized "%s" widget type by controller "%s"' % (widget_type.__name__, controller_attribute))
                    else:
                        widget_type = BetSlipDesktop
                        self._logger.warning('*** As controller type is not recognized by attribute "%s" returning default "%s" type'
                                             % (controller_attribute, widget_type.__name__))
                else:
                    widget_type = RightColumnItem
            else:
                widget_type = widget_attributes[data_crlat_attribute]
            self._logger.debug('*** Recognized "%s" widget type by attribute "%s"' % (widget_type.__name__, data_crlat_attribute))

        else:
            widget_type = RightColumnItem
            self._logger.warning('*** As widget type is not recognized by attribute "%s" returning default "%s" type'
                                 % (data_crlat_attribute, widget_type.__name__))

        widget_item = widget_type(web_element=widget)
        return widget_item.name, widget_item

    @property
    @retry(stop=stop_after_attempt(2), retry=retry_if_exception_type(StaleElementReferenceException), reraise=True)
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict([self._get_widget_item_type(widget=item_we) for item_we in items_we])
        return items_ordered_dict

    @property
    def bet_slip_widget(self):
        widgets = self.items_as_ordered_dict
        cms = get_cms_config()

        widget = widgets.get(cms.constants.BETSLIP_WIDGET_NAME)
        if widget:
            return widget
        raise VoltronException(f'{cms.constants.BETSLIP_WIDGET_NAME} widget was not found among "%s" widgets' % ', '.join(widgets.keys()))

    @property
    def offer_image_link(self):
        return self._find_element_by_selector(selector=self._offer_image, timeout=1).get_attribute('alt')
