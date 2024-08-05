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
class Test_C29388_Featured_Price_is_Changed_for_One_Boosted_Race_SP_Selection(Common):
    """
    TR_ID: C29388
    NAME: Featured: Price is Changed for One Boosted Race SP Selection
    DESCRIPTION: This test case verifies price change for one boosted Race SP selection.
    DESCRIPTION: **JIRA Ticket** : BMA-2451 'Feature tab: Live serve price updates'
    PRECONDITIONS: 1. CMS and OB TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 1. To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXX - event ID
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. There should be an event with Boosted Race SP selection (on CMS event is added by **selection Id**) on 'Featured' tab
    PRECONDITIONS: 3. Make sure that 'Expanded by default' check box is checked for the module that contains tested selection
    """
    keep_browser_open = True

    def test_001_go_to_home_page_gt_featured_module(self):
        """
        DESCRIPTION: Go to Home page &gt; Featured module
        EXPECTED: Home page with Featured module is displayed
        """
        pass

    def test_002_find_a_module_with_boosted_selection_from_preconditions(self):
        """
        DESCRIPTION: Find a module with Boosted Selection from preconditions
        EXPECTED: Module with a Boosted Selection is displayed with 'SP' outcome
        """
        pass

    def test_003_trigger_price_change_for_the_outcome_of_the_boosted_selection(self):
        """
        DESCRIPTION: Trigger price change for the outcome of the Boosted Selection
        EXPECTED: The 'Price/Odds' button is NOT displaying new price and is NOT highlighted in any color because only 'SP' is shown instead of price/odds button
        """
        pass

    def test_004_collapsethe_module(self):
        """
        DESCRIPTION: Collapse the module
        EXPECTED: Module is collapsed
        """
        pass

    def test_005_trigger_price_change_for_the_outcome_of_the_boosted_selection_again(self):
        """
        DESCRIPTION: Trigger price change for the outcome of the Boosted Selection again
        EXPECTED: Nothing happens, no blinking or color changing on UI
        """
        pass

    def test_006_expand_the_module(self):
        """
        DESCRIPTION: Expand the module
        EXPECTED: Module is expanded and the 'Price/Odds' button is NOT displaying new price and is NOT highlighted in any color because only 'SP' is shown instead of price/odds button
        """
        pass
