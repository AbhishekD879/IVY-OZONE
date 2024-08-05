import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C9726418_Event_Hub_Verify_deleted_Surface_Bets_displaying(Common):
    """
    TR_ID: C9726418
    NAME: Event Hub: Verify deleted Surface Bets displaying
    DESCRIPTION: Test case verifies that deleted Surface Bet isn't shown on Event hub tab
    PRECONDITIONS: 1. There are a few Surface Bet added to the Event Hub in the CMS
    PRECONDITIONS: 2. Open this Event Hub tab in the application
    PRECONDITIONS: CMS path for the Event Hub: Sport Pages > Event Hub > Edit Event Hub > Surface Bets Module
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
