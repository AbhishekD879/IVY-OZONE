import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from collections import OrderedDict
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Involves creation of events
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.sanity
@vtest
class Test_C2389906_Verify_Breadcrumbs_functionality_across_the_application(BaseSportTest, BaseRacing):
    """
    TR_ID: C2389906
    NAME: Verify Breadcrumbs functionality across the application
    DESCRIPTION: This test case verifies Breadcrumbs functionality across the application
    DESCRIPTION: partly covered in AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_id=735049&group_order=asc and [C9698302]
    PRECONDITIONS: Open Oxygen app
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def breadcrumbs_verification(self, breadcrumb1=None, breadcrumb2=None, breadcrumb3=None, breadcrumb4=None, length=None):
        """
        This method verifies breadcrumbs details
        """
        if length == 2:
            breadcrumbs = OrderedDict((key.strip(), self.site.sports_page.breadcrumbs.items_as_ordered_dict[key])
                                      for key in self.site.sports_page.breadcrumbs.items_as_ordered_dict)
            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

            self.assertEqual(list(breadcrumbs.keys()).index(breadcrumb1), 0,
                             msg='Home page is not shown the first by default')
            self.assertTrue(breadcrumbs[breadcrumb1].angle_bracket,
                            msg=f'Angle bracket is not shown after "{breadcrumb1}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index(breadcrumb2), 1,
                             msg=f'"{breadcrumb2}" sport title is not shown after "{breadcrumb1}"')
            self.assertFalse(breadcrumbs[breadcrumb2].angle_bracket,
                             msg=f'Angle bracket is shown after "{breadcrumb2}" breadcrumb')

            self.assertTrue(
                int(breadcrumbs[breadcrumb2].link.css_property_value('font-weight')) == 700,
                msg=f'"{breadcrumb2}" '
                    f'hyper link from breadcrumbs is not highlighted according to the selected page')
        elif length == 3:
            breadcrumbs = OrderedDict((key.strip(), self.site.sports_page.breadcrumbs.items_as_ordered_dict[key])
                                      for key in self.site.sports_page.breadcrumbs.items_as_ordered_dict)
            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

            self.assertEqual(list(breadcrumbs.keys()).index(breadcrumb1), 0,
                             msg='Home page is not shown the first by default')
            self.assertTrue(breadcrumbs[breadcrumb1].angle_bracket,
                            msg=f'Angle bracket is not shown after "{breadcrumb1}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index(breadcrumb2), 1,
                             msg=f'"{breadcrumb2}" sport title is not shown after "{breadcrumb1}"')
            self.assertTrue(breadcrumbs[breadcrumb2].angle_bracket,
                            msg=f'Angle bracket is not shown after "{breadcrumb2}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index(breadcrumb3), 2,
                             msg=f'"{breadcrumb3}" sub tab name is not shown after "{breadcrumb2}"')
            self.assertFalse(breadcrumbs[breadcrumb3].angle_bracket,
                             msg=f'Angle bracket is shown after "{breadcrumb3}" breadcrumb')

            self.assertTrue(
                int(breadcrumbs[breadcrumb3].link.css_property_value('font-weight')) == 700,
                msg=f'"{breadcrumb3}" '
                    f'hyper link from breadcrumbs is not highlighted according to the selected page')
        else:
            breadcrumbs = OrderedDict((key.strip(), self.site.sports_page.breadcrumbs.items_as_ordered_dict[key])
                                      for key in self.site.sports_page.breadcrumbs.items_as_ordered_dict)
            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

            self.assertEqual(list(breadcrumbs.keys()).index(breadcrumb1), 0,
                             msg='Home page is not shown the first by default')
            self.assertTrue(breadcrumbs[breadcrumb1].angle_bracket,
                            msg=f'Angle bracket is not shown after "{breadcrumb1}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index(breadcrumb2), 1,
                             msg=f'"{breadcrumb2}" sport title is not shown after "{breadcrumb1}"')
            self.assertTrue(breadcrumbs[breadcrumb2].angle_bracket,
                            msg=f'Angle bracket is not shown after "{breadcrumb2}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index(breadcrumb3), 2,
                             msg=f'"{breadcrumb3}" sport title is not shown after "{breadcrumb2}"')
            self.assertTrue(breadcrumbs[breadcrumb3].angle_bracket,
                            msg=f'Angle bracket is not shown after "{breadcrumb3}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index(breadcrumb4), 3,
                             msg=f'"{breadcrumb4}" sub tab name is not shown after "{breadcrumb3}"')
            self.assertFalse(breadcrumbs[breadcrumb4].angle_bracket,
                             msg=f'Angle bracket is shown after "{breadcrumb4}" breadcrumb')

            self.assertTrue(
                int(breadcrumbs[breadcrumb4].link.css_property_value('font-weight')) == 700,
                msg=f'"{breadcrumb4}" '
                    f'hyper link from breadcrumbs is not highlighted according to the selected page')

        # Can not automate right now - there are no changes in html when
        # hovering the mouse over items from Breadcrumbs

    def test_000_precondition(self):
        """
        DESCRIPTION: Precondition
        EXPECTED: Event Created
        """
        self.ob_config.add_autotest_premier_league_football_outright_event()
        football_event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.football_event_id = football_event_params.event_id
        self.__class__.football_event_name = football_event_params.team1 + ' v ' + football_event_params.team2
        self.ob_config.add_UK_racing_event(number_of_runners=2, is_tomorrow=True)
        racing_event = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.racing_eventID = racing_event.event_id
        self.__class__.racing_event_name = f'{self.horseracing_autotest_uk_name_pattern}'

    def test_001_navigate_to_sports_landing_page_and_verify_breadcrumbs_displaying(self):
        """
        DESCRIPTION: Navigate to Sports Landing page and verify Breadcrumbs displaying
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Sports Landing page: 'Home' > 'Sports Name' > 'Sub Tab Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state(state_name='FOOTBALL')
        self.__class__.sport_tab_from_cms = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                    self.ob_config.football_config.category_id)
        self.__class__.expected_sport_tab = self.site.football.tabs_menu.current
        self.assertEqual(self.expected_sport_tab, self.sport_tab_from_cms,
                         msg=f'Default tab is not "{self.sport_tab_from_cms}", it is "{self.expected_sport_tab}"')
        self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='Football', breadcrumb3=self.expected_sport_tab.title(), length=3)

    def test_002_choose_some_tab_from_sports_sub_tab_menu(self):
        """
        DESCRIPTION: Choose some tab from Sports Sub Tab menu
        EXPECTED: 'Sub Tab Name' is changed in breadcrumbs trail according to the selected tab (e.g. 'Outrights')
        """
        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.outrights)
        self.assertEqual(self.site.football.tabs_menu.current, self.expected_sport_tabs.outrights,
                         msg=f'"{self.expected_sport_tabs.outrights}" tab is not active')
        breadcrumbs = OrderedDict((key.strip(), self.site.football.breadcrumbs.items_as_ordered_dict[key])
                                  for key in self.site.football.breadcrumbs.items_as_ordered_dict)
        tab_name = self.expected_sport_tabs.outrights.replace('-', ' ').title() if self.expected_sport_tabs.outrights != 'ACCA' else 'ACCA'
        self.assertIn(tab_name, breadcrumbs, msg=f'Sub tab name is not changed to "{tab_name}" in Breadcrumbs trail')

    def test_003_navigate_to_sports_event_details_page_and_verify_breadcrumbs_displaying(self):
        """
        DESCRIPTION: Navigate to Sports Event Details page and verify Breadcrumbs displaying
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Sports * Event Details page: 'Home' > 'Sports Name' > 'Event Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        self.navigate_to_edp(self.football_event_id)
        self.site.wait_content_state(state_name='EventDetails')
        self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='Football', breadcrumb3=self.football_event_name, length=3)

    def test_004_click_on_sports_name_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Sports Name' hyperlink from the breadcrumbs
        EXPECTED: * Default Sports Landing page is loaded
        EXPECTED: * Breadcrumbs are displayed in the next format at the Default * Sports Landing page: 'Home' > 'Sports Name' > 'Sub Tab * * Name' ('Matches' tab is selected by default when navigating to Sports Landing page)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        breadcrumbs = OrderedDict((key.strip(), self.site.football.breadcrumbs.items_as_ordered_dict[key])
                                  for key in self.site.football.breadcrumbs.items_as_ordered_dict)
        breadcrumbs['Football'].link.click()
        self.site.wait_content_state(state_name='Football')
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, self.sport_tab_from_cms,
                         msg=f'Matches tab is not active, active is "{active_tab}"')
        self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='Football', breadcrumb3=active_tab.title(),
                                      length=3)

    def test_005_click_on_back_button_on_the_sports_header(self):
        """
        DESCRIPTION: Click on 'Back' button on the 'Sports' header
        EXPECTED: * Previously selected page is opened
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        self.site.football.header_line.back_button.click()
        self.site.wait_content_state(state_name='EventDetails')
        self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='Football', breadcrumb3=self.football_event_name,
                                      length=3)

    def test_006_repeat_steps_1_5_for_races_and_verify_breadcrumbs_functionality(self):
        """
        DESCRIPTION: Repeat steps 1-5 for Races and verify Breadcrumbs functionality
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        racing_current_tab = self.site.horse_racing.tabs_menu.current
        if self.brand == 'ladbrokes':
            self.assertEqual(racing_current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                             msg=f'Current tab "{racing_current_tab}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')
            self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='Horse Racing',
                                          breadcrumb3=vec.racing.RACING_FEATURED_TAB_NAME.lower(), length=3)
        else:
            self.assertEqual(racing_current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                             msg=f'Current tab "{racing_current_tab}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')
            self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='Horse Racing',
                                          breadcrumb3=vec.racing.RACING_DEFAULT_TAB_NAME.lower(), length=3)
        self.site.horse_racing.tabs_menu.click_button(vec.racing.RACING_FUTURE_TAB_NAME)
        self.assertEqual(self.site.horse_racing.tabs_menu.current, vec.racing.RACING_FUTURE_TAB_NAME,
                         msg=f'"{vec.racing.RACING_FUTURE_TAB_NAME}" tab is not active')
        breadcrumbs = OrderedDict((key.strip(), self.site.sports_page.breadcrumbs.items_as_ordered_dict[key])
                                  for key in self.site.sports_page.breadcrumbs.items_as_ordered_dict)
        tab_name = vec.racing.RACING_FUTURE_TAB_NAME.replace('-', ' ').title() if vec.racing.RACING_FUTURE_TAB_NAME != 'ACCA' else 'ACCA'
        self.assertIn(tab_name.lower(), breadcrumbs, msg=f'Sub tab name is not changed to "{tab_name}" in Breadcrumbs trail')
        self.navigate_to_edp(self.racing_eventID, sport_name='horse-racing')
        self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='Horse Racing',
                                      breadcrumb3=self.racing_event_name, length=3)
        breadcrumbs = OrderedDict((key.strip(), self.site.sports_page.breadcrumbs.items_as_ordered_dict[key])
                                  for key in self.site.sports_page.breadcrumbs.items_as_ordered_dict)
        breadcrumbs['Horse Racing'].link.click()
        self.site.wait_content_state(state_name='Horseracing')
        active_tab = self.site.horse_racing.tabs_menu.current
        if self.brand == 'ladbrokes':
            self.assertEqual(active_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                             msg=f'Current tab "{active_tab}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')
            self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='Horse Racing',
                                          breadcrumb3=vec.racing.RACING_FEATURED_TAB_NAME.lower(), length=3)
        else:
            self.assertEqual(active_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                             msg=f'Current tab "{active_tab}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')
            self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='Horse Racing',
                                          breadcrumb3=vec.racing.RACING_DEFAULT_TAB_NAME.lower(), length=3)
        self.site.horse_racing.header_line.back_button.click()
        self.site.wait_content_state_changed(timeout=5)
        self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='Horse Racing',
                                      breadcrumb3=self.racing_event_name, length=3)

    def test_007_navigate_to_promotions_page_and_verify_breadcrumbs_displaying_at_the_promotions_page(self):
        """
        DESCRIPTION: Navigate to Promotions page and verify Breadcrumbs displaying at the 'Promotions' page
        EXPECTED: * Breadcrumbs are located below the 'Promotions' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the 'Promotions' page: 'Home' > 'Promotions'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        self.navigate_to_page(name='promotions/all')
        self.site.wait_content_state('promotions')
        self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='promotions', length=2)

    def test_008_repeat_the_same_for_player_betsyourcallvirtualslotto_pages(self):
        """
        DESCRIPTION: Repeat the same for 'Player Bets'/'YourCall'/'Virtuals'/'Lotto' pages
        """
        self.site.open_sport(name=self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')
        self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='Virtuals', length=2)
        if self.brand == 'ladbrokes':
            self.navigate_to_page(name='lotto')
            self.site.wait_content_state(state_name='Lotto')
            self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='lotto', length=2)

    def test_009_navigate_to_olympics_landing_page_and_verify_breadcrumbs_functionality(self):
        """
        DESCRIPTION: Navigate to Olympics Landing page and verify Breadcrumbs functionality
        EXPECTED: * Breadcrumbs are located below the 'Olympics' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Olympics Landing page: 'Home' > 'Olympics'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        self.navigate_to_page(name='olympics')
        self.site.wait_content_state_changed(timeout=5)
        self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='olympics', length=2)

    def test_010_choose_some_sport_from_the_list_and_verify_breadcrumbs_displaying_at_the_sports_olympics_landing_page(self):
        """
        DESCRIPTION: Choose some Sport from the list and verify Breadcrumbs displaying at the Sports Olympics Landing page
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Sports Olympics Landing page: 'Home' > 'Olympics' > 'Sports Name' > 'Sub Tab Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        self.navigate_to_page(name='olympics/football')
        self.site.wait_content_state_changed(timeout=5)
        sport_tab_from_cms = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                     self.ob_config.football_config.category_id)
        expected_sport_tab = self.site.football.tabs_menu.current
        self.assertEqual(expected_sport_tab, sport_tab_from_cms,
                         msg=f'Default tab is not "{sport_tab_from_cms}", it is "{expected_sport_tab}"')
        self.breadcrumbs_verification(breadcrumb1='Home', breadcrumb2='olympics', breadcrumb3='Football',
                                      breadcrumb4=expected_sport_tab.title(), length=4)

    def test_011_navigate_to_olympic_sports_event_details_page_and_verify_breadcrumbs_trail(self):
        """
        DESCRIPTION: Navigate to Olympic Sports Event Details page and verify Breadcrumbs trail
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Olympic Sports Event Details page: 'Home' > 'Olympics' > 'Olympic Sports Name' > 'Event Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        # Covered in step 1
