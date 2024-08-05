import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C14742507_Verify_Quick_Bet_receipt_after_bet_placement_using_FreeBet_bonuses(Common):
    """
    TR_ID: C14742507
    NAME: Verify Quick Bet receipt after bet placement using FreeBet bonuses
    DESCRIPTION: This test case verifies Quick Bet receipt after bet placement using FreeBet bonuses
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. User should have Free Bets available on their account
    PRECONDITIONS: 4. Make bet placement for selection using only free bet bonuses
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    """
    keep_browser_open = True

    def test_001_verify_bet_receipt_after_bet_placement_using_only_for_example_500_freebet_bonuses(self):
        """
        DESCRIPTION: Verify bet receipt after bet placement using only, for example, £5.00 FreeBet bonuses
        EXPECTED: The following info is displayed:
        EXPECTED: - 'Bet receipt' header with 'X'
        EXPECTED: - 'Bet Placed Successfully' and time when bet was placed in the format '11/07.2019, 16:25'
        EXPECTED: - bet type name e.g. Single
        EXPECTED: - price of selection bet was struck at e.g. '@ 8/11'
        EXPECTED: - bet id (Coral): receipt no (Ladbrokes)
        EXPECTED: - selection name
        EXPECTED: - market name / event name
        EXPECTED: - promo icons (if available)
        EXPECTED: - Cashout icon (if available)
        EXPECTED: Stake for this bet: £5.00 ('Total Stake' for Coral)
        EXPECTED: Free Bet Amount: -£5.00
        EXPECTED: Potential Returns: £xx.xx ('Est. Returns' for Coral)
        EXPECTED: *[From OX100]*
        EXPECTED: The following info is displayed:
        EXPECTED: - 'Bet receipt' header with 'X'
        EXPECTED: - 'Bet Placed Successfully' and time when bet was placed in the format '11/07.2019, 16:25'
        EXPECTED: - bet type name e.g. Single
        EXPECTED: - price of selection bet was struck at e.g. '@ 8/11'
        EXPECTED: - bet id (Coral): receipt no (Ladbrokes)
        EXPECTED: - selection name
        EXPECTED: - market name / event name
        EXPECTED: - promo icons (if available)
        EXPECTED: - Cashout icon (if available)
        EXPECTED: Stake for this bet: FB £5.00 ('Stake' for Coral)
        EXPECTED: Potential Returns: £xx.xx ('Est. Returns' for Coral)
        """
        pass

    def test_002_verify_bet_receipt_after_bet_placement_using_for_example_500_freebet_bonuses_plus_500_cash_stake(self):
        """
        DESCRIPTION: Verify bet receipt after bet placement using, for example, £5.00 FreeBet bonuses + £5.00 Cash stake
        EXPECTED: The following info is displayed:
        EXPECTED: - 'Bet receipt' header with 'X'
        EXPECTED: - 'Bet Placed Successfully' and time when bet was placed in the format '11/07.2019, 16:25'
        EXPECTED: - bet type name e.g. Single
        EXPECTED: - price of selection bet was struck at e.g. '@ 8/11'
        EXPECTED: - bet id (Coral): receipt no (Ladbrokes)
        EXPECTED: - selection name
        EXPECTED: - market name / event name
        EXPECTED: - promo icons (if available)
        EXPECTED: - Cashout icon (if available)
        EXPECTED: Stake for this bet: £10.00 ('Total Stake' for Coral)
        EXPECTED: Free Bet Amount: -£5.00
        EXPECTED: Potential Returns: £xx.xx ('Est. Returns' for Coral)
        EXPECTED: *[From OX100]*
        EXPECTED: The following info is displayed:
        EXPECTED: - 'Bet receipt' header with 'X'
        EXPECTED: - 'Bet Placed Successfully' and time when bet was placed in the format '11/07.2019, 16:25'
        EXPECTED: - bet type name e.g. Single
        EXPECTED: - price of selection bet was struck at e.g. '@ 8/11'
        EXPECTED: - bet id (Coral): receipt no (Ladbrokes)
        EXPECTED: - selection name
        EXPECTED: - market name / event name
        EXPECTED: - promo icons (if available)
        EXPECTED: - Cashout icon (if available)
        EXPECTED: Stake for this bet: FB £5.00 + £5.00 ('Stake' for Coral)
        EXPECTED: Potential Returns: £xx.xx ('Est. Returns' for Coral)
        """
        pass
