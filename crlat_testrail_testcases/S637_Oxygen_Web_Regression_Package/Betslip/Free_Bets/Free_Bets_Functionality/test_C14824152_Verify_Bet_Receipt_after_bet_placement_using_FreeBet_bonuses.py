import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C14824152_Verify_Bet_Receipt_after_bet_placement_using_FreeBet_bonuses(Common):
    """
    TR_ID: C14824152
    NAME: Verify Bet Receipt after bet placement using FreeBet bonuses
    DESCRIPTION: This test case verifies Bet Receipt after bet placement using FreeBet bonuses
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. User should have Free Bets available on their account
    PRECONDITIONS: 4. Make bet placement for selection using only free bet bonuses
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    PRECONDITIONS: ----
    PRECONDITIONS: For DEV/TST env. - https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: For PROD/HL envs:
    PRECONDITIONS: Coral: https://sports.coral.co.uk/promotions/details/new-customer-offer (Open a new online, mobile or telephone account with Coral. Place a £5+ Win or £5+ Each Way bet on any sport. Coral will give you an instant four x £5 free bets.)
    PRECONDITIONS: Ladbrokes: https://m.ladbrokes.com/en-gb/#!/promotions/0 (Register a new Ladbrokes account on mobile or online using promo code '20FREE'. Place cumulative qualifying stakes to a total of £5 win or £5 each-way at odds totalling 1/2 or greater.)
    """
    keep_browser_open = True

    def test_001_verify_bet_receipt_after_bet_placement_using_only_for_example_500_freebet_bonuses(self):
        """
        DESCRIPTION: Verify bet receipt after bet placement using only, for example, £5.00 FreeBet bonuses
        EXPECTED: *[Before OX100]*
        EXPECTED: Stake for this bet: £5.00  ('Stake' for Coral)
        EXPECTED: Free Bet Amount: -£5.00
        EXPECTED: Potential Returns: £xx.xx  ('Est. Returns' for Coral)
        EXPECTED: Total Stake £5.00
        EXPECTED: Potential Returns: £xx.xx ('Estimated Returns' for Coral)
        EXPECTED: *[From OX100.1]*
        EXPECTED: **Coral:**
        EXPECTED: - "Stake: [Free Bet signposting icon][Free Bet value (e.g.£5.00)]"
        EXPECTED: - "Est. Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: - "Total Stake: [Free Bet signposting icon][Free Bet value (e.g.£5.00)]"
        EXPECTED: - "Estimated Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: **Ladbrokes:**
        EXPECTED: - "Stake for this bet: [Free Bet signposting icon][Free Bet value (e.g.£5.00)]"
        EXPECTED: - "Potential Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: - "Total Stake: [Free Bet signposting icon][Free Bet value (e.g.£5.00)]"
        EXPECTED: - "Potential Returns: [Value, (e.g.£xx.xx or N/A)]"
        """
        pass

    def test_002_verify_bet_receipt_after_bet_placement_using_for_example_500_freebet_bonuses_plus_1000_cash_stake(self):
        """
        DESCRIPTION: Verify bet receipt after bet placement using, for example, £5.00 FreeBet bonuses + £10.00 Cash stake
        EXPECTED: *[Before OX100]*
        EXPECTED: Stake for this bet: £15.00  ('Stake' for Coral)
        EXPECTED: Free Bet Amount: -£5.00
        EXPECTED: Potential Returns: £xx.xx   ('Est. Returns' for Coral)
        EXPECTED: Total Stake £15.00
        EXPECTED: Potential Returns: £xx.xx    ('Estimated Returns' for Coral)
        EXPECTED: *[From OX100.1]*
        EXPECTED: **Coral:**
        EXPECTED: - "Stake: [Free Bet signposting icon][Free Bet value (e.g.£5.00)] [+] [Stake value, (e.g.£10.00)]"
        EXPECTED: - "Est. Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: - "Total Stake: [Free Bet signposting icon][Free Bet(s) value (e.g.£5.00)] [+] [Stake(s) value (e.g.£10.00)]"
        EXPECTED: - "Estimated Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: **Ladbrokes:**
        EXPECTED: - "Stake for this bet: [Free Bet signposting icon][Free Bet value (e.g.£5.00)] [+] [Stake value, (e.g.£10.00)]"
        EXPECTED: - "Potential Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: - "Total Stake: [Free Bet signposting icon][Free Bet(s) value (e.g.£5.00)] [+] [Stake(s) value (e.g.£10.00)]"
        EXPECTED: - "Potential Returns: [Value, (e.g.£xx.xx or N/A)]"
        """
        pass
