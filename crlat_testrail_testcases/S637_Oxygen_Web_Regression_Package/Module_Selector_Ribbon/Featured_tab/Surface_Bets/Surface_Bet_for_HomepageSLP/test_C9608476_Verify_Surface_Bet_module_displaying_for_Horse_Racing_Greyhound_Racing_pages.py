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
class Test_C9608476_Verify_Surface_Bet_module_displaying_for_Horse_Racing_Greyhound_Racing_pages(Common):
    """
    TR_ID: C9608476
    NAME: Verify Surface Bet module displaying for Horse Racing/Greyhound Racing pages
    DESCRIPTION: Test case verifies that Surface bets aren't shown on Racing landing pages
    DESCRIPTION: AUTOTEST [C9771292]
    PRECONDITIONS: _Currently both Greyhound racing and Horse racing are present in the list of Sports Categories and can be selected_
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Greyhound and Horse racing categories in the CMS
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_application_on_the_greyhound_racing_landing_page_verify_the_surface_bet_module_isnt_shown(self):
        """
        DESCRIPTION: In the application, on the Greyhound racing landing page verify the Surface Bet module isn't shown
        EXPECTED: Surface Bet module isn't shown
        """
        pass

    def test_002_on_the_horse_racing_landing_page_verify_the_surface_bet_module_isnt_shown(self):
        """
        DESCRIPTION: On the Horse racing landing page verify the Surface Bet module isn't shown
        EXPECTED: Surface Bet module isn't shown
        """
        pass
