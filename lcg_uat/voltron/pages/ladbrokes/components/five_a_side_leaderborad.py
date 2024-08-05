from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class WelcomeOverlay(ComponentBase):
    _header_title = 'xpath=.//*[@class="overlay-title ng-star-inserted"]'
    _section_title = 'xpath=.//*[@class="overlay-section ng-star-inserted"]'
    _preview_title = 'xpath=.//*[@class="overlay-footer ng-star-inserted"]'
    _get_started = 'xpath=.//*[@class="getStarted"]'

    @property
    def get_started_button(self):
        return ButtonBase(selector=self._get_started, context=self._we)

    @property
    def header_title(self):
        return self._get_webelement_text(selector=self._header_title, context=self._we)

    @property
    def section_title(self):
        return self._get_webelement_text(selector=self._section_title, context=self._we)

    @property
    def preview_title(self):
        return self._get_webelement_text(selector=self._preview_title, context=self._we)


class FiveASideLobbyOverlay(WelcomeOverlay):
    _welcome_header = 'xpath=.//*[contains(@class,"overlay-header ng")]'
    _welcome_line_1 = 'xpath=.//*[contains(@class,"overlay-content ng")][1]'
    _welcome_line_2 = 'xpath=.//*[contains(@class,"overlay-content ng")][2]'
    _welcome_line_3 = 'xpath=.//*[contains(@class,"overlay-content ng")][3]'
    lobby_overlay_next_button = 'xpath=.//*[contains(@class,"navigation-button")]'
    _signpostings_title = 'xpath=.//*[contains(@class,"overlay-content ng")]'
    _entry_info_title = 'xpath=.//*[contains(@class,"overlay-content ng")]'
    _showdown_card_title = 'xpath=.//*[contains(@class,"overlay-content ng")]'

    @property
    def welcome_header(self):
        return self._get_webelement_text(selector=self._welcome_header, context=self._we)

    @property
    def welcome_line_1(self):
        return self._get_webelement_text(selector=self._welcome_line_1, context=self._we)

    @property
    def welcome_line_2(self):
        return self._get_webelement_text(selector=self._welcome_line_2, context=self._we)

    @property
    def welcome_line_3(self):
        return self._get_webelement_text(selector=self._welcome_line_3, context=self._we)

    @property
    def signposting_title(self):
        return self._get_webelement_text(selector=self._signpostings_title, context=self._we)

    @property
    def entry_info_title(self):
        return self._get_webelement_text(selector=self._entry_info_title, context=self._we)

    @property
    def lobby_next_button(self):
        return ButtonBase(selector=self.lobby_overlay_next_button, context=self._we)

    @property
    def showdown_card_title(self):
        return self._get_webelement_text(selector=self._showdown_card_title, context=self._we)

    @property
    def finish_button(self):
        return ButtonBase(selector=self.lobby_overlay_next_button, context=self._we)


class FiveASideLeaderboard(ComponentBase):
    _five_a_side_welcome_overlay = 'xpath=.//*[@id="fiveaside-welcome-overlay"]'
    _five_a_side_pre_event_overlay = 'xpath=.//*[@id="fiveaside-pre-event-tutorial"]'
    _five_a_side_prizepool_information = 'xpath=.//*[@id="fiveaside-prizepool-tutorial"]'
    _five_a_side_rules_entry_information = 'xpath=.//*[@id="fiveaside-rulesarea-tutorial"]'
    _five_a_side_buildteam_information = 'xpath=.//*[@id="fiveaside-entrybutton-tutorial"]'
    _five_a_side_rulesbutton_info = 'xpath=.//*[@id="fiveaside-rulesbutton-tutorial"]'
    _terms_rules_header = 'xpath=.//*[@class="terms-rules-header"]'
    _build_btn = 'xpath=.//*[@class="build-btn"]'
    _five_a_side_entry_list = 'xpath=.//fiveaside-entry-list'
    _home_team_name = 'xpath=.//*[contains(@class, "home-name")]'
    _away_team_name = 'xpath=.//*[contains(@class, "away-name")]'
    _contest_name = 'xpath=.//*[@class="description-name"]'
    _return_to_lobby = 'xpath=.//*[@class="return-to-lobby"]'
    _total_entries = 'xpath=.//*[@class="total-entries"]'
    _entries_per_user = 'xpath=.//*[not(contains(text(),"maxUserEntries")) and @class="user-entries-normal"]'

    @property
    def five_a_side_welcome_overlay(self):
        return WelcomeOverlay(selector=self._five_a_side_welcome_overlay, context=self._we)

    @property
    def five_a_side_pre_event_overlay(self):
        return FiveASidePreEventOverlay(selector=self._five_a_side_pre_event_overlay, context=self._we)

    @property
    def five_a_side_prizepool_information(self):
        return FiveASidePrizePoolInformation(selector=self._five_a_side_prizepool_information, context=self._we)

    @property
    def five_a_side_rules_entry_information(self):
        return FiveASideRulesEntryInformation(selector=self._five_a_side_rules_entry_information, context=self._we)

    @property
    def five_a_side_buildteam_information(self):
        return FiveASideBuildTeamInformation(selector=self._five_a_side_buildteam_information, context=self._we)

    def five_a_side_rulesbutton_info(self):
        return FiveASideRulesButtonInfo(selector=self._five_a_side_rulesbutton_info, context=self._we)

    @property
    def terms_rules_header(self):
        return self._find_element_by_selector(selector=self._terms_rules_header, context=self._we)

    @property
    def build_btn(self):
        return self._find_element_by_selector(selector=self._build_btn, context=self._we)

    @property
    def five_a_side_entry_list(self):
        return FiveASideEntryList(selector=self._five_a_side_entry_list, context=self._we)

    @property
    def return_to_lobby(self):
        return self._find_element_by_selector(selector=self._return_to_lobby, context=self._we)

    @property
    def contest_name(self):
        return self._get_webelement_text(selector=self._contest_name, context=self._we)

    @property
    def total_entries(self):
        return self._find_element_by_selector(selector=self._total_entries, context=self._we)

    @property
    def entries_per_user(self):
        return self._find_element_by_selector(selector=self._entries_per_user, context=self._we)

    @property
    def home_team_name(self):
        return self._find_element_by_selector(selector=self._home_team_name, context=self._we)

    @property
    def away_team_name(self):
        return self._find_element_by_selector(selector=self._away_team_name, context=self._we)


class FiveASidePreEventOverlay(FiveASideLeaderboard):
    _welcome_page_title = 'xpath=.//*[@class="overlay-header animating fadeIn"]'
    _welcome_page_content = 'xpath=.//*[@class="overlay-content animating fadeIn"][1]'
    _welcome_page_footer = 'xpath=.//*[@class="overlay-content animating fadeIn"][2]'
    _pre_event_next_button = 'xpath=.//*[@class="animating-start fadeIn"]'

    @property
    def welcome_page_title(self):
        return self._get_webelement_text(selector=self._welcome_page_title, context=self._we)

    @property
    def welcome_page_content(self):
        return self._get_webelement_text(selector=self._welcome_page_content, context=self._we)

    @property
    def welcome_page_footer(self):
        return self._get_webelement_text(selector=self._welcome_page_footer, context=self._we)

    @property
    def pre_event_next_button(self):
        return ButtonBase(selector=self._pre_event_next_button, context=self._we)

    @property
    def finish_button(self):
        return self.lobby_next_button


class FiveASidePrizePoolInformation(FiveASidePreEventOverlay):
    _prize_pool_information = 'xpath=.//*[@class="overlay-content animated-prize-text fadeIn"]'
    _ppi_next_button = 'xpath=.//*[@class="getStarted animated-prize-btn fadeIn"]'

    @property
    def prize_pool_information(self):
        return self._get_webelement_text(selector=self._prize_pool_information, context=self._we)

    @property
    def ppi_next_button(self):
        return ButtonBase(selector=self._ppi_next_button, context=self._we)


class FiveASideRulesEntryInformation(FiveASidePrizePoolInformation):
    _rules_entry_information = 'xpath=.//*[@id="rules-area-text"]'
    _rei_next_button = 'xpath=.//*[@id="go-to-entry"]'

    @property
    def rules_entry_information(self):
        return self._get_webelement_text(selector=self._rules_entry_information, context=self._we)

    @property
    def rei_next_button(self):
        return ButtonBase(selector=self._rei_next_button, context=self._we)


class FiveASideBuildTeamInformation(FiveASideRulesEntryInformation):
    _build_team_information = 'xpath=.//*[@id="entry-area-text"]'
    _bti_next_button = 'xpath=.//*[@id="go-to-rules-button"]'

    @property
    def build_team_information(self):
        return self._get_webelement_text(selector=self._build_team_information, context=self._we)

    @property
    def bti_next_button(self):
        return ButtonBase(selector=self._bti_next_button, context=self._we)


class FiveASideRulesButtonInfo(FiveASideBuildTeamInformation):
    _rules_button_information = 'xpath=.//*[@class="overlay-content animated-rules fadeIn"]'
    _rbi_finish_button = 'xpath=.//*[@class="getEnded animated-rules fadeIn"]'

    @property
    def rules_button_information(self):
        return self._get_webelement_text(selector=self._rules_button_information, context=self._we)

    @property
    def rbi_finish_button(self):
        return ButtonBase(selector=self._rbi_finish_button, context=self._we)


class FiveASideEntrySummary(ComponentBase):
    _name = 'xpath=.//*[@class="col name"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class FiveASideEntryList(ComponentBase):
    _list = 'xpath=.//fiveaside-entry-summary'
    _list_item_type = FiveASideEntrySummary
    _my_entries = 'xpath=.//*[contains(@class,"my-entries")]'

    @property
    def my_entries(self):
        return self._get_webelement_text(selector=self._my_entries)
