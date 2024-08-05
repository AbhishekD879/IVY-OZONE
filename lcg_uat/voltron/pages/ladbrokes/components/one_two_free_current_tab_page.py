from collections import OrderedDict
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.base_content import ComponentContent
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class ScoreSwitcher(ComponentContent):
    _score_value = 'xpath=.//*[contains(@class,"visibleBar")]'
    _increase_score = 'xpath=.//*[contains(@class,"increaseScore")]'
    _decrease_score = 'xpath=.//*[contains(@class,"decreaseScore")]'
    _my_prediction = 'xpath=.//*[contains(@class,"myPrediction")]'
    @property
    def score(self):
        score = self._get_webelement_text(selector=self._score_value, context=self._we).split('\n')
        return score[1] if len(score) > 1 and score[0] != '9' else score[0]

    @property
    def my_prediction(self):
        return self._get_webelement_text(selector=self._my_prediction, context=self._we)

    @property
    def increase_score_up_arrow(self):
        return ButtonBase(selector=self._increase_score, context=self._we)

    @property
    def decrease_score_down_arrow(self):
        return ButtonBase(selector=self._decrease_score, context=self._we)


class TeamInfo(ComponentContent):
    _name = 'xpath=.//*[contains(@class,"teamName")]'
    _silk = 'xpath=.//*[contains(@class,"silkContainer")]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=5)

    @property
    def silk_icon(self):
        return self._find_element_by_selector(selector=self._silk, timeout=5)


class ScoreContainer(ComponentContent):
    _item = 'xpath=.//*[contains(@class,"scoreSwitcher__17OmA")]'
    _list_item_type = ScoreSwitcher


class EventItemContainer(ComponentContent):
    _channel_icon = 'xpath=.//*[contains(@class,"channelContainer")]'
    _name = 'xpath=.//*[contains(@class,"matchNo")]'
    _event_body = 'xpath=.//*[contains(@class,"eventBody")]'
    _match_start_date = 'xpath=.//*[contains(@class,"matchDateOrResult")]'
    _score_selector_container = 'xpath=.//*[contains(@class,"scoreSelectorContainer")]'
    _lost_or_won = 'xpath=.//*[contains(@class,"matchResultIndicator")]/span'
    _match_number = 'xpath=.//*[contains(@class,"matchNo")]'
    _match_result = 'xpath=.//*[contains(@class,"matchDateOrResult")]'
    _item = 'xpath=.//*[contains(@class,"teamInfoContainer")]'
    _list_item_type = TeamInfo

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=5)

    @property
    def match_start_date(self):
        return self._get_webelement_text(selector=self._match_start_date, timeout=5)

    @property
    def match_number(self):
        return self._get_webelement_text(selector=self._match_number, timeout=5)

    @property
    def match_result(self):
        return self._get_webelement_text(selector=self._match_result, timeout=5)

    @property
    def lost_or_won(self):
        return self._get_webelement_text(selector=self._lost_or_won, timeout=5)

    @property
    def channel_icon(self):
        return self._find_element_by_selector(selector=self._channel_icon, timeout=5)

    @property
    def score_selector_container(self):
        return ScoreContainer(selector=self._score_selector_container, context=self._we)


class ResultsTabItem(ComponentBase):
    _item_name = 'xpath=.//*[contains(@class,"tabSwitcherBadge")]/p'


class WeeksResultsTabsList(ComponentBase):
    _item = 'xpath=.//*[contains(@class,"tabSwitcherBadge")]'
    _list_item_type = ResultsTabItem
    _selected_item = 'xpath=.//*[contains(@class,"tabSwitcherBadge") and contains(@class,"Active")]'

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({item_we.text: list_item})
        return items_ordered_dict

    @property
    def current(self):
        return self._find_element_by_selector(selector=self._selected_item, context=self._we, timeout=3).text


class MyBadgesTeamInfo(ComponentBase):
    _name = 'xpath=.//*[contains(@class,"teamDisplayName")]'
    _silk = 'xpath=.//*[contains(@class,"teamWrapper")]'
    _blank_silk = 'xpath=.//*[contains(@class,"teamImage") and contains(@src,"blank-kit")]'
    _primary_silk = 'xpath=.//*[contains(@class,"teamImage") and not (contains(@src,"blank-kit"))]'
    _secondary_silk = 'xpath=.//*[contains(@class,"teamImage") and not (contains(@src,"blank-kit"))]/following-sibling::img[contains(@class,"greenTick")]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=5)

    @property
    def silk_icon(self):
        return self._find_element_by_selector(selector=self._silk, timeout=5)

    @property
    def blank_silk(self):
        return self._find_element_by_selector(selector=self._blank_silk)

    @property
    def primary_silk(self):
        return self._find_element_by_selector(selector=self._primary_silk, timeout=2)

    @property
    def secondary_silk(self):
        return self._find_element_by_selector(selector=self._secondary_silk, timeout=2)

class LastWeekResults(ComponentBase):
    _did_not_play = 'xpath=.//*[contains(@class,"tabsContainer")]//div[contains(@class,"warning")]'

    @property
    def did_not_play_game_label(self):
        try:
            return self._find_element_by_selector(selector=self._did_not_play, timeout=5).text
        except:
            return ''

class MyBadges(ComponentBase):
    _my_badges_text = 'xpath=.//*[contains(@class,"rulesDisplay")]/div'
    _my_badges_element = 'xpath=.//*[@id="MyBadgesTab"]/p'
    _last_updated = 'xpath=.//*[contains(@class,"lastUpdated")]/span'
    _item = 'xpath=.//*[contains(@class,"teamWrapper")]/parent::*'
    _list_item_type = MyBadgesTeamInfo

    @property
    def last_updated(self):
        return self._get_webelement_text(selector=self._last_updated, timeout=5)

    @property
    def my_badges_text(self):
        return self._get_webelement_text(selector=self._my_badges_text, timeout=5)

    @property
    def my_badges_text_element(self):
        return ComponentBase(selector=self._my_badges_text, timeout=5)

    @property
    def my_badges_element(self):
        return ComponentBase(selector=self._my_badges_element, timeout=5)
