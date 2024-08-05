import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.build_your_bet
@vtest
class Test_C2552948_Mobile_Tablet_Build_Your_Bet_Bet_Builder_tab_displaying_on_the_Homepage(Common):
    """
    TR_ID: C2552948
    NAME: Mobile/Tablet: 'Build Your Bet'/'Bet Builder' tab displaying on the Homepage
    DESCRIPTION: This test case verifies displaying of **Build Your Bet** (for  Coral)/ **Bet Builder** (for Ladbrokes) section on the Homepage for Mobile/Tablet
    DESCRIPTION: AUTOTEST [C2555024]
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. Request for Banach upcoming leagues: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=%&tz=%
    PRECONDITIONS: 2. Request for Banach events of the particular league for defined period of time: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events?dateFrom=2018-06-14T21:00:00.000Z&dateTo=2018-06-15T21:00:00.000Z&leagueIds=xxxx
    PRECONDITIONS: 3. CMS configuration:
    PRECONDITIONS: **Build Your Bet** (for  Coral)/ **Bet Builder** (for Ladbrokes) tab is available on the Homepage:
    PRECONDITIONS: 1) **Build Your Bet** (for  Coral)/ **Bet Builder** (for Ladbrokes) section is enabled in CMS
    PRECONDITIONS: mobile/tablet/desktop
    PRECONDITIONS: Module Ribbon Tab -> **Build Your Bet** (for  Coral)/ **Bet Builder** (for Ladbrokes); 'Visible' = True;
    PRECONDITIONS: 2) Leagues are available when:
    PRECONDITIONS: - Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: - Banach league is mapped on Banach side
    """
    keep_browser_open = True

    def test_001_verify_build_your_bet_for__coral_bet_builder_for_ladbrokes_tab_presence_in_the_module_selector_ribbonon_the_homepage(self):
        """
        DESCRIPTION: Verify **Build Your Bet** (for  Coral)/ **Bet Builder** (for Ladbrokes) tab presence in the 'Module Selector Ribbon'on the Homepage
        EXPECTED: * **Build Your Bet** (for  Coral)/ **Bet Builder** (for Ladbrokes) tab is displayed in the 'Module Selector Ribbon' on the Homepage
        EXPECTED: * **Build Your Bet** (for  Coral)/ **Bet Builder** (for Ladbrokes) tab position corresponds to the position set in CMS (Module Ribbon Tabs order)
        """
        pass

    def test_002_verify_title_on_build_your_bet_for__coral_bet_builder_for_ladbrokes_tab(self):
        """
        DESCRIPTION: Verify title on **Build Your Bet** (for  Coral)/ **Bet Builder** (for Ladbrokes) tab
        EXPECTED: * **Build Your Bet** (for  Coral)/ **Bet Builder** (for Ladbrokes) tab title corresponds name set in CMS
        """
        pass
