import re

import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import get_in_play_module_from_ws


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.mobile_only
@vtest
class Test_C8146752_See_all_counter_and_link_on_In_Play_module_on_SLP(BaseSportTest):
    """
    TR_ID: C8146752
    VOL_ID: C58216978
    NAME: 'See all' counter and link on 'In-Play' module on SLP
    DESCRIPTION: This test case verifies 'See all' counter and link redirection on 'In-Play' module on SLP
    PRECONDITIONS: 1) CMS config:
    PRECONDITIONS: * 'In-Play' module is enabled in CMS > System Configuration > Structure > Inplay Module
    PRECONDITIONS: * 'In-Play' module is created in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: * 'In-play' module is set to 'Active'
    PRECONDITIONS: * 'Inplay event count' is set to any digit e.g. 10
    PRECONDITIONS: 2) In-play events should be present for selected sport e.g. Football
    PRECONDITIONS: 3) To check value, displayed in counter open Dev Tools->Network->WS > featured-sports > FEATURED_STRUCTURE_CHANGED > InplayModule > 'totalEvents' attribute
    PRECONDITIONS: Load the app and navigate to <Sport> Landing page under test e.g. Football
    PRECONDITIONS: Open 'Matches' tab
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load the app and navigate to <Sport> Landing page under test e.g. Football
        DESCRIPTION: Open 'Matches' tab
        """
        inplay_module = self.cms_config.get_sport_module(sport_id=self.ob_config.backend.ti.football.category_id,
                                                         module_type='INPLAY')
        if inplay_module[0]['disabled']:
            raise CmsClientException('"In play module" module is disabled for Football category')
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        result = self.site.football.tabs_menu.click_button(self.expected_sport_tabs.matches)
        self.assertTrue(result, msg=f'"{self.expected_sport_tabs.matches}" tab was not opened')

    def test_001_verify_see_all_link_within_in_play_module(self):
        """
        DESCRIPTION: Verify 'See all' link within 'In-Play' module
        EXPECTED: 'See all' link is located in the header of 'In-Play' module
        """
        self.__class__.see_all_link = self.site.home.tab_content.in_play_module.see_all_link
        self.assertTrue(self.see_all_link.is_displayed(),
                        msg='"See all" link is not located in the header of "In-Play" module')

    def test_002_verify_counter_within_see_all_link(self):
        """
        DESCRIPTION: Verify counter within 'See all' link
        EXPECTED: * Counter shows total number of in-play events for specific sport
        EXPECTED: * Value in Counter corresponds to 'totalEvents' attribute in WS (see preconditions)
        """
        actual_number_of_events = int(re.search(r'\d+', self.see_all_link.name).group())
        in_play_module = get_in_play_module_from_ws()
        expected_number_of_events = in_play_module['totalEvents']
        self.assertEqual(actual_number_of_events, expected_number_of_events,
                         msg=f'Counter within "See all" link "{actual_number_of_events}" is not the same as '
                             f'expected "{expected_number_of_events}"')

    def test_003_tap_on_see_all_link(self):
        """
        DESCRIPTION: Tap on 'See all' link
        EXPECTED: Navigation to In-play page with specific sport tab selected e.g. In-play > Football
        """
        sport_name = vec.siteserve.FOOTBALL_TAB if not self.brand == 'ladbrokes' else vec.siteserve.FOOTBALL_TAB.title()
        self.see_all_link.click()
        self.site.wait_content_state('InPlay', timeout=3)
        sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict

        sport = sports.get(sport_name)
        self.assertTrue(sport, msg=f'"{sport_name}" not found in "{list(sports.keys())}"')
        self.assertTrue(sport.is_selected(),
                        msg=f'"{sport_name}" tab is not selected after navigation to In-Play page')
