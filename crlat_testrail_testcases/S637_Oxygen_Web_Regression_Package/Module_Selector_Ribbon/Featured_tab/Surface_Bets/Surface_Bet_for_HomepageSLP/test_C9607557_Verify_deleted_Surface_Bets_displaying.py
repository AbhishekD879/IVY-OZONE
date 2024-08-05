import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C9607557_Verify_deleted_Surface_Bets_displaying(Common):
    """
    TR_ID: C9607557
    NAME: Verify deleted Surface Bets displaying
    DESCRIPTION: Test case verifies that deleted Surface Bet isn't shown
    PRECONDITIONS: 1. There are a few Surface Bet added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_delete_the_surface_bet_from_the_cms(self):
        """
        DESCRIPTION: Delete the Surface Bet from the CMS
        EXPECTED: 
        """
        pass

    def test_002_in_the_application_refresh_the_slphomepageverify_the_surface_bet_is_deleted(self):
        """
        DESCRIPTION: In the application refresh the SLP/Homepage
        DESCRIPTION: Verify the Surface bet is deleted
        EXPECTED: Deleted Surface Bet isn't shown on the page
        """
        pass
