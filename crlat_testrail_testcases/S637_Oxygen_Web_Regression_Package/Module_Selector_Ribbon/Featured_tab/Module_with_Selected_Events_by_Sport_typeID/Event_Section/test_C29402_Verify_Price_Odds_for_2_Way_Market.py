import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C29402_Verify_Price_Odds_for_2_Way_Market(Common):
    """
    TR_ID: C29402
    NAME: Verify Price/Odds for 2-Way Market
    DESCRIPTION: This test case verifies Price/Odds buttons of Pre-Match and BIP event.
    PRECONDITIONS: 1. There are featured modules by <Sports> Type ID with non-US events
    PRECONDITIONS: 2. In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. User is logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_module_selector_ribbon(self):
        """
        DESCRIPTION: Go to Module Selector Ribbon
        EXPECTED: 
        """
        pass

    def test_003_go_to_event_section(self):
        """
        DESCRIPTION: Go to Event section
        EXPECTED: 
        """
        pass

    def test_004_verify_data_of_priceodds_for_verified_event(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified event
        EXPECTED: 'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        """
        pass

    def test_005_verify_order_of_priceodds_buttons_for_2_way_market(self):
        """
        DESCRIPTION: Verify order of Price/Odds buttons for 2-Way Market
        EXPECTED: Price/Odds are in **Win/Win** order according to **Primary Market**, where:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home Win
        EXPECTED: *   outcomeMeaningMinorCode="A" is a Away Win
        """
        pass

    def test_006_click_on_priceodds_button_to_add_selection_to_the_betslip_from_the_module(self):
        """
        DESCRIPTION: Click on Price/Odds button to add selection to the Betslip from the module
        EXPECTED: Selection is added to the Betslip
        """
        pass
