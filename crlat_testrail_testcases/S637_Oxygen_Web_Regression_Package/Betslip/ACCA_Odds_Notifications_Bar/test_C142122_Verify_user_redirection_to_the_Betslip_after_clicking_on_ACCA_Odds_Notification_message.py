import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C142122_Verify_user_redirection_to_the_Betslip_after_clicking_on_ACCA_Odds_Notification_message(Common):
    """
    TR_ID: C142122
    NAME: Verify user redirection to the Betslip after clicking on ACCA Odds Notification message
    DESCRIPTION: AUTOTEST: [C9690002]
    DESCRIPTION: This test case verifies user redirection to the Betslip after clicking on ACCA Odds Notification message
    PRECONDITIONS: - Application is loaded
    PRECONDITIONS: - There are <Sport> events and <Race> events with LP prices
    """
    keep_browser_open = True

    def test_001_open_sport_landing_page(self):
        """
        DESCRIPTION: Open <Sport> Landing page
        EXPECTED: 
        """
        pass

    def test_002_add_two_selections_from_different_sport_events_to_the_betslip(self):
        """
        DESCRIPTION: Add two selections from different <Sport> events to the Betslip
        EXPECTED: * ACCA Odds Notification message appears
        """
        pass

    def test_003_tap_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Tap on ACCA Odds Notification message
        EXPECTED: * User is redirected to the Betslip
        EXPECTED: * Betslip is scrolled up so relevant Multiple is visible for the User
        """
        pass

    def test_004_add_more_selections_from_different_sport_events_to_the_betslip__tap_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Add more selections from different <Sport> events to the Betslip > Tap on ACCA Odds Notification message
        EXPECTED: * User is redirected to the Betslip
        EXPECTED: * Betslip is scrolled up so relevant Multiple is visible for the User
        """
        pass

    def test_005_repeat_steps_1_3_for_race_events_with_lp_selections(self):
        """
        DESCRIPTION: Repeat steps 1-3 for <Race> events with LP selections
        EXPECTED: 
        """
        pass
