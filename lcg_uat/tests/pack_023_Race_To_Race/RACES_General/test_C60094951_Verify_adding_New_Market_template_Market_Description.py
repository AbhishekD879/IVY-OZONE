import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot add events on prod
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C60094951_Verify_adding_New_Market_template_Market_Description(Common):
    """
    TR_ID: C60094951
    NAME: Verify adding New Market template- Market Description
    DESCRIPTION: Verify that as an Admin role user has access to add New Market template to the Market Description table
    PRECONDITIONS: 1: User should have CMS access
    """
    keep_browser_open = True
    markets = [('win_only',)]

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be logged into CMS
        """
        if self.cms_config.get_system_configuration_structure()['RacingEDPMarketsDescription']['enabled']:
            self.cms_config.update_system_configuration_structure(config_item='RacingEDPMarketsDescription',
                                                                  field_name='enabled', field_value=True)

    def test_002_navigate_to_racing_edp_template_and_add_new_market_to_the_market_description_table(self):
        """
        DESCRIPTION: Navigate to Racing EDP template and add new market to the Market description table
        EXPECTED: User should be able to Add new market to the Market description table
        """
        self.cms_config.create_and_update_markets_with_description(name='Win Only', description='Win Only bet is a single bet.', New_badge=True)
        event = self.ob_config.add_virtual_racing_event(number_of_runners=1, markets=self.markets)
        self.navigate_to_page('horse-racing')
        self.navigate_to_edp(event_id=event.event_id, sport_name='horse-racing')
        self.site.wait_content_state_changed()
        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='No market tabs found on EDP')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_only)
        result = self.site.racing_event_details.market_description
        cms_markets = self.cms_config.get_markets_with_description()
        expected_description = next((market['description'] for market in cms_markets if market['name'] == 'Win Only'))
        self.assertEqual(result, expected_description, msg=f'Actual description "{result}" is not same as Expected description "{expected_description}"')
