import json
import re

import pytest
import requests

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import get_featured_structure_changed, get_in_play_module_from_ws
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.featured
@pytest.mark.in_play
@pytest.mark.mobile_only
@pytest.mark.reg167_fix
@vtest
class Test_C9229458_See_all_counter_and_link_on_In_Play_module_on_the_Featured_tab_at_the_Homepage(BaseSportTest):
    """
    TR_ID: C9229458
    VOL_ID: C10475255
    NAME: 'See all' counter and link on 'In-Play' module on the 'Featured' tab at the Homepage
    DESCRIPTION: This test case verifies 'See all' counter and link on 'In-Play' module on the 'Featured' tab at the Homepage
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: 3. 'In-Play' module with live events is displayed in 'Featured' tab
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - At least 2 Sports with Live event are added in CMS > Sports Pages > Homepage > In-Play module > Add Sport > Set number of events for Sport
    PRECONDITIONS: - To check data received in featured-sports MS open Dev Tools > Network > WS > featured-sports
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: The homepage is opened and 'Featured' tab is selected
        """
        inplay_module = self.cms_config.get_sport_module(module_type='INPLAY')
        if inplay_module[0]['disabled']:
            raise CmsClientException('"In play module" module is disabled in "Featured" tab')

        self.site.wait_content_state(state_name='HomePage', timeout=5)
        home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(current_tab, home_featured_tab_name,
                         msg=f'Actual Module Ribbon tab selected by default: "{current_tab}", '
                             f'expected: "{home_featured_tab_name}"')

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
        EXPECTED: * Counter shows the total number of in-play events for all Sports
        EXPECTED: * Value in Counter corresponds to 'totalEvents' attribute in WS
        """
        url = 'https://cms-hl.coral.co.uk/cms/api/bma/fsc/0' if self.brand == 'bma' else \
            'https://cms-prod.ladbrokes.com/cms/api/ladbrokes/fsc/0'

        home_page_data = requests.get(url=url)
        # Check the response status code and print the response content
        if home_page_data.status_code == 200:
            # Convert the response content (which is a JSON string) to a dictionary
            homepage_data_response_dict = json.loads(home_page_data.content)
            self.assertTrue(homepage_data_response_dict, msg='Data object is not expected to be empty.')

        result = wait_for_result(
            lambda: abs(int(re.search(r'\d+', self.see_all_link.name).group()) - next((module.get('totalEvents', 0) for module
                                                                                       in homepage_data_response_dict
                                                                                      .get('modules', []) if module.get('@type') == 'InplayModule'),
                                                                                      0)) < 2,
            bypass_exceptions=(AttributeError, ),
            name='Counter to be equal',
            timeout=5)
        expected_counter = next((module.get('totalEvents', 0) for module in homepage_data_response_dict
                                .get('modules', []) if module.get('@type') == 'InplayModule'), 0)
        actual_counter = int(re.search(r'\d+', self.see_all_link.name).group())
        self.assertTrue(result, msg=f'Counter within "See all" link "{actual_counter}" is not the same as received '
                                    f'in WS "{expected_counter}" within delta 1')

    def test_003_tap_on_see_all_link(self):
        """
        DESCRIPTION: Tap on 'See all' link
        EXPECTED: The user navigates to 'In-play' page the first Sports tab is selected by default e.g. In-play > Football
        """
        self.see_all_link.click()
        self.site.wait_content_state('InPlay', timeout=3)
        sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(sports, msg='Sports list tab is not present')
        selected_tab_name = next((tab_name for tab_name, tab in sports.items() if tab.is_selected(timeout=5)), None)
        self.assertTrue(selected_tab_name, msg='Cannot find selected tab')
        first_tab_name, _ = list(sports.items())[1]
        self.assertEqual(selected_tab_name, first_tab_name,
                         msg=f'Selected tab "{selected_tab_name}" is not first tab "{first_tab_name}"')
