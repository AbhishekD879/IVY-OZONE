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
class Test_C64597386_Verify_that_the_default_date_range_data_to_be_displayed_in_the_Calendar_in_the_Cashout_tab_is_seven_days(Common):
    """
    TR_ID: C64597386
    NAME: Verify that the default date range data to be displayed in the Calendar in the Cashout tab is seven days.
    DESCRIPTION: Verify that the default date range data to be displayed in the Calendar in the Cashout tab is seven days.
    PRECONDITIONS: User should be successfully logged in and navigate to the My Bets section -&gt; Cashout tab.
    """
    keep_browser_open = True

    def test_001_1_login_successfully_with_valid_credentials2_mobile_my_bets_page__gt_cashout_tab(self):
        """
        DESCRIPTION: 1. Login successfully with valid credentials.
        DESCRIPTION: 2. Mobile: 'My Bets' page -&gt; 'Cashout tab'
        EXPECTED: 1. The user should be successfully logged in.
        EXPECTED: 2. Verify that the Calendar shows up in the Cashout tab.
        """
        pass

    def test_002_verify_the_default_data_shown_in_the_section(self):
        """
        DESCRIPTION: Verify the default data shown in the section
        EXPECTED: By default the last seven days bet details should be displayed in the section.
        """
        pass
