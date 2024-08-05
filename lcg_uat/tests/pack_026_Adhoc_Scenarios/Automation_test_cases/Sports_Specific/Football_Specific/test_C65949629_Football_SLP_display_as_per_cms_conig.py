import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.football_specific
@pytest.mark.adhoc_suite
@pytest.mark.sports_specific
@pytest.mark.desktop
@vtest
class Test_C65949629_Football_SLP_display_as_per_cms_conig(BaseSportTest):
    """
    TR_ID: C65949629
    NAME: Football SLP display as per cms conig.
    DESCRIPTION: This test case is to validate SLP data displaying as per cms config.
    PRECONDITIONS: User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: Football entry points
    PRECONDITIONS: Navigate to     menus>subheadermenus>Football.
    PRECONDITIONS: Click on Football.
    PRECONDITIONS: Make the active check box and in app check box as active.
    PRECONDITIONS: Click on save changes button.
    PRECONDITIONS: Navigate to sport pages>sport categories>football>Genral sport configuration.
    PRECONDITIONS: Enable all the checkboxes present out there.
    PRECONDITIONS: Enter all the mandatory fields.
    PRECONDITIONS: Note : Add primary markets there.
    PRECONDITIONS: Scroll down amd make sure to enable all the tabs(matches,inplay,Specials,outrights) .
    PRECONDITIONS: Click on any one of the tab shown below the tab name and add the market switcher labels.
    PRECONDITIONS: Click on save changes button.
    """
    keep_browser_open = True
    default_date_tab = vec.sb.SPORT_DAY_TABS.today
    all_sports_page = 'az-sports'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Lauch the Ladbrokes/Coral application.
        EXPECTED: Application should be loaded successfully. By-default user is on home page
        """
        all_sport_tabs = self.cms_config.get_sport_tabs(sport_id=16)
        self.__class__.expected_sports_tabs = []
        for tab in all_sport_tabs:
            if tab['enabled'] and not (tab['checkEvents'] and not tab['hasEvents']):
                self.expected_sports_tabs.append(tab['displayName'].upper())
        matches_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, category_id=16)
        if matches_tab_name not in self.expected_sports_tabs:
            raise CmsClientException(f'Matches tab is not enabled for Football in CMS')

    def test_001_lauch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Lauch the Ladbrokes/Coral application.
        EXPECTED: Application should be loaded successfully. By-default user is on home page
        """
        self.site.go_to_home_page()

    def test_002_desktop_navigate_to_sub_header_menu_and_click_on_footballmobile__navigate_to_sports_ribbon_and_click_on_click_on_football(self):
        """
        DESCRIPTION: Desktop: navigate to sub header menu and click on football.
        DESCRIPTION: Mobile : navigate to sports ribbon and click on football.
        EXPECTED: User should be navigated to the  Football landing  page.
        EXPECTED: by default user is in matches tab.
        """
        if self.device_type == 'desktop':
            self.__class__.actual_sports = self.site.header.sport_menu.items_as_ordered_dict
        else:
            self.__class__.actual_sports = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(self.actual_sports, msg='No mobile sport tabs found')
        for sport_name, sport in self.actual_sports.items():
            if sport_name.upper() == 'FOOTBALL':
                sport.click()

    def test_003_then_navigate_to_other_tabs_present_out_there(self):
        """
        DESCRIPTION: Then navigate to other tabs present out there.
        EXPECTED: Events should be loaded successfully
        """
        self.__class__.actual_sports_tabs = self.site.football.tabs_menu.items_as_ordered_dict
        tabs_names = list(self.actual_sports_tabs.keys())
        self.assertListEqual(self.expected_sports_tabs, tabs_names, msg=f' expected sport tabs "{self.expected_sports_tabs}" are not same as actual tabs "{tabs_names}"')
        for tab_name, tab in self.actual_sports_tabs.items():
            tab.click()
            if tab_name.upper() == "INSIGHTS":
                wait_for_haul(2)
            self.site.wait_content_state_changed()
            if self.device_type == 'mobile' and tab_name.upper() == 'COMPETITIONS':
                sections = self.site.football.tab_content.competitions_categories.n_items_as_ordered_dict(no_of_items=3)
            else:
                sections = self.site.football.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=3)
            if not sections:
                self.assertTrue(self.site.football.tab_content.has_no_events_label(), msg=f"No Events found message not displayed under {tab_name} tab even events are not available")
                continue

    def test_004_navigate_to_future_tab(self):
        """
        DESCRIPTION: navigate to future tab
        EXPECTED: Events should be loaded successfully
        """
        self.actual_sports_tabs.get(self.expected_sport_tabs.matches).click()
        if self.device_type == 'desktop':
            current_date_tab = self.site.football.date_tab.current_date_tab
            self.assertEqual(current_date_tab, self.default_date_tab, msg=f'"{self.default_date_tab}" date tab is not '
                                                                          f'active, Current date tab is "{current_date_tab}"')
            date_tabs = self.site.football.date_tab.items_as_ordered_dict
            for tab_name, tab in date_tabs.items():
                if tab_name.upper() == 'FUTURE':
                    tab.click()
                    sections = self.site.football.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=3)
                    if not sections:
                        self.assertTrue(self.site.football.tab_content.has_no_events_label(),
                                        msg=f"No Events found message not displayed under {tab_name} tab even events are not available")
                    break

    def test_005_navigate_back_to_the_home_page(self):
        """
        DESCRIPTION: navigate back to the home page.
        EXPECTED: User should be navigated back to the home page.
        """
        self.site.go_to_home_page()

    def test_006_desktop__navigate_to_a_z_menu_and_click_on_footballmobile__navigate_to_footer_menu_and_click_on_a_z_menu_and_click_on__football(self):
        """
        DESCRIPTION: Desktop : Navigate to A-Z menu and click on football.
        DESCRIPTION: Mobile : navigate to footer menu and click on A-Z menu and click on  football.
        EXPECTED: User should be navigated to the football landing  page.
        """
        if self.device_type == 'desktop':
            a_z_menu = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
        else:
            self.navigate_to_page(name=self.all_sports_page)
            a_z_menu = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
        for sport_name, sport in a_z_menu.items():
            if sport_name.upper() == 'FOOTBALL':
                sport.click()
                break
        self.site.wait_content_state('football')

    def test_007_repeat_3_4_steps(self):
        """
        DESCRIPTION: Repeat 3-4 steps
        EXPECTED: tabs should be loaded successfully.
        """
        # COVERED

    def test_008_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application.
        EXPECTED: Application should be loaded successfully.By default user is on home page
        """
        self.site.login()

    def test_009_repeat_all_the_above_steps(self):
        """
        DESCRIPTION: Repeat all the above steps.
        EXPECTED: Should work as expected.
        """
        self.test_003_then_navigate_to_other_tabs_present_out_there()
        self.test_004_navigate_to_future_tab()
        self.test_005_navigate_back_to_the_home_page()
        self.test_006_desktop__navigate_to_a_z_menu_and_click_on_footballmobile__navigate_to_footer_menu_and_click_on_a_z_menu_and_click_on__football()
