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
class Test_C44870362_Verify_Cash_Out_and_Edit_My_links_at_the_bottom_of_Open_Settled_Bets(Common):
    """
    TR_ID: C44870362
    NAME: Verify Cash Out and Edit My links at the bottom of Open/Settled Bets.
    DESCRIPTION: This TC is verify Cash Out and EMA Terms & Conditions present in MY BETS.
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True

    def test_001__verify_cash_out_terms__conditions_verify_edit_my_acca_terms__conditionsby_scrolling_down_your_bets_and_see_if_links_are_navigating_to_relevant_pages(self):
        """
        DESCRIPTION: -Verify Cash Out Terms & Conditions
        DESCRIPTION: -Verify Edit My Acca Terms & Conditions
        DESCRIPTION: by scrolling down your bets and see if links are navigating to relevant pages.
        EXPECTED: User should be able to see these links at the bottom of My Bets with Right Arrow present and is clickable.
        EXPECTED: Cash Out Terms & Conditions
        EXPECTED: Edit My Acca Terms & Conditions
        """
        pass
