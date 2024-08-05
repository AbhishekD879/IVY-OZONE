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
class Test_C28984_Verify_Rules_for_Price_Displaying___To_be_archived(Common):
    """
    TR_ID: C28984
    NAME: Verify Rules for Price Displaying  -  To be archived
    DESCRIPTION: This test case verifies how prices will be shown for selections on the 'Results' tab
    PRECONDITIONS: To retrieve data from the Site Server use the following link:
    PRECONDITIONS: 1) To verify Results for events use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/HistoricDrilldown/X.XX/ResultedEvent/XXXXXX?translationLang=LL
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   *XXXXXX - an event id (Note, several event ids can also be pasted using comma as a separator. e.g.1574736,1574926**)*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'resultedOutcome id'** - to see the particular outcome
    PRECONDITIONS: **'priceTypeCode' ** on resulted outcome level - to see the SP or LP price attribute
    PRECONDITIONS: **'priceNum'**, **'priceDen'**,** 'priceDec**' on outcome level - to see attributes for Price/Odds buttons
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
        EXPECTED: Grid content for the event is shown
        """
        pass

    def test_005_verify_price_sp_column_in_the_results_section(self):
        """
        DESCRIPTION: Verify **'Price (SP)'** column in the Results section
        EXPECTED: Actual Price/Odds are shown
        """
        pass

    def test_006_verify_price__odds_buttons_correctness_for_resulted_outcome(self):
        """
        DESCRIPTION: Verify Price / Odds buttons correctness for resulted outcome
        EXPECTED: *   Prices are taken ONLY from the "SP" attribute (see **priceTypeCodes='SP'** on resultedOutcome level ).
        EXPECTED: *   Prices correspond to **'priceNum'**/**'priceDen'** attributes - for fractional price displaying - default state
        EXPECTED: *   Prices correspond to the** 'PriceDec'** attribure - for decimal prices displaying
        """
        pass
