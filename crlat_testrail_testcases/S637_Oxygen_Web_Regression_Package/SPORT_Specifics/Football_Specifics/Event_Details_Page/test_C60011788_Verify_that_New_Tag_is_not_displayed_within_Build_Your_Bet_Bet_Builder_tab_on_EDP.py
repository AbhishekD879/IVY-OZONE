import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60011788_Verify_that_New_Tag_is_not_displayed_within_Build_Your_Bet_Bet_Builder_tab_on_EDP(Common):
    """
    TR_ID: C60011788
    NAME: Verify that New Tag is not displayed within Build Your Bet/Bet Builder tab on EDP
    DESCRIPTION: Test case to verify if "New" sign isn't displayed on Football EDP near Build Your Bet/Bet Builder tab
    PRECONDITIONS: **Build Your Bet/Bet Builder config:**
    PRECONDITIONS: * Feature is enabled in CMS > System Configuration -> Structure -> YourCallIconsAndTabs -> enable tab
    PRECONDITIONS: * Banach leagues are added and enabled in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for BYB’ is ticked
    PRECONDITIONS: * Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: * Event is prematch (not live)
    PRECONDITIONS: 1) Load the app
    PRECONDITIONS: 2) Navigate to Football event details page that has all BYB configs
    PRECONDITIONS: **NOTE:** Will be implemented for Ladbrokes after OX 108
    """
    keep_browser_open = True

    def test_001_verify_build_your_betbet_builder_tab_displaying(self):
        """
        DESCRIPTION: Verify Build Your Bet/Bet Builder tab displaying
        EXPECTED: * Build Your Bet/Bet Builder tab is displayed
        EXPECTED: * No 'New' sign is displayed on the tab
        """
        pass
