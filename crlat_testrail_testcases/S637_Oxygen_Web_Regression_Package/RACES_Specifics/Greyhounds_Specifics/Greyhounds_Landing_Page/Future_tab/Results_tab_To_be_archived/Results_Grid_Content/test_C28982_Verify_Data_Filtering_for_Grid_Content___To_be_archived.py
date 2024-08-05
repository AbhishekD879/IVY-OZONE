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
class Test_C28982_Verify_Data_Filtering_for_Grid_Content___To_be_archived(Common):
    """
    TR_ID: C28982
    NAME: Verify Data Filtering for Grid Content  -  To be archived
    DESCRIPTION: This test case verifies what selections will be shown on the grid content
    PRECONDITIONS: In order to see events in the 'Results' tab event should be resulted:
    PRECONDITIONS: **'isResulted'='true' - **on event level
    PRECONDITIONS: To retrieve data from the Site Server use the following link:
    PRECONDITIONS: 1) To verify Results for events use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/HistoricDrilldown/X.XX/ResultedEvent/XXXXXX?translationLang=LL
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   *XXXXXX - an event id (Note, several event ids can also be pasted using comma as a separator. e.g.1574736,1574926**)*
    PRECONDITIONS: *   *LL - language (e.g. en, ukr) *
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'resultCode'** - to see whether selection is Win or Lose
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_from_the_sports_menu_ribbon_tap_greyhounds_icon(self):
        """
        DESCRIPTION: From the Sports Menu Ribbon tap 'Greyhounds'  icon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_003_tap_results_tab(self):
        """
        DESCRIPTION: Tap 'Results' tab
        EXPECTED: 'Results' tab is opened
        """
        pass

    def test_004_go_to_the_results_section_for_the_event(self):
        """
        DESCRIPTION: Go to the Results section for the event
        EXPECTED: Grid content for event is shown
        """
        pass

    def test_005_verify_selections_which_are_shown_for_event(self):
        """
        DESCRIPTION: Verify selections which are shown for event
        EXPECTED: Selections ONLY from the **'Win or Each Way'** market are shown in the result
        """
        pass

    def test_006_verify_selections_with_attributeresultcodesw(self):
        """
        DESCRIPTION: Verify selections with attribute **'resultCodes'='W'**
        EXPECTED: 'Win' selections are displayed on the 'Results' tab
        """
        pass

    def test_007_verify_selections_with_attribute_resultcodesp(self):
        """
        DESCRIPTION: Verify selections with attribute **'resultCodes'='P'**
        EXPECTED: ** **'Placed' selection are shown on the 'Results' tab
        """
        pass

    def test_008_verify_selection_with_attribute_resultcodel(self):
        """
        DESCRIPTION: Verify selection with attribute **'resultCode'='L' **
        EXPECTED: 'Lose' selection are NOT displayed in the 'Results' tab
        """
        pass

    def test_009_verify_unnamed_favorite_selection(self):
        """
        DESCRIPTION: Verify 'Unnamed Favorite' selection
        EXPECTED: 'Unnamed Favorite' selection IS NOT shown on the 'Results' tab
        """
        pass

    def test_010_verify_unnamed_2nd_favourite_selection(self):
        """
        DESCRIPTION: Verify 'Unnamed 2nd Favourite' selection
        EXPECTED: 'Unnamed 2nd Favourite' selection is NOT shown on the 'Results' tab
        """
        pass
