from collections import OrderedDict
from selenium.common.exceptions import NoSuchElementException
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.accordions_container import AccordionHeader
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import RacingBetButton
from voltron.pages.shared.contents.base_contents.common_base_components.promotion_icons import PromotionIcons
from voltron.pages.shared.contents.my_stable.my_stable_page import MyStableNotes
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class ShowDetails(ComponentBase):
    _horse_name_details = 'xpath=.//*[contains(@data-crlat, "horseNameDetails")]'
    _jockey_name_details = 'xpath=.//*[@data-crlat="jockeyNameDetails"]'
    _trainer_name_details = 'xpath=.//*[@data-crlat="trainerNameDetails"]'
    _form_details = 'xpath=.//*[@data-crlat="formGuideDetails"]'
    _age_details = 'xpath=.//*[@data-crlat="ageDetails"]'
    _weight_details = 'xpath=.//*[@data-crlat="weightDetails"]'
    _stall_no_details = 'xpath=.//*[@data-crlat="stallDetails"]'
    _rating_details = 'xpath=.//*[@data-crlat="ratingDetails"]'

    @property
    def horse_name(self):
        return self._get_webelement_text(self._horse_name_details, timeout=0, context=self._we)

    @property
    def jockey_name(self):
        return self._get_webelement_text(self._jockey_name_details, timeout=0, context=self._we)

    @property
    def trainer_name(self):
        return self._get_webelement_text(self._trainer_name_details, timeout=0, context=self._we)

    @property
    def form(self):
        return self._get_webelement_text(self._form_details, timeout=0, context=self._we)

    @property
    def age(self):
        return self._get_webelement_text(self._age_details, timeout=0, context=self._we)

    @property
    def stall_no(self):
        return self._get_webelement_text(self._stall_no_details, timeout=0, context=self._we)

    @property
    def rating(self):
        return self._get_webelement_text(self._rating_details, timeout=0, context=self._we)

    @property
    def weight(self):
        return self._get_webelement_text(self._weight_details, timeout=0, context=self._we)


class Spotlight(ComponentBase):
    _show_summary = 'xpath=.//*[@data-crlat="racingSpotlight.showSummary"]'

    @property
    def show_summary_button(self):
        return ButtonBase(self._show_summary, timeout=0, context=self._we)

    def has_show_summary_button(self, expected_result=True, timeout=1, poll_interval=0.5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._show_summary,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Show summary button status to be {expected_result}',
                               poll_interval=poll_interval)

class YourNotes(ComponentBase):
    _header_text = 'xpath=.//*[@data-crlat="notes"]'
    _notes_text = 'xpath=.//*[@data-crlat="notes"]/following-sibling::*'

    @property
    def header_text(self):
        return self._get_webelement_text(selector=self._header_text, context=self._we)

    @property
    def notes_text(self):
        return self._get_webelement_text(selector=self._notes_text, context=self._we)


class ExpandedSummary(ComponentBase):
    _summary_button = 'xpath=.//*[@data-crlat="buttonSummary"]'
    _details_button = 'xpath=.//*[@data-crlat="buttonDetails"]'
    _outcome_overview = 'xpath=.//*[@data-crlat="outcomeOverview"]'
    _spotlight_info = 'xpath=.//*[@data-crlat="spotlightInfo"]'
    _spotlight_info_type = Spotlight
    _last_run = 'xpath=.//*[@class="runner-lastrun-details"]'
    _last_run_table = 'xpath=.//*[@class="horse-form-table"]'
    _show_details = 'xpath=.//*[@data-crlat="noDetails"]'
    _show_details_type = ShowDetails
    _last_run_item = 'xpath=.//*[@class="horse-form-table"]/tr'
    _last_run_label = 'xpath=.//*[@class="runner-lastrun-details"]/*[contains(text(), "Last Run")]'
    _last_run_text = 'xpath=.//*[@class="runner-lastrun-details"]/p'
    _last_run_table_header_info = 'xpath=.//*[@class="horse-form-table"]/tr/th'
    _last_run_table_data_info = 'xpath=.//*[@class="horse-form-table"]/tr/td'
    _my_stable_your_notes = 'xpath=.//*[@data-crlat="mystableNotes"]'
    _my_stable_your_notes_type = YourNotes

    @property
    def my_stable_your_notes(self):
        return self._my_stable_your_notes_type(selector=self._my_stable_your_notes)

    @property
    def last_run_item_details(self):
        return self._find_elements_by_selector(selector=self._last_run_item, context=self._we, timeout=self._timeout)

    @property
    def outcome_overview(self):
        return self._get_webelement_text(selector=self._outcome_overview)

    @property
    def has_summary_button(self):
        return self._find_element_by_selector(selector=self._summary_button, timeout=0) is not None

    @property
    def summary_button(self):
        return self._find_element_by_selector(selector=self._summary_button)

    @property
    def has_details_button(self):
        return self._find_element_by_selector(selector=self._details_button, timeout=0) is not None

    @property
    def details_button(self):
        we = self._find_element_by_selector(selector=self._details_button, context=self._we)
        self.scroll_to_we(web_element=we)
        return ButtonBase(web_element=we)

    @property
    def show_details(self):
        return self._show_details_type(selector=self._show_details, context=self._we)

    @property
    def spotlight_info(self):
        return self._spotlight_info_type(selector=self._spotlight_info, context=self._we)

    @property
    def has_spotlight_info(self, expected_result=True, timeout=1, poll_interval=0.5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._spotlight_info,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Show spotlight info status to be {expected_result}',
                               poll_interval=poll_interval)

    @property
    def last_run_info(self):
        return self._find_element_by_selector(selector=self._last_run, context=self._we)

    @property
    def last_run_info_label(self):
        return ComponentBase(selector=self._last_run_label, timeout=2, context=self._we)

    @property
    def last_run_info_text(self):
        return ComponentBase(selector=self._last_run_text, timeout=2, context=self._we)

    @property
    def has_last_run_info(self, expected_result=True, timeout=1, poll_interval=0.5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._last_run,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Show lastrun info status to be {expected_result}',
                               poll_interval=poll_interval)

    @property
    def has_last_run_table_info(self, expected_result=True, timeout=1, poll_interval=0.5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._last_run_table, timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Show lastrun info status to be {expected_result}',
                               poll_interval=poll_interval)

    @property
    def last_run_table_header_info(self):
        return ComponentBase(selector=self._last_run_table_header_info, timeout=2, context=self._we)

    @property
    def last_run_table_data_info(self):
        return ComponentBase(selector=self._last_run_table_data_info, timeout=2, context=self._we)


class OddItem(ComponentBase):
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'
    _previous_price = 'xpath=.//*[@data-crlat="previousPrices"]'

    @property
    def bet_button(self):
        return RacingBetButton(selector=self._bet_button, context=self._we, timeout=2)


    def has_bet_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._bet_button,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Bet button shown status to be {expected_result}')

    @property
    def name(self):
        if self.has_bet_button():
            return self.bet_button.name
        else:
            return ''

    @property
    def previous_price(self):
        return self._get_webelement_text(selector=self._previous_price)


class SummaryText(TextBase):

    @property
    def value(self):
        return self._get_webelement_text(we=self._we, timeout=0.5).replace('Show More', '').replace('Show Less',
                                                                                                    '').strip()

    def is_truncated(self, we=None, selector='', context=None):
        text = self.value
        if text:
            is_len_100 = True if len(text) <= 104 else False  # for mobile 100 symbols + 3 dots
            is_ended_with_dots = True if text[-3:] == '...' else False
            return is_len_100 and is_ended_with_dots
        return False


class SpotlightOverview(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="racing.spotlightTitle"] | .//*[@class="runner-spotlight-title"]'
    _official_rating = 'xpath=.//*[@data-crlat="racingFormOutcome.officialRating"]'
    _age = 'xpath=.//*[@data-crlat="racingFormOutcome.age"]'
    _weight = 'xpath=.//*[@data-crlat="racingFormOutcome.weight"]'
    _summery_text = 'xpath=.//*[@data-crlat="text"]'
    _show_summary_link = 'xpath=.//*[@data-crlat="racingSpotlight.showSummary"]'
    _course_distance_winner = 'xpath=.//*[@data-crlat="courseDistanceWinner"]'

    def has_summary_text(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._summery_text,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Runner comment status to be {expected_result}')

    @property
    def summary_text(self):
        return SummaryText(selector=self._summery_text, context=self._we)

    @property
    def show_summary_link(self):
        return LinkBase(selector=self._show_summary_link, context=self._we)

    def has_official_rating(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._official_rating,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Official Rating status to be {expected_result}')

    @property
    def spotlight_title(self):
        return TextBase(selector=self._title, context=self._we)

    @property
    def official_rating(self):
        return TextBase(selector=self._official_rating, context=self._we)

    @property
    def age(self):
        return TextBase(selector=self._age, context=self._we)

    @property
    def weight(self):
        return TextBase(selector=self._weight, context=self._we)

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, timeout=1)

    def has_course_distance_winner(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._course_distance_winner,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Course Distance Winner status to be {expected_result}')

    @property
    def course_distance_winner(self):
        return TextBase(selector=self._course_distance_winner, context=self._we)


class StarContainer(ComponentBase):
    _star_count = 'xpath=.//*[@data-crlat="stars"]'

    def get_star_rating(self, is_active=False):
        attr = 'active' if is_active else 'star-icon'
        stars = self._find_elements_by_selector(selector=self._star_count, context=self._we)
        rating = len([star for star in stars if attr in star.get_attribute('class')])
        return rating


class MyStableBookMark(ButtonBase):
    _tooltip_container = 'xpath=.//*[@class="tooltip-container-mybets"]'
    _go_to_my_stable = 'xpath=.//*[@class="tooltip-container-mybets"]/a'

    def is_tooltip_container_appear(self,expected_result=True, poll_interval=0.5, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._tooltip_container, context=self._we, timeout=0) is not None,
            name=f'{self.__class__.__name__} – My Stable Tooltip Container status to be {expected_result}',
            expected_result=expected_result,
            poll_interval=poll_interval,
            timeout=timeout)

    @property
    def error_msg(self):
        msg = self._get_webelement_text(selector=self._tooltip_container, context=self._we, timeout=0)
        link_text = self.go_to_my_stable_page_link.text
        res = msg.rstrip(link_text).strip('\n').strip()
        return res

    @property
    def go_to_my_stable_page_link(self):
        return LinkBase(selector=self._go_to_my_stable, context=self._we)


class MyBetsMyStableBookMark(MyStableBookMark):
    _tooltip_container = 'xpath=.//following-sibling::tooltip/*'
    _state = 'xpath=.//*[@class="bookmark"]/*'

    @property
    def is_bookmarked(self):
        book_mark_text = self._find_element_by_selector(selector=self._state, timeout=0,
                                                        context=self._we).get_attribute('xlink:href')
        return 'fill' in book_mark_text

    @property
    def tooltip_container_message(self):
        return self._get_webelement_text(selector=self._tooltip_container, context=self._we, timeout=0)


class Outcome(ComponentBase):
    _horse_name = 'xpath=.//*[@data-crlat="horseName"]'
    _jockey_name = 'xpath=.//*[@data-crlat="jockeyName"]'
    _trainer_name = 'xpath=.//*[@data-crlat="trainerName"]'
    _jockey_trainer_info = 'xpath=.//*[@data-crlat="jockeyAndTrainer"]'
    _course_distance_winner = 'xpath=.//*[@data-crlat="courseDistanceWinner"]'
    _form = 'xpath=.//*[@data-crlat="racingForm" or @class="timeform-label"]'
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'
    _output_price = 'xpath=.//*[@data-crlat="betButton"]'
    _previous_price = 'xpath=.//*[@data-crlat="previousPrices"]'
    _no_silks = 'xpath=.//*[contains(@data-crlat, "sectionSilkImg")]'
    _runner_number = 'xpath=.//*[@data-crlat="runnerNumber"]'
    _draw = 'xpath=.//*[@data-crlat="outcomeDraw"]'
    _silks = 'xpath=.//*[@data-crlat="imageSilk" or @data-crlat="gh-silk"]'
    _bespoke_silks = 'xpath=.//*[@data-crlat="imageSilk" and contains(@style, "background-image:")]'
    _show_summary_toggle = 'xpath=.//*[@data-crlat="toggleIcon"]'
    _expanded_summary = 'xpath=.//*[@data-crlat="spotlight" or @data-crlat="runnerSpotlight"]'
    _star_icons = 'xpath=.//*[@data-crlat="starsContainer"]'
    _expanded_summary_type = ExpandedSummary
    _spotlight_overview = 'xpath=.//*[@data-crlat="runnerSpotlight"]'
    _item = 'xpath=.//*[@data-crlat="marketEntity.outcomes"]'
    _non_runner = 'xpath=.//*[@data-crlat="nr"]'
    _list_item_type = OddItem
    # Get items from parent needed to avoid wrong odd assignment when some market have no selection
    _fixture_header_item = 'xpath=./..//*[@data-crlat="title"]'
    _stars = 'xpath=.//*[@data-crlat="starRating"]'
    _stars_container_type = StarContainer
    _my_stable_bookmark = 'xpath=.//*[@data-crlat="bsMystableBookmark"]'
    _my_stable_signposting = 'xpath=.//*[@data-crlat="myStableSignpostingSvg"]'
    _my_stable_notes_signposting = 'xpath=.//*[@data-crlat="myStableNotesSignpostingSvg"]'
    _my_stable_notes = 'xpath=.//*[@data-crlat="myStableNotes"]'
    _my_stable_bookmark_state = 'xpath=.//*[@data-crlat="bsMystableBookmark"]/*/*'

    @property
    def my_stable_notes(self):
        return MyStableNotes(selector=self._my_stable_notes, context=self._we)

    @property
    def my_stable_bookmark(self):
        return MyStableBookMark(selector=self._my_stable_bookmark, context=self._we)

    def has_my_stable_bookmark(self, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._my_stable_bookmark, context=self._we,
                                                   timeout=0) is not None, timeout=timeout)

    @property
    def is_bookmark_filled(self):
        book_mark_text = self._find_element_by_selector(selector=self._my_stable_bookmark_state, timeout=0,
                                                        context=self._we).get_attribute('xlink:href')
        return 'fill' in book_mark_text

    def fill_bookmark(self, notes=None):
        if not self.is_bookmark_filled:
            self.my_stable_bookmark.click()
            if notes:
                self.my_stable_notes.input_notes.value = notes
                self.my_stable_notes.save.click()
            else:
                self.my_stable_notes.cancel.click()

    def clear_bookmark(self):
        if self.is_bookmark_filled:
            self.my_stable_bookmark.click()

    @property
    def my_stable_sign_posting(self):
        return self._find_element_by_selector(selector=self._my_stable_signposting, context=self._we, timeout=0)

    def has_my_stable_notes_sign_posting(self, expected_result=True, poll_interval=0.5, timeout=5) -> bool:
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._my_stable_notes_signposting, context=self._we, timeout=0) is not None,
            name=f'{self.__class__.__name__} – My Stable  Notes Sign Posting status to be {expected_result}',
            expected_result=expected_result,
            poll_interval=poll_interval,
            timeout=timeout)

    def has_my_stable_sign_posting(self, expected_result=True, poll_interval=0.5, timeout=5) -> bool:
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._my_stable_signposting, context=self._we, timeout=0) is not None,
            name=f'{self.__class__.__name__} – My Stable shown status to be {expected_result}',
            expected_result=expected_result,
            poll_interval=poll_interval,
            timeout=timeout)

    @property
    def greyhound_runner_number(self):
        we = self._find_element_by_selector(selector=self._silks)
        return we.get_attribute("class")

    def has_spotlight_overview(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._spotlight_overview,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Spotlight overview shown status to be {expected_result}')

    @property
    def spotlight_overview(self):
        return SpotlightOverview(selector=self._spotlight_overview, context=self._we)

    @property
    def runner_number(self):
        return self._get_webelement_text(self._runner_number, timeout=0, context=self._we)

    @property
    def draw_number(self):
        return self._get_webelement_text(self._draw, timeout=0, context=self._we).replace('(', '').replace(')', '')

    @property
    def jockey_trainer_info(self):
        return self._get_webelement_text(selector=self._jockey_trainer_info, timeout=0, context=self._we)

    @property
    def jockey_name(self):
        return self.jockey_trainer_info.split('/')[0].strip()

    @property
    def trainer_name(self):
        return self.jockey_trainer_info.split('/')[1].lstrip()

    @property
    def trainer_label(self):
        return self.jockey_trainer_info.split(':')[0]

    @property
    def form_value(self):
        return self.form.split(':')[1].lstrip()

    @property
    def course_distance_winner(self):
        distances_names = []
        all_distances = self._find_elements_by_selector(selector=self._course_distance_winner, timeout=0, context=self._we)
        for distance in all_distances:
            distances_names.append(self._get_webelement_text(we=distance))
        return distances_names

    def has_course_distance_winner(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._course_distance_winner,
                                                                      timeout=0, context=self._we),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Course distance winner status to be {expected_result}')

    @property
    def is_non_runner(self):
        return self._find_element_by_selector(selector=self._non_runner, timeout=.5) is not None

    @property
    def has_silks(self):
        we = self._find_element_by_selector(selector=self._silks, timeout=.5)
        return we is not None and we.is_displayed()

    @property
    def has_bespoke_silks(self):
        return self._find_element_by_selector(selector=self._bespoke_silks, timeout=.5) is not None

    @property
    def has_no_silks(self):
        return self._find_element_by_selector(selector=self._no_silks, timeout=.5) is not None

    def has_stars(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._stars,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Star rating icon status to be {expected_result}')

    @property
    def stars_rating_value(self):
        return TextBase(selector=self._stars, context=self._we)

    def get_silk_attribute(self, attribute):
        we = self._find_element_by_selector(selector=self._silks)
        if not we:
            return None
        return we.get_attribute(attribute)

    @property
    def silk(self):
        return self.get_silk_attribute('style')

    @property
    def is_silk_generic(self):
        if not self.has_silks:
            raise VoltronException('No silk is displayed at all. Thus cannot tell if it\'s generic or not')
        if self.silk:
            return 'background-image' not in self.silk
        else:
            return True

    @property
    def form(self):
        we = self._find_element_by_selector(selector=self._form)
        if we is not None:
            return we.text
        else:
            raise VoltronException('No element matching {0} was found'.format(self._form))

    @property
    def horse_name(self):
        return self._get_webelement_text(self._horse_name, timeout=0, context=self._we)

    @property
    def name(self):
        return self.horse_name

    @property
    def bet_button(self):
        return RacingBetButton(selector=self._bet_button, context=self._we)

    @property
    def odds_button(self):
        return self._find_element_by_selector(selector=self._bet_button, timeout=2)

    @property
    def is_odds_button_disabled(self, expected_result=True, timeout=2):
        odds_button_status = wait_for_result(lambda: self._find_element_by_selector(selector=self._bet_button, timeout=2).get_attribute('disabled'),
                        name=f'odds button disabled status to be {expected_result}',
                        timeout=timeout,
                        expected_result=expected_result)
        return odds_button_status == 'true'

    @property
    def output_price(self):
        we = self._find_element_by_selector(selector=self._output_price)
        if we is not None:
            return we.text
        else:
            raise VoltronException('No element matching {0} was found'.format(self._output_price))

    @property
    def previous_price(self):
        return self._get_webelement_text(self._previous_price)

    def has_previous_price(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._previous_price,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Has previous price status to be {expected_result}')

    def has_show_summary_toggle(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._show_summary_toggle,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Expanded summary shown status to be {expected_result}')

    @property
    def show_summary_toggle(self):
        return ButtonBase(selector=self._show_summary_toggle, context=self._we)

    def has_expanded_summary(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._expanded_summary,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Expanded summary shown status to be {expected_result}')

    @property
    def expanded_summary(self):
        return self._expanded_summary_type(selector=self._expanded_summary, context=self._we)

    @property
    def toggle_icon_name(self):
        return self._get_webelement_text(self._show_summary_toggle, timeout=0, context=self._we)

    @property
    def stars_container(self):
        return self._stars_container_type(selector=self._star_icons, context=self._we)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        market_titles = self._find_elements_by_selector(selector=self._fixture_header_item, context=self._we)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            name = f'{market_titles[items_we.index(item_we)].text}-{list_item.name}'
            items_ordered_dict.update({name: list_item})
        return items_ordered_dict


class FixtureHeaderItem(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we, timeout=0.5)


class MarketSectionHeader(AccordionHeader):
    _item = 'xpath=.//*[@data-crlat="title"]'
    _list_item_type = FixtureHeaderItem
    _cash_out_label = 'xpath=.//*[@data-crlat="labelCashout"]'
    _promotion_icons = 'xpath=.//*[@data-crlat="promotionIcons"]'
    _ew_terms = 'xpath=.//*[@data-crlat="eachWayContainer"]'
    _bpg_icon = 'xpath=.//*[@data-crlat="bogIcon"]'
    _terms_class = 'xpath=.//*[@data-crlat="termsClass"]'
    _extra_place_icon = 'xpath=.//*[@data-crlat="promotionIcon.EPR"]'

    @property
    def cash_out_label(self):
        return IconBase(selector=self._cash_out_label, context=self._we)

    def has_cashout_label(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._cash_out_label, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Cashout label presence status to be "{expected_result}"')

    @property
    def promotion_icons(self):
        return PromotionIcons(selector=self._promotion_icons, context=self._we)

    def has_promotion_icons(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._promotion_icons, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Promotion icons presence status to be "{expected_result}"')

    def is_bpg_icon_present(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._bpg_icon, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'BPG icon presence status to be "{expected_result}"')

    @property
    def each_way_class(self):
        return ComponentBase(selector=self._terms_class, context=self._we)

    def has_each_way_class(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._terms_class, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Each way class presence status to be "{expected_result}"')

    @property
    def bpg_icon(self):
        return IconBase(selector=self._bpg_icon, context=self._we)

    @property
    def bog_icon(self):
        return self._find_element_by_selector(selector=self._bpg_icon, context=self._we, timeout=0)

    @property
    def each_way(self):
        return ComponentBase(selector=self._ew_terms, context=self._we)

    @property
    def each_way_terms(self):
        return self._get_webelement_text(selector=self._ew_terms, context=self._we)

    def has_each_way_terms(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._ew_terms, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Each way terms presence status to be "{expected_result}"')

    def has_extra_place_icon(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._extra_place_icon, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Extra place icon presence status to be "{expected_result}"')


class ForecastTricastItem(RacingBetButton):
    _runner = 'xpath=.//*[@data-crlat="checkbox.runner"]'

    @property
    def name(self):
        return wait_for_result(lambda: self.after_element(selector=self._runner, context=self._we),
                               timeout=0.5,
                               name=f'{self.__class__.__name__} Name to appear')

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        result = wait_for_result(lambda: 'checked' in self.get_attribute('class').strip(' ').split(' '),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result


class ForecastTricastButtons(Outcome):
    _item = 'xpath=.//*[@data-crlat="betButton"]'
    _list_item_type = ForecastTricastItem

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=3)
        if not items_we:
            raise NoSuchElementException(f'No elements found, length is: {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict


class RacingMarketSection(Accordion):
    _item = 'xpath=.//*[@data-crlat="outcomeEntity"]'
    _header = 'xpath=.//*[@data-crlat="raceMarketHeader"]'
    _header_type = MarketSectionHeader
    _forecast_tricast = 'xpath=.//*[@data-crlat="raceCard.forTri"]'
    _event_title = 'xpath=.//*[@data-crlat="eventTitle"]'

    @property
    def _list_item_type(self):
        is_forecast_tricast = self._find_element_by_selector(selector=self._forecast_tricast, timeout=0)
        if is_forecast_tricast:
            return ForecastTricastButtons
        return Outcome

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        list_item_type = self._list_item_type
        for item_we in items_we:
            list_item = list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict

    @property
    def section_header(self):
        return self._header_type(selector=self._header, context=self._we)

    def has_header(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._header,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Header shown status to be {expected_result}')

    @property
    def name(self):
        return self.section_header.title_text

    @property
    def event_title(self):
        return self._get_webelement_text(selector=self._event_title, timeout=3)
