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
class Test_C64749868_Verify_Surface_Bet_module_enabling_disabling_for_the_Sport_category(Common):
    """
    TR_ID: C64749868
    NAME: Verify Surface Bet module enabling/disabling for the Sport category
    DESCRIPTION: Test case verifies possibility to enable or disable
    DESCRIPTION: the Surface Bet module on the home page or
    DESCRIPTION: sport category page
    PRECONDITIONS: 1. There is at least one Surface Bet added to the SLP/Homepage in CMS.
    PRECONDITIONS: 2. Open this SLP/Homepage in Oxygen application.
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_cms_make_a_module_for_the_homepageslp_not_activein_the_application_refresh_the_homepageslpverify_the_surface_bet_module_isnt_displayed(self):
        """
        DESCRIPTION: In the CMS make a module for the homepage/SLP not active.
        DESCRIPTION: In the application refresh the homepage/SLP.
        DESCRIPTION: Verify the Surface Bet module isn't displayed.
        EXPECTED: Surface Bet module isn't shown
        """
        pass

    def test_002_in_the_cms_make_a_module_for_the_homepageslp_activein_the_application_refresh_the_homepageslp_verify_the_surface_bet_module_is_displayed(self):
        """
        DESCRIPTION: In the CMS make a module for the homepage/SLP active
        DESCRIPTION: In the application refresh the homepage/SLP. Verify the Surface Bet module is displayed
        EXPECTED: Surface Bet module is shown
        """
        pass
