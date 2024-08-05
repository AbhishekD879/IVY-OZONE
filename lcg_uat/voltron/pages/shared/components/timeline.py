from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class Timeline(ComponentBase):
    _timeline_bubble = 'xpath=.//*[contains(@class, "timeline-bar ")]'
    _title = 'xpath=.//*[contains(@class, "timeline-bar ")]/div[@class="title"]'
    _timeline_slider = 'xpath=.//div[contains(@class,"slider-panel-overlay")]'
    _timeline_tutorial_overlay = 'xpath=.//*[@id="timeline-tutorial-overlay"]'
    _new_post_notification = 'xpath=.//*[@class="new-badge coral-badge-background" or @class="new-badge lads-badge-background"]'

    @property
    def timeline_bubble(self):
        return self._find_element_by_selector(selector=self._timeline_bubble, timeout=1)

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, timeout=2)

    def is_lounge_closed(self, timeout=5, expected_result=True):
        section = self._find_element_by_selector(selector=self._timeline_slider, context=self._we, timeout=2)
        if section:
            result = wait_for_result(lambda: 'closed' in section.get_attribute('class'),
                                     name=f'Drop down expand status to be "{expected_result}"',
                                     expected_result=expected_result,
                                     timeout=timeout)
            self._logger.debug(f'*** Timeline Bubble expanded status is {result}')
            return result
        else:
            return False

    @property
    def timeline_campaign(self):
        return TimelineCampaign(selector=self._timeline_slider, context=self._we)

    @property
    def timeline_splash_page(self):
        return SplashPage(selector=self._timeline_tutorial_overlay, timeout=5)

    @property
    def new_post_notification(self):
        return self._find_element_by_selector(selector=self._new_post_notification, timeout=1)

    @property
    def new_post_bg_color(self):
        return ComponentBase(selector=self._new_post_notification, context=self._we).background_color_value


class TimelinePostContainer(ComponentBase):
    _name = 'xpath=.//div[@class="timeline-post-title"]/span'
    _post_time = 'xpath=.//div[contains(@class,"timeline-post-time")]'
    _post_description = 'xpath=.//div[@class="timeline-post-description"]'
    _post_bet_prompt_header = 'xpath=.//div[@class="bet-text"]/span'
    _post_bet_button = 'xpath=.//button[@data-crlat="betButton"]'
    _post_odds_price = 'xpath=.//span[contains(@class,"odds-price")]'
    _post_icon = 'xpath=.//*[contains(@class,"timeline-post-icon")]'
    _post_redirection_link = 'xpath=.//*[@class="redirect-arrow"]'
    _post_spotlight = 'xpath=.//*[contains(@class,"timeline-post-spotlight")]'
    _post_verdict = 'xpath=.//*[contains(@class,"timeline-post-verdict")]'
    _post_yellow_header = 'xpath=.//*[contains(@class,"timeline-post-label yellow")]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=2)

    @property
    def post_time(self):
        return self._get_webelement_text(selector=self._post_time, timeout=2)

    @property
    def post_description(self):
        return self._get_webelement_text(selector=self._post_description, timeout=2)

    @property
    def post_spotlight(self):
        return self._get_webelement_text(selector=self._post_spotlight, timeout=2)

    @property
    def post_verdict(self):
        return self._get_webelement_text(selector=self._post_verdict, timeout=2)

    @property
    def post_bet_prompt_header(self):
        return self._get_webelement_text(selector=self._post_bet_prompt_header, timeout=2)

    @property
    def post_bet_button(self):
        return self._find_element_by_selector(selector=self._post_bet_button, context=self._we, timeout=2)

    @property
    def post_icon(self):
        return self._find_element_by_selector(selector=self._post_icon, timeout=2)

    @property
    def post_redirection_link(self):
        return self._find_element_by_selector(selector=self._post_redirection_link, timeout=2)

    @property
    def post_odds_price(self):
        return self._get_webelement_text(selector=self._post_odds_price, timeout=2)

    def bet_button_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        bet_button = self._find_element_by_selector(selector=self._post_bet_button, context=self._we, timeout=2)
        result = wait_for_result(lambda: 'active' in bet_button.get_attribute('class').strip(' ').split(' '),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result

    @property
    def bet_button_bg_color(self):
        return ComponentBase(selector=self._post_bet_button, context=self._we).background_color_value

    @property
    def post_yellow_header(self):
        return self._get_webelement_text(selector=self._post_yellow_header, timeout=2)


class TimelineCampaign(ComponentBase):
    _timeline_minimise = 'xpath=.//*[contains(@class, "minimise")]'
    _timeline_header = 'xpath=.//div[@class="timeline-title"]'
    _list_item_type = TimelinePostContainer
    _item = 'xpath=.//timeline-post/div[contains(@class,"timeline-post")]'
    _post_banner_color = 'xpath=.//timeline-post/div[contains(@class,"timeline-post blue-line")] | .//timeline-post/div[contains(@class,"timeline-post red-line")]'

    @property
    def timeline_minimise(self):
        return self._find_element_by_selector(selector=self._timeline_minimise, timeout=2)

    @property
    def timeline_header(self):
        return self._find_element_by_selector(selector=self._timeline_header, timeout=2)

    @property
    def post_banner_color(self):
        return self._find_element_by_selector(selector=self._post_banner_color, timeout=2)


class SplashPage(ComponentBase):
    _close_button = 'xpath=.//*[@class="tlt-close"]'
    _title = 'xpath=.//*[@class="title"]'
    _ok_thanks_button = 'xpath=.//*[contains(@class,"btn tlt-btn")]'
    _left_top_arrow = 'xpath=.//*[@class="tlt-arr top-arr"]'
    _left_bottom_arrow = 'xpath=.//*[@class="tlt-arr bottom-arr"]'
    _right_bottom_arrow = 'xpath=.//*[@class="tlt-arr bottom-arr bottom-arr--right"]'
    _phone_svg_img = 'xpath=.//*[contains(@class,"splash-img")]'

    @property
    def close_button(self):
        return self._find_element_by_selector(selector=self._close_button, timeout=2)

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, timeout=2)

    @property
    def ok_thanks_button(self):
        return self._find_element_by_selector(selector=self._ok_thanks_button, timeout=2)

    @property
    def left_top_arrow(self):
        return self._find_element_by_selector(selector=self._left_top_arrow, timeout=2)

    @property
    def left_bottom_arrow(self):
        return self._find_element_by_selector(selector=self._left_bottom_arrow, timeout=2)

    @property
    def right_bottom_arrow(self):
        return self._find_element_by_selector(selector=self._right_bottom_arrow, timeout=2)

    @property
    def phone_svg(self):
        return self._find_element_by_selector(selector=self._phone_svg_img, timeout=2)
