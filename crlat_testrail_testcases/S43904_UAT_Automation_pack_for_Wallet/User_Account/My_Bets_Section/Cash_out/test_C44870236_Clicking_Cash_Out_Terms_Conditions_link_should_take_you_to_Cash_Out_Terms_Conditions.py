import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870236_Clicking_Cash_Out_Terms_Conditions_link_should_take_you_to_Cash_Out_Terms_Conditions(Common):
    """
    TR_ID: C44870236
    NAME: Clicking Cash Out Terms & Conditions link should take you to Cash Out Terms & Conditions
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_log_in_and_go_to_my_bets_open_bets(self):
        """
        DESCRIPTION: Log in and go to My Bets->Open Bets
        EXPECTED: You should be on My Bets->Open Bets
        """
        pass

    def test_002_scroll_to_the_bottom_of_the_page_to_where_the_cash_out_terms__conditions_link_is(self):
        """
        DESCRIPTION: Scroll to the bottom of the page to where the Cash Out Terms & Conditions link is
        EXPECTED: You should be at the Cash Out Terms & Conditions link
        """
        pass

    def test_003_click_on_the_link_and_verify_that_you_are_taken_to_the_cash_out_terms__conditions_page(self):
        """
        DESCRIPTION: Click on the link and verify that you are taken to the Cash Out Terms & Conditions page
        EXPECTED: You should be on the Cash Out Terms & Conditions page
        """
        pass
