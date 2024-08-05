from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.edp.racing_edp_market_section import StarContainer
from voltron.utils.waiters import wait_for_result


class RacePostVerdictOverlayHeader(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="verdict"]'
    _close_button = 'xpath=.//*[@data-crlat="drawer.closeButton"]'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)


class VerdictHorse(StarContainer):
    _name = 'xpath=.//*[@data-crlat="itemName"]'
    _star_container = 'xpath=.//*[@data-crlat="starsContainer"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)

    def has_star_container(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._star_container, timeout=0) is not None,
            name=f'Star container displayed status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)


class RacingPostRating(ComponentBase):
    _title = 'xpath= .//*[@data-crlat="header"]'
    _item = 'xpath=  .//*[@data-crlat="item"]'
    _list_item_type = VerdictHorse

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, context=self._we)


class MostTipped(RacingPostRating):
    _title = 'xpath= .//*[@data-crlat="header"]'
    _item = 'xpath=  .//*[@data-crlat="item"]'
    _list_item_type = TextBase

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, context=self._we)


class RacingPostTips(RacingPostRating):
    _list_item_type = TextBase


class RacePostVerdictOverlay(ComponentBase):
    _header = 'xpath=.//*[@data-crlat="drawer.header"]'
    _overlay = 'xpath=//*[@data-crlat="drawer.content"]'
    _header_type = RacePostVerdictOverlayHeader
    _racing_post_rating = 'xpath=.//*[@data-crlat="ratingSec"][contains(@class,"rating-section")]'
    _most_tipped = 'xpath=.//*[@data-crlat="ratingSec"][contains(@class,"most-tipped")]'
    _most_tipped_type = MostTipped
    _racing_post_rating_type = RacingPostRating
    _racing_post_tips = 'xpath=.//*[@data-crlat="tipsSec"]'
    _racing_post_tips_type = RacingPostTips
    _summary = 'xpath=.//*[@data-crlat="verdictInfo"]'
    _course_map_location = 'xpath=.//*[@data-crlat="verdictInfo"]/following-sibling::img'

    @property
    def header(self):
        return self._header_type(selector=self._header, context=self._we)

    @property
    def racing_post_rating(self):
        return self._racing_post_rating_type(selector=self._racing_post_rating, context=self._we)

    @property
    def most_tipped(self):
        return self._most_tipped_type(selector=self._most_tipped, context=self._we)

    @property
    def racing_post_tips(self):
        return self._racing_post_tips_type(selector=self._racing_post_tips, context=self._we)

    @property
    def summary(self):
        return TextBase(selector=self._summary, context=self._we)

    def is_at_bottom(self, timeout=1, expected_result=True):
        section = self._find_element_by_selector(selector=self._overlay, context=self._we)
        result = wait_for_result(lambda: 'bottom ' in section.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Racing post verdict overlay position',
                                 expected_result=expected_result,
                                 timeout=timeout)
        result = result if result else False
        return result

    def is_coursemap_located_after_verdict(self):
        section = self._find_element_by_selector(selector=self._course_map_location, context=self._we)
        result = True if section else False
        return result


class RacePostVerdictOverlayDesktop(RacePostVerdictOverlay):
    _header = 'xpath=.//*[@data-crlat="racingPost.logo"]'
    _course_map = 'xpath=.//*[@data-crlat="map"]'
    _course_map_location = 'xpath=.//*[@data-crlat="tipsSec"]/following-sibling::img'

    @property
    def header(self):
        return self._find_element_by_selector(selector=self._header, context=self._we)

    @property
    def course_map(self):
        return ComponentBase(selector=self._course_map).get_attribute('src')

    def is_coursemap_at_bottom(self):
        section = self._find_element_by_selector(selector=self._course_map_location, context=self._we)
        result = True if section else False
        return result
