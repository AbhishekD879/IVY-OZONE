import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28447_Verify_Price_Odds(Common):
    """
    TR_ID: C28447
    NAME: Verify Price/Odds
    DESCRIPTION: This test case verifies Price/Odds buttons of event.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
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

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing page
        EXPECTED: *Desktop*:
        EXPECTED: *    <Sport> Landing Page is opened
        EXPECTED: *   'Matches'->'Today' sub tab is opened by default
        EXPECTED: *Mobile*:
        EXPECTED: *    <Sport> Landing Page is opened
        EXPECTED: *   'Matches' tab is opened by default
        """
        pass

    def test_003_verify_data_of_priceodds_for_verified_event_in_fraction_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified event in fraction format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **<price>** button is displayed instead of prices if **eventStatusCode="S"**
        """
        pass

    def test_004_verify_data_of_priceodds_for_verified_event_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified event in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **<price>** button is displayed instead of prices if **eventStatusCode="S"**
        """
        pass

    def test_005_add_selection_to_the_betslip_from_sport_landing_page(self):
        """
        DESCRIPTION: Add selection to the Betslip from <Sport> Landing Page
        EXPECTED: Bet indicator displays 1.
        """
        pass

    def test_006_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        pass

    def test_007_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by tapping 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        pass
