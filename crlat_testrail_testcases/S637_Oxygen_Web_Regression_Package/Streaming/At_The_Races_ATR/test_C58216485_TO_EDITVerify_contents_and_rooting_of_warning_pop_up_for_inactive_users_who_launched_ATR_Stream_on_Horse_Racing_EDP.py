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
class Test_C58216485_TO_EDITVerify_contents_and_rooting_of_warning_pop_up_for_inactive_users_who_launched_ATR_Stream_on_Horse_Racing_EDP(Common):
    """
    TR_ID: C58216485
    NAME: [TO-EDIT]Verify contents and rooting of warning pop-up for inactive users who launched ATR Stream on Horse Racing EDP
    DESCRIPTION: [TO-EDIT - after BMA-54820 is implemented we don't need to mock these messages]This test case verifies contents and button functions of the warning pop-up shown to inactive user who tries to view ATR stream on Horse Racing Event Details Page.
    PRECONDITIONS: In order to properly run this test case you need to have a configured **Charles** application on your desktop.
    PRECONDITIONS: Please use following instruction to configure the basic interception for the application: https://confluence.egalacoral.com/display/SPI/Charles+-+HTTP%28S%29+Debugging
    PRECONDITIONS: In order to find out the API url used for Requests/Responses sending/receiving open the Development Tools in your browser, switch to 'Horse Racing' Event Details Page of the event that you will use for the testing and tap/click on 'Watch'/'Live Stream' button.
    PRECONDITIONS: Once that is done, filter the responses with following input 'optin'. Copy the Request URL from the response.
    PRECONDITIONS: ![](index.php?/attachments/get/100978313)
    PRECONDITIONS: In order to intercept request within the Oxygen App, please open your **Charles app**, select 'Proxy' -> 'Breakpoint Settings' option in the header menu.
    PRECONDITIONS: ![](index.php?/attachments/get/66425163)
    PRECONDITIONS: Once 'Breakpoint Settings' modal is opened, make sure that 'Enable Breakpoints' checkbox is checked, and click 'Add' button.
    PRECONDITIONS: ![](index.php?/attachments/get/66425164)
    PRECONDITIONS: In the 'Edit Breakpoint' sub-modal window paste the 'Host name and Domain name' of the previously copied Request URL into the 'Host' field (i.e. optin-tst0.ladbrokesoxygen.nonprod.cloud.ladbrokescoral.com).
    PRECONDITIONS: Also, paste the 'Path' of the previously copied Request URL into the 'Path' field(i.e. /api/video/igame/# - where # is the ID of the event).
    PRECONDITIONS: Select 'HTTPS' protocol within 'Protocol' dropdown and check the 'Response' checkbox'.
    PRECONDITIONS: ![](index.php?/attachments/get/100978312)
    PRECONDITIONS: Once that is done, click 'OK' button to close the sub-modal window, and another 'OK' button to close the modal window.
    PRECONDITIONS: (!) Following pre-conditions should be met:
    PRECONDITIONS: 1. SiteServer event should be configured to support ATR streaming (**'drilldownTagNames'**='EVFLAG_AVA' flag should be set) and should be mapped to ATR stream event
    PRECONDITIONS: 2. HORSE RACING event should have the following attributes:
    PRECONDITIONS: *isMarketBetInRun = "true"
    PRECONDITIONS: 3. User is logged into the Oxygen app and has a positive balance.
    PRECONDITIONS: 4. It should be 2 minutes or less left before event Start Time
    PRECONDITIONS: **Response mock is:**
    PRECONDITIONS: {
    PRECONDITIONS: "code": 1405,
    PRECONDITIONS: "description": "Error on passing qualification",
    PRECONDITIONS: "details": {
    PRECONDITIONS: "failureCode": "4105",
    PRECONDITIONS: "failureKey": "account.videoMinStakeNotPlaced",
    PRECONDITIONS: "failureReason": "Minimum stake bet not placed",
    PRECONDITIONS: "failureDebug": "account.videoMinStakeNotPlaced Minimum stake bet not placed"
    PRECONDITIONS: }
    PRECONDITIONS: }
    PRECONDITIONS: **(!) 'Event countdown' timer is only shown on web and responsive mode for devices - native apps don't have this feature.**
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_horse_racing_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Horse Racing> for the event which satisfies Preconditions
        EXPECTED: Event details page is opened
        EXPECTED: * Mobile or Tablet Responsive:
        EXPECTED: 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_002_mobile_or_tablet_responsivetapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **Mobile or Tablet Responsive**
        DESCRIPTION: Tap/click on 'Watch'/'Live Stream' button
        EXPECTED: * NO Video player is shown above market tabs
        EXPECTED: Optin Request is sent to a microservice(and visible in XHR)
        EXPECTED: ![](index.php?/attachments/get/100978311)
        EXPECTED: 'Breakpoint' is shown within the **Charles** application
        EXPECTED: ![](index.php?/attachments/get/100978314)
        """
        pass

    def test_003_while_the_breakpoint_with_a_response_is_shown_in_charles_select_edit_response___json_text__and_changecopy_the_response_mock_from_pre_conditions_and_pastereplace_the_shown_one_with_it_the_response_submitting_a_change_with_a_click_on_execute_buttonindexphpattachmentsget66425168indexphpattachmentsget66425169indexphpattachmentsget100978315_if_first_request_is_empty_and_has_no_json_text_simply_execute_it_and_repeat_actions_of_this_step_for_the_second_request(self):
        """
        DESCRIPTION: While the Breakpoint with a response is shown in Charles, select 'Edit Response' -> 'JSON Text',  and change(copy the response mock from pre-conditions and paste/replace the shown one with it) the response submitting a change with a click on 'Execute' button
        DESCRIPTION: ![](index.php?/attachments/get/66425168)
        DESCRIPTION: ![](index.php?/attachments/get/66425169)
        DESCRIPTION: ![](index.php?/attachments/get/100978315)
        DESCRIPTION: **!** (If first request is empty and has no JSON Text, simply execute it, and repeat actions of this step for the second request)
        EXPECTED: [Mobile or Tablet Responsive]
        EXPECTED: Pop-up with 2 buttons, header text, description text and countdown timer is shown in to a user.
        EXPECTED: **User is not able to watch the stream.**
        EXPECTED: ![](index.php?/attachments/get/101002679)
        """
        pass

    def test_004_verify_contents_of_the_shown_pop_up(self):
        """
        DESCRIPTION: Verify contents of the shown pop-up
        EXPECTED: Pop-up contains:
        EXPECTED: **Header text**: "Watch Live" in black color
        EXPECTED: **Description text**: "In order to watch the race you must have a funded account or have placed a bet in the last 24 hours"
        EXPECTED: **Countdown timer label**: "RACE OFF COUNTDOWN:" written in upper case and black color
        EXPECTED: **Countdown timer** in MM:SS format and red color
        EXPECTED: 'NO, THANKS' transparrent **button** with text written in upper case and black color
        EXPECTED: "DEPOSIT" yellow **button** with text written in upper case and black color
        """
        pass

    def test_005_tap_on_the_deposit_button(self):
        """
        DESCRIPTION: Tap on the "DEPOSIT" button
        EXPECTED: Background changes
        EXPECTED: User is redirected to a 'Deposit' page, with a ladbrokes splash logo being shown in the process
        """
        pass

    def test_006_return_to_homepagequit_the_deposit_page_and_repeat_steps_12_and_3(self):
        """
        DESCRIPTION: Return to Homepage(Quit the Deposit page) and repeat steps 1,2 and 3
        EXPECTED: 
        """
        pass

    def test_007_tap_on_the_no_thanks_button(self):
        """
        DESCRIPTION: Tap on the "NO, THANKS" button
        EXPECTED: Pop-up is closed
        EXPECTED: User remains on the EDP of the event that he/she was previously on
        EXPECTED: Previously tapped stream button returns to its original state
        """
        pass
