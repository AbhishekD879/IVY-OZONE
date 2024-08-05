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
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-54020')
# todo VOL-5709[tst] Adapt pack_008_SPORT_General › Sport_Landing_Page
@vtest
class Test_C58209232_Verify_Specials_Events_Live_updates_on_Specials_tab(BaseSportTest):
    """
    TR_ID: C58209232
    NAME: Verify Specials Events Live updates on 'Specials' tab
    DESCRIPTION: This Test Case verifies Specials Events Live updates on 'Specials' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: - Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: - **Special** events should contain the following attributes:
    PRECONDITIONS: **Market level:**
    PRECONDITIONS: * drilldownTagNames = MKTFLAG_SP
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 1. 'Specials' tab is enabled in CMS for 'Tier 1/2' Sport and data are available
    PRECONDITIONS: 2. **SPECIAL** events of the same Type are created for the particular Sport (2 Events):
    PRECONDITIONS: * Event with 2 selections in specific market
    PRECONDITIONS: * Event with only one selection in specific market
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the selected 'Tier 1/2' Sports Landing Page
    PRECONDITIONS: 3. Choose the 'Specials' tab
    PRECONDITIONS: 4. Make sure created Events are displayed and Price/Odds buttons is displayed for Event with only one selection
    """
    keep_browser_open = True
    sport_name = vec.football.FOOTBALL_TITLE
    market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score

    def verify_event_displaying(self, event_name=None, displayed=None, has_chevron=None):
        """
        This method verifies whether specified event appearance on the page
        """
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No Specials sections found')

        section = sections.get(self.league_name)
        self.assertTrue(section, msg=f'Specials section "{self.league_name}" not found')
        section.expand()

        if displayed:
            result = wait_for_result(lambda: event_name in list(section.items_as_ordered_dict.keys()),
                                     name=f'Event "{event_name}" to appear')
            self.assertTrue(result, msg=f'Event "{event_name}" did not appear')

            events = section.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events found for section "{self.league_name}')

            event = events.get(event_name)
            self.assertTrue(event, msg=f'Event name "{event_name}" not found')
            self.assertEqual(event.name, event_name,
                             msg=f'Event name "{event.name}" '
                                 f'is not as expected "{event_name}"')
            if has_chevron:
                self.assertTrue(event.has_chevron_arrow(), msg=f'Right-side arrow is not shown')
            else:
                self.assertTrue(event.bet_button.is_displayed(), msg=f'Bet button is not displayed')
        else:
            result = wait_for_result(lambda: event_name not in list(section.items_as_ordered_dict.keys()),
                                     name=f'Event "{event_name}" to disappear')
            self.assertTrue(result, msg=f'Event "{event_name}" did not disappear')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Run preconditions
        """
        specials_tab_cms_name = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials

        specials_tab_name = self.get_sport_tab_name(name=specials_tab_cms_name,
                                                    category_id=self.ob_config.football_config.category_id)

        event_params = self.ob_config.add_autotest_premier_league_football_event(
            suspend_at=self.get_date_time_formatted_string(days=2), special=True, default_market_name=self.market_name)
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        created_event_name = event_params.ss_response['event']['name']
        self.__class__.selection_1 = selection_ids.get(event_params.team2)
        self.__class__.league_name = self.get_accordion_name_for_event_from_ss(event=event_params.ss_response)

        self._logger.info(f'*** Created 1st Football event "{self.created_event_name}" with ID "{event_params.event_id}"')

        event_params_2 = self.ob_config.add_autotest_premier_league_football_event(
            suspend_at=self.get_date_time_formatted_string(days=2), special=True, default_market_name=self.market_name)
        self.__class__.eventID_2, selection_ids_2 = event_params_2.event_id, event_params_2.selection_ids
        created_event_name_2 = event_params_2.ss_response['event']['name']
        self.__class__.selection_2 = selection_ids_2.get(event_params_2.team1)

        self._logger.info(f'*** Created 2nd Football event "{created_event_name_2}" with ID "{event_params_2.event_id}"')

        # disabling 1 selection for 1st event - event with 2 selections
        self.ob_config.change_selection_state(selection_id=selection_ids.get('Draw'))

        # disabling 2 selections for 2nd event - event with 1 selection only
        self.ob_config.change_selection_state(selection_id=selection_ids_2.get('Draw'))
        self.ob_config.change_selection_state(selection_id=selection_ids_2.get(event_params_2.team2))

        # reassigning event names
        self.__class__.event_name_1 = created_event_name        # 1st event name
        self.__class__.event_name_1_team1 = event_params.team1  # 1st event name with 1 selection
        self.__class__.event_name_2 = event_params_2.team1      # 2nd event name with 1 selection only

        result = wait_for_result(
            lambda: self.is_tab_present(tab_name=specials_tab_cms_name,
                                        category_id=self.ob_config.football_config.category_id) is True,
            name='Specials tab to be displayed',
            poll_interval=2,
            timeout=10)
        self.assertTrue(result, msg='Specials tab is not displayed')

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name=self.sport_name)

        tabs_menu = self.site.football.tabs_menu
        tabs_menu.click_button(specials_tab_name)
        self.assertEqual(tabs_menu.current, specials_tab_name,
                         msg=f'Actual opened tab "{tabs_menu.current} '
                             f'is not as expected "{specials_tab_name}"')

        self.verify_event_displaying(event_name=self.event_name_1, displayed=True, has_chevron=True)
        self.verify_event_displaying(event_name=self.event_name_2, displayed=True, has_chevron=False)

    def test_001_undisplay_event_with_2_selections_and_verify_event_is_disappeared(self):
        """
        DESCRIPTION: * Navigate to TI and **undisplay** Event with 2 Selections.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Do NOT refresh the page.
        EXPECTED: Event is disappeared from the page
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=True)
        self.verify_event_displaying(event_name=self.event_name_1, displayed=False)

    def test_002_display_the_undisplayed_event_and_verify_the_event_is_displayed(self):
        """
        DESCRIPTION: * Navigate to TI and **display** undisplayed (in Step1) Event.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Refresh the page.
        EXPECTED: * Event is displayed on the page
        EXPECTED: * Event Name is displayed on Event's card
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.verify_event_displaying(event_name=self.event_name_1, displayed=True, has_chevron=True)

    def test_003_undisplay_selection_for_event_with_2_selections_and_verify_event_is_displayed(self):
        """
        DESCRIPTION: * Navigate to TI and **undisplay** Selection for Event with 2 Selections.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Do NOT refresh the page.
        EXPECTED: * Event is displayed in Type accordion
        EXPECTED: * Selection Name and Price/Odds button is displayed on Event's card
        """
        self.ob_config.change_selection_state(selection_id=self.selection_1, displayed=False, active=True)
        self.verify_event_displaying(event_name=self.event_name_1_team1, displayed=True, has_chevron=False)

    def test_004_display_undisplayed_in_step3_selection_for_event_with_2_selections_and_verify_event_is_displayed(self):
        """
        DESCRIPTION: * Navigate to TI and **display** undisplayed (in Step3) Selection for Event with 2 Selections.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Refresh the page.
        EXPECTED: * Event is displayed in Type accordion
        EXPECTED: * Event Name is displayed on Event's card
        """
        self.ob_config.change_selection_state(selection_id=self.selection_1, displayed=True, active=True)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.verify_event_displaying(event_name=self.event_name_1, displayed=True, has_chevron=True)

    def test_005_undisplay_selection_for_event_with_only_one_selection_and_verify_event_is_disappeared(self):
        """
        DESCRIPTION: * Navigate to TI and **undisplay** Selection for Event with only one Selection.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Do NOT refresh the page.
        EXPECTED: Event is disappeared from Type accordion
        """
        self.ob_config.change_selection_state(selection_id=self.selection_2, displayed=False, active=True)
        self.verify_event_displaying(event_name=self.event_name_2, displayed=False)

    def test_006_display_selection_for_event_with_only_one_selection_and_verify_event_is_displayed(self):
        """
        DESCRIPTION: * Navigate to TI and **display** Selection for Event with only one Selection.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Refresh the page.
        EXPECTED: * Event is displayed in Type accordion
        EXPECTED: * Selection Name and Price/Odds button is displayed on Event's card
        """
        self.ob_config.change_selection_state(selection_id=self.selection_2, displayed=True, active=True)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.verify_event_displaying(event_name=self.event_name_2, displayed=True, has_chevron=False)

    def test_007_undisplay_all_events_of_the_same_type_and_verify_events_are_disappeared(self):
        """
        DESCRIPTION: Navigate to TI and **undisplay** all Events of the same Type
        EXPECTED: * Events are disappeared from Type accordion
        EXPECTED: * Type accordion is disappeared
        """
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No Specials sections found')

        if len(sections) == 1:
            self.ob_config.add_football_event_to_spanish_la_liga(
                suspend_at=self.get_date_time_formatted_string(days=2), special=True, default_market_name=self.market_name)

        section = sections.get(self.league_name)
        self.assertTrue(section, msg=f'Specials section "{self.league_name}" not found')
        section.expand()

        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found for section "{self.league_name}')

        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=True)
        self.ob_config.change_event_state(event_id=self.eventID_2, displayed=False, active=True)

        if len(events) > 2:
            self.verify_event_displaying(event_name=self.event_name_1, displayed=False)
            self.verify_event_displaying(event_name=self.event_name_2, displayed=False)
        else:
            result = wait_for_result(lambda: self.league_name not in list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.keys()),
                                     name=f'Section "{self.league_name}" to disappear', timeout=10)
            self.assertTrue(result, msg=f'Section "{self.league_name}" did not disappear')
