import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C9770792_Verify_Surface_Bet_module_displaying_on_Event_Details_Page_with_no_Surface_bets_assigned(Common):
    """
    TR_ID: C9770792
    NAME: Verify Surface Bet module displaying on Event Details Page with no Surface bets assigned
    DESCRIPTION: Test case verifies that Surface Bets aren't shown on other Event Details Pages
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_application_open_the_edp_without_added_surface_betsverify_this_edp_doesnt_contain_surface_bet_module(self):
        """
        DESCRIPTION: In the application open the EDP without added Surface Bets
        DESCRIPTION: Verify this EDP doesn't contain Surface Bet module
        EXPECTED: Surface Bet module isn't shown on the other EDP
        """
        pass
