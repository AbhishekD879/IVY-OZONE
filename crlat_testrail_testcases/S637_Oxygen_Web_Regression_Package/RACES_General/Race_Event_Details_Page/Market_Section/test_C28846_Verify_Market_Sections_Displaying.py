import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28846_Verify_Market_Sections_Displaying(Common):
    """
    TR_ID: C28846
    NAME: Verify Market Sections Displaying
    DESCRIPTION: Verify market sections displaying on event details page
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-6586 - Racecard Layout Update - Markets and Selections area
    DESCRIPTION: Applies to mpobile, tablet & desktop
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

    def test_004_verify_market_section(self):
        """
        DESCRIPTION: Verify market section
        EXPECTED: *   Available markets are displayed as tabs labeled as a market name
        EXPECTED: *   'Win or E/W' tab is selected and highlighted by default
        """
        pass

    def test_005_navigate_between_tabs(self):
        """
        DESCRIPTION: Navigate between tabs
        EXPECTED: *   User is redirected to next tab
        EXPECTED: *   Tab is selected and highlighted
        """
        pass

    def test_006_verify_markets_tab_when_four_and_more_market_typesare_available(self):
        """
        DESCRIPTION: Verify markets tab when four and more market types are available
        EXPECTED: Four market tabs are displayed filling all available width
        """
        pass

    def test_007_verify_markets_tab_when_three_market_types_are_available(self):
        """
        DESCRIPTION: Verify markets tab when three market types are available
        EXPECTED: Three market tabs are displayed filling all available width
        """
        pass

    def test_008_verify_markets_tab_when_two_market_types_are_available(self):
        """
        DESCRIPTION: Verify markets tab when two market types are available
        EXPECTED: Two market tabs are displayed filling all available width
        """
        pass

    def test_009_verify_markets_tab_when_one_market_type_is_available(self):
        """
        DESCRIPTION: Verify markets tab when one market type is available
        EXPECTED: One market tab is displayed filling all available width
        """
        pass
