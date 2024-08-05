import pytest
from voltron.utils.waiters import wait_for_haul
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import get_in_play_module_from_ws


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.featured
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.homepage
@pytest.mark.mobile_only
@vtest
class Test_C3245165_Sports_ordering_within_In_Play_module_on_the_Featured_tab(BaseSportTest):
    """
    TR_ID: C3245165
    VOL_ID: C10397629
    NAME: Sports ordering within 'In-Play' module on the 'Featured' tab
    DESCRIPTION: This test case verifies Sports ordering within 'In-Play' module on the 'Featured' tab
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
        DESCRIPTION: Verify Sports ordering within 'In-Play' module
        EXPECTED: Featured tab is opened
        """
        inplay_module_config = self.get_initial_data_system_configuration().get('Inplay Module', {})
        if not inplay_module_config:
            inplay_module_config = self.cms_config.get_system_configuration_item('Inplay Module')
        if not inplay_module_config.get('enabled'):
            raise CmsClientException('"Inplay Module" module is disabled on system config')
        inplay_module = self.cms_config.get_sport_module(module_type='INPLAY')
        id_ = inplay_module[0].get('id')
        sport_details = self.cms_config.get_sport_module_details(_id=id_)
        if inplay_module[0]['disabled']:
            raise CmsClientException('"In play module" module is disabled on homepage')
        num_of_sports_to_display = sport_details.get('inplayConfig').get('maxEventCount')
        self.assertTrue(num_of_sports_to_display >= 2, msg=f'Number of events for Sport is not more then 2'
                                                           f'current {num_of_sports_to_display}')
        self.site.wait_content_state(state_name='HomePage', timeout=5)
        home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(current_tab, home_featured_tab_name,
                         msg=f'Actual Module Ribbon tab selected by default: "{current_tab}", '
                             f'expected: "{home_featured_tab_name}"')

    def test_001_verify_sports_ordering_within_in_play_module(self):
        """
        DESCRIPTION: Verify Sports ordering within 'In-Play' module
        EXPECTED: The ordering of Sports is based on 'categoryDisplayOrder' in ascending set in TI
        """
        inplay_module = get_in_play_module_from_ws()
        self.assertTrue(inplay_module, 'Failed to get inplay module in featured structure changed response in WS')

        inplay_data = inplay_module['data']
        inplay_sports = {}
        for sport_segment in inplay_data:
            if sport_segment['eventCount'] != 0:
                inplay_sports[sport_segment['categoryName']] = sport_segment['displayOrder']
        if not self.brand == 'ladbrokes':
            expected_sports_order = sorted(inplay_sports, key=inplay_sports.get)
        else:
            expected_sports_order = [x.upper() for x in sorted(inplay_sports, key=inplay_sports.get)]
        inplay_module_items = self.site.home.tab_content.in_play_module.items_as_ordered_dict
        self.assertTrue(inplay_module_items, msg='Can not find any module items')
        self.assertEqual(list(inplay_module_items.keys()), expected_sports_order,
                         msg=f'Actual in play module items "{list(inplay_module_items.keys())}'
                             f'is not equal to expected "{expected_sports_order}"')
