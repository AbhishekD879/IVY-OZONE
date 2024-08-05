import pytest

from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.bpg
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C10474861_BPG_icon_presence_on_Racing_EDP(Common):
    """
    TR_ID: C10474861
    NAME: BPG icon presence on Racing EDP
    DESCRIPTION: Test is used to check BPG icon presence status on Racing EDP depending on GP checkbox set on market level in TI
    PRECONDITIONS: 1. Event with GP price is available (GP available checkbox is selected on market level in TI (isGpAvailable="true" attribute is returned for the market from SiteServer)) is present
    PRECONDITIONS: 2. Event without GP price is available
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        self.__class__.eventID = self.ob_config.add_UK_racing_event(number_of_runners=1, gp=True, lp_prices=['2/3']).event_id
        self.__class__.eventID_not_gp = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=['3/4']).event_id

    def test_001_open_race_even_details_page_with_gp_price(self):
        """
        DESCRIPTION: Open <Race> Even Details Page with GP price
        EXPECTED: BPG icon is displayed on market header
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]

        self.assertTrue(market.section_header.is_bpg_icon_present(), msg='BPG icon is not shown')

    def test_002_open_race_even_details_page_without_gp_price(self):
        """
        DESCRIPTION: Open <Race> Even Details Page without GP price
        EXPECTED: BPG icon is not displayed on market header
        """
        self.navigate_to_edp(event_id=self.eventID_not_gp, sport_name='horse-racing')

        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]

        self.assertFalse(market.section_header.is_bpg_icon_present(expected_result=False),
                         msg='BPG icon is not shown')
