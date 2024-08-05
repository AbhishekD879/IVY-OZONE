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
class Test_C11250805_Verify_redesigned_user_tabs_on_Sport_EDP(Common):
    """
    TR_ID: C11250805
    NAME: Verify redesigned user tabs on <Sport> EDP
    DESCRIPTION: This test case verifies the appearance of new redesigned user tabs "Markets", "My Bets" on <Sport> EDP when configured in CMS.
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Note: User tabs like 'Markets'/'My Bets' are available for all sports. If configured in CMS, they appear on UI redesigned, if not, the old design of tabs is shown (2 buttons of yellow and blue colors)
    PRECONDITIONS: CMS configuration is described here: https://ladbrokescoral.testrail.com/index.php?/cases/view/10852269
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User has positive balance
    PRECONDITIONS: - User is on any <sport> EDP (and has NOT yet placed a bet for any of its selections)
    PRECONDITIONS: - New redesigned tabs are already configured in CMS
    """
    keep_browser_open = True

    def test_001_check_the_area_below_the_scoreboards(self):
        """
        DESCRIPTION: Check the area below the scoreboards
        EXPECTED: There are no tabs available like "Markets","My Bets" (on the area where 'watch' icon is placed)
        """
        pass

    def test_002_place_a_bet_for_any_selection_on_this_page(self):
        """
        DESCRIPTION: Place a bet for any selection on this page
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_003_refresh_the_page_and_check_if_tabs_appeared(self):
        """
        DESCRIPTION: Refresh the page and check if tabs appeared
        EXPECTED: - After page refresh 2 tabs "Markets","My Bets" appear below the scoreboards (along with 'watch' icon, if in-play event) with white text name on dark blue background
        EXPECTED: - User can switch between the tabs
        EXPECTED: - "My Bets" tab has counter of the bets placed
        EXPECTED: - The active tab looks underlined
        """
        pass
