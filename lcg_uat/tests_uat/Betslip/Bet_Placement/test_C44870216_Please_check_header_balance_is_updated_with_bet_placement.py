import pytest
from tests.base_test import vtest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.p1
@vtest
class Test_C44870216_Please_check_header_balance_is_updated_with_bet_placement(BaseBetSlipTest):
    """
    TR_ID: C44870216
    NAME: Please check header balance is updated with bet placement
    DESCRIPTION: this test case verify header balance updation
    PRECONDITIONS: UserName: goldenbuild1  Password: password1
    """
    keep_browser_open = True

    def test_000_precondition(self):
        """
        DESCRIPTION: unable to login with this User
        """
        self.site.login()

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage opened
        """
        # This step is covered in precondition

    def test_002_add__any_selection_to_qickbetbetslip(self):
        """
        DESCRIPTION: Add  any selection to QickBet/Betslip
        EXPECTED: Selection added
        """
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), simple_filter(
            LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                    all_available_events=True,
                                                    additional_filters=cashout_filter,
                                                    in_play_event=False)[0]
        market = next((market for market in event['event']['children']), None)
        outcomes_resp = market['market']['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                             for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
        self.open_betslip_with_selections(selection_ids=list(all_selection_ids.values())[0])

    def test_003_verify_the_header_balance_before_placing_bet(self):
        """
        DESCRIPTION: Verify the header balance before placing bet
        EXPECTED: Balance verified
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.place_and_validate_single_bet()

    def test_004_verify_the_header_balance_after_placing_bet(self):
        """
        DESCRIPTION: Verify the header balance after placing bet
        EXPECTED: Balance updated successfully
        """
        self.site.wait_splash_to_hide(3)
        betplaced_balance = self.site.header.user_balance
        self.assertGreater(self.user_balance, betplaced_balance, msg='Balance not updated successfully')
