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
class Test_C64658634_Verify_GO_TO_SPORTS_CTA_on_My_Bets_page_if_user_not_selects_valid_date_range_from_calendar(Common):
    """
    TR_ID: C64658634
    NAME: Verify 'GO TO SPORTS' CTA on My Bets page if user not selects valid date range from calendar
    DESCRIPTION: Verify 'GO TO SPORTS' CTA on My Bets page if user not selects valid date range from calendar
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * User should have open bets & settled bets
    PRECONDITIONS: Note: Applies to only Mobile Web
    """
    keep_browser_open = True

    def test_001_launch_any_casino_game(self):
        """
        DESCRIPTION: Launch any casino game
        EXPECTED: * User redirects to particular gaming page ex: Roulette page
        EXPECTED: * User able to see 'sports' icon on EZNav panel(header) in gaming page
        """
        pass

    def test_002_tap_sports_icon_from_eznav_panel(self):
        """
        DESCRIPTION: Tap 'sports' icon from ezNav panel
        EXPECTED: * User navigates to 'MyBets' overlay & displays below tabs:
        EXPECTED: Cashout
        EXPECTED: Openbets
        EXPECTED: Settledbets
        """
        pass

    def test_003_tap_openbets_tab(self):
        """
        DESCRIPTION: Tap 'Openbets' tab
        EXPECTED: * User able to see openbets & 'GO TO SPORTS' CTA at bottom of the page
        """
        pass

    def test_004_select_date_range_as_more_than_3_months_of_bet_history(self):
        """
        DESCRIPTION: Select date range as more than 3 months of bet history
        EXPECTED: * User gets a message like 'If you require account or gambling history over longer periods please contact us'
        EXPECTED: * 'GO TO SPORTS' CTA displayed below the message
        """
        pass

    def test_005_select_invalid_date_range_that_is_future_bet_history(self):
        """
        DESCRIPTION: Select invalid date range that is future bet history
        EXPECTED: * User gets a message like 'Please select a valid time range'
        EXPECTED: * 'GO TO SPORTS' CTA displayed below the message
        """
        pass

    def test_006_repeat_step_45_in_all_inner_tabs_of_settled_bets(self):
        """
        DESCRIPTION: Repeat step-4,5 in all inner tabs of settled bets
        EXPECTED: 
        """
        pass
