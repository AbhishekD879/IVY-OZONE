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
class Test_C58212498_Launching_Perform_Stream_for_inactive_users_on_Horse_Racing_EDP(Common):
    """
    TR_ID: C58212498
    NAME: Launching Perform Stream for inactive users on Horse Racing EDP
    DESCRIPTION: This test case verifies proper front-end handling of a response from opt-in micro service in regard to a specific 'failureCode', triggered by inactive user who tries to view Perform stream on Horse Racing Event Details Page.
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
    PRECONDITIONS: 1. SiteServer event should be configured to support Perform streaming (**'typeFlagCodes'**='PVA , ... ' AND **'drilldownTagNames'**='EVFLAG_PVM' flags should be set) and should be mapped to Perform stream event
    PRECONDITIONS: 2. HORSE RACING event should have the following attributes:
    PRECONDITIONS: *isMarketBetInRun = "true"
    PRECONDITIONS: 3. User is logged into the Oxygen app and has a positive balance.
    PRECONDITIONS: 4. Ukraine should be whitelisted by Perform
    PRECONDITIONS: 5. It should be 5 or more minutes left before event Start Time
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
        EXPECTED: * Desktop:
        EXPECTED: 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile or Tablet Responsive:
        EXPECTED: 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_002_mobile_or_tablet_responsivedesktoptapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **Mobile or Tablet Responsive/Desktop**
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
        DESCRIPTION: **! (If first request is empty and has no JSON Text, simply execute it, and repeat actions of this step for the second request)**
        EXPECTED: [Mobile or Tablet Responsive]
        EXPECTED: Pop up opens with message "This stream has not yet started. Please try again soon".
        EXPECTED: Timer countdown is shown below the text.
        EXPECTED: There is an ability to close pop-up with a 'OK' button
        EXPECTED: ![](index.php?/attachments/get/101002537)
        EXPECTED: [Desktop]
        EXPECTED: Warning message is shown with a following text : "This stream has not yet started. Please try again soon".
        EXPECTED: ![](index.php?/attachments/get/101002538)
        EXPECTED: **User is not able to watch the stream.**
        """
        pass

    def test_004_wait_till_2_or_less_minutes_left_before_event_start_time_refresh_the_page_and_repeat_steps_2_3(self):
        """
        DESCRIPTION: Wait till 2 or less minutes left before event Start Time, refresh the page and repeat steps 2-3
        EXPECTED: [Mobile or Tablet Responsive]
        EXPECTED: Pop-up is shown with a following text "In order to watch the race you must have a funded account or have placed a bet in the last 24 hours"
        EXPECTED: Timer countdown is shown below the text.
        EXPECTED: There is an ability to close pop-up with a 'No, Thanks' button
        EXPECTED: ![](index.php?/attachments/get/100978322)
        EXPECTED: [Desktop]
        EXPECTED: Warning message is shown with a following text : "In order to watch the race you must have a funded account or have placed a bet in the last 24 hours"
        EXPECTED: ![](index.php?/attachments/get/100978327)
        EXPECTED: **User is not able to watch the stream.**
        """
        pass

    def test_005_wait_for_the_event_start_time_to_comeevent_to_become_live_refresh_the_page_and_repeat_steps_2_3(self):
        """
        DESCRIPTION: Wait for the event start time to come(event to become live), refresh the page and repeat steps 2-3
        EXPECTED: Expected results match ER of steps **2** and **4**, with only difference for [mobile/tablet responsive] view:
        EXPECTED: Timer countdown is no longer shown within pop-up.
        """
        pass