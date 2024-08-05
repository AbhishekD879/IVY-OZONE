import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C53638574_Verify_ACCA_Odds_Notification_feature_toggle_for_quick_recalculation(Common):
    """
    TR_ID: C53638574
    NAME: Verify ACCA Odds Notification feature toggle for quick recalculation
    DESCRIPTION: This test case verifies ACCA Odds Notification feature toggle for quick recalculation
    PRECONDITIONS: - Application is loaded
    PRECONDITIONS: - CMS:
    PRECONDITIONS: system-configuration/structure- accaQuickRecalculation- 'enabled' checkbox is ticked, 'allowLoadingAnimation' checkbox is ticked
    PRECONDITIONS: - Slow 3g is turned on
    PRECONDITIONS: - Filter by 'buildbet' in Network/all
    """
    keep_browser_open = True

    def test_001_add_at_least_two_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip
        EXPECTED: * ACCA Odds Notification message appears
        EXPECTED: * Odds value is shown on Acca bar BEFORE buildBet response came
        EXPECTED: * There is no animation on Acca bar
        """
        pass

    def test_002_go_to_cms_and_disable_accaquickrecalculationrefresh_the_app_and_add_one_more_selection_from_a_different_event(self):
        """
        DESCRIPTION: Go to CMS and disable 'accaQuickRecalculation'
        DESCRIPTION: Refresh the app and add one more selection from a different event
        EXPECTED: * Odds value is updated on Acca bar AFTER buildBet response came
        EXPECTED: * Animation is shown on Acca bar to show the progress of updating acca bar while awaiting of bpp response when no FE calculation performed
        """
        pass

    def test_003_go_to_cms_and_disable_allowloadinganimationrefresh_the_app_and_add_one_more_selection_from_a_different_event(self):
        """
        DESCRIPTION: Go to CMS and disable 'allowLoadingAnimation'
        DESCRIPTION: Refresh the app and add one more selection from a different event
        EXPECTED: * Odds value is updated on Acca bar AFTER buildBet response came
        EXPECTED: * Animation is NOT shown on Acca bar
        """
        pass
