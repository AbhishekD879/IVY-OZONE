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
class Test_C28986_Verify_Resulted_Events_With_Invalid_Data___To_be_archived(Common):
    """
    TR_ID: C28986
    NAME: Verify Resulted Events With Invalid Data  -  To be archived
    DESCRIPTION: This test case verifies how events which have invalid data are shown in the 'Results' tab
    PRECONDITIONS: To retrieve data from the Site Server use the following link:
    PRECONDITIONS: 1) To verify Results for events use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/HistoricDrilldown/X.XX/ResultedEvent/XXXXXX?translationLang=LL
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   *XXXXXX - an event id (Note, several event ids can also be pasted using comma as a separator. e.g.1574736,1574926**)*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'resultedCode'** - to see the type of selection (Win, Loose or Placed)
    PRECONDITIONS: **'priceTypeCode' ** on resulted outcome level - to see the SP or LP price attribute
    PRECONDITIONS: 2) Make sure there are the following resulted events:
    PRECONDITIONS: - All selections are loose
    PRECONDITIONS: - Prices are absent for 'SP' part on resulted outcome level
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

    def test_004_verify_events_which_have_all_loose_selections_resultcodesl(self):
        """
        DESCRIPTION: Verify events which have all loose selections (**'resultCodes'**="L")
        EXPECTED: Events with ALL Loose selections ARE NOT shown on the 'Results' tab
        """
        pass

    def test_005_verify_event_which_doesnt_have_prices_for_sp_part_prices_are_absent_on_pricetypecode_sp_level(self):
        """
        DESCRIPTION: Verify event which doesn't have prices for 'SP' part (prices are absent on '**priceTypeCode**'= "SP" level)
        EXPECTED: Events without prices ARE NOT shown on the 'Results' tab
        """
        pass
