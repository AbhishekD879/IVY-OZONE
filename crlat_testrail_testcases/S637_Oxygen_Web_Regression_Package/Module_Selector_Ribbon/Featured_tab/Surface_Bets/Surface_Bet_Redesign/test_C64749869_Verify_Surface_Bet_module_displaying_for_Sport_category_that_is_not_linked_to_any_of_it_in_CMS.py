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
class Test_C64749869_Verify_Surface_Bet_module_displaying_for_Sport_category_that_is_not_linked_to_any_of_it_in_CMS(Common):
    """
    TR_ID: C64749869
    NAME: Verify Surface Bet module displaying for
 Sport category that is not linked to any of it in CMS.
    DESCRIPTION: Test case verifies that Surface Bet module is not
    DESCRIPTION: shown on the Sport Landing Page if there isn't
    DESCRIPTION: Surface Bet added to this sport category
    PRECONDITIONS: 1. There is sport category that is not linked to any Surface bets module in CMS.
    PRECONDITIONS: 2. In application open Sport landing page for selected category.
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_verify_the_surface_bet_module_isnt_shown_if_there_is_no_available_sb_for_the_sport_category(self):
        """
        DESCRIPTION: Verify the Surface Bet module isn't shown if there is no available SB for the sport category.
        EXPECTED: Surface Bet module isn't shown
        """
        pass
