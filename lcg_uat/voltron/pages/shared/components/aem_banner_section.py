import re
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.banner_section import BannerSection
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from collections import OrderedDict


class AEMBanner(ComponentBase):
    _banner_url = 'xpath=.//a[@target]'
    _terms = 'xpath=.//*[@data-crlat="banner-terms"]'
    _image = 'xpath=.//img[contains(@class, "lc-offer__image")]'

    @property
    def width(self):
        size = self._we.size
        return size['width'] if size else 0

    @property
    def url(self):
        we = self._find_element_by_selector(selector=self._banner_url, timeout=5)
        if we:
            return we.get_attribute('href')
        return ''

    @property
    def target(self):
        we = self._find_element_by_selector(selector=self._banner_url, timeout=5)
        if we:
            return we.get_attribute('target')
        return ''

    @property
    def name(self):
        return self.url

    def has_terms(self, timeout=4, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._terms, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'{self.__class__.__name__} – Terms displayed status to be "{expected_result}"'
                               )

    @property
    def terms_and_conditions_text(self):
        text = self._get_webelement_text(selector=self._terms, timeout=2)
        if text:
            terms = re.compile(r'<[^>]+>').sub('', text)
            return terms
        return ''

    @property
    def terms_and_conditions_url(self):
        we = self._find_element_by_selector(selector=self._terms, timeout=2)
        if we:
            return we.get_attribute('href')
        return ''

    @property
    def image_url(self):
        we = self._find_element_by_selector(selector=self._image)
        if we:
            return we.get_attribute('src')
        return ''


class AEMBannerSection(BannerSection):
    _item = 'xpath=.//slide[not(contains(@class, "copy"))]'
    _all_items = 'xpath=.//div[contains(@class, "swiper-slide")]'
    _list_item_type = AEMBanner
    _active_banner = 'xpath=.//slide[contains(@class, "swiper-slide-active")]'
    _next_banner = 'xpath=.//div[contains(@class, "swiper-slide") and contains(@class, "next")]'
    _prev_banner = 'xpath=.//div[contains(@class, "swiper-slide") and contains(@class, "prev") and not(contains(@class, "duplicate"))]'
    _progress_bar = 'xpath=.//div[@class="lc-carousel__timer"]'
    _timer = 'xpath=.//*[contains(@style,"animation-duration")]'
    _arrow_previous = 'xpath=.//*[@class="lc-carousel__prev"] | .//*[@class="lc-carousel__prev arrow-chevron"]'
    _arrow_next = 'xpath=.//*[@class="lc-carousel__next"] | .//*[@class="lc-carousel__next arrow-chevron"]'
    _slide_container = 'tag=slidecontainer'
    _slide_buttons = 'xpath=.//*[@data-crlat="slideDotContainer"]'
    _non_active_slide_buttons = 'xpath=.//*[@data-crlat="slideDotContainer" and not(contains(@class, "slide-active"))]'

    # For Desktop
    @property
    def has_arrow_previous(self):
        return self._find_element_by_selector(selector=self._arrow_previous, timeout=1) is not None

    # For Desktop
    @property
    def arrow_previous(self):
        return ButtonBase(selector=self._arrow_previous, timeout=3)

    # For Desktop
    @property
    def arrow_next(self):
        return ButtonBase(selector=self._arrow_next, timeout=3)

    # For Desktop
    @property
    def has_arrow_next(self):
        return self._find_element_by_selector(selector=self._arrow_next, timeout=1) is not None

    # For Mobile
    @property
    def non_active_slide_buttons(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._non_active_slide_buttons, context=self._we,
                                                   timeout=self._timeout)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = ButtonBase(web_element=item_we)
            items_ordered_dict.update({items_we.index(item_we): list_item})
        return items_ordered_dict


    @property
    def number_of_banners(self):
        return len(self._find_elements_by_selector(selector=self._item))

    def has_progress_bar(self, expected_result=True, timeout=5):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._progress_bar, timeout=1) is not None,
                                 name=f'AEM banner tab progress bar status to be "{expected_result}"',
                                 expected_result=expected_result,
                                 timeout=timeout)
        return result

    @property
    def timer(self):
        we = self._find_element_by_selector(selector=self._timer)
        if we:
            find = re.search(r'(\d+)ms', we.get_attribute('style'))
            if not find:
                raise VoltronException('No timer value found')
            timer = find.groups()[0]
            return timer
        return 0

    @property
    def prev_banner_index(self):
        return int(self._find_element_by_selector(selector=self._prev_banner).get_attribute('data-swiper-slide-index'))

    @property
    def active_banner_index(self):
        wait_for_result(lambda: self.active_banner.is_displayed(timeout=0), name='Active banner to display', timeout=2)
        banner_position_we = self.active_banner._find_element_by_selector(selector='xpath=.//*[@data-position]')
        return int(banner_position_we.get_attribute('data-position'))

    @property
    def active_banner(self):
        return AEMBanner(selector=self._active_banner, context=self._we)

    @property
    def active_banner_name(self):
        wait_for_result(lambda: self.active_banner.is_displayed(timeout=2), name='Active banner to display', timeout=1)
        banner_position_we = AEMBanner(selector=self._active_banner)._find_element_by_selector(selector='xpath=.//a/img')
        return banner_position_we.get_attribute('alt')

    @property
    def next_banner_index(self):
        return int(self._find_element_by_selector(selector=self._next_banner).get_attribute('data-swiper-slide-index'))

    @property
    def calculated_aem_banner_width(self):
        we = self._find_element_by_selector(selector=self._slide_container, context=self._we)
        size = we.size
        return size['width'] if size else 0
