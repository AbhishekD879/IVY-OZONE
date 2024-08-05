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
class Test_C17305408_Vanilla_Recently_Played_Games_Handle_Request_Response(Common):
    """
    TR_ID: C17305408
    NAME: [Vanilla] Recently Played Games: Handle Request/Response
    DESCRIPTION: This test case verifies  handle the request/response between iFrame and the GVC RPG Component,
    DESCRIPTION: NOTICE: test user testgvccl-is008/123qwe
    DESCRIPTION: Autotest: [C29855318]
    PRECONDITIONS: 1. Recently Played games widget is created and configured in CMS > Sports Pages > Homepage > Recently Played Games;
    PRECONDITIONS: 2. Recently Played games widget is active in CMS;
    PRECONDITIONS: 3. Oxygen app is loaded;
    PRECONDITIONS: 4. User is registered and logged into the app;
    PRECONDITIONS: 5. User is landed on the Home page;
    PRECONDITIONS: 6. Developer Tools is opened - "Verbose" mode is ON, postMessages debugger is installed (https://chrome.google.com/webstore/detail/postmessage-debugger/ibnkhbkkelpcgofjlfnlanbigclpldad?hl=en);
    PRECONDITIONS: NOTE:
    PRECONDITIONS: 1. Link to visual designs: https://app.zeplin.io/project/5cf14a4dd64fdd1e164d8159?seid=5cf7e65e2d86001d8c6e58
    PRECONDITIONS: 2. Link to technical documentation: https://docs.google.com/document/d/1niWXC8SbCIXGGidLkyWRBZyLk0yCI_sVYZGZpSMhGgI/edit?usp=sharing
    """
    keep_browser_open = True

    def test_001_navigate_to_the_home_page(self):
        """
        DESCRIPTION: Navigate to the Home page;
        EXPECTED: User navigated and see the Home page;
        """
        pass

    def test_002_observe_the_page(self):
        """
        DESCRIPTION: Observe the page;
        EXPECTED: - Recently Played Games iframe is loaded and visible to User;
        EXPECTED: - "eventName: LobbyLoaded is loaded" notification is visible in Console;
        """
        pass

    def test_003_tap_on_the_one_of_the_gvc_mini_games_displayed_within_iframe(self):
        """
        DESCRIPTION: Tap on the one of the GVC mini games displayed within iframe
        EXPECTED: - Game launch notification is received:
        EXPECTED: {Name:GameLaunch,
        EXPECTED: params:
        EXPECTED: redirectUrl: xx}
        EXPECTED: - User is redirected to the respective URL within the same window.
        """
        pass

    def test_004_return_to_the_home_screen(self):
        """
        DESCRIPTION: Return to the Home screen
        EXPECTED: User is landed on the Home screen;
        """
        pass

    def test_005_navigate_to_iframe_and_click_on_see_all_link(self):
        """
        DESCRIPTION: Navigate to iframe and click on "See All" link;
        EXPECTED: The User is redirected to the Games Lobby
        """
        pass
