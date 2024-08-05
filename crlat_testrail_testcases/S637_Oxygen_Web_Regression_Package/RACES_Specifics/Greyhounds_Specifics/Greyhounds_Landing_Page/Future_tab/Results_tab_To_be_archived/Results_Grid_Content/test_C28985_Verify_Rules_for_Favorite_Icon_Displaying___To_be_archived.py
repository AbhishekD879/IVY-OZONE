import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28985_Verify_Rules_for_Favorite_Icon_Displaying___To_be_archived(Common):
    """
    TR_ID: C28985
    NAME: Verify Rules for Favorite Icon Displaying  -  To be archived
    DESCRIPTION: This test case verifies rules for displaying of Favourite icon next to the Position information
    PRECONDITIONS: To retrieve data from the Site Server use the following link:
    PRECONDITIONS: 1) To verify Results for events use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/HistoricDrilldown/X.XX/ResultedEvent/XXXXXX?translationLang=LL
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   *XXXXXX - an event id (Note, several event ids can also be pasted using comma as a separator. e.g.1574736,1574926**)*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'resultedOutcome id'** - to see the particular outcome
    PRECONDITIONS: **'priceTypeCode' ** on resulted outcome level - to see the SP or LP price attribute
    PRECONDITIONS: **'priceNum'**, **'priceDen'**,** 'priceDec**' on outcome level - to see attributes for Price/Odds buttons and define selection prices
    PRECONDITIONS: NOTE, defining favorite icons occurs among all selections on the Site Server and only after that they will be filtered by** 'resultCode' **attribute
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
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
        EXPECTED: Grid content for verified event is shown
        """
        pass

    def test_005_verify_place_column(self):
        """
        DESCRIPTION: Verify **'Place'** column
        EXPECTED: Place and a favorite icon (if available) are shown in the **'Place'** column
        """
        pass

    def test_006_verifyf_icon(self):
        """
        DESCRIPTION: Verify **'F'** icon
        EXPECTED: *   Selection with the lowest price (**'priceNum'/** **'priceDen'**) -> display **'F'** next to the selection
        EXPECTED: *   Filtering occurs among all selections from the Site Server response
        """
        pass

    def test_007_verify_2f_icon(self):
        """
        DESCRIPTION: Verify **'2F' **icon
        EXPECTED: *   Selection with the 2nd lowest price  (**'priceNum'/** **'priceDen'**)-> display **'2F'** next to selection
        EXPECTED: *   NOTE, Filtering occurs among all selections from the Site Server (Win, Lose and Placed)
        """
        pass

    def test_008_verify_jf_icon(self):
        """
        DESCRIPTION: Verify** 'JF' **icon
        EXPECTED: *   Is there are TWO selections with the same lowest price (**'priceNum'/** **'priceDen'**) -> display **'JF' **near each selection
        EXPECTED: *   NOTE, filtering occurs among all selections from the Site Server (Win, Lose and Placed)
        """
        pass

    def test_009_verify_2jf_icon(self):
        """
        DESCRIPTION: Verify **'2JF'** icon
        EXPECTED: *   If there are TWO selections with the same 2nd lowest prices (**'priceNum'/** **'priceDen'**) -> display** '2JF'** near each selection
        EXPECTED: *   NOTE, filtering occurs among all selections from the Site Server (Win, Lose and Placed)
        """
        pass
