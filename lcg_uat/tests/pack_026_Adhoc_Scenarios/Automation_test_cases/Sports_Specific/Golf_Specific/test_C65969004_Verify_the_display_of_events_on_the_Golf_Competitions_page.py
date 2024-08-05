import pytest
from crlat_cms_client.utils.exceptions import CMSException
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.sports_specific
@pytest.mark.golf_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
# @pytest.mark.hl
@vtest

class Test_C65969004_Verify_the_display_of_events_on_the_Golf_Competitions_page(Common):
    """
    TR_ID: C65969004
    NAME: Verify the display of events on the Golf Competitions page
    DESCRIPTION: This test case verifies the display of events in the Golf Competitions tab
    PRECONDITIONS: 1. CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf.
    PRECONDITIONS: 2. Click on the Competitions tab-&gt; Enable/Disable
    """
    keep_browser_open = True
    all_sports_page = 'az-sports'

    def get_sport_tab_status(self, tab):
        check_events = tab.get("checkEvents")
        has_events = tab.get("hasEvents")
        enabled = tab.get("enabled")
        if not enabled:
            return False
        if check_events is None or has_events is None:
            raise CMSException(
                f'check_events:{check_events} and has_events:{has_events},The paremeters are not present in response')
        if check_events and not has_events:
            return False
        return True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf.
        PRECONDITIONS: 2. Click on the Competitions tab-&gt; Enable/Disable
        """
        all_sub_tabs_for_golf = self.cms_config.get_sport_tabs(sport_id=18)
        competition_tab = next(
            (tab for tab in all_sub_tabs_for_golf if tab.get("displayName").upper() == "COMPETITIONS"),
            None)
        self.assertTrue(competition_tab, msg="Competition tab not found")
        competition_tab_status = self.get_sport_tab_status(competition_tab)
        self.assertTrue(competition_tab_status, msg="Competition tab does not have event")

    def test_001_launch_the_ladbrokes_and_coral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes and Coral application.
        EXPECTED: The application should be launched successfully.
        """
        self.site.go_to_home_page()
        self.site.wait_content_state('Home')
        self._logger.info(f'=====> Launched application and Home page loaded successfully')

    def test_002_select_the_golf_sport_either_from_the_sports_ribbon_or_through_the_a_z_menu(self):
        """
        DESCRIPTION: Select the Golf Sport either from the sports ribbon or through the A-Z menu.
        EXPECTED: User should be redirected to the Golf sport landing page.
        """
        self.navigate_to_page(name=self.all_sports_page)
        a_z_menu = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
        self.assertTrue(a_z_menu, msg='A-Z menu is not present')
        golf = a_z_menu.get('Golf')
        self.assertTrue(golf, msg='golf sport is not present in a-z sports')
        golf.click()
        self.site.wait_content_state(state_name='Golf')
        self._logger.info(f'=====> Navigated to Golf sport page successfully')

    def test_003_select_the_competitions_tab(self):
        """
        DESCRIPTION: Select the Competitions tab
        EXPECTED: User should be redirected to the Golf Competitions page.
        EXPECTED: The various Competitions should be displayed on the page.
        """
        current_tab = self.site.golf.tabs_menu.current
        if current_tab.upper() != vec.SB.TABS_NAME_COMPETITIONS.upper():
            self.site.golf.tabs_menu.click_button(vec.SB.TABS_NAME_COMPETITIONS.upper())

    def test_004_verify_the_accordions_on_the_page(self):
        """
        DESCRIPTION: Verify the accordion's on the page.
        EXPECTED: User should be able to see first 3 accordion's should be expanded by default.
        EXPECTED: User should be able to expand/collapse the accordion's
        """
        accordions = list(self.site.golf.tab_content.competitions_categories_list.items_as_ordered_dict.items())
        self.assertTrue(accordions, msg='No accordions found on page')
        for accordion_name, accordion in accordions[0:3]:
            self.assertTrue(accordion.is_expanded(), msg=f'accordion {accordion_name} is not expanded by default')
            accordion.collapse()
            self.assertFalse(accordion.is_expanded(), msg=f'accordion {accordion_name} is not collapsed after clicking on it')
            accordion.expand()
            self.assertTrue(accordion.is_expanded(), msg=f'accordion {accordion_name} is not expanded after clicking on it')

