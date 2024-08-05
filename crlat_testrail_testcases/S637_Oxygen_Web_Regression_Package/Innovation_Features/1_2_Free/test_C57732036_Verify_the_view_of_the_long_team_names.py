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
class Test_C57732036_Verify_the_view_of_the_long_team_names(Common):
    """
    TR_ID: C57732036
    NAME: Verify the view of the long team names
    DESCRIPTION: This test case verifies the view of the long team names.
    DESCRIPTION: type long names from CMS for different teams and check it on UI
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. The Quick link 'Play 1-2-FREE predictor and win £150' is available on the Home page / Football page.
    PRECONDITIONS: 3. Open the Oxygen CMS.
    PRECONDITIONS: 4. Navigate to the 1-2-Free section.
    PRECONDITIONS: 5. Select the 'Game View' subsection.
    PRECONDITIONS: 6. Click on the active game.
    PRECONDITIONS: 7. Scroll to the 'Game events list:' section.
    PRECONDITIONS: 8. Enter "Panthessaloníkios Athlitikós Ómilos Konstantinoupolitón Football Club" into 'Home team name' row.
    PRECONDITIONS: 9. Enter "Panthessaloníkios Athlitikós Ómilos Konstantinoupolitón Football Club" into 'Away team name' row.
    PRECONDITIONS: 10. Click on the 'Save Changes' button.
    PRECONDITIONS: 11. Click on the 'Yes' button in the 'Saving of: ' pop-up.
    """
    keep_browser_open = True

    def test_001_open_the_website__app(self):
        """
        DESCRIPTION: Open the website / app.
        EXPECTED: The website / app is opened.
        """
        pass

    def test_002_tap_on_the_1_2_free_link(self):
        """
        DESCRIPTION: Tap on the '1-2-Free' link.
        EXPECTED: The 'This week' tab is opened.
        EXPECTED: The long name of a team is cut and displayed with three dots (...).
        EXPECTED: The Splash page is opened (only on mobile).
        """
        pass

    def test_003_tap_on_the_play_now_button_only_on_mobile(self):
        """
        DESCRIPTION: Tap on the 'Play now' button (only on mobile).
        EXPECTED: The 'This week' tab is opened (only on mobile).
        EXPECTED: The long name of a team is cut and displayed with three dots (...) (only on mobile).
        """
        pass
