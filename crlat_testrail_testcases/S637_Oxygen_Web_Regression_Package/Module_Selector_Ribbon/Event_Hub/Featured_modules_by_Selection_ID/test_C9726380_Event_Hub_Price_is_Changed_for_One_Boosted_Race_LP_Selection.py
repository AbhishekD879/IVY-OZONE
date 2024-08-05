import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726380_Event_Hub_Price_is_Changed_for_One_Boosted_Race_LP_Selection(Common):
    """
    TR_ID: C9726380
    NAME: Event Hub: Price is Changed for One Boosted Race LP Selection
    DESCRIPTION: This test case verifies price change for one boosted Race SP selection on Event hub.
    PRECONDITIONS: 1. CMS and OB TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2. To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXX - event ID
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. There should be an event with Boosted Race LP selection (on CMS event is added by **selection Id**) on 'Featured' tab
    PRECONDITIONS: 4. Make sure that 'Expanded by default' check box is checked for the module that contains tested selection
    PRECONDITIONS: 5. User is on Homepage > Event Hub tab
    """
    keep_browser_open = True

    def test_001_find_a_module_with_boosted_selection_from_preconditions(self):
        """
        DESCRIPTION: Find a module with Boosted Selection from preconditions
        EXPECTED: Module with a Boosted Selection is displayed with correct outcome
        """
        pass

    def test_002_trigger_price_change_for_the_outcome_of_the_boosted_selection(self):
        """
        DESCRIPTION: Trigger price change for the outcome of the Boosted Selection
        EXPECTED: The 'Price/Odds' button is displaying a new price immediately and it changes its color to:
        EXPECTED: *   blue color if a price has decreased
        EXPECTED: *   pink color if a price has increased
        """
        pass

    def test_003_collapsethe_module(self):
        """
        DESCRIPTION: Collapse the module
        EXPECTED: Module is collapsed
        """
        pass

    def test_004_trigger_price_change_for_the_outcome_of_the_boosted_selection_again(self):
        """
        DESCRIPTION: Trigger price change for the outcome of the Boosted Selection again
        EXPECTED: Nothing happens, no blinking or color changing on UI
        """
        pass

    def test_005_expand_the_module_in_a_few_seconds_after_price_changing(self):
        """
        DESCRIPTION: Expand the module in a few seconds after price changing
        EXPECTED: The module is expanded and the 'Price/Odds' button is displaying a new price, no color changing on UI
        """
        pass
