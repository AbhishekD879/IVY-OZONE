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
class Test_C44870364__verify_user_can_navigates_to_bet_history_page_by_clicking_on_My_Account(Common):
    """
    TR_ID: C44870364
    NAME: "- verify user can navigates to bet history page by clicking on My Account.
    DESCRIPTION: It is verify Bet History and its contents.
    PRECONDITIONS: Used should be logged in
    PRECONDITIONS: User should have some settled bets.
    """
    keep_browser_open = True

    def test_001_verify_user_can_navigates_to_bet_history_page_by_clicking_on_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: verify user can navigates to bet history page by clicking on History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: User is able to see My Bets with OPEN BETS and SETTLED BETS tabs.
        """
        pass

    def test_002___verify_user_can_view_settled_bets_for_given_time_duration_by_setting_the_calender_dates__from_and_to_dates(self):
        """
        DESCRIPTION: - Verify user can view settled bets for given time duration by setting the Calender dates  (From and To Dates)
        EXPECTED: User is able to see all settled bets based on dates range set in calender.
        """
        pass

    def test_003___verify_bet_history_of__sports__lotto_pools_tabs(self):
        """
        DESCRIPTION: - Verify bet history of  'Sports' , 'Lotto', 'Pools' tabs
        EXPECTED: User is able to see all settled bets based on dates range set in calender for these different bets.
        """
        pass

    def test_004___verify_user_can_scroll_down_the_past_bet_history(self):
        """
        DESCRIPTION: - Verify user can scroll down the past bet history
        EXPECTED: User is able to scroll down and see all bets.
        """
        pass
