import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C9770799_Verify_displaying_of_deleted_Surface_Bets(Common):
    """
    TR_ID: C9770799
    NAME: Verify displaying of deleted Surface Bets
    DESCRIPTION: Test case verifies that deleted Surface Bet isn't shown
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
    PRECONDITIONS: 2. Open this EDP
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_delete_the_surface_bet_from_the_cms(self):
        """
        DESCRIPTION: Delete the Surface Bet from the CMS
        EXPECTED: 
        """
        pass

    def test_002_in_the_application_refresh_the_edpverify_the_surface_bet_is_deleted(self):
        """
        DESCRIPTION: In the application refresh the EDP
        DESCRIPTION: Verify the Surface bet is deleted
        EXPECTED: Deleted Surface Bet isn't shown on the page
        """
        pass
