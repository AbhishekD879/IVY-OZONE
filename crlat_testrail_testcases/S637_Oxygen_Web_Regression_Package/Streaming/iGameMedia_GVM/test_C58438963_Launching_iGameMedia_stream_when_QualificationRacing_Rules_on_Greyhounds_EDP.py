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
class Test_C58438963_Launching_iGameMedia_stream_when_QualificationRacing_Rules_on_Greyhounds_EDP(Common):
    """
    TR_ID: C58438963
    NAME: Launching iGameMedia stream when Qualification=Racing Rules on Greyhounds EDP
    DESCRIPTION: This test case verifies messages displayed to active/inactive users when trying to launch iGameMedia stream on Greyhounds EDP in case stream is set up with Qualification=Racing Rules
    PRECONDITIONS: 1. Greyhounds event should have iGameMedia stream mapped. When mapping select 'Racing Rules' in 'Qualification' column:
    PRECONDITIONS: ![](index.php?/attachments/get/102440637)
    PRECONDITIONS: [How to Map Video Streams to Events][1]
    PRECONDITIONS: [1]:https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events?preview=/36604217/36604218/HowToMapVideoStreamsToEvents.pdf
    PRECONDITIONS: 2. Two users should be created:
    PRECONDITIONS: - inactive i.e. with 0 balance or haven't placed a bet in the last 24 hours
    PRECONDITIONS: - active #1: with positive balance or have placed any bet in the last 24 hours
    PRECONDITIONS: - active #2: with positive balance or have placed any bet in the last 24 hours AND have placed a bet on the event under test
    PRECONDITIONS: NOTE! What message is displayed on frontend depends on **failureCode** received in **opt-in** response:
    PRECONDITIONS: https://optin-tst0.ladbrokesoxygen.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID}
    """
    keep_browser_open = True

    def test_001___log_in_as_inactive_user__navigate_to_greyhounds_edp_from_pre_conditions__clicktap_on_watch_button(self):
        """
        DESCRIPTION: - Log in as inactive user
        DESCRIPTION: - Navigate to Greyhounds EDP from pre-conditions
        DESCRIPTION: - Click/tap on 'Watch' button
        EXPECTED: * failureCode: "4104" is received in 'opt-in' response
        EXPECTED: * Pop-up is displayed with the following on Mobile:
        EXPECTED: 1) 'Watch Live' title
        EXPECTED: 2) 'In order to view this event you need to place a be greater than or equal to £1' text
        EXPECTED: 3) Event countdown timer
        EXPECTED: 4) 'OK' button
        EXPECTED: ![](index.php?/attachments/get/102922910)
        EXPECTED: * On Desktop only text is displayed:
        EXPECTED: ![](index.php?/attachments/get/102922916)
        """
        pass

    def test_002___log_in_as_active_user_1__navigate_to_greyhounds_edp_from_pre_conditions__clicktap_on_watch_button(self):
        """
        DESCRIPTION: - Log in as active user #1
        DESCRIPTION: - Navigate to Greyhounds EDP from pre-conditions
        DESCRIPTION: - Click/tap on 'Watch' button
        EXPECTED: * failureCode: "4104" is received in 'opt-in' response
        EXPECTED: * Pop-up is displayed with the following on Mobile:
        EXPECTED: 1) 'Watch Live' title
        EXPECTED: 2) 'In order to view this event you need to place a be greater than or equal to £1' text
        EXPECTED: 3) Event countdown timer
        EXPECTED: 4) 'OK' button
        EXPECTED: ![](index.php?/attachments/get/102922910)
        EXPECTED: * On Desktop only text is displayed:
        EXPECTED: ![](index.php?/attachments/get/102922916)
        """
        pass

    def test_003___log_in_as_active_user_2__navigate_to_greyhounds_edp_from_pre_conditions__clicktap_on_watch_button(self):
        """
        DESCRIPTION: - Log in as active user #2
        DESCRIPTION: - Navigate to Greyhounds EDP from pre-conditions
        DESCRIPTION: - Click/tap on 'Watch' button
        EXPECTED: * No failureCode is received in 'opt-in' response
        EXPECTED: * Pop-up is displayed with the following on Mobile:
        EXPECTED: 1) 'Watch Live' title
        EXPECTED: 2) 'This stream has not yet started. Please try again soon' text
        EXPECTED: 3) Event countdown timer
        EXPECTED: 4) 'OK' button
        EXPECTED: ![](index.php?/attachments/get/102924223)
        EXPECTED: * On Desktop only 'This stream has not yet started. Please try again soon' text is displayed
        """
        pass
