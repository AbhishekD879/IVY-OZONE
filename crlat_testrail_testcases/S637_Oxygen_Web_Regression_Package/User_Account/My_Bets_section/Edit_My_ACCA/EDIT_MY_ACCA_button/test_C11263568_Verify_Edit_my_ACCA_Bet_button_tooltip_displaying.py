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
class Test_C11263568_Verify_Edit_my_ACCA_Bet_button_tooltip_displaying(Common):
    """
    TR_ID: C11263568
    NAME: Verify 'Edit my ACCA/Bet' button tooltip displaying
    DESCRIPTION: Test case verified Edit my Acca tooltip appearing on Open Bets/Cash Out
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place a few Acca bets
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_pageverify_the_tooltip_is_shown_below_the_edit_my_accabet_button_if_visit_open_bets_page_after_the_login(self):
        """
        DESCRIPTION: Navigate to Open Bets page
        DESCRIPTION: Verify the tooltip is shown below the Edit my Acca/Bet button if visit Open Bets page after the login
        EXPECTED: Tooltip with text 'Now you can remove selections from your acca to keep your bet alive' is shown below the first "Edit my Acca/Bet" button
        """
        pass

    def test_002_tap_the_screen_verify_the_tooltip_disappears(self):
        """
        DESCRIPTION: Tap the screen. Verify the tooltip disappears
        EXPECTED: Tooltip disappears
        """
        pass

    def test_003_refresh_the_page_verify_the_tooltip_isnt_shown(self):
        """
        DESCRIPTION: Refresh the page. Verify the tooltip isn't shown
        EXPECTED: Tooltip isn't shown
        """
        pass

    def test_004_suspend_one_of_the_events_from_the_accarelogin_and_verify_the_tooltip_is_not_shown(self):
        """
        DESCRIPTION: Suspend one of the events from the acca.
        DESCRIPTION: Relogin and verify the tooltip is not shown.
        EXPECTED: Tooltip isn't shown if the Edit Acca button is disabled.
        """
        pass

    def test_005_navigate_to_cash_out_pagerelogin_and_verify_the_tooltip_is_shown_below_the_edit_my_accabet_button_if_visit_cash_out_page_after_the_login(self):
        """
        DESCRIPTION: Navigate to Cash Out page
        DESCRIPTION: Relogin and verify the tooltip is shown below the Edit my Acca/Bet button if visit Cash Out page after the login
        EXPECTED: Tooltip with text 'Now you can remove selections from your acca to keep your bet alive' is shown below the first "Edit my Acca/Bet" button
        EXPECTED: OX 105:
        EXPECTED: Tooltip is not shown - rest of the steps should be removed and  are not relevant
        """
        pass

    def test_006_tap_the_screen_verify_the_tooltip_disappears(self):
        """
        DESCRIPTION: Tap the screen. Verify the tooltip disappears
        EXPECTED: Tooltip disappears
        """
        pass

    def test_007_refresh_the_page_verify_the_tooltip_isnt_shown(self):
        """
        DESCRIPTION: Refresh the page. Verify the tooltip isn't shown
        EXPECTED: Tooltip isn't shown
        """
        pass

    def test_008_suspend_one_of_the_events_from_the_accarelogin_and_verify_the_tooltip_is_not_shown(self):
        """
        DESCRIPTION: Suspend one of the events from the acca.
        DESCRIPTION: Relogin and verify the tooltip is not shown.
        EXPECTED: Tooltip isn't shown if the Edit Acca button is disabled.
        """
        pass
