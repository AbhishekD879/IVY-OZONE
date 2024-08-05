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
class Test_C64597396_Verify_the_availability_of_the_Calendar_feature_in_the_Open_Bets_tab__Sports_section(Common):
    """
    TR_ID: C64597396
    NAME: Verify the availability of the Calendar feature in the Open Bets tab - Sports section.
    DESCRIPTION: Verify the availability of the Calendar feature in the Open Bets tab - Sports section.
    PRECONDITIONS: User should be successfully logged in and navigate to the My Bets section -&gt; Open Bets tab -&gt; Sports section.
    """
    keep_browser_open = True

    def test_001_1_login_successfully_with_valid_credentials2_mobile_my_bets_page__gt_open_bets_tabtabletdesktop_my_bets_section__gt_open_bets__tab__gt_sports_section(self):
        """
        DESCRIPTION: 1. Login successfully with valid credentials.
        DESCRIPTION: 2. Mobile: 'My Bets' page -&gt; 'Open Bets tab'
        DESCRIPTION: Tablet/Desktop: 'My Bets' Section' -&gt; 'Open Bets  tab -&gt; Sports section'
        EXPECTED: 1. The user should be successfully logged in.
        EXPECTED: 2. Verify that the Calendar shows up in the My Bets tab - Sports section.
        """
        pass
