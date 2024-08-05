import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C59534687_Verify_local_storage_values(Common):
    """
    TR_ID: C59534687
    NAME: Verify local storage values
    DESCRIPTION: This test case verifies that Local storage is filled with correct value after first visit to 5-A-Side onbarding
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Dev Tools - Application - Local Storage - 'five-a-side-journey-seen': false
    PRECONDITIONS: - Onboarding is properly configured in CMS (https://ladbrokescoral.testrail.com/index.php?/cases/edit/59498785/1)
    PRECONDITIONS: -  User doesn't have free bet
    PRECONDITIONS: Event linking(Banach to Openbet TI) is done through an email - see following article: https://confluence.egalacoral.com/display/SPI/Request+Banach+%28BYB%2C+5-A-Side%2C+Player+Bets%29+Test+Events+Mapping
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Switch to 5-A-Side tab
    PRECONDITIONS: 4. Click/Tap 'BUILD TEAM' button
    """
    keep_browser_open = True

    def test_001_verify_on_boarding_screen_availability(self):
        """
        DESCRIPTION: Verify 'on-boarding' screen availability
        EXPECTED: 'On-boarding' screen IS displayed at the bottom of 5-A-Side overlay
        EXPECTED: ![](index.php?/attachments/get/115916684)
        """
        pass

    def test_002_open___dev_tools___application___local_storage(self):
        """
        DESCRIPTION: Open - Dev Tools - Application - Local Storage
        EXPECTED: 'five-a-side-journey-seen': true
        EXPECTED: key - value is present
        """
        pass

    def test_003_reload_the_app(self):
        """
        DESCRIPTION: Reload the app
        EXPECTED: 'On-boarding' screen IS NOT displayed at the bottom of 5-A-Side overlay
        """
        pass

    def test_004_clear_storage_and_reload_the_app(self):
        """
        DESCRIPTION: Clear storage and reload the app
        EXPECTED: 'On-boarding' screen IS displayed at the bottom of 5-A-Side overlay
        """
        pass
