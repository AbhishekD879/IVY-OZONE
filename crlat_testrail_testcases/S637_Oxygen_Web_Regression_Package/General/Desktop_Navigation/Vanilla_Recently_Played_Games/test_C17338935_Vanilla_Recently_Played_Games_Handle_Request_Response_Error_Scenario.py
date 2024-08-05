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
class Test_C17338935_Vanilla_Recently_Played_Games_Handle_Request_Response_Error_Scenario(Common):
    """
    TR_ID: C17338935
    NAME: [Vanilla] Recently Played Games: Handle Request/Response (Error Scenario)
    DESCRIPTION: This test case verifies  handle the request/response between iFrame and the GVC RPG `Component`,
    PRECONDITIONS: 1. Recently Played games widget is created and configured in CMS > Sports Pages > Homepage > Recently Played Games;
    PRECONDITIONS: 2. Recently Played games widget is active in CMS;
    PRECONDITIONS: 3. Oxygen app is loaded;
    PRECONDITIONS: 4. User is registered and logged into the app;
    PRECONDITIONS: 5. User is landed on the Home page;
    PRECONDITIONS: 6. Developer Tools is opened - "Verbose" mode is ON, postMessages debugger is installed (https://chrome.google.com/webstore/detail/postmessage-debugger/ibnkhbkkelpcgofjlfnlanbigclpldad?hl=en);
    PRECONDITIONS: NOTE:
    PRECONDITIONS: 1. Link to visual designs: https://app.zeplin.io/project/5cf14a4dd64fdd1e164d8159?seid=5cf7e65e2d86001d8c6e58
    PRECONDITIONS: 2. Link to technical documentation: https://docs.google.com/document/d/1niWXC8SbCIXGGidLkyWRBZyLk0yCI_sVYZGZpSMhGgI/edit?usp=sharing
    PRECONDITIONS: 3. Link to technical documentation: https://docs.google.com/document/d/1IY0sMVAE7QP4DJO86Gn3uYZEubFZZR1Diu_aAL-lrII/edit?usp=sharing
    """
    keep_browser_open = True

    def test_001_navigate_to_the_bottom_of_the_home_page(self):
        """
        DESCRIPTION: Navigate to the bottom of the Home page;
        EXPECTED: User navigated and see the bottom of the Home page;
        """
        pass

    def test_002_observe_the_page(self):
        """
        DESCRIPTION: Observe the page;
        EXPECTED: - Recently Played Games iframe is loaded and visible to User;
        EXPECTED: - "eventName: LobbyLoaded is loaded" notification is visible in Console;
        """
        pass

    def test_003_trigger_error_message___notice___ask_someone_in_gvc_team___prashantkivycomptechcom_is_key_person(self):
        """
        DESCRIPTION: Trigger error message
        DESCRIPTION: -- NOTICE! - (ask someone in GVC team - prashantk@ivycomptech.com is key person)
        EXPECTED: - `Error message is triggered` ;
        EXPECTED: >   {
        EXPECTED: >   eventName:‘Error,
        EXPECTED: >   params:
        EXPECTED: >   {
        EXPECTED: >   errorMessages: <and array of error messages>,
        EXPECTED: >   redirectUrl: xx
        EXPECTED: >   }
        EXPECTED: - iframe is not displayed;
        """
        pass
