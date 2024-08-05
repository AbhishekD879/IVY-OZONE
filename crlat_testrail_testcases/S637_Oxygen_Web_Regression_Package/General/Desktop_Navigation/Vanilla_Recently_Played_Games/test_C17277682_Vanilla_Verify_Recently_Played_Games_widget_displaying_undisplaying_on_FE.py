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
class Test_C17277682_Vanilla_Verify_Recently_Played_Games_widget_displaying_undisplaying_on_FE(Common):
    """
    TR_ID: C17277682
    NAME: [Vanilla] Verify Recently Played Games widget displaying/ undisplaying on FE
    DESCRIPTION: This test case verifies Recently Played Games iFrame displaying/undisplaying on FE on Mobile devices and Wrappers.
    PRECONDITIONS: 1. Recently Played games widget is created and configured in CMS > Sports Pages > Homepage > Recently Played Games;
    PRECONDITIONS: 2. Recently Played games widget is active in CMS (Default position for RPG should be bottom of the page;
    PRECONDITIONS: 3. Oxygen app is loaded;
    PRECONDITIONS: 4. User is registered and logged into the app;
    PRECONDITIONS: 5. User is landed on the Home page;
    PRECONDITIONS: 6. **USER SHOULD PLAY CASINO GAMES, OTHERWISE, NO RPG WIDGET WILL BE DISPLAYED!!!** > Go to "Gaming" section (bottom menu) and play few games (slots);
    PRECONDITIONS: 7. Developer Tools is opened - "Verbose" mode is ON, post messages debugger is installed (https://chrome.google.com/webstore/detail/postmessage-debugger/ibnkhbkkelpcgofjlfnlanbigclpldad?hl=en);
    PRECONDITIONS: NOTE:
    PRECONDITIONS: 1. Link to visual designs: https://app.zeplin.io/project/5cf14a4dd64fdd1e164d8159?seid=5cf7e65e2d86001d8c6e587c
    PRECONDITIONS: 2. Link to technical documentation: https://docs.google.com/document/d/1niWXC8SbCIXGGidLkyWRBZyLk0yCI_sVYZGZpSMhGgI/edit?usp=sharing
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

    def test_003_log_out_from_the_app_and_observe_rpg_iframe(self):
        """
        DESCRIPTION: Log out from the App and observe RPG iframe;
        EXPECTED: User logged out and RPG iframe is hidden and cannot be visible to the User;
        """
        pass

    def test_004_login_to_the_app_again_and_observe_iframe(self):
        """
        DESCRIPTION: Login to the App again and observe iframe;
        EXPECTED: - RPG iframe is displayed and can be visible to the User;
        EXPECTED: - "eventName: LobbyLoaded is loaded" notification is visible in Console;
        """
        pass

    def test_005_go_to_cms__sports_pages__homepage(self):
        """
        DESCRIPTION: Go to CMS > Sports Pages > Homepage;
        EXPECTED: RPG section is displayed among other modules;
        """
        pass

    def test_006_change_position_of_rpg_section_via_pressing_updown_arrows__save__observe_application(self):
        """
        DESCRIPTION: Change Position of "RPG" section via pressing "UP/DOWN" arrows > Save > Observe Application;
        EXPECTED: RPG iframe position is changed in comparison  with the previous step;
        """
        pass
