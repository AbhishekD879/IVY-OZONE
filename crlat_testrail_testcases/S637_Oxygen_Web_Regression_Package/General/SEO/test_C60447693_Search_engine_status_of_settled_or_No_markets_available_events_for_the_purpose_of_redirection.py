import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C60447693_Search_engine_status_of_settled_or_No_markets_available_events_for_the_purpose_of_redirection(Common):
    """
    TR_ID: C60447693
    NAME: Search engine status of settled or No markets available events for the purpose of redirection.
    DESCRIPTION: Settled events or Events with "No markets available" message should have "410:HTTP" status so that - If customer searches for that particular event which is finished/undisplayed /settled then he doesn't get redirected to our sites.
    PRECONDITIONS: The following chrome extension should be present.
    PRECONDITIONS: https://www.ayima.com/uk/insights/redirect-checker.html
    PRECONDITIONS: To confirm the result is expected or not we can search by changing the User agent as follows:
    PRECONDITIONS: Navigate to Network conditions from "More Tools" in Developer Tool.
    PRECONDITIONS: ![](index.php?/attachments/get/128158700)
    PRECONDITIONS: Can select user agent as "Googlebot Desktop"
    PRECONDITIONS: ![](index.php?/attachments/get/128158695)
    """
    keep_browser_open = True

    def test_001_pass_url_of_the_settled_event_in_a_browser_for_normal_user_with_google_chrome_default_agent(self):
        """
        DESCRIPTION: Pass URL of the settled event in a browser for normal user with google chrome default agent.
        EXPECTED: The particular event is opened with "No markets are currently available for this event" message.
        EXPECTED: Should display 200:HTTP as follows
        EXPECTED: ![](index.php?/attachments/get/128158703)
        """
        pass

    def test_002_from_chrome_extension_and_user_agent_with_googlebot_desktop_navigate_to_redirect_path_and_check_for_the_status(self):
        """
        DESCRIPTION: From chrome extension and user agent with Googlebot Desktop, Navigate to Redirect Path and check for the status.
        EXPECTED: Status should not be 200:HTTP as follows
        EXPECTED: ![](index.php?/attachments/get/128158704)
        EXPECTED: As the event is already settled and expired.
        EXPECTED: Instead status should be 410: HTTP as follows:
        EXPECTED: ![](index.php?/attachments/get/128158701)
        """
        pass

    def test_003_to_re_verify_check_the_status_by_changing_the_user_agentas_mentioned_in_pre_conditions(self):
        """
        DESCRIPTION: To re-verify check the status by changing the User agent(as mentioned in Pre-conditions)
        EXPECTED: Status of the expired event should be 410: HTTP as follows:
        EXPECTED: ![](index.php?/attachments/get/128158702)
        """
        pass
