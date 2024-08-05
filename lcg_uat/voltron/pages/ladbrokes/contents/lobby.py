from voltron.pages.shared.components.base import ComponentBase


class LobbyContest(ComponentBase):
    _name = 'xpath=.//*[contains(@class,"contest-info")]'
    _entry_info = 'xpath=.//*[@id="card-entry-info"]'
    _match_start_time = 'xpath=.//*[@class="content-center-flex historic-match-date"]'
    _entry_total_text = 'xpath=.//*[@class="signpost-text total"]'
    _max_entry_text = 'xpath=.//*[@class="signpost-text max"]'

    @property
    def name(self):
        return self._find_element_by_selector(selector=self._name, context=self._we).get_attribute('innerText')

    @property
    def entry_info(self):
        return self._get_webelement_text(selector=self._entry_info, context=self._we)

    @property
    def match_start_time(self):
        return self._get_webelement_text(selector=self._match_start_time, context=self._we)

    @property
    def entry_total_text(self):
        return self._get_webelement_text(selector=self._entry_total_text, context=self._we)

    @property
    def max_entry_text(self):
        return self._get_webelement_text(selector=self._max_entry_text, context=self._we)


class LobbySection(ComponentBase):
    _item = 'xpath=.//div[@id="showdown-card-main"]'
    _list_item_type = LobbyContest


class LeaderBoardContainer(ComponentBase):
    _show_down_cards = 'xpath=.//*[@id="showdown-cards"]'

    @property
    def lobby_section(self):
        return LobbySection(selector=self._show_down_cards)


class Lobby(ComponentBase):
    _leader_board_container = 'xpath=.//*[@class="leaderboard-container five-a-side-bg"] | .//*[contains(@class, "overFlow five-a-side-bg")]'

    @property
    def leaderboard_container(self):
        return LeaderBoardContainer(selector=self._leader_board_container, context=self._we)
