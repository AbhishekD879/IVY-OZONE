import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28796_Verify_Back_button(Common):
    """
    TR_ID: C28796
    NAME: Verify Back button
    DESCRIPTION: This test case verifies Back button functionality
    PRECONDITIONS: **JIRA ticket **: BMA-3547, BMA-4830
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_greyhounds_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon on the Sports Menu Ribbon
        EXPECTED: 'Greyhounds' Landing Page is opened
        """
        pass

    def test_003_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_navigate_within_the_event_details_page__tap_back_button(self):
        """
        DESCRIPTION: Navigate within the event details page > tap Back Button
        EXPECTED: User is directed to <Race> landing page irrespectively to the previously navigated tabs
        """
        pass

    def test_005____navigate_to_event_details_page___place_add_selections_to_the_bet_slip___tap_bet_slip_button(self):
        """
        DESCRIPTION: *   Navigate to Event details page
        DESCRIPTION: *   Place add selection(s) to the Bet Slip
        DESCRIPTION: *   Tap "Bet Slip" button
        EXPECTED: *   User is navigated to the Bet Slip page
        EXPECTED: *   Added selection(s) is/are displayed within Bet Slip
        """
        pass

    def test_006_tap_back_button(self):
        """
        DESCRIPTION: Tap Back button
        EXPECTED: User is navigated back to the Event details page, where selections have been added to the Bet Slip
        """
        pass

    def test_007_go_to_other_than_default_tabsubcontrol_on_landing_page__tap_back_button(self):
        """
        DESCRIPTION: Go to other than default tab/subcontrol on Landing page > tap  Back Button
        EXPECTED: User is directed to the landing page irrespectively to the previously navigated tabs/subcontrols
        """
        pass

    def test_008_go_to_the_app_via_direct_link__navigate_inside_the_app___tap_back_button_several_times(self):
        """
        DESCRIPTION: Go to the app via direct link > navigate inside the app -> tap Back button several times
        EXPECTED: User is redirected to the Oxygen Homepage
        """
        pass
