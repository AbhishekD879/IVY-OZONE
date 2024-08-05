from voltron.pages.ladbrokes.components.one_two_free_current_tab_page import EventItemContainer, WeeksResultsTabsList, \
    MyBadges, LastWeekResults
from voltron.pages.ladbrokes.components.one_two_free_you_are_in_page import UpCellMarketItemContainer
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import ComponentContent
from collections import OrderedDict
from voltron.utils.waiters import wait_for_result


class OneTwoFreeWelcomeScreen(ComponentContent):
    _logo = 'xpath=.//*[@data-crlat="logo"]'
    _play_button = 'xpath=.//*[@data-crlat="play"]'
    _cancel_button = 'xpath=.//*[@data-crlat="cancel"]'
    _welcome_text = 'xpath=.//*[@data-crlat="text"]'
    _submit_button = 'xpath=.//*[contains(@class,"btnCta")]'
    _back_icon = 'xpath=//*[@data-crlat="btnBack"]'

    @property
    def logo(self):
        return ButtonBase(selector=self._logo, context=self._we)

    @property
    def play_button(self):
        return ButtonBase(selector=self._play_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def text(self):
        return self._get_webelement_text(selector=self._welcome_text, context=self._we)

    @property
    def back_icon(self):
        return ButtonBase(selector=self._back_icon, context=self._we)


class OneTwoFreeCurrentScreen(ComponentContent):
    _submit_button = 'xpath=.//*[contains(@class,"btnCta")]'
    _close = 'xpath=.//*[@id="close"]'
    _item = 'xpath=.//*[contains(@class,"eventInfoRespWrap")] | .//*[contains(@class,"slideItem")]'
    _already_in_text = 'xpath=.//*[contains(@class,"pageContent ")]//p'
    _list_item_type = EventItemContainer
    _back_icon = 'xpath=//*[@data-crlat="btnBack"]'
    _tab_content = 'xpath=.//*[contains(@class,"tabsSwitcherContainer")]'
    _my_badges_tab_content = 'xpath=.//*[contains(@class,"tabsWrapper")]'

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({f'{items_we.index(item_we)} {list_item.name}': list_item})
        return items_ordered_dict

    @property
    def submit_button(self):
        return ButtonBase(selector=self._submit_button, context=self._we)

    def has_submit_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._submit_button, timeout=0) is not None,
                               name=f'"Submit" button shown status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def close(self):
        return ButtonBase(selector=self._close, context=self._we)

    @property
    def already_entered_text(self):
        return self._find_element_by_selector(selector=self._already_in_text)

    @property
    def back_icon(self):
        return ButtonBase(selector=self._back_icon, context=self._we)

    @property
    def tab_items(self):
        return WeeksResultsTabsList(selector=self._tab_content, context=self._we)

    @property
    def my_badges(self):
        return MyBadges(selector=self._my_badges_tab_content, context=self._we)

    @property
    def last_week_results(self):
        return LastWeekResults(selector=self._my_badges_tab_content, context=self._we)

class OneTwoFreeYouAreInShareButton(ComponentContent):
    _share_button = 'xpath=.//*[@id="intialiseShareFonts"]/parent::div'
    _share_text = 'xpath=.//*[@id="intialiseShareFonts"]/following-sibling::p/span'
    _share_logo = 'xpath=.//*[@id="intialiseShareFonts"]/following-sibling::p/img[@data-crlat="otf-share-ios-icon"]'

    @property
    def share_logo(self):
        return self._find_element_by_selector(selector=self._share_logo)

    @property
    def share_text(self):
        return self._find_element_by_selector(selector=self._share_text)

    @property
    def share_button(self):
        return ButtonBase(selector=self._share_button, context=self._we)


class OneTwoFreeYouAreIn(ComponentContent):
    _close = 'xpath=.//*[@class="close"]'
    _item = 'xpath=.//*[contains(@class,"upsellSlider")]'
    _list_item_type = UpCellMarketItemContainer
    _you_are_in_img = 'xpath=.//*[contains(@class,"youAreIn")]//img'
    _back_to_betting_button = 'xpath=.//*[contains(@class,"backBtn")]//button'
    _view_my_badge_button = 'xpath=.//*[contains(@class,"ViewYourBadgesCtaButton")]'
    _share_button = 'xpath=.//*[@id="intialiseShareFonts"]/parent::div'

    @property
    def close(self):
        return ButtonBase(selector=self._close, context=self._we)

    @property
    def back_to_betting_button(self):
        return ButtonBase(selector=self._back_to_betting_button, context=self._we)

    @property
    def view_my_badge_button(self):
        return ButtonBase(selector=self._view_my_badge_button, context=self._we)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({f'{items_we.index(item_we)} {list_item.market_header}': list_item})
        return items_ordered_dict

    def has_you_are_in_icon_shown(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._you_are_in_img, timeout=1),
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def share_button_container(self):
        return OneTwoFreeYouAreInShareButton(selector=self._share_button, context=self._we)


class OneTwoFreePrimaryBadge(ComponentContent):
    _title = 'xpath=.//*[contains(@class,"congratsHeader")]'
    _description = 'xpath=.//*[contains(@class,"congratsMessage")]'
    _exit = 'xpath=.//button[contains(@class,"closePopup")]'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, timeout=5)

    @property
    def description(self):
        return self._get_webelement_text(selector=self._description, timeout=5)

    @property
    def exit_button(self):
        return ButtonBase(selector=self._exit, timeout=5)


class OneTwoFreeSecondaryBadge(OneTwoFreePrimaryBadge):
    pass


class OneTwoFree(ComponentContent):
    _url_pattern = r'^http[s]?:\/\/.+\/1-2-free'
    _one_two_free_welcome_screen = 'xpath=.//*[@data-crlat="stepOne"]'
    _one_two_free_current_screen = 'xpath=.//*[@id="CurrentTabStep"]'
    _one_two_free_you_are_in = 'xpath=.//*[contains(@class,"youAreIn")]'
    _login_to_play_button = 'xpath=.//button[@class="otf-login-btn otf-btn"]'
    _login_page_cancel_button = 'xpath=.//button[@class="otf-btn otf-cancel-login-btn"]'
    _my_badges_popup = 'xpath=.//*[contains(@class,"modal_content")]'

    @property
    def one_two_free_welcome_screen(self):
        return OneTwoFreeWelcomeScreen(selector=self._one_two_free_welcome_screen)

    @property
    def one_two_free_current_screen(self):
        return OneTwoFreeCurrentScreen(selector=self._one_two_free_current_screen)

    @property
    def one_two_free_you_are_in(self):
        return OneTwoFreeYouAreIn(selector=self._one_two_free_you_are_in)

    @property
    def login_to_play_button(self):
        return ButtonBase(selector=self._login_to_play_button, context=self._we)

    @property
    def login_page_cancel_button(self):
        return ButtonBase(selector=self._login_page_cancel_button, context=self._we)

    @property
    def primary_badge_popup(self):
        return OneTwoFreePrimaryBadge(selector=self._my_badges_popup, context=self._we)

    @property
    def secondary_badge_popup(self):
        return OneTwoFreeSecondaryBadge(selector=self._my_badges_popup, context=self._we)
