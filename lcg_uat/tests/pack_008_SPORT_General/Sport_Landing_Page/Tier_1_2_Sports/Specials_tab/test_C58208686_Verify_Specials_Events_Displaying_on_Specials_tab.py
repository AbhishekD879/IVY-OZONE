import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.specials
@pytest.mark.desktop
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-53563')
@vtest
class Test_C58208686_Verify_Specials_Events_Displaying_on_Specials_tab(BaseSportTest):
    """
    TR_ID: C58208686
    NAME: Verify Specials Events Displaying on 'Specials' tab
    DESCRIPTION: This test case verifies data of Specials Events which displayed on Specials tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: - Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: - **Specials** Events should be created only with **No Primary** markets
    PRECONDITIONS: - **Special** events should contain **drilldownTagNames = MKTFLAG_SP** for **Market level**
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 1. 'Specials' tab is enabled in CMS for 'Tier 1/2' Sport and data are available
    PRECONDITIONS: 2. **SPECIAL** events are created for the particular Sport:
    PRECONDITIONS: * Events for at least two different Types
    PRECONDITIONS: * Event with only one selection in specific market
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the selected 'Tier 1/2' Sports Landing Page
    PRECONDITIONS: 3. Choose the 'Specials' tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Run preconditions
        """
        sport_name = vec.football.FOOTBALL_TITLE
        market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score
        specials_tab_cms_name = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials

        specials_tab_name = self.get_sport_tab_name(name=specials_tab_cms_name,
                                                    category_id=self.ob_config.football_config.category_id)

        event_params = self.ob_config.add_autotest_premier_league_football_event(
            suspend_at=self.get_date_time_formatted_string(days=2), special=True, default_market_name=market_name)
        self.__class__.created_event_name = event_params.ss_response['event']['name']
        self.__class__.league_name = self.get_accordion_name_for_event_from_ss(event=event_params.ss_response)

        self._logger.info(
            f'*** Created 1st Football event "{self.created_event_name}" with ID "{event_params.event_id}"')

        event_params_2 = self.ob_config.add_football_event_to_spanish_la_liga(
            suspend_at=self.get_date_time_formatted_string(days=2), special=True, default_market_name=market_name)
        self.__class__.team1, team2, selection_ids_2 = event_params_2.team1, event_params_2.team2, event_params_2.selection_ids
        created_event_name_2 = event_params.ss_response['event']['name']
        self.__class__.league_name_2 = self.get_accordion_name_for_event_from_ss(event=event_params_2.ss_response)

        self._logger.info(
            f'*** Created 2nd Football event "{created_event_name_2}" with ID "{event_params_2.event_id}"')

        # make 2nd event with 1 selection only
        self.ob_config.change_selection_state(selection_id=selection_ids_2.get('Draw'), displayed=False, active=False)
        self.ob_config.change_selection_state(selection_id=selection_ids_2.get(team2), displayed=False, active=False)

        result = wait_for_result(
            lambda: self.is_tab_present(tab_name=specials_tab_cms_name,
                                        category_id=self.ob_config.football_config.category_id),
            name='Specials tab to be displayed',
            poll_interval=4,
            timeout=40)
        self.assertTrue(result, msg='Specials tab is not displayed')

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name=sport_name)

        tabs_menu = self.site.football.tabs_menu
        tabs_menu.click_button(specials_tab_name)
        self.assertEqual(tabs_menu.current, specials_tab_name,
                         msg=f'Actual opened tab "{tabs_menu.current} '
                             f'is not as expected "{specials_tab_name}"')

    def test_001_check_type_accordions_displaying(self):
        """
        DESCRIPTION: Check Type accordions displaying
        EXPECTED: * Events are shown within Type accordions
        EXPECTED: * First Type accordion is expanded by default and other Type accordions are collapsed by default
        EXPECTED: * Type accordion header title contains <Class> - <Type>
        """
        self.__class__.sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No Specials sections found')

        specials_name, special = list(self.sections.items())[0]
        self.assertTrue(special.is_expanded(), msg=f'Special section "{specials_name}" is not expanded by default')

        if len(self.sections) > 1:
            for specials_name, special in list(self.sections.items())[1:]:
                self.assertFalse(special.is_expanded(expected_result=False),
                                 msg=f'Special section "{specials_name}" is not expanded by default')

        self.__class__.section = self.sections.get(self.league_name)
        self.assertTrue(self.section, msg=f'Specials section "{self.league_name}" not found')

        self.__class__.section_2 = self.sections.get(self.league_name_2)
        self.assertTrue(self.section_2, msg=f'Specials section "{self.league_name_2}" not found')

    def test_002_check_special_event_displaying_when_event_contains_more_than_one_selection_within_market(self):
        """
        DESCRIPTION: Check special event displaying when event contains more than one selection within market
        EXPECTED: Only event name (without price/odds button) and right-side arrow are shown
        """
        self.section.expand()
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found for section "{self.league_name}')

        self.__class__.event = events.get(self.created_event_name)
        self.assertTrue(self.event, msg=f'Event name "{self.created_event_name}" not found')
        self.assertTrue(self.event.has_chevron_arrow(), msg=f'Right-side arrow is not shown')
        self.assertEqual(self.event.name, self.created_event_name,
                         msg=f'Event name "{self.event.name}" '
                             f'is not as expected "{self.created_event_name}"')

    def test_003_check_special_event_displaying_if_event_contains_only_one_selection_within_market(self):
        """
        DESCRIPTION: Check Special event displaying if event contains only one selection within market
        EXPECTED: Selection name and price/odds button is shown
        """
        self.section_2.expand()
        events = self.section_2.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found for section "{self.league_name_2}')

        event = events.get(self.team1)
        self.assertTrue(event, msg=f'Event "{self.team1}" not found')

        self.assertTrue(event.bet_button.is_displayed(), msg=f'Bet button is not displayed')

    def test_004_click_tap_on_event_selection_name(self):
        """
        DESCRIPTION: Click/Tap on 'Event/Selection' name
        EXPECTED: Event details page is opened
        """
        self.event.click()
        self.site.wait_content_state(state_name='EventDetails')

        # TODO  https://jira.egalacoral.com/browse/VOL-5780
        event_name_details_page = self.site.sport_event_details.event_title_bar.event_name
        expected_event_name = self.created_event_name.upper() \
            if self.device_type == 'desktop' and self.brand != 'ladbrokes' else self.created_event_name
        # TODO: BMA-53563 workaround
        expected_event_name = event_name_details_page.title() \
            if self.device_type == 'desktop' and self.brand == 'ladbrokes' else expected_event_name
        self.assertEqual(event_name_details_page, expected_event_name,
                         msg=f'Item text "{event_name_details_page}" '
                             f'is not as expected "{expected_event_name}"')
