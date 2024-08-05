from collections import OrderedDict

import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
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
@vtest
class Test_C846779_Breadcrumbs_functionality_on_the_Sports_Landing_page_for_the_logged_out_user(BaseSportTest):
    """
    TR_ID: C846779
    VOL_ID: C9689874
    NAME: Breadcrumbs functionality on the Sports Landing page for the logged out user
    DESCRIPTION: This test case verifies breadcrumbs functionality on the Sports Landing pages for the logged out user.
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. The user is logged out
    PRECONDITIONS: 3. Sports Landing page is opened
    PRECONDITIONS: 4. 'Matches'->'Today' tab is opened by default
    """
    keep_browser_open = True
    default_date_tab = vec.sb.SPORT_DAY_TABS.today
    home_breadcrumb = 'Home'
    sport_name = 'Football'
    device_name = tests.desktop_default
    last_selected_tab = ''

    def breadcrumbs_verification(self):
        """
        This method verifies breadcrumbs details
        """
        breadcrumbs = OrderedDict((key.strip(), self.site.football.breadcrumbs.items_as_ordered_dict[key])
                                  for key in self.site.football.breadcrumbs.items_as_ordered_dict)
        self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

        self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                         msg='Home page is not shown the first by default')
        self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                        msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')

        self.assertEqual(list(breadcrumbs.keys()).index(self.sport_name), 1,
                         msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
        self.assertTrue(breadcrumbs[self.sport_name].angle_bracket,
                        msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')

        self.assertEqual(list(breadcrumbs.keys()).index(self.expected_sport_tab.title()), 2,
                         msg=f'"{self.expected_sport_tab}" sub tab name is not shown after "{self.expected_sport_tab}"')
        self.assertFalse(breadcrumbs[self.expected_sport_tab.title()].angle_bracket,
                         msg=f'Angle bracket is shown after "{self.expected_sport_tab}" breadcrumb')

        self.assertTrue(
            int(breadcrumbs[self.expected_sport_tab.title()].link.css_property_value('font-weight')) == 700,
            msg=f'"{self.expected_sport_tab}" '
                f'hyper link from breadcrumbs is not highlighted according to the selected page')

        # Can not automate right now - there are no changes in html when
        # hovering the mouse over items from Breadcrumbs
        # breadcrumbs[self.sport_name].link.mouse_over()

    def tabs_verification(self, tab_name):
        """
        This method verifies if sub tab is changed in breadcrumbs trail according to selected tab
        """
        self.site.football.tabs_menu.click_button(tab_name)
        self.assertEqual(self.site.football.tabs_menu.current, tab_name,
                         msg=f'"{tab_name}" tab is not active')
        breadcrumbs = OrderedDict((key.strip(), self.site.football.breadcrumbs.items_as_ordered_dict[key])
                                  for key in self.site.football.breadcrumbs.items_as_ordered_dict)
        tab_name = tab_name.replace('-', ' ').title() if tab_name != 'ACCA' else 'ACCA'
        self.assertIn(tab_name, breadcrumbs, msg=f'Sub tab name is not changed to "{tab_name}" in Breadcrumbs trail')

    def test_000_precondition(self):
        """
        DESCRIPTION: Precondition
        EXPECTED: Oxygen app is loaded
        EXPECTED: Sports Landing page is opened
        EXPECTED: 'Matches'->'Today' tab is opened by default
        """
        self.ob_config.add_autotest_premier_league_football_outright_event()
        self.site.open_sport(name=self.sport_name)
        self.site.wait_content_state(state_name=self.sport_name)
        self.__class__.sport_tab_from_cms = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                    self.ob_config.football_config.category_id)
        self.__class__.expected_sport_tab = self.site.football.tabs_menu.current
        self.assertEqual(self.expected_sport_tab, self.sport_tab_from_cms,
                         msg=f'Default tab is not "{self.sport_tab_from_cms}", it is "{self.expected_sport_tab}"')
        current_date_tab = self.site.football.date_tab.current_date_tab
        self.assertEqual(current_date_tab, self.default_date_tab, msg=f'"{self.default_date_tab}" is not active'
                                                                      f' date tab, active is "{current_date_tab}"')

    def test_001_verify_breadcrumbs_displaying_at_the_sports_landing_page(self):
        """
        DESCRIPTION: Verify Breadcrumbs displaying at the Sports Landing page
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Sports Landing page:
        EXPECTED: 'Home' > 'Sports Name' > 'Sub Tab Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        self.breadcrumbs_verification()

    def test_002_choose_outrights_tab_from_sports_sub_tab_menu(self):
        """
        DESCRIPTION: Choose 'Outrights' tab from Sports Sub Tab menu
        EXPECTED: 'Sub Tab Name' is changed in breadcrumbs trail according to selected tab (e.g. 'Outrights')
        """
        self.tabs_verification(self.expected_sport_tabs.outrights)

    def test_003_repeat_step_2_for_all_tabs_in_sports_sub_tab_menu(self):
        """
        DESCRIPTION: Repeat step 2 for all tabs in Sports Sub Tab menu
        EXPECTED: 'Sub Tab Name' is changed in breadcrumbs trail according to selected tab
        """
        tabs = self.cms_config.get_sport_config(category_id=self.ob_config.football_config.category_id).get('tabs')
        tabs_names = [i['label'].upper() for i in tabs if not i['hidden']]
        for tab_name in tabs_names:
            self.__class__.last_selected_tab = tab_name
            self.tabs_verification(tab_name)

    def test_004_click_on_sports_name_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Sports Name' hyperlink from the breadcrumbs
        EXPECTED: * Default Sports Landing page is loaded
        EXPECTED: * Breadcrumbs are displayed in the next format at the Default Sports Landing page:
        EXPECTED: 'Home' > 'Sports Name' > 'Sub Tab Name' ('Matches' tab is selected by default when navigating to Sports Landing page)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        # Click on 'Football' hyperlink from the breadcrumbs
        breadcrumbs = OrderedDict((key.strip(), self.site.football.breadcrumbs.items_as_ordered_dict[key])
                                  for key in self.site.football.breadcrumbs.items_as_ordered_dict)
        breadcrumbs[self.sport_name].link.click()
        self.site.wait_content_state(state_name=self.sport_name)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, self.sport_tab_from_cms,
                         msg=f'Matches tab is not active, active is "{active_tab}"')
        self.breadcrumbs_verification()

    def test_005_click_on_back_button_on_the_sports_header(self):
        """
        DESCRIPTION: Click on 'Back' button on the 'Sports' header
        EXPECTED: * Previously selected page is opened
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        self.site.football.header_line.back_button.click()
        active_tab = self.site.football.tabs_menu.current
        sport_tab_from_cms = \
            self.get_sport_tab_name(self.last_selected_tab.lower(), self.ob_config.football_config.category_id)
        self.assertEqual(active_tab, sport_tab_from_cms,
                         msg=f'"{sport_tab_from_cms}" tab is not active, active is "{active_tab}"')
        self.__class__.breadcrumbs = \
            OrderedDict((key.strip(), self.site.football.breadcrumbs.items_as_ordered_dict[key])
                        for key in self.site.football.breadcrumbs.items_as_ordered_dict)
        self.assertTrue(
            int(self.breadcrumbs[sport_tab_from_cms.title()].link.css_property_value('font-weight')) == 700,
            msg=f'"{sport_tab_from_cms}" hyperlink from breadcrumbs is not highlighted according to the selected page')

    def test_006_click_on_home_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Home' hyperlink  from the breadcrumbs
        EXPECTED: Homepage is loaded
        """
        self.breadcrumbs[self.home_breadcrumb].link.click()
        self.site.wait_content_state(state_name='HomePage')
