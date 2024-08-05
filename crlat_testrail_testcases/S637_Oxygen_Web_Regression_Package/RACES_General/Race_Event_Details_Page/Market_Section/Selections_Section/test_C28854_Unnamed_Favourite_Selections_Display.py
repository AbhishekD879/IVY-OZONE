import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28854_Unnamed_Favourite_Selections_Display(Common):
    """
    TR_ID: C28854
    NAME: Unnamed Favourite Selections Display
    DESCRIPTION: This test case verify Unnamed Favourite and Unnamed 2nd Favourite Selections Display
    DESCRIPTION: AUTOTEST [C2688416]
    PRECONDITIONS: There is a <Race> with unnamed favourite selections:
    PRECONDITIONS: - Unnamed Favourite
    PRECONDITIONS: - Unnamed 2nd Favourite
    """
    keep_browser_open = True

    def test_001_open_race_event_details_page(self):
        """
        DESCRIPTION: Open <Race> Event Details page
        EXPECTED: 
        """
        pass

    def test_002_verify_ordering_of_unnamed_favourite_selections(self):
        """
        DESCRIPTION: Verify ordering of Unnamed Favourite Selections
        EXPECTED: Unnamed Favourites are displayed at the end of the list in the following order:
        EXPECTED: 1st - Unnamed Favourite
        EXPECTED: 2nd - Unnamed 2nd Favourite
        """
        pass

    def test_003_verify_unnamed_favourite_selection_displaying(self):
        """
        DESCRIPTION: Verify Unnamed Favourite selection displaying
        EXPECTED: Name is "Unnamed Favourite" (corresponds to the **'name'** attribute in SiteServer)
        EXPECTED: Note: attribute **'outcomeMeaningMinorCode'**=1 for this selection
        """
        pass

    def test_004_verify_unnamed_2nd_favourite_selection_displaying(self):
        """
        DESCRIPTION: Verify Unnamed 2nd Favourite selection displaying
        EXPECTED: Name is "Unnamed 2nd Favourite" (corresponds to the **'name' **attribute in SiteServer)
        EXPECTED: Note: attribute **'outcomeMeaningMinorCode'**=2 for this selection
        """
        pass

    def test_005_verify_priceodds_button(self):
        """
        DESCRIPTION: Verify price/odds button
        EXPECTED: Price/Odds is SP for both selections
        """
        pass
