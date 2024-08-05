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
class Test_C9607556_Verify_expired_future_Surface_Bets_displaying(Common):
    """
    TR_ID: C9607556
    NAME: Verify expired/future Surface Bets displaying
    DESCRIPTION: Test case verifies that expired/future Surface Bet isn't shown
    DESCRIPTION: AUTOTEST [C9776272]
    PRECONDITIONS: 1. There are a Surface Bet added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_cms_edit_the_surface_bet_set_display_fromto_to_the_past(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet: set Display From/To to the past.
        EXPECTED: 
        """
        pass

    def test_002_in_the_application_refresh_the_slphomepage_verify_this_surface_bet_isnt_displayed(self):
        """
        DESCRIPTION: In the application refresh the SLP/Homepage verify this Surface bet isn't displayed
        EXPECTED: Surface Bet isn't displayed
        """
        pass

    def test_003_in_the_cms_edit_the_surface_bet_set_display_fromto_to_the_future(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet: set Display From/To to the future.
        EXPECTED: 
        """
        pass

    def test_004_in_the_application_refresh_the_slphomepage_verify_this_surface_bet_isnt_displayed(self):
        """
        DESCRIPTION: In the application refresh the SLP/Homepage verify this Surface bet isn't displayed
        EXPECTED: Surface Bet isn't displayed
        """
        pass
