import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870265_Verify_the_odd_boost_token_priority_When_placing_bets_priority_token_will_be_odd_boost_page_token_order__Verify_restricted_bets_functionality(Common):
    """
    TR_ID: C44870265
    NAME: "Verify the odd boost token priority, (When placing bets priority token will be odd boost page token order ) - Verify restricted bets functionality"
    DESCRIPTION: "Verify the odd boost token priority,
    DESCRIPTION: -
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_verify_the_odd_boost_token_priority(self):
        """
        DESCRIPTION: "Verify the odd boost token priority,
        EXPECTED: (When placing bets priority token will be odd boost page token order )
        EXPECTED: Odds boost is displayed in the betslip and the odds can be boosted.
        """
        pass

    def test_002_verify_restricted_bets_functionality(self):
        """
        DESCRIPTION: Verify restricted bets functionality"
        EXPECTED: Odds boost tokens which are not allowed for the restricted bets shows the error message
        EXPECTED: eg: using a free bet while boosting the odds > restricts the odds boost
        EXPECTED: Screenshot for reference
        EXPECTED: ![](index.php?/attachments/get/114766081)
        """
        pass
