import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.event_details
@pytest.mark.american_football
@pytest.mark.baseball
@pytest.mark.basketball
@pytest.mark.football
@pytest.mark.tennis
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.slow
@pytest.mark.timeout(800)
@pytest.mark.safari
@vtest
class Test_C29172_Verify_Leagues_Type_Names_With_Cash_Out(BaseSportTest):
    """
    TR_ID: C29172
    NAME: Verify Leagues/Type Names with Cash Out option available
    DESCRIPTION: This test case verifies Leagues/Type Names with Cash Out option available on Event Landing Pages
    """
    keep_browser_open = True
    events = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        self.__class__.sport_events = {
            # 'American Football-Money Line': self.ob_config.add_american_football_event_to_autotest_league().event_id,  # BMA-38098
            # 'Baseball-Money Line': self.ob_config.add_baseball_event_to_us_league().event_id,  # BMA-38098
            'Basketball-Money Line': self.ob_config.add_basketball_event_to_us_league().event_id,
            f'Football-Match {"Result" if self.brand != "ladbrokes" else "Betting"}':
                self.ob_config.add_autotest_premier_league_football_event().event_id,
            'Tennis-Match Betting': self.ob_config.add_tennis_event_to_autotest_trophy().event_id,
        }

    def test_001_verify_cashout_for_different_sports(self):
        """
        DESCRIPTION: Verify CashOut availability for different sport types and not displaying on Outrights tab
        """
        for event in self.sport_events:
            sport = event.split('-')[0]
            market = event.split('-')[1]
            event_id = self.sport_events[event]
            self.step_001_verify_cashout_available(sport_name=sport.replace(' ', '-').lower())
            self.step_002_verify_cashout_unavailable()
            self.step_003_verify_cashout_available_on_event_details(event_id=event_id, market=market.upper())

    def step_001_verify_cashout_available(self, sport_name):
        """
        DESCRIPTION: Navigate to Sport page and verify CashOut icon is not available on Matches tab
        """
        self.navigate_to_page(name=f'sport/{sport_name}')
        self.site.wait_content_state(state_name=sport_name)
        self.verify_cashout_label(is_available=False)

    def step_002_verify_cashout_unavailable(self):
        """
        DESCRIPTION: Navigate to Outrights tab and verify CashOut icon unavailable
        """
        self.site.sports_page.tabs_menu.click_button(self.expected_sport_tabs.outrights)
        self.verify_cashout_label(is_available=False)

    def step_003_verify_cashout_available_on_event_details(self, event_id, market):
        """
        DESCRIPTION: Verify CashOut icon available on event details page
        """
        self.navigate_to_edp(event_id=event_id)
        accordions_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        accordions_list = {item_name.upper(): item for item_name, item in accordions_list.items()}
        self.assertTrue(accordions_list, msg='No market was found on page')
        self.assertIn(market, accordions_list)
        found_market = accordions_list[market]
        self.assertTrue(found_market, msg=f'Market {market} was not found')
        self.assertTrue(found_market.market_section_header.has_cash_out_mark(),
                        msg=f'Market {market} have no cashout indicator')
        self.site.go_to_home_page()
        self.site.wait_content_state('HomePage')
