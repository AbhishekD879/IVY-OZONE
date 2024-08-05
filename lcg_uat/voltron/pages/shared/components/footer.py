from voltron.pages.shared.components.base import ComponentBase
from collections import OrderedDict


class FooterNavLogoItems(ComponentBase):
    _name = 'xpath=.//a/img | .//*[contains(@class,"menu-item-link footer-nav-link")]/img'

    @property
    def name(self):
        return self._find_element_by_selector(selector=self._name, timeout=0).get_attribute('alt')


class FooterNavLogo(ComponentBase):
    _item = 'xpath=.//*[@imageclass="footer-nav-link-img"]'
    _list_item_type = FooterNavLogoItems
    _game_stop = 'xpath=.//*[contains(@alt,"gamstop")]/ancestor::a'

    @property
    def game_stop(self):
        return self._find_element_by_selector(selector=self._game_stop, context=self._we)


class HelpInformationItems(ComponentBase):
    _name = 'xpath=.//*[contains(@class,"menu-item-link footer-nav-link")]/span'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)


class HelpInformation(ComponentBase):
    _item = 'xpath=.//*[@class="menu-item"]'
    _title = 'xpath=.//*[@class="footer-menu-section-title"]'
    _list_item_type = HelpInformationItems

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, context=self._we)


class FooterFollowUsItems(ComponentBase):
    _name = 'xpath=.//*[@class="social-content"]//img'

    @property
    def name(self):
        return self._find_element_by_selector(selector=self._name, timeout=0).get_attribute('alt')


class FooterFollowUs(ComponentBase):
    _item = 'xpath=.//*[@class="social-content"]/a'
    _list_item_type = FooterFollowUsItems


class FooterContentPayment(ComponentBase):
    _item = 'xpath=.//*[@class="footer-payment-logo"]'
    _footer_follow_up = 'xpath=.//*[@class="social-wrapper"]'
    _footer_connect = 'xpath=.//*[@class="coral-connect-wrapper"]//div[@class="social-content"]//img'
    _footer_text = 'xpath=.//*[@data-id="uklicence"]//vn-pc-text//*[@class="pc-txt"]'
    _footer_help_info = 'xpath=.//a[contains(text(),"Help & Information")]'
    _payment_methods_list = 'xpath=.//*[@class="footer-payment-logo"]'
    _ref_links = 'xpath=.//p/a'
    _title = 'xpath=.//*[@class="social-title"]'

    @property
    def footer_follow_up_section(self):
        return FooterFollowUs(selector=self._footer_follow_up, context=self._we)

    @property
    def text_links_dict(self):
        elements = self._find_elements_by_selector(selector=self._ref_links)
        item_dict = OrderedDict()
        for element in elements:
            item_we = element.text
            item_dict.update({item_we: element})
        return item_dict

    @property
    def payment_methods_dict(self):
        elements = self._find_elements_by_selector(selector=self._payment_methods_list)
        item_dict = OrderedDict()
        for element in elements:
            item_we = element.get_attribute('alt')
            item_dict.update({item_we: element})
        return item_dict

    @property
    def footer_connect(self):
        we = self._find_element_by_selector(selector=self._footer_connect, timeout=5)
        self.scroll_to_we(we)
        return we

    @property
    def footer_text(self):
        we = self._find_element_by_selector(selector=self._footer_text, timeout=5)
        self.scroll_to_we(we)
        return we

    @property
    def footer_help(self):
        we = self._find_element_by_selector(selector=self._footer_help_info)
        self.scroll_to_we(we)
        return we

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, timeout=3)


class FooterHelp(ComponentBase):
    _sub_header_title = 'xpath=.//*[@class="navigation-menu sub-menu"]//header'

    @property
    def sub_header_help(self):
        return self._find_element_by_selector(selector=self._sub_header_title)


class Footer(ComponentBase):
    _footer_bottom_section = 'xpath=.//*[@class="footer-nav-logos"]'
    _footer_up_section = 'xpath=.//div[@class="footer-nav-seo-container"]'
    _footer_content = 'xpath=.//div[@class="content-message-container"]'
    _copy_right = 'xpath=.//vn-f-copyright'

    def __init__(self, *args, **kwargs):
        super(Footer, self).__init__(*args, **kwargs)
        self.scroll_to_we(web_element=self._we)

    @property
    def footer_section_top(self):
        return HelpInformation(selector=self._footer_up_section, context=self._we)

    @property
    def footer_section_bottom(self):
        return FooterNavLogo(selector=self._footer_bottom_section, context=self._we)

    @property
    def footer_content_section(self):
        return FooterContentPayment(selector=self._footer_content, context=self._we)

    @property
    def footer_copy_right(self):
        return self._find_element_by_selector(selector=self._copy_right, timeout=5)

    @property
    def is_time_panel_shown(self, timeout=1, expected_result=True):
        raise NotImplementedError(f'Time Panel is not present on {self.__class__.__name__}')

    @property
    def time_panel(self):
        raise NotImplementedError(f'Time Panel is not present on {self.__class__.__name__}')

    @property
    def responsible_gambling_link(self):
        raise NotImplementedError(f'Responsible Gambling is not present on {self.__class__.__name__}')

    @property
    def links(self):
        raise NotImplementedError(f'Links section is not present on {self.__class__.__name__}')
