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
class Test_C29418_Verify_Price_Odds_Buttons(Common):
    """
    TR_ID: C29418
    NAME: Verify Price/Odds Buttons
    DESCRIPTION: This test case is for checking of odds for each event which is displayed in <Race> events carousel
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: -  **'priceTypeCodes'** to specify a type of price / odds buttons
    PRECONDITIONS: - **'priceDen' **and** ****'priceNum'** to specify price/odds value
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_for_mobiletabletgo_to_module_selector_ribbon___module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID
        EXPECTED: *   'Feature' tab is selected by default
        EXPECTED: *   Module created by <Race> type ID is shown
        """
        pass

    def test_003_for_desktopscroll_the_page_down_to_featured_section____module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section ->-> Module created by <Race> type ID
        EXPECTED: * 'Featured' section is displayed below the following sections: Enhanced/ Sports offer carousel, In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: * Module created by <Race> type ID is shown
        """
        pass

    def test_004_from_the_site_server_find_event_where___pricetypecodes_sp_and_check_price__odds_in_the_race_events_carousel(self):
        """
        DESCRIPTION: From the Site Server find event where:
        DESCRIPTION: *   '**priceTypeCodes'** = 'SP, '
        DESCRIPTION: and check price / odds in the <Race> events carousel
        EXPECTED: One 'SP' price / odds button is displayed next to each selection
        """
        pass

    def test_005_from_the_site_server_find_event_where___pricetypecodes_lp_and_check_priceodd_in_the_race_events_carousel(self):
        """
        DESCRIPTION: From the Site Server find event where:
        DESCRIPTION: *    **'priceTypeCodes'** = 'LP, '
        DESCRIPTION: and check price/odd in the <Race> events carousel
        EXPECTED: The 'LP' price/odd button is displayed in decimal or fractional format (depends upon the users chosen odds display preference)
        EXPECTED: Prices correspond to the **'priceNum'** and** 'priceDen'** attributes from the Site Server
        """
        pass

    def test_006_from_the_site_server_response_find_event_where___pricetypecodesp_lp____prices_are_availabe_for_outcomesand_check_priceodds_in_the_race_events_carousel(self):
        """
        DESCRIPTION: From the Site Server response find event where:
        DESCRIPTION: *   **'priceTypeCode'**='SP, LP, '
        DESCRIPTION: *   Prices ARE availabe for outcomes
        DESCRIPTION: and check price/odds in the <Race> events carousel
        EXPECTED: Only one 'LP' price / odd button is displayed in fractional / decimal format next to each selection
        EXPECTED: Prices correspond to the **'priceNum'** and** 'priceDen'** attributes from the Site Server
        """
        pass

    def test_007_from_the_site_server_response_find_event_where___pricetypecodesp_lp____prices_are_not_availabe_for_outcomesand_check_priceodds_in_the_race_events_carousel(self):
        """
        DESCRIPTION: From the Site Server response find event where:
        DESCRIPTION: *   **'priceTypeCode'**='SP, LP, '
        DESCRIPTION: *   Prices are NOT availabe for outcomes
        DESCRIPTION: and check price/odds in the <Race> events carousel
        EXPECTED: Only one 'SP' price / odds button is shown next to each selection
        """
        pass
