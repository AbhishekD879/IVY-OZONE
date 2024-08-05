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
class Test_C59013477_Verify_that_one_SS_response_is_received_during_certain_actions_regarding_selections_in_Betslip(Common):
    """
    TR_ID: C59013477
    NAME: Verify that one SS response is received during certain actions regarding selections in Betslip
    DESCRIPTION: Test case verifies data source being set as SS for certain actions regarding <Race>/<Sport> selections within Betslip.
    PRECONDITIONS: * Upcoming events should be present for a chosen <Race/<Sport> type
    PRECONDITIONS: * At least 1 'undisplayed' selection from an active event should be present in TI
    PRECONDITIONS: * Oxygen app should be opened
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: **Steps 1,2 can be skipped when tested in Desktop/Tablet views**
    PRECONDITIONS: DevTools should be opened (Click on 'Inspect') -> 'Network' tab -> 'XHR' filter
    """
    keep_browser_open = True

    def test_001_mobile_onlyadd_any_selection_to_betslip_via_quickbet(self):
        """
        DESCRIPTION: (Mobile Only)
        DESCRIPTION: Add any selection to Betslip via QuickBet
        EXPECTED: * New selection is added into the Betslip
        EXPECTED: * SS 'simple' response is received with event ID that contains added selection and its data
        EXPECTED: ![](index.php?/attachments/get/113549351)
        """
        pass

    def test_002_mobile_onlyclear_betslip_by_tapping_on_x_button__or_remove_all_button(self):
        """
        DESCRIPTION: (Mobile Only)
        DESCRIPTION: Clear Betslip by tapping on 'X' button  or 'Remove All' button
        EXPECTED: * Betslip is cleared of any stakes and closed
        EXPECTED: * SS 'simple' response is not received
        """
        pass

    def test_003_add_a_selection_through_a_deeplink_into_the_betslipbetslipaddselectionidyou_can_set_a_quicklink_containing_a_deeplink_for_testing_on_mobile_wrappers(self):
        """
        DESCRIPTION: Add a selection through a deeplink into the betslip
        DESCRIPTION: '/betslip/add/#selectionID'
        DESCRIPTION: (you can set a QuickLink containing a deeplink for testing on mobile wrappers)
        EXPECTED: * New selection is added into the Betslip
        EXPECTED: * SS 'outcomeforoutcome' response is received with event ID that contains added selection and its data
        EXPECTED: ![](index.php?/attachments/get/113549353)
        """
        pass

    def test_004_try_to_add_an_undisplayed_selection_through_a_deeplink_into_the_betslipbetslipaddselectionidyou_can_set_a_quicklink_containing_a_deeplink_for_testing_on_mobile_wrappers(self):
        """
        DESCRIPTION: Try to Add an 'undisplayed' selection through a deeplink into the betslip
        DESCRIPTION: '/betslip/add/#selectionID'
        DESCRIPTION: (you can set a QuickLink containing a deeplink for testing on mobile wrappers)
        EXPECTED: * Error page is opened
        EXPECTED: * "One or more of your selections are currently unavailable." message is shown
        EXPECTED: * New selection is not added into the Betslip
        EXPECTED: * SS 'outcomeforoutcome' is received but doesn't contain any data regarding selection(or related event) that user tried to add into the betslip
        EXPECTED: ![](index.php?/attachments/get/113549354)
        """
        pass

    def test_005_navigate_to_racesport_edp_with_active_selectionsin_devtools_disable_internet_connectionset_status_to_offline_and_add_1_more_selection_into_betslip(self):
        """
        DESCRIPTION: Navigate to <Race>/<Sport> EDP with active selections
        DESCRIPTION: In DevTools, disable internet connection(set status to Offline) and Add 1 more selection into Betslip
        EXPECTED: * Betslip counter is increased
        EXPECTED: * "Oops! We are having trouble loading this page. Please check your connection" message is shown with 'Try Again' button instead of selections in Betslip
        EXPECTED: * SS 'simple' response is not received
        """
        pass

    def test_006_in_devtools_restore_internet_connectionset_status_to_online_and_tapclick_on_try_again_button(self):
        """
        DESCRIPTION: In DevTools, restore internet connection(set status to Online) and tap/click on 'Try Again' button
        EXPECTED: * New selection is added into the Betslip
        EXPECTED: * SS 'simple' response is received with event ID that contains newly added selection and its data
        EXPECTED: ![](index.php?/attachments/get/113549360)
        """
        pass
