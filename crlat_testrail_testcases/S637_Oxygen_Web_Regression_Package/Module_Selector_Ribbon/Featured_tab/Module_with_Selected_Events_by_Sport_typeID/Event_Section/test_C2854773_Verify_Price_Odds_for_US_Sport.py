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
class Test_C2854773_Verify_Price_Odds_for_US_Sport(Common):
    """
    TR_ID: C2854773
    NAME: Verify Price/Odds for US Sport
    DESCRIPTION: This test case verifies Price/Odds buttons of Pre-Match and BIP events for US Sport.
    PRECONDITIONS: 1. There are featured modules with US events and non-US events
    PRECONDITIONS: 2. In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. In order to determine US/non-US event use **typeFlagCodes="US" **(for US events)
    PRECONDITIONS: 4. User is logged in
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * For DESKTOP: 'Price/Odds' button size depends on screen resolution (see https://ladbrokescoral.testrail.com/index.php?/cases/view/1474609 test case).
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
        EXPECTED: *   outcomeMeaningMinorCode="A" is a Away Win
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home Win
        """
        pass

    def test_006_verify_order_of_priceodds_buttons_for_3_way_market(self):
        """
        DESCRIPTION: Verify order of Price/Odds buttons for 3-Way Market
        EXPECTED: Price/Odds are in Win/Draw/Win order according to Primary**** Market, where:
        EXPECTED: outcomeMeaningMinorCode="A" is an Away Win
        EXPECTED: outcomeMeaningMinorCode="D" is a Draw
        EXPECTED: outcomeMeaningMinorCode="H" is a Home Win
        """
        pass

    def test_007_click_on_priceodds_button_to_add_selection_to_the_betslip_from_the_module(self):
        """
        DESCRIPTION: Click on Price/Odds button to add selection to the Betslip from the module
        EXPECTED: Selection is added to the Betslip
        """
        pass
