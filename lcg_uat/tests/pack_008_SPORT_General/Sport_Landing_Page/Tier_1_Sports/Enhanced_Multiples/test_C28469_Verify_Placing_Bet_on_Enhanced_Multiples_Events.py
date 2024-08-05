import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.enhanced_multiples
@pytest.mark.football
@pytest.mark.ob_smoke
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C28469_Verify_Placing_Bet_on_Enhanced_Multiples_Events(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28469
    VOL_ID: C9698092
    NAME: Verify placing a bet on Enhanced Multiples events
    """
    keep_browser_open = True
    expected_bet_type = 'Single (To Win)'
    selection_type = "all to win in 90 Mins"
    selection_name = None
    bet_amount = 1  # specials are configured in TI with min bet != 0.01

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football enhanced multiples event
        """
        event_params = self.ob_config.add_football_event_enhanced_multiples()
        self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
            event_params.team1, event_params.team2, event_params.selection_ids
        self.__class__.selection_name = f'{self.team1}, {self.team2} {self.selection_type}'

    def test_001_login(self):
        """
        DESCRIPTION: Login as user that have enough money to place bet
        EXPECTED: Appropriate user is logged in
        """
        self.site.login()

    def test_002_verify_event_section(self):
        """
        DESCRIPTION: Verify event section
        EXPECTED: name, Price/Odds, Start Time are present and are not empty
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')

        sections = self.site.football.tab_content.accordions_list.get_items(name=vec.racing.ENHANCED_MULTIPLES_NAME)
        self.assertTrue(sections, msg='No event sections are present on page')
        self.assertIn(vec.racing.ENHANCED_MULTIPLES_NAME, sections,
                      msg='No "ENHANCED MULTIPLES" section found in list')
        section = sections[vec.racing.ENHANCED_MULTIPLES_NAME]
        section.expand()
        section_items = section.items_as_ordered_dict
        self.assertTrue(section_items, msg=f'No events found in event section: "{vec.racing.ENHANCED_MULTIPLES_NAME}"')
        event = section_items.get(self.selection_name)
        self.assertTrue(event, msg=f'Event "{self.selection_name}" not found in {list(section_items.keys())}')
        self.verify_event_time_is_present(event)
        self._verify_event_name(event)
        all_prices = event.get_active_prices()
        self.assertTrue(all_prices, msg=f'Event "{self.selection_name}" does not have active selections')

    def test_003_add_selection_with_deep_link(self):
        """
        DESCRIPTION: Add selection with deep link
        EXPECTED: Betslip counter increased
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.selection_name])

    def test_004_enter_stake(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button, Bet is placed successfully, Bet Receipt is shown
        """
        self.__class__.betslip_info = self.place_and_validate_single_bet()

    def test_005_check_bet_receipt(self):
        """
        DESCRIPTION: Check bet receipt
        """
        self.check_bet_receipt_is_displayed()
        self.check_bet_receipt(betslip_info=self.betslip_info)
        self.site.bet_receipt.footer.click_done()

    def test_006_check_balance(self):
        """
        DESCRIPTION: Check user balance has changed
        """
        expected_user_balance = self.user_balance - self.betslip_info['total_stake']
        self.verify_user_balance(expected_user_balance=expected_user_balance)
