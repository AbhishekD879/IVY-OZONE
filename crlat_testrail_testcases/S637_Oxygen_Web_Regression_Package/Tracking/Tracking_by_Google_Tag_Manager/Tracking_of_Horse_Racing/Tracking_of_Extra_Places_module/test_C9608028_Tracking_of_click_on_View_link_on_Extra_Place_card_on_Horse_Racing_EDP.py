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
class Test_C9608028_Tracking_of_click_on_View_link_on_Extra_Place_card_on_Horse_Racing_EDP(Common):
    """
    TR_ID: C9608028
    NAME: Tracking of click on 'View' link on 'Extra Place' card on Horse Racing EDP
    DESCRIPTION: This test case verifies tracking in Google Analytic's data Layer of click on 'View' link on 'Extra Place' card on Horse Racing EDP
    PRECONDITIONS: 1. Enable 'Next Races' tab on Horse Racing EDP in CMS(CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
    PRECONDITIONS: 2. 'Extra Place' horse racing events should be present
    PRECONDITIONS: 3. User is viewing Horse Racing > 'Next Races' tab
    PRECONDITIONS: 4. Browser console should be opened
    PRECONDITIONS: **To configure HR Extra Place Race meeting use TI tool** (click [here](https://confluence.egalacoral.com/display/SPI/OpenBet+Systems) for credentials):
    PRECONDITIONS: - HR event should be not started ('rawIsOffCode'= 'N' in SS response)
    PRECONDITIONS: - HR event should have a primary market 'Win or Each Way'
    PRECONDITIONS: - HR event should have 'Extra Place Race' flag ticked on market level ('drilldownTagNames'='MKTFLAG_EPR' in SS response)
    """
    keep_browser_open = True

    def test_001_click_on__sign_for_ladbrokes(self):
        """
        DESCRIPTION: Click on:
        DESCRIPTION: * '>' sign for Ladbrokes
        EXPECTED: User is redirected to the event details page
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: {'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'extra place race module',
        EXPECTED: 'eventLabel' : 'view event'
        """
        pass

    def test_003_navigate_back_to_horse_racing__next_races_tab(self):
        """
        DESCRIPTION: Navigate back to Horse Racing > 'Next Races' tab
        EXPECTED: 
        """
        pass

    def test_004_click_on_extra_place_card(self):
        """
        DESCRIPTION: Click on Extra place card
        EXPECTED: User is redirected to the event details page
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: {'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'extra place race module',
        EXPECTED: 'eventLabel' : 'view event'
        """
        pass
