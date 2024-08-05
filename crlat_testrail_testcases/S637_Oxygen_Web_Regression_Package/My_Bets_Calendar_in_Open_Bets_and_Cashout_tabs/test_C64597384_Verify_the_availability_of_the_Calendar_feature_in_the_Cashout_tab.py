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
class Test_C64597384_Verify_the_availability_of_the_Calendar_feature_in_the_Cashout_tab(Common):
    """
    TR_ID: C64597384
    NAME: Verify the availability of the Calendar feature in the Cashout tab.
    DESCRIPTION: Verify the availability of the Calendar feature in the Cashout tab.
    PRECONDITIONS: User should be successfully logged in and navigate to the My Bets section -&gt; Cashout tab.
    """
    keep_browser_open = True

    def test_001_1login_successfully_with_valid_credentials2mobile_my_bets_page__gt_cashout_tabtabletdesktop_my_bets_section__gt_cashout_tab(self):
        """
        DESCRIPTION: 1.Login successfully with valid credentials.
        DESCRIPTION: 2.Mobile: 'My Bets' page -&gt; 'Cashout tab'
        DESCRIPTION: Tablet/Desktop: 'My Bets' Section' -&gt; 'Cashout tab'
        EXPECTED: 1. The user should be successfully logged in.
        EXPECTED: 2. Verify that the Calendar shows up in the Cashout tab.
        """
        pass
