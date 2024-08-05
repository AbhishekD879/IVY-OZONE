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
class Test_C9770797_Verify_displaying_of_undisplayed_Surface_Bets(Common):
    """
    TR_ID: C9770797
    NAME: Verify displaying of "undisplayed" Surface Bets
    DESCRIPTION: Test case verifies that undisplayed Surface Bet isn't shown
    DESCRIPTION: This test case needs to be reviewed. It can be a duplicate of https://ladbrokescoral.testrail.com/index.php?/cases/view/9770795
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
    PRECONDITIONS: 2. Open this EDP
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_cms_disable_one_of_the_surface_bets_and_save_changes(self):
        """
        DESCRIPTION: In CMS disable one of the Surface Bets and save changes.
        EXPECTED: 
        """
        pass

    def test_002_in_application_refresh_the_pageverify_disabled_surface_bet_isnt_shown_within_the_carousel(self):
        """
        DESCRIPTION: In application refresh the page.
        DESCRIPTION: Verify disabled Surface Bet isn't shown within the carousel.
        EXPECTED: Disabled Surface bet isn't shown
        """
        pass

    def test_003_in_cms_enable_previously_disabled_surface_bets(self):
        """
        DESCRIPTION: In CMS enable previously disabled Surface Bets.
        EXPECTED: 
        """
        pass

    def test_004_in_application_refresh_the_pageverify_reenabled_surface_bet_is_shown_within_the_carousel(self):
        """
        DESCRIPTION: In application refresh the page.
        DESCRIPTION: Verify reenabled Surface Bet is shown within the carousel.
        EXPECTED: Surface bet is now shown
        """
        pass
