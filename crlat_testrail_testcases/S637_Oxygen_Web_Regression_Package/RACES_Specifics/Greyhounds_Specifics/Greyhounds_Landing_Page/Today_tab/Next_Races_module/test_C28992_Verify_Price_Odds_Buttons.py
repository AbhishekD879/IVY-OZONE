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
class Test_C28992_Verify_Price_Odds_Buttons(Common):
    """
    TR_ID: C28992
    NAME: Verify Price/Odds Buttons
    DESCRIPTION: This test case is for checking of odds for each event which is displayed in 'Next 4 Races' module
    PRECONDITIONS: To retrieve information from Site Server use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYY?racingForm=outcome&translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *YYYYY - an event id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: -  **'priceTypeCodes'** to specify a type of price / odds buttons
    PRECONDITIONS: - **'priceDen' **and** ****'priceNum'** to specify price/odds value
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_003_verify_next_races_module(self):
        """
        DESCRIPTION: Verify 'Next Races' module
        EXPECTED: The available 'Next Races' events are shown
        """
        pass

    def test_004_from_the_site_server_find_event_where___pricetypecodes__sp_and_check_price__odds_in_the_next_races_module(self):
        """
        DESCRIPTION: From the Site Server find event where:
        DESCRIPTION: *   '**priceTypeCodes'** = 'SP, '
        DESCRIPTION: and check price / odds in the 'Next Races' module
        EXPECTED: 'SP' price / odds are displayed next to each selection
        """
        pass

    def test_005_from_the_site_server_find_event_where___pricetypecodes__lp_and_check_priceodd_in_the_next_races_module(self):
        """
        DESCRIPTION: From the Site Server find event where:
        DESCRIPTION: *    **'priceTypeCodes'** = 'LP, '
        DESCRIPTION: and check price/odd in the 'Next Races' module
        EXPECTED: The 'LP' price/odd button is displayed in decimal or fractional format (depends upon the users chosen odds display preference)
        EXPECTED: Prices correspond to the **'priceNum'** and** 'priceDen'** attributes from the Site Server
        """
        pass

    def test_006_from_the_site_server_response_find_event_where___pricetypecodesp_lp____prices_are_availabe_for_outcomesand_check_priceodds_in_the_next_races_module(self):
        """
        DESCRIPTION: From the Site Server response find event where:
        DESCRIPTION: *   **'priceTypeCode'**='SP, LP, '
        DESCRIPTION: *   Prices ARE availabe for outcomes
        DESCRIPTION: and check price/odds in the 'Next Races' module
        EXPECTED: Only one 'LP' price / odd button is displayed in fractional / decimal format
        EXPECTED: Prices correspond to the **'priceNum'** and** 'priceDen'** attributes from the Site Server
        """
        pass

    def test_007_from_the_site_server_response_find_event_where___pricetypecodesp_lp____prices_are_not_availabe_for_outcomesand_check_priceodds_in_the_next_races_module(self):
        """
        DESCRIPTION: From the Site Server response find event where:
        DESCRIPTION: *   **'priceTypeCode'**='SP, LP, '
        DESCRIPTION: *   Prices are NOT availabe for outcomes
        DESCRIPTION: and check price/odds in the 'Next Races' module
        EXPECTED: Only one 'SP' price / odds button is shown for each selection
        """
        pass
