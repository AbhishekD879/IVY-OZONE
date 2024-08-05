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
class Test_C9770809_Verify_Surface_Bet_module_displaying_on_EDP_if_Surface_Bets_on_this_Sport_Category_are_disabled(Common):
    """
    TR_ID: C9770809
    NAME: Verify Surface Bet module displaying on EDP if Surface Bets on this Sport Category are disabled
    DESCRIPTION: Test case verifies that Surface Bet remains on the EDP even if Surface Bets are disabled for the related category
    PRECONDITIONS: 1. There is a single Surface Bet added to the Event Details page and to the related Sport Category.
    PRECONDITIONS: 2. Valid Selection Id is set
    PRECONDITIONS: 3. Surface Bets are disabled for the related Sport Category
    PRECONDITIONS: 4. Open this EDP page
    """
    keep_browser_open = True

    def test_001_verify_the_surface_bet_is_shown_on_the_edp_if_surface_bets_are_disabled_for_the_related_category(self):
        """
        DESCRIPTION: Verify the Surface Bet is shown on the EDP if Surface Bets are disabled for the related category
        EXPECTED: Surface Bet is shown
        """
        pass
