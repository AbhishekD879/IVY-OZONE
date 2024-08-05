import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.streaming
@vtest
class Test_C29266_API_error(Common):
    """
    TR_ID: C29266
    NAME: API error
    DESCRIPTION: This test case verifies behavior of the application when API returns an error during the opt-in call for stream data reception
    DESCRIPTION: Applies to <Race> events
    PRECONDITIONS: 1. SiteServer event should be configured to support RUK/Perform streaming (**'drilldownTagNames'**='EVFLAG_RVA' flag should be set) and should be mapped to RUK/Perform stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: * isStarted = "true", but stream has not run for more than 1 minute after the 'start time'
    PRECONDITIONS: * isMarketBetInRun = "true"
    PRECONDITIONS: 3. User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: 4. API should return an error(case of a broken/missing token)
    PRECONDITIONS: In order to reproduce this behavior, use a '/auth/invalidateSession' DELETE command in POSTMAN (you will need BPP Request URL, username and BPP token - first 1 can be found in XHR response by 'bp' input in the search field); last 2 can be found in Application - Local Storage of the Web Browser
    PRECONDITIONS: ![](index.php?/attachments/get/18576789) / ![](index.php?/attachments/get/18576792)
    PRECONDITIONS: **--> NOTE!**
    PRECONDITIONS: If you kill user token before event/stream start time and click/tap 'Watch Live'/'Watch' afterwards, you receive following error "This stream has not yet started. Please try again soon."
    PRECONDITIONS: **This is an expected behavior and for now left as it is.**
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_race_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event which satisfies Preconditions
        EXPECTED: * Desktop:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050952) (Coral) / 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile/Tablet:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050954) (Coral) / 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_002_use_the_delete_authinvalidatesession_command_through_postmanie_httpsbpp_tst0coralsportsnonprodcloudladbrokescoralcomproxyauthinvalidatesessionheaders_2token_6994aa6ae06d0926601282a284449d4939a7c1bf5010c349ca92a67d363c56d0username_james_pond(self):
        """
        DESCRIPTION: Use the DELETE '/auth/invalidateSession' command through POSTMAN:
        DESCRIPTION: (i.e. https://bpp-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/Proxy/auth/invalidateSession
        DESCRIPTION: Headers (2)
        DESCRIPTION: token: 6994aa6ae06d0926601282a284449d4939a7c1bf5010c349ca92a67d363c56d0
        DESCRIPTION: username: james_pond)
        EXPECTED: '204 No Content' Status should be shown as a result of command execution
        """
        pass

    def test_003_all_devicestapclick_on_watch_livestream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch Live'/'Stream' button
        EXPECTED: * [ **Coral** desktop / **Ladbrokes** desktop]: Message is displayed: "The Stream for this event is currently not available"
        EXPECTED: * [ **Ladbrokes**  and **Coral** tablet/mobile]: Pop up opens with message "The Stream for this event is currently not available"
        EXPECTED: **User is not able to watch the stream**
        EXPECTED: Request to OptIn MS is sent (see preconditions) to indetify stream provider, but ends up with an error
        EXPECTED: ![](index.php?/attachments/get/18576783)
        EXPECTED: * Application does not crash, and handles API error correctly
        """
        pass
