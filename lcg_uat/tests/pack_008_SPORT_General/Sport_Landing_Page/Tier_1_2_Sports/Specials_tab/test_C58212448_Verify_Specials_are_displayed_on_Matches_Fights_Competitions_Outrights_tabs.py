import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C58212448_Verify_Specials_are_displayed_on_Matches_Fights_Competitions_Outrights_tabs(Common):
    """
    TR_ID: C58212448
    NAME: Verify Specials are displayed on Matches/Fights, Competitions, Outrights tabs
    DESCRIPTION: This test case verifies Specials are displayed on Matches/Fights, Competitions, Outrights tabs
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: - Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: - **Special** events should contain **drilldownTagNames = MKTFLAG_SP** for **Market level**
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 1. 'Specials', 'Competitions', 'Outrights', 'Fights/Matches' tabs are enabled in CMS for 'Tier 1/2' Sport and data are available
    PRECONDITIONS: 2. **SPECIAL** events are created for the particular Sport (4 different Events):
    PRECONDITIONS: * Matches Event with Primary market with ticked 'Specials' checkbox on market level (there should be 2 Selections created for market)
    PRECONDITIONS: * Outright Event with Outright market with ticked 'Specials' checkbox on market level (there should be 2 Selections created for market)
    PRECONDITIONS: * Matches Event with Primary market with ticked 'Specials' checkbox on market level (there should be only 1 Selection created for market)
    PRECONDITIONS: * Outright Event with Outright market with ticked 'Specials' checkbox on market level (there should be only 1 Selection created for market)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the selected 'Tier 1/2' Sports Landing Page
    PRECONDITIONS: 3. Choose the 'Specials' tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        # Matches event with specials ticked at market level and having double selection
        event1 = self.ob_config.add_autotest_premier_league_football_event(special=True)
        selection_ids = event1.selection_ids
        self.ob_config.change_selection_state(selection_id=selection_ids.get(event1.team2), displayed=False, active=False)
        self.__class__.event1_name = event1.ss_response['event']['name']
        self.__class__.section_name = event1.ss_response['event']['className'].replace("Football ", "") + " - " + \
                                      event1.ss_response['event']['typeName']

        # Matches event with specials ticked at market level and having single selection
        event2 = self.ob_config.add_autotest_premier_league_football_event(special=True)
        selection_ids = event2.selection_ids
        self.ob_config.change_selection_state(selection_id=selection_ids.get('Draw'), displayed=False, active=False)
        self.ob_config.change_selection_state(selection_id=selection_ids.get(event2.team2), displayed=False, active=False)
        self.__class__.event2_name = event2.ss_response['event']['name']
        self.__class__.E2_sel_name = event2.team1

        # Outright event with specials ticked at market level and having double selection
        event3 = self.ob_config.add_autotest_premier_league_football_outright_event(special=True, selections_number=2)
        self.__class__.event3_name = event3.ss_response['event']['name']

        # Outright event with specials ticked at market level and having single selection
        event4 = self.ob_config.add_autotest_premier_league_football_outright_event(special=True, selections_number=1)
        self.__class__.event4_name = event4.ss_response['event']['name']
        self.__class__.E4_sel_name = list(event4.selection_ids.keys())[0]

        specials_tab_cms_name = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials
        specials_tab_name = self.get_sport_tab_name(name=specials_tab_cms_name,
                                                    category_id=self.ob_config.football_config.category_id)

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name=vec.football.FOOTBALL_TITLE)

        tabs_menu = self.site.football.tabs_menu
        tabs_menu.click_button(specials_tab_name)
        self.assertEqual(tabs_menu.current, specials_tab_name,
                         msg=f'Actual opened tab "{tabs_menu.current} '
                             f'is not as expected "{specials_tab_name}"')

    def test_001_check_specials_events_are_displayed_on_specials_tab(self):
        """
        DESCRIPTION: Check Specials Events are displayed on 'Specials' tab
        EXPECTED: * 4 Events are displayed on Specials tab:
        EXPECTED: * 2 Events with 2 Selections for each event:
        EXPECTED: 'Event Name' and 'right side' arrow are displayed
        EXPECTED: * 2 Events with only 1 Selection for each event:
        EXPECTED: 'Selection Name' and 'Price/Odds' button are displayed
        EXPECTED: ![](index.php?/attachments/get/100880874)
        """
        league = self.site.football.tab_content.accordions_list.items_as_ordered_dict.get(self.section_name.upper())
        expected_events = [self.event1_name, self.E2_sel_name, self.event3_name, self.E4_sel_name]
        events = league.items_as_ordered_dict
        for event in expected_events:
            self.assertIn(event, list(events),
                          msg=f'Expected event "{event}" is not found in list of existing events "{list(events)}"')
        for event_name, event in events.items():
            if event_name in expected_events[1::2]:
                self.assertTrue(event.template.bet_button.is_displayed(),
                                msg=f'No outcome displayed for event "{event_name}"')
            if event_name in expected_events[0::2]:
                self.assertTrue(event.chevron_arrow.is_displayed(),
                                msg=f'No chevron displayed for event "{event_name}"')

    def test_002__navigate_to_matchesfights_tab_check_specials_events_are_displayed(self):
        """
        DESCRIPTION: * Navigate to 'Matches'/'Fights' tab.
        DESCRIPTION: * Check Specials Events are displayed.
        EXPECTED: * 2 Events (Matches only) are displayed on Matches/Fights tab:
        EXPECTED: 'Start Date&Time', 'Event Name' and 'Price/Odds' button(s) are displayed
        EXPECTED: ![](index.php?/attachments/get/100880875)
        """
        matches_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
        self.site.football.tabs_menu.click_button(matches_tab_name)
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, matches_tab_name,
                         msg=f'Actual opened tab "{current_tab} '
                             f'is not as expected "{matches_tab_name}"')
        league = self.site.football.tab_content.accordions_list.items_as_ordered_dict.get(self.section_name.upper())
        events = league.items_as_ordered_dict
        expected_events = [self.event1_name, self.event2_name]
        for event in expected_events:
            self.assertIn(event, list(events),
                          msg=f'Expected event "{event}" is not found in list of existing events "{list(events)}"')
        for event_name, event in events.items():
            if event_name in expected_events:
                self.assertTrue(event.template.has_outcomes(),
                                msg=f'No Outcomes displayed for event "{event_name}"')
                self.assertTrue(event.template.event_name, msg=f'No name displayed for event "{event_name}"')
                self.assertTrue(event.template.event_time, msg=f'No date and time displayed for event "{event_name}"')

    def test_003__navigate_to_competitions_tab_check_specials_events_are_displayed(self):
        """
        DESCRIPTION: * Navigate to 'Competitions' tab.
        DESCRIPTION: * Check Specials Events are displayed.
        EXPECTED: * 4 Events are displayed on Specials tab:
        EXPECTED: * 2 Events (Matches):
        EXPECTED: 'Start Date&Time', 'Event Name' and 'Price/Odds' button(s) are displayed
        EXPECTED: * 2 Events (Outrights):
        EXPECTED: 'Event Name' and 'right side' arrow are displayed
        EXPECTED: ![](index.php?/attachments/get/100880876)
        """
        competitions_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.competitions.upper()
        tabs_menu = self.site.football.tabs_menu
        tabs_menu.click_button(competitions_tab_name)
        self.assertEqual(tabs_menu.current, competitions_tab_name,
                         msg=f'Actual opened tab "{tabs_menu.current}'
                             f'is not as expected "{competitions_tab_name}"')

        if self.device_type == 'mobile':
            section = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict.get('AUTO TEST')
        else:
            self.site.football.tab_content.grouping_buttons.click_item(vec.sb_desktop.COMPETITIONS_SPORTS)
            section_name = 'Auto Test' if self.brand == 'ladbrokes' else 'AUTO TEST'
            section = self.site.football.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
        if not section.is_expanded():
            section.expand()
        section.items_as_ordered_dict.get('Autotest Premier League').click()
        day = 'TODAY' if self.brand == 'ladbrokes' and self.device_type == 'mobile' else 'Today'
        matches = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.get(day)
        today_events = matches.items_as_ordered_dict
        expected_events = [self.event1_name, self.event2_name]
        for event in expected_events:
            self.assertIn(event, today_events,
                          msg=f'Expected event "{event}" is not found in list of existing events "{today_events}"')
        for event_name, event in today_events.items():
            if event_name in expected_events:
                self.assertTrue(event.template.has_outcomes(),
                                msg=f'No Outcomes displayed for event "{event_name}"')
                self.assertTrue(event.template.event_name, msg=f'No name displayed for event "{event_name}"')
                self.assertTrue(event.template.event_time, msg=f'No date and time displayed for event "{event_name}"')
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            outrights_tab = 'Outrights'
        else:
            outrights_tab = 'OUTRIGHTS'
        self.site.competition_league.tabs_menu.items_as_ordered_dict.get(outrights_tab).click()
        if self.device_type == 'mobile':
            outright_events = self.site.competition_league.tab_content.event_league
            self.assertTrue(outright_events, msg=f'No Outrights events displayed')
        else:
            outright_events = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(outright_events, msg=f'No Outrights events displayed')
            expected_events = [self.event3_name.upper(), self.event4_name.upper()]
            for event in expected_events:
                self.assertIn(event, outright_events,
                              msg=f'Expected event "{event}" is not found in list of existing events "{outright_events}"')
            for event_name, event in outright_events.items():
                if event_name in expected_events:
                    self.assertTrue(event.name,
                                    msg=f'No name displayed for event "{event_name}"')
                    self.assertTrue(event.chevron_arrow.is_displayed(),
                                    msg=f'No chevron displayed for event "{event_name}"')
        self.device.go_back()

    def test_004__navigate_to_outrights_tab_check_specials_events_are_displayed(self):
        """
        DESCRIPTION: * Navigate to 'Outrights' tab.
        DESCRIPTION: * Check Specials Events are displayed.
        EXPECTED: * 2 Events (Outrights only) are displayed on Matches/Fights tab:
        EXPECTED: 'Event Name' and 'right side' arrow are displayed
        EXPECTED: ![](index.php?/attachments/get/100880877)
        """
        outrights_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper()
        tabs_menu = self.site.football.tabs_menu
        tabs_menu.click_button(outrights_tab_name)
        self.assertEqual(tabs_menu.current, outrights_tab_name,
                         msg=f'Actual opened tab "{tabs_menu.current} '
                             f'is not as expected "{outrights_tab_name}"')
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            section_name = self.section_name
        else:
            section_name = self.section_name.upper()
        league = self.site.football.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
        league.expand()
        events = league.items_as_ordered_dict
        expected_events = [self.event3_name, self.event4_name]
        for event in expected_events:
            self.assertIn(event, list(events),
                          msg=f'Expected event "{event}" is not found in list of existing events "{list(events)}"')
        for event_name, event in events.items():
            if event_name in expected_events:
                self.assertTrue(event.name,
                                msg=f'No name displayed for event "{event_name}"')
