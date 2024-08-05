import time
import pytest
from collections import OrderedDict

import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.back_button
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.login
@vtest
class Test_C2513021_Breadcrumbs_functionality_on_the_Football_Landing_page_for_logged_in_user(BaseSportTest):
    """
    TR_ID: C2513021
    VOL_ID: C9698201
    NAME: Breadcrumbs functionality on the Football Landing page for logged in user
    DESCRIPTION: This test case verifies breadcrumbs functionality on the Football Landing page for logged in user.
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. The user is logged in
    PRECONDITIONS: 3. Football Landing page is opened
    PRECONDITIONS: 4. 'Matches'->'Today' tab is opened by default
    PRECONDITIONS: **Note:**
    PRECONDITIONS: The chosen tab is recorded to Local Storage, in 'key' column see 'OX./football-tab-<username>' parameter and find <tab name> in 'value' column.
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    home_breadcrumb = vec.sb.HOME_FOOTER_ITEM.title()
    default_date_tab = vec.sb.SPORT_DAY_TABS.today
    sport_name = vec.siteserve.FOOTBALL_TAB.title()
    autotest_coupon = vec.siteserve.EXPECTED_COUPON_NAME
    outright_name = f'Outright {int(time.time())}'

    def breadcrumbs_verification(self, expected_name: str = None, page_name='sports_page'):
        """
        This method verifies breadcrumbs details
        :param expected_name: expected tab or event name
        :param page_name: page where to test
        """
        if page_name == 'sports_page':
            page = self.site.sports_page
        elif page_name == 'sport_event_details':
            page = self.site.sport_event_details
        else:
            page = self.site.sports_page
        expected_name = expected_name if expected_name else self.expected_sport_tab
        breadcrumbs = OrderedDict((key.strip(), page.breadcrumbs.items_as_ordered_dict[key])
                                  for key in page.breadcrumbs.items_as_ordered_dict)

        self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

        self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                         msg='Home page is not shown the first by default')
        self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                        msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')

        self.assertEqual(list(breadcrumbs.keys()).index(self.sport_name), 1,
                         msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
        self.assertTrue(breadcrumbs[self.sport_name].angle_bracket,
                        msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')

        if expected_name != 'ACCA' and expected_name.isupper():
            expected_name = expected_name.replace('-', ' ').title()

        self.assertEqual(list(breadcrumbs.keys()).index(expected_name), 2,
                         msg=f'"{expected_name}" item name is not shown after "{self.sport_name}"')
        self.assertFalse(breadcrumbs[expected_name].angle_bracket,
                         msg=f'Angle bracket is shown after "{expected_name}" breadcrumb')
        self.assertTrue(
            int(breadcrumbs[expected_name].link.css_property_value('font-weight')) == 700,
            msg=f'"{expected_name}" hyperlink from breadcrumbs is not highlighted according to the selected page')

        # Can not automate right now - there are no changes in html when
        # hovering the mouse over items from Breadcrumbs
        # breadcrumbs[self.sport_name].link.mouse_over()

    def test_000_precondition(self):
        """
        DESCRIPTION: Login to Oxygen application and create events
        EXPECTED: Oxygen app is loaded
        EXPECTED: The user is logged in
        EXPECTED: Football Landing page is opened
        EXPECTED: 'Matches'->'Today' tab is opened by default
        EXPECTED: Events for all sub tabs are created
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(vec.siteserve.FOOTBALL_TAB)
        self.__class__.expected_sport_tab = self.site.football.tabs_menu.current
        sport_tab_from_cms = \
            self.get_sport_tab_name(
                self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, self.ob_config.football_config.category_id)
        self.assertEqual(self.expected_sport_tab, sport_tab_from_cms,
                         msg=f'Default tab is not "{sport_tab_from_cms}", it is "{self.expected_sport_tab}"')
        current_date_tab = self.site.football.date_tab.current_date_tab
        self.assertEqual(current_date_tab, self.default_date_tab,
                         msg=f'"{self.default_date_tab}" is not active date tab, active is "{current_date_tab}"')
        # outright event
        outright_event_params = self.ob_config.add_autotest_premier_league_football_outright_event(
            event_name=self.outright_name,
            selections_number=1)
        self.__class__.event_outright_id = outright_event_params.event_id
        # in-play event
        start_time = self.get_date_time_formatted_string(seconds=10)
        event_in_play_params = self.ob_config.add_autotest_premier_league_football_event(
            is_live=True,
            start_time=start_time)
        self.__class__.event_in_play_id = event_in_play_params.event_id
        self.__class__.event_in_play_name = f'{event_in_play_params.team1} v {event_in_play_params.team2}'
        # matches/competition event
        event_matches_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_matches_id = event_matches_params.event_id
        self.__class__.event_matches_name = f'{event_matches_params.team1} v {event_matches_params.team2}'
        # coupons

        market_short_name = self.ob_config.football_config.\
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        event_coupons_id = self.ob_config.market_ids[event_matches_params.event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=event_coupons_id, coupon_name=self.autotest_coupon)
        # specials event
        event_specials_params = self.ob_config.add_autotest_premier_league_football_event(special=True)
        self.__class__.event_specials_id = event_specials_params.event_id
        self.__class__.event_specials_name = f'{event_specials_params.team1} v {event_specials_params.team2}'

    def test_001_verify_breadcrumbs_displaying_at_the_football_landing_page(self):
        """
        DESCRIPTION: Verify Breadcrumbs displaying at the Football Landing page
        EXPECTED: * Breadcrumbs are located below the 'Football' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Football Landing page:
        EXPECTED: 'Home' > 'Football' > 'Sub Tab Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        self.breadcrumbs_verification()

    def test_002_choose_outrights_tab_from_football_sub_tab_menu(self, switch_btn=None):
        """
        DESCRIPTION: Choose 'Outrights' tab from Football Sub Tab menu
        EXPECTED: 'Sub Tab Name' is changed in breadcrumbs trail according to selected tab (e.g. 'Outrights')
        """
        switch_btn = switch_btn if switch_btn else self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights, self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(switch_btn)
        self.assertEqual(self.site.football.tabs_menu.current, switch_btn,
                         msg=f'"{switch_btn}" tab is not active')
        breadcrumbs = OrderedDict((key.strip(), self.site.sports_page.breadcrumbs.items_as_ordered_dict[key])
                                  for key in self.site.sports_page.breadcrumbs.items_as_ordered_dict)
        self.assertTrue(breadcrumbs, msg='No breadcrumbs found')
        tab_name = switch_btn.replace('-', ' ').title() if switch_btn != 'ACCA' else 'ACCA'
        self.assertIn(tab_name, breadcrumbs, msg=f'Sub tab name is not changed to "{tab_name}" in Breadcrumbs trail')

    def test_003_navigate_to_outrights_event_page(self, expected_event_id=None, expected_event_name=None):
        """
        DESCRIPTION: Navigate to 'Outrights' event page
        EXPECTED: * Breadcrumbs are located below the 'Football' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Football Outright Event Details page: 'Home' > 'Football' > 'Event Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        event_id, event_name = (expected_event_id, expected_event_name) if expected_event_id and expected_event_name \
            else (self.event_outright_id, self.outright_name)
        self.navigate_to_edp(event_id=event_id)
        self.breadcrumbs_verification(expected_name=event_name, page_name='sport_event_details')

    def test_004_click_on_football_hyperlink_from_the_breadcrumbs(self, switch_btn=None):
        """
        DESCRIPTION: Click on 'Football' hyperlink from the breadcrumbs
        EXPECTED: * Football Landing page is loaded
        EXPECTED: * Breadcrumbs are displayed in the next format at the Football Landing page:
        EXPECTED: 'Home' > 'Football' > 'Sub Tab Name' (Previously selected tab is opened (e.g. 'Outright') when navigating to Football Landing page)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        switch_btn = switch_btn if switch_btn else self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights, self.ob_config.football_config.category_id)
        breadcrumbs = OrderedDict((key.strip(), self.site.sport_event_details.breadcrumbs.items_as_ordered_dict[key])
                                  for key in self.site.sport_event_details.breadcrumbs.items_as_ordered_dict)
        breadcrumbs[self.sport_name].link.click()
        self.site.wait_content_state(state_name='FOOTBALL')
        self.breadcrumbs_verification(expected_name=switch_btn)

    def test_005_click_on_home_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Home' hyperlink  from the breadcrumbs
        EXPECTED: Homepage is loaded
        """
        breadcrumbs = OrderedDict((key.strip(), self.site.sports_page.breadcrumbs.items_as_ordered_dict[key])
                                  for key in self.site.sports_page.breadcrumbs.items_as_ordered_dict)
        breadcrumbs[self.home_breadcrumb].link.click()
        self.site.wait_content_state(state_name='HomePage')

    def test_006_navigate_to_football_landing_page_again_and_verify_which_tab_is_selected(self, switch_btn=None):
        """
        DESCRIPTION: Navigate to Football Landing page again and verify which tab is selected
        EXPECTED: * Breadcrumbs are located below the 'Football' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Football Landing page:
        EXPECTED: 'Home' > 'Football' > 'Sub Tab Name' (Remembered tab is selected in this case from step 4)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        switch_btn = switch_btn if switch_btn else self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights, self.ob_config.football_config.category_id)
        self.site.open_sport(name=self.sport_name)
        self.site.wait_content_state(state_name=self.sport_name)
        self.breadcrumbs_verification(expected_name=switch_btn)

    def test_007_repeat_steps_2_6_for_tabs_on_football_landing_page(self):
        """
        DESCRIPTION: Repeat steps 2-6 for tabs on Football Landing page
        """
        tab_dict = dict.fromkeys([
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                    self.ob_config.football_config.category_id),
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                    self.ob_config.football_config.category_id),
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
                                    self.ob_config.football_config.category_id),
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials,
                                    self.ob_config.football_config.category_id)], (
            self.event_matches_id, self.event_matches_name))
        tab_dict_sp = {self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                               self.ob_config.football_config.category_id): (
            self.event_in_play_id, self.event_in_play_name),
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials,
                                    self.ob_config.football_config.category_id): (
                self.event_specials_id, self.event_specials_name)}
        tab_dict.update(tab_dict_sp)

        for tab, tab_values in tab_dict.items():
            self.test_002_choose_outrights_tab_from_football_sub_tab_menu(switch_btn=tab)
            self.test_003_navigate_to_outrights_event_page(expected_event_id=tab_values[0],
                                                           expected_event_name=tab_values[1])
            self.test_004_click_on_football_hyperlink_from_the_breadcrumbs(switch_btn=tab)
            self.test_005_click_on_home_hyperlink_from_the_breadcrumbs()
            self.test_006_navigate_to_football_landing_page_again_and_verify_which_tab_is_selected(switch_btn=tab)
