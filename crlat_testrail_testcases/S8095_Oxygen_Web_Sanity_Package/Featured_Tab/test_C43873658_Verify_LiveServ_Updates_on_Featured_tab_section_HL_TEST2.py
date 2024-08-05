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
class Test_C43873658_Verify_LiveServ_Updates_on_Featured_tab_section_HL_TEST2(Common):
    """
    TR_ID: C43873658
    NAME: Verify LiveServ Updates on 'Featured' tab/section [HL/TEST2]
    DESCRIPTION: This test case verifies LiveServ Updates on 'Featured' tab/section
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to 'Featured' tab/section
    PRECONDITIONS: 3. Find the 'Featured' module created by 'Type ID'
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) Live event should contain the following attributes:
    PRECONDITIONS: * "rawIsOffCode" : "Y"
    PRECONDITIONS: * "isStarted" : "true"
    PRECONDITIONS: * "drilldownTagNames" : "EVFLAG_BL"
    PRECONDITIONS: * "isMarketBetInRun: : "true"
    PRECONDITIONS: 2) For creating the module in the 'Featured' tab/section by 'Selection ID' via CMS use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=126685715
    PRECONDITIONS: 3) For reaching the appropriate CMS per env use the following link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To get SiteServer info about the event please use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: 2) To verify price updates check new received values in "lp_den" and "lp_num" attributes using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: PRICE
    PRECONDITIONS: 3) To verify suspension/unsuspension check new received values in "status" attribute using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: EVENT/EVMKT/SELCT depends on level of triggering the status changes (event/market/outcome)
    PRECONDITIONS: 4) Be aware that Live events are not displayed in the 'Featured' modules for Desktop
    """
    keep_browser_open = True

    def test_001_verify_price_change_for_any_outcome_of_the_event(self):
        """
        DESCRIPTION: Verify price change for any outcome of the event
        EXPECTED: Corresponding 'Price/Odds' button immediately displays the new price and for a few seconds it changes its color to:
        EXPECTED: - blue color if the price has decreased
        EXPECTED: - pink color if the price has increased
        """
        pass

    def test_002_verify_suspension_on_eventmarketoutcome_level_for_one_of_the_events(self):
        """
        DESCRIPTION: Verify suspension on event/market/outcome level for one of the events
        EXPECTED: Corresponding 'Price/Odds' buttons are displayed as greyed out and become disabled
        """
        pass

    def test_003_verify_unsuspension_on_eventmarketoutcome_level_for_one_of_the_events(self):
        """
        DESCRIPTION: Verify unsuspension on event/market/outcome level for one of the events
        EXPECTED: Corresponding 'Price/Odds' buttons are displayed as active and clickable
        """
        pass

    def test_004_repeat_steps_1_3_for_the_featured_module_created_by__race_type_id__selection_id(self):
        """
        DESCRIPTION: Repeat steps 1-3 for the 'Featured' module created by:
        DESCRIPTION: - 'Race Type ID'
        DESCRIPTION: - 'Selection ID'
        EXPECTED: 
        """
        pass
