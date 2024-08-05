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
class Test_C16268955_Vanilla_Verify_Order_of_Pop_ups_after_LogIn(Common):
    """
    TR_ID: C16268955
    NAME: [Vanilla] Verify Order of Pop-ups after LogIn
    DESCRIPTION: Verify ordering of pop-ups after successful log in
    PRECONDITIONS: The expected sequence of pop-ups after successful login :
    PRECONDITIONS: TutorialOverlay (ONLY **CORAL** )
    PRECONDITIONS: FreeBets pop-up (returned from OB freebets)
    PRECONDITIONS: Odds boost pop-up
    PRECONDITIONS: FreeBets expiry message
    PRECONDITIONS: Note: Following Pop-ups are not displayed as its unplugged on vanilla
    PRECONDITIONS: Login messages
    PRECONDITIONS: Verify Your Account (Netverify)
    PRECONDITIONS: RetailUpgradeOncePrompt after card/pin login
    PRECONDITIONS: Deposit limits increase notification
    PRECONDITIONS: Quick Deposit after Login
    PRECONDITIONS: **Tutorial Overlay pop up only for Tablet and Mobile**
    """
    keep_browser_open = True

    def test_001_clicktap_log_in_button(self):
        """
        DESCRIPTION: Click/Tap 'Log In' button
        EXPECTED: 'Log In' form is displayed
        """
        pass

    def test_002_enter_valid_credentials_and_taplog_in_button(self):
        """
        DESCRIPTION: Enter valid credentials and tap 'Log In' button
        EXPECTED: User is logged in successfully
        EXPECTED: TutorialOverlay is displayed for the user
        EXPECTED: (note: working for the user who logged the first time OR after cleaning cache/incognito window)
        EXPECTED: ![](index.php?/attachments/get/34245)
        """
        pass

    def test_003_close_tutorial_overlay_pop_up(self):
        """
        DESCRIPTION: Close Tutorial Overlay pop-up
        EXPECTED: FreeBets pop-up appears. All available for User Free Bets are displayed in the pop-up.
        EXPECTED: ![](index.php?/attachments/get/34242)
        """
        pass

    def test_004_close_freebets_pop_up(self):
        """
        DESCRIPTION: Close FreeBets pop-up
        EXPECTED: Odds boost pop-up should be displayed for the user.
        EXPECTED: ![](index.php?/attachments/get/34243)
        """
        pass

    def test_005_close_odds_boost(self):
        """
        DESCRIPTION: Close Odds boost
        EXPECTED: FreeBets expiry message should be displayed for the user.
        EXPECTED: (note: Is displayed in case the user has at least 1 free bat that will be expired in future 24h)
        EXPECTED: ![](index.php?/attachments/get/34244)
        """
        pass

    def test_006_verify_whether_the_following_sequence_of_pop_ups_is_kept_tutorialoverlayfreebets_pop_up_returned_from_ob_freebetsodds_boost_pop_upfreebets_expiry_messageon_the_login_journey_this_should_be_last_in_the_queue_to_appearif_one_of_the_pop_ups_is_missed_the_next_one_from_the_above_sequence_is_displayed_instead(self):
        """
        DESCRIPTION: Verify whether the following sequence of pop-ups is kept :
        DESCRIPTION: TutorialOverlay
        DESCRIPTION: FreeBets pop-up (returned from OB freebets)
        DESCRIPTION: Odds boost pop-up
        DESCRIPTION: FreeBets expiry message
        DESCRIPTION: On the login journey, this should be last in the queue to appear
        DESCRIPTION: If one of the pop-ups is missed, the next one from the above sequence is displayed instead
        EXPECTED: 
        """
        pass
