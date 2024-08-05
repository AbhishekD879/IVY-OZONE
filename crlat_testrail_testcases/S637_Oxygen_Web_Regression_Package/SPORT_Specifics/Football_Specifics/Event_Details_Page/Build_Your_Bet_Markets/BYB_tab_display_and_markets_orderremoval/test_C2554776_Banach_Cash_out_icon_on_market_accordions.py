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
class Test_C2554776_Banach_Cash_out_icon_on_market_accordions(Common):
    """
    TR_ID: C2554776
    NAME: Banach. Cash out icon on market accordions
    DESCRIPTION: This test case verifies 'cash out' icon being displayed/not displayed on Banach market accordions on 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab
    PRECONDITIONS: **Config:**
    PRECONDITIONS: Build Your Bet tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: Event belonging to Banach league is mapped (on Banach side) and created in OpenBet (T.I.)
    PRECONDITIONS: BYB markets are added in CMS -> BYB -> BYB Markets
    PRECONDITIONS: Guide for Banach CMS configuration: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Banach
    PRECONDITIONS: **Requests:**
    PRECONDITIONS: Request for Banach leagues : https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach event data: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events/obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Navigate to the Event Details page where 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is available
    """
    keep_browser_open = True

    def test_001_clicktap_on_build_your_bet_coral__bet_builder_ladbrokes_tab(self):
        """
        DESCRIPTION: Click/Tap on 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab
        EXPECTED: * 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is opened and selected
        EXPECTED: * Markets which are coming in **markets-grouped** request and are added in CMS are displayed as market accordions
        """
        pass

    def test_002_verify_cash_out_icon(self):
        """
        DESCRIPTION: Verify 'cash out' icon
        EXPECTED: * 'Cash out' icon is displayed on all market accordions apart from 'Player Bets'
        EXPECTED: * 'Cash out' icon is hard-coded
        """
        pass
