import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C58438962_Launching_iGameMedia_stream_when_QualificationSport_Rules_on_Greyhounds_EDP(Common):
    """
    TR_ID: C58438962
    NAME: Launching iGameMedia stream when Qualification=Sport Rules on Greyhounds EDP
    DESCRIPTION: This test case verifies messages displayed to active/inactive users when trying to launch iGameMedia stream on Greyhounds EDP in case stream is set up with Qualification=Sport Rules
    DESCRIPTION: On Coral only text 'In order to watch the race you must have a funded account or have placed a bet in the last 24 hours' is displayed without No Thanks' & 'Deposit' CTA buttons
    PRECONDITIONS: 1. Greyhounds event should have iGameMedia stream mapped. When mapping select 'Sport Rules' in 'Qualification' column:
    PRECONDITIONS: ![](index.php?/attachments/get/102440637)
    PRECONDITIONS: [How to Map Video Streams to Events][1]
    PRECONDITIONS: [1]:https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events?preview=/36604217/36604218/HowToMapVideoStreamsToEvents.pdf
    PRECONDITIONS: 2. Two users should be created:
    PRECONDITIONS: - inactive i.e. with 0 balance or haven't placed a bet in the last 24 hours
    PRECONDITIONS: - active i.e. with positive balance or have placed a bet in the last 24 hours
    PRECONDITIONS: NOTE! What message is displayed on frontend depends on **failureCode** received in **opt-in** response:
    PRECONDITIONS: https://optin-tst0.ladbrokesoxygen.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID}
    """
    keep_browser_open = True

    def test_001___log_in_as_inactive_user__navigate_to_greyhounds_edp_from_pre_conditions__clicktap_on_watch_button(self):
        """
        DESCRIPTION: - Log in as inactive user
        DESCRIPTION: - Navigate to Greyhounds EDP from pre-conditions
        DESCRIPTION: - Click/tap on 'Watch' button
        EXPECTED: * failureCode: "4105" is received in 'opt-in' response
        EXPECTED: * Pop-up is displayed with the following on Mobile:
        EXPECTED: 1) 'Watch Live' title
        EXPECTED: 2) 'In order to watch the race you must have a funded account or have placed a bet in the last 24 hours' text
        EXPECTED: 3) Event countdown timer
        EXPECTED: 4) 'No, Thanks' & 'Deposit' CTA buttons
        EXPECTED: ![](index.php?/attachments/get/102920769)
        EXPECTED: * On Desktop only text is displayed:
        EXPECTED: ![](index.php?/attachments/get/102920770)
        """
        pass

    def test_002_clicktap_on_no_thanks_button(self):
        """
        DESCRIPTION: Click/tap on 'No Thanks' button
        EXPECTED: * Pop-up is closed
        EXPECTED: * Greyhounds EDP is shown
        """
        pass

    def test_003__clicktap_on_watch_button_again_clicktap_on_deposit_button(self):
        """
        DESCRIPTION: * Click/tap on 'Watch' button again
        DESCRIPTION: * Click/tap on 'Deposit' button
        EXPECTED: Redirection to 'Deposit' page occurs
        """
        pass

    def test_004___log_in_as_active_user__navigate_to_greyhounds_edp_from_pre_conditions__clicktap_on_watch_button(self):
        """
        DESCRIPTION: - Log in as active user
        DESCRIPTION: - Navigate to Greyhounds EDP from pre-conditions
        DESCRIPTION: - Click/tap on 'Watch' button
        EXPECTED: * No failureCode is received in 'opt-in' response
        EXPECTED: * Pop-up is displayed with the following:
        EXPECTED: 1) 'Watch Live' title
        EXPECTED: 2)'This stream has not yet started. Please try again soon' text
        EXPECTED: 3) Event countdown timer
        EXPECTED: 4) 'OK' button
        EXPECTED: ![](index.php?/attachments/get/102920772)
        EXPECTED: * On Desktop only text is displayed:
        EXPECTED: ![](index.php?/attachments/get/102920775)
        """
        pass
