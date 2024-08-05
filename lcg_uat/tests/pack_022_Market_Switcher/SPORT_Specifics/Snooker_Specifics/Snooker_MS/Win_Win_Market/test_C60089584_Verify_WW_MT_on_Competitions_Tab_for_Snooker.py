import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Events can not be created in Prod/Beta
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60089584_Verify_WW_MT_on_Competitions_Tab_for_Snooker(Common):
    """
    TR_ID: C60089584
    NAME: Verify 'WW’ MT on Competitions Tab for Snooker
    DESCRIPTION: This test case verifies displaying of ‘WW market’ Template is displaying while changing the markets in the Market Switcher dropdown on  Competition Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Match Betting|,|1st Frame Winner|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Competition Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Match Betting (WW)| - "Match Result"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    preplay_list = []
    inplay_list = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Matches Tab'
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='Market switcher is disabled for All Sports')
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='snooker',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Snooker sport')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.backend.ti.snooker.category_id,
                                                       disp_sort_names='HH,MH,WH,HL',
                                                       primary_markets='|Match Result|,|Match Betting|,|Handicap Match Result|,'
                                                                       '|Total Frames Over/Under|,|Match Handicap|')
        self.ob_config.add_snooker_event_to_snooker_all_snooker()

        self.navigate_to_page(name='sport/snooker')
        self.site.wait_content_state('Snooker')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.snooker_config.category_id)
        competition_tab = self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name)
        self.assertTrue(competition_tab, msg=f'"{expected_tab_name}" tab is not enabled in CMS')
        competition_tab.click()
        current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' Coral
        """
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Snooker')
        self.__class__.dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if self.device_type == 'desktop':
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                sleep(2)
                self.assertFalse(self.dropdown.is_expanded(), msg=f'"Dropdown Arrow" is not pointing downwards')
        else:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            sleep(2)
            self.assertFalse(self.dropdown.is_expanded(), msg=f'"Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result,
                         msg=f'Actual market value: "{selected_value.upper()}" is not same as'
                             f'Expected market value: "{vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        """
        self.__class__.options = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.assertIn(vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result.title(), list(self.options.keys()),
                      msg=f'market: "{vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result.title()}" is not found in the list: {list(self.options.keys())}')

    def test_003_select_match_result_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Result' in the 'Market Selector' dropdown list
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: • Match Result (Preplay and Inplay)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        self.options.get(vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result.title()).click()
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result}"')

        self.__class__.leagues = list(
            self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(self.leagues, msg='Leagues not found')

        for league in self.leagues:
            events = list(league.items_as_ordered_dict.values())
            self.assertTrue(events, msg='Events not found')
            for event in events:
                event_template = event.template
                is_live = event_template.is_live_now_event
                self.inplay_list.append(is_live) if is_live else self.preplay_list.append(is_live)
                odds = list(event_template.items_as_ordered_dict.values())
                for odd in odds:
                    self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                self.assertTrue(event_template.event_name,
                                msg=' "Event Name" not displayed')
                if is_live:
                    self._logger.info(f'{event_template.event_name} is live event')
                else:
                    self.assertTrue(event_template.event_time,
                                    msg=' "Event time" not displayed')
                if event_template.has_markets():
                    self._logger.info(f'{event_template.event_name} has more markets')
                else:
                    self._logger.info(f'{event_template.event_name} has no more markets')

        if len(self.inplay_list) > 0 and len(self.preplay_list) == 0:
            self._logger.info(msg=f'Only "In-Play" events are available ')
        elif len(self.inplay_list) == 0 and len(self.preplay_list) > 0:
            self._logger.info(msg=f'Only "Pre-Play" events are available ')
        else:
            self._logger.info(msg=f'Both "In-Play" and "Pre-play" events are available ')

    def test_004_verify_text_of_the_labels_for_match_result(self):
        """
        DESCRIPTION: Verify text of the labels for 'Match Result'
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels 1 & 2.
        """
        # corresponding Odds are present under Labels  1 and 2 - verified in step3
        fixture = self.leagues[0].fixture_header
        self.assertEqual(fixture.header1, '1',
                         msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                             f'Expected "{1}"')
        self.assertEqual(fixture.header3, '2',
                         msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                             f'Expected "{2}"')

    def test_005_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: • Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        # functionality covered in the step test_003
