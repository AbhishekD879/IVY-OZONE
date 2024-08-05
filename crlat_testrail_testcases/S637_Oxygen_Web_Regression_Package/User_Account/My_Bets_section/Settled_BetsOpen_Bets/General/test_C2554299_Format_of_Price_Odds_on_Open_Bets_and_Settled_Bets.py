import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C2554299_Format_of_Price_Odds_on_Open_Bets_and_Settled_Bets(Common):
    """
    TR_ID: C2554299
    NAME: Format of Price/Odds on 'Open Bets' and 'Settled Bets'
    DESCRIPTION: This test case verifies Price/Odds in decimal and fractional format on 'Open Bets' and 'Settled Bets'.
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed Singles and Multiple bets on events;
    PRECONDITIONS: User has SETTLED Singles and Multiple bets on event;
    PRECONDITIONS: To change price format you should navigate to My Account->Settings;
    PRECONDITIONS: Fractional format is selected by default
    PRECONDITIONS: Note
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tab_on_my_bets_pageverify_priceodds_of_single_selection(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab on 'My Bets' page
        DESCRIPTION: Verify Price/Odds of Single selection
        EXPECTED: Format of Price/Odds corresponds to: **'priceNum'/'priceDen'** attributes (i.e.9/1)
        """
        pass

    def test_002_verify_priceodds_of_multiples_selection(self):
        """
        DESCRIPTION: Verify Price/Odds of Multiples selection
        EXPECTED: Fractional format Price/Odds correspons to: **'priceNum'/'priceDen'** attributes (i.e.9/1)
        """
        pass

    def test_003_switch_to_decimal_format_for_the_user(self):
        """
        DESCRIPTION: Switch to Decimal format for the user
        EXPECTED: 
        """
        pass

    def test_004_navigate_to_open_bets_tab_on_my_bets_pageverify_priceodds_of_single_selection(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab on 'My Bets' page
        DESCRIPTION: Verify Price/Odds of Single selection
        EXPECTED: Format of Price/Odds corresponds to: **'priceDec'** atribute (i.e.10)
        """
        pass

    def test_005_verify_priceodds_of_multiples_selection(self):
        """
        DESCRIPTION: Verify Price/Odds of Multiples selection
        EXPECTED: Format of Price/Odds corresponds to: **'priceDec'** atribute (i.e.10)
        """
        pass
