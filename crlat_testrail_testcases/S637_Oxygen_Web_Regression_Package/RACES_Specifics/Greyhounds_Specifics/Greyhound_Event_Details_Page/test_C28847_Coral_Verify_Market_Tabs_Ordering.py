import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28847_Coral_Verify_Market_Tabs_Ordering(Common):
    """
    TR_ID: C28847
    NAME: [Coral] Verify Market Tabs Ordering
    DESCRIPTION: This test case verifie markets tabs ordering
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-6586 Racecard Layout Update - Markets and Selections area
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the Sports Menu Ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_verify_market_tabs_ordering(self):
        """
        DESCRIPTION: Verify market tabs ordering
        EXPECTED: The tabs are sorted in following order:
        EXPECTED: *   'Win Or E/W' tab
        EXPECTED: *   'Win Only' tab
        EXPECTED: *   'Betting WO' tab
        EXPECTED: *   'More Markets' tab
        """
        pass
