from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.content_header import HeaderLine
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.contents.base_content import ComponentContent, BaseContent
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import RacingBetButton
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class EditStable(ButtonBase):
    _state = 'xpath=.//*[@data-crlat="state"]'
    _svg_icon = 'xpath=.//*[@data-crlat="bookmark"]/*[1]'

    @property
    def state_name(self):
        return self._get_webelement_text(selector=self._state)

    @property
    def edit_stable_svg_icon(self):
        return ComponentBase(selector=self._svg_icon).get_attribute('xlink:href')


class DropDownOption(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="itemName"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)


class MyStableDropDown(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="item"]'
    _list_item_type = DropDownOption


class SortBy(ButtonBase):
    _selected_option = 'xpath=.//*[@data-crlat="selectedOption"]'
    _drop_down = 'xpath=.//*[@data-crlat="sortSelector"]'
    _label = 'xpath=.//*[contains(@class, "sort-by-title")]'
    _chevron = 'xpath=.//*[contains(@class,"sort-by-arrow")]'
    _drop_down_type = MyStableDropDown

    @property
    def drop_down(self):
        return self._drop_down_type(selector=self._drop_down, context=self._we)

    @property
    def label(self):
        return self._get_webelement_text(selector=self._label)

    @property
    def selected_option(self):
        return self._get_webelement_text(selector=self._selected_option)

    @property
    def chevron(self):
        return self._find_element_by_selector(selector=self._chevron)


class MyStableNotes(ComponentBase):
    _input_notes = 'xpath=.//*[@data-crlat="notesTextArea"]'
    _char_limit = 'xpath=.//*[@data-crlat="notesCharLimit"]'
    _cancel = 'xpath=.//*[@data-crlat="notesCancel" or @data-crlat="closeIcon"]'
    _save = 'xpath=.//*[@data-crlat="notesSave"]'

    @property
    def input_notes(self):
        return InputBase(selector=self._input_notes, context=self._we)

    @property
    def char_limit(self):
        return self._get_webelement_text(selector=self._char_limit, context=self._we)

    @property
    def cancel(self):
        return ButtonBase(selector=self._cancel, context=self._we)

    @property
    def save(self):
        return ButtonBase(selector=self._save, context=self._we)


class MyStableRaceCardHeader(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _book_mark = 'xpath=.//*[@data-crlat="bsMystableBookmark"]'

    @property
    def bookmark(self):
        return ButtonBase(selector=self._book_mark, context=self._we)

    @property
    def text(self):
        title = self._find_element_by_selector(self._title, timeout=1)
        if title is not None:
            text = self._get_webelement_text(we=title)
        else:
            text = self._get_webelement_text(we=self._we, timeout=2)
        return text

    @property
    def title_text(self):
        wait_for_result(lambda: self.text,
                        name='Header text is not empty',
                        timeout=5)
        return self.text


class MyStableRaceCard(Accordion):
    _header_type = MyStableRaceCardHeader
    _trainer_name = 'xpath=.//*[@data-crlat="stableTrainer"]'
    _form = 'xpath=.//*[@data-crlat="stableFormId"]'
    _event_name = 'xpath=.//*[@data-crlat="eventName"]'
    _event_date = 'xpath=.//*[@data-crlat="eventDate"]'
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'
    _silks = 'xpath=.//*[@data-crlat="Silk"]'
    _add_notes_button = 'xpath=.//*[@data-crlat="myStableAddNotes"]'
    _hide_notes_button = 'xpath=.//*[@data-crlat="stableViewNotes"]'
    _edit_icon = 'xpath=.//*[@data-crlat="homeEditIcon"]'
    _existing_note = 'xpath=.//*[@data-crlat="homeNotesText"]'
    _notes = 'xpath=.//*[contains(@class,"home-horse-notes")]'
    _notes_type = MyStableNotes

    @property
    def horse_name(self):
        return self.name

    @property
    def trainer_name(self):
        trainer_name = self._get_webelement_text(selector=self._trainer_name, context=self._we)
        if not trainer_name:
            raise VoltronException(f'Trainer name not available in my stable page for {self.horse_name}')
        return trainer_name.strip()

    @property
    def form(self):
        we = self._find_element_by_selector(selector=self._form, context=self._we)
        if we is not None:
            return we.text
        else:
            raise VoltronException('No element matching {0} was found'.format(self._form))

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._event_name, context=self._we)

    @property
    def event_date(self):
        return self._get_webelement_text(selector=self._event_date, context=self._we)

    @property
    def bet_button(self):
        return RacingBetButton(selector=self._bet_button, context=self._we, timeout=2)

    def has_bet_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._bet_button,context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Bet button shown status to be {expected_result}')

    @property
    def has_silks(self):
        we = self._find_element_by_selector(selector=self._silks, context=self._we, timeout=.5)
        return we is not None and we.is_displayed()

    @property
    def add_notes_button(self):
        return ButtonBase(selector=self._add_notes_button, context=self._we)

    @property
    def hide_notes_button(self):
        return ButtonBase(selector=self._hide_notes_button, context=self._we)

    @property
    def view_notes_button(self):
        return ButtonBase(selector=self._hide_notes_button, context=self._we)

    @property
    def edit_notes_button(self):
        return ButtonBase(selector=self._edit_icon, context=self._we)

    @property
    def existing_notes(self):
        return self._get_webelement_text(selector=self._existing_note, context=self._we)

    @property
    def notes(self):
        return MyStableNotes(selector=self._notes, context=self._we)

    def clear_bookmark(self):
        self.section_header.bookmark.click()


class MyStable(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/my-stable'
    _header_line = 'xpath=.//*[@data-crlat="topBar"] | .//*[@data-crlat="bsTab" and contains(text(),"My Bets")] | ' \
                   './/*[contains(@data-crlat,"topBar")] | .//top-bar[@class="ng-star-inserted"]' \
                   ' | .//*[contains(@data-crlat,"topBar")] /ancestor::top-bar'
    _header_line_type = HeaderLine
    _my_horses = 'xpath=.//*[@data-crlat="myHorses"]'
    _running_today = 'xpath=.//*[@data-crlat="runningToday"]'
    _sort_by = 'xpath=.//*[@class="sort-by-container"]'
    _edit_stable = 'xpath=.//*[@data-crlat="saveEditStable"]'
    _item = 'xpath=.//section[@data-crlat="accordion"]'
    _list_item_type = MyStableRaceCard
    _no_favorite_horses_icon = 'xpath=.//*[@data-crlat="noFavoriteHorsesIcon"]'
    _no_favorite_horses_label = 'xpath=.//*[@data-crlat="emptyStableLabel"]/p[1]'
    _no_favorite_horses_info = 'xpath=.//*[@data-crlat="emptyStableLabel"]/p[2]'
    _view_todays_races = 'xpath=.//*[@data-crlat="navToHRCTC"]'


    @property
    def header(self):
        return self._header_line_type(selector=self._header_line)

    @property
    def my_horses(self):
        text = self._get_webelement_text(selector=self._my_horses)
        contents = [item.strip() for item in text.split(':')]
        res = {'name': contents[0].upper(), 'count': int(contents[1])}
        return res

    @property
    def running_today(self):
        text = self._get_webelement_text(selector=self._running_today)
        contents = [item.strip() for item in text.split(':')]
        res = {'name': contents[0].upper(), 'count': int(contents[1])}
        return res

    @property
    def sort_by(self):
        return SortBy(selector=self._sort_by)

    @property
    def edit_stable(self):
        return EditStable(selector=self._edit_stable)

    @property
    def my_stable_race_cards(self):
        return self.items_as_ordered_dict

    def has_no_favorite_horses_icon(self, expected_result=True, timeout=5):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._no_favorite_horses_icon, timeout=0) is not None,
                                 expected_result=expected_result,
                                 name=f'No Favorite Horses Icon status to be "{expected_result}"',
                                 timeout=timeout)
        return result

    def has_no_favorite_horses_label(self, expected_result=True, timeout=5):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._no_favorite_horses_label, timeout=0) is not None,
            expected_result=expected_result,
            name=f'No Favorite Horses Label status to be "{expected_result}"',
            timeout=timeout)
        return result

    @property
    def no_favorite_horses_label_text(self):
        return self._get_webelement_text(selector=self._no_favorite_horses_label)

    def has_no_favorite_horses_info(self, expected_result=True, timeout=5):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._no_favorite_horses_info, timeout=0) is not None,
            expected_result=expected_result,
            name=f'No Favorite Horses Info status to be "{expected_result}"',
            timeout=timeout)
        return result

    @property
    def no_favorite_horses_info_text(self):
        return self._get_webelement_text(selector=self._no_favorite_horses_info)

    def has_view_todays_races(self, expected_result=True, timeout=5):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._view_todays_races, timeout=0) is not None,
            expected_result=expected_result,
            name=f'No Favorite Horses Icon status to be "{expected_result}"',
            timeout=timeout)
        return result

    @property
    def has_view_todays_races_text(self):
        return self._get_webelement_text(selector=self._view_todays_races)

    @property
    def view_todays_races(self):
        return ButtonBase(selector=self._view_todays_races)
