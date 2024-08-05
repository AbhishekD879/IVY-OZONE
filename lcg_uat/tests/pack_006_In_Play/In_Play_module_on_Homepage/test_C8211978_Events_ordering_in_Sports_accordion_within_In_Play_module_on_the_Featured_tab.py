import pytest

from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, retry_if_exception_type

from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_expected_inplay_events_order, get_in_play_module_from_ws
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.mobile_only
@pytest.mark.featured
@vtest
class Test_C8211978_Events_ordering_in_Sports_accordion_within_In_Play_module_on_the_Featured_tab(Common):
    """
    TR_ID: C8211978
    VOL_ID: C10559418
    NAME: Events ordering in 'Sports' accordion within 'In-Play' module on the 'Featured' tab
    DESCRIPTION: This test case verifies events ordering in 'Sports' accordion within 'In-Play' module on the 'Featured' tab
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: 3. 'In-Play' module with live events is displayed in 'Featured' tab
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - At least 2 Sports with Live event from different Types are added in CMS > Sports Pages > Homepage > In-Play module > Add Sport > Set number of events for Sport
    PRECONDITIONS: - To check data received in featured-sports MS open Dev Tools > Network > WS > featured-sports
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def get_displayed_events(self, inplay_module_items):
        displayed_events = []
        try:
            for _, sport in inplay_module_items.items():
                displayed_events += list(sport.items_as_ordered_dict.keys())
        except StaleElementReferenceException:
            inplay_module_items = self.site.home.tab_content.in_play_module.items_as_ordered_dict
            displayed_events = []
            for _, sport in inplay_module_items.items():
                displayed_events += list(sport.items_as_ordered_dict.keys())
        return displayed_events

    def test_000_preconditions(self):
        """
        DESCRIPTION: The homepage is opened and 'Featured' tab is selected
        DESCRIPTION: 'In-Play' module with live events is displayed in 'Featured' tab
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
        for _ in range(0, 5):
            inplay_module = get_in_play_module_from_ws()
            if len(inplay_module.keys()) != 0:
                break
            else:
                wait_for_haul(60)
        self.assertTrue(inplay_module, 'Failed to get inplay module in featured structure changed response in WS')

    def test_001_verify_events_ordering_in_sports_accordion_within_in_play_module(self):
        """
        DESCRIPTION: Verify Events ordering in 'Sports' accordion within 'In-Play' module
        EXPECTED: Ordering is as follows:
        EXPECTED: * Sport <Classes> are ordered based on 'classDisplayOrder' attribute from TI in ascending where minus ordinals are displayed first
        EXPECTED: * Sport <Types> within each class are ordered based on 'typeDisplayOrder' attribute from TI in ascending
        EXPECTED: * The events from the same <Type>(Competition) are ordered in the following way:
        EXPECTED: * 'startTime' - chronological order in the first instance
        EXPECTED: * Event 'displayOrder' in ascending
        EXPECTED: * Alphabetical order
        """
        inplay_module_items = self.site.home.tab_content.in_play_module.items_as_ordered_dict
        if not inplay_module_items:
            raise SiteServeException('There are no available In-Play events')

        displayed_events = self.get_displayed_events(inplay_module_items)

        expected_events = get_expected_inplay_events_order()
        self.assertListEqual(displayed_events.sort(), expected_events.sort(),
                             msg=f'Incorrect events order.\nActual is:\n{displayed_events}\n'
                             f'Expected is:\n{expected_events}')
