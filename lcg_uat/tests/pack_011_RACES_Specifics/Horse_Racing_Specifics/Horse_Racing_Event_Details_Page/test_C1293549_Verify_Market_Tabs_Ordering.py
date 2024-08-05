import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod # Coral only
# @pytest.mark.crl_hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.markets
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.low
@vtest
class Test_C1293549_Verify_Market_Tabs_Ordering(BaseRacing):
    """
    TR_ID: C1293549
    NAME: Verify Market Tabs Ordering
    """
    keep_browser_open = True

    def test_000_create_events(self):
        """
        DESCRIPTION: Create event in OB TI
        """
        markets = [
            ('win_only', {'cashout': True}),
            ('betting_without', {'without_runner': 2}),
            ('to_finish_second',),
            ('to_finish_third',),
            ('to_finish_fourth',),
            ('place_insurance_2',),
            ('place_insurance_3',),
            ('place_insurance_4',),
            ('top_2_finish',),
            ('top_3_finish',),
            ('top_4_finish',)
        ]
        event_params = self.ob_config.add_UK_racing_event(markets=markets)
        self._logger.info('*** Created Horse racing event with parameters {}'.format(event_params))
        self.__class__.eventID = event_params.event_id

    def test_001_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_002_verify_market_tabs_ordering(self):
        """
        DESCRIPTION: Verify market tabs ordering
        EXPECTED: The tabs are sorted in following order:
        EXPECTED: *   'Win Or E/W' tab
        EXPECTED: *   'Win Only' tab
        EXPECTED: *   'Betting WO' tab
        EXPECTED: *   'To Finish' tab
        EXPECTED: *   'Top Finish' tab
        EXPECTED: *   'Place Insurance' tab
        EXPECTED: *   'More Markets' tab
        """
        expected_tabs = [vec.racing.RACING_EDP_MARKET_TABS.win_or_ew, vec.racing.RACING_EDP_MARKET_TABS.win_only,
                         vec.racing.RACING_EDP_MARKET_TABS.betting_wo, vec.racing.RACING_EDP_MARKET_TABS.to_finish,
                         vec.racing.RACING_EDP_MARKET_TABS.top_finish, vec.racing.RACING_EDP_MARKET_TABS.more_markets]
        tabs = list(self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.
                    items_as_ordered_dict.keys())
        self.assertEqual(tabs, expected_tabs,
                         msg=f'Tabs on event details page: "{tabs}", expected tabs: "{expected_tabs}"')
