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
class Test_C896761_BYB__Build_Your_Bet_icons_and_module_ribbon_tab(Common):
    """
    TR_ID: C896761
    NAME: BYB - Build Your Bet icons and module ribbon tab
    DESCRIPTION: This test case verifies display of Build Your Bet icons, and 'Build Your Bet' **CORAL**/'Bet Builder' **LADBROKES** ribbon tab
    DESCRIPTION: AUTOTEST [C49405228]
    PRECONDITIONS: In order to have Banach leagues, cms setup should be made and Banach provider should return data (to be requested if none)
    PRECONDITIONS: CMS guide on Banach setup
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Banach
    PRECONDITIONS: HL requests:
    PRECONDITIONS: Request for Banach leagues:  https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/selections?obEventId=xxxxx&marketIds=[ids]
    PRECONDITIONS: CMS config for 'Build Your Bet' **CORAL**/'Bet Builder' **LADBROKES** ribbon tab on the Home page: CMS->Module Ribbon Tabs
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: - 'BET BUILDER' tab name for **LADBROKES**, 'BUILD YOUR BET' tab name for **CORAL**
    PRECONDITIONS: - Build Your bet Promo Icons should **NOT** be displayed on **LADBROKES**
    """
    keep_browser_open = True

    def test_001_coral_only__navigate_to_football_landing_page_competitions_page_accumulators_page__verify_build_your_bet_icon_where_banach_provider_is_available(self):
        """
        DESCRIPTION: **CORAL ONLY**
        DESCRIPTION: - Navigate to Football Landing Page, Competitions page, Accumulators page
        DESCRIPTION: - Verify Build Your Bet icon where Banach provider is available
        EXPECTED: - Build Your Bet icon is not present on League level (on accordion)
        EXPECTED: - Build Your Bet icon is present on event card level only
        """
        pass

    def test_002_coral_onlynavigate_to_featured_page_and_verify_the_icon(self):
        """
        DESCRIPTION: **CORAL ONLY**
        DESCRIPTION: Navigate to Featured page and verify the icon
        EXPECTED: - Build Your Bet icon is not present on League level (on accordion)
        EXPECTED: - Build Your Bet icon is present on event card level only
        """
        pass

    def test_003_navigate_to_build_your_bet_coral__bet_builder_ladbrokes_module_ribbon_tab_takes_leagues_from_banach_provider_only(self):
        """
        DESCRIPTION: Navigate to 'Build Your Bet' **CORAL** / 'Bet Builder' **LADBROKES** module ribbon tab (takes leagues from Banach provider only)
        EXPECTED: 'Build Your Bet' **CORAL** / 'Bet Builder' **LADBROKES** tab is opened
        """
        pass

    def test_004_verify_today_upcoming_tabs_presence(self):
        """
        DESCRIPTION: Verify 'Today', 'Upcoming' tabs presence
        EXPECTED: - If no leagues returned from Banach - message "Sorry, no Build Your Bet **CORAL**/Bet Builder **LADBROKES** events are available at this time" and no 'Today', 'Upcoming' tabs
        EXPECTED: - If request returns leagues for today and next 5 days - there 2 tabs ('Today' and 'Upcoming')
        EXPECTED: - If request returns leagues either for today or next 5 days - only one corresponding tab is displayed
        """
        pass

    def test_005_verify_accordions_within_build_your_bet_coralbet_builder_ladbrokes_tab(self):
        """
        DESCRIPTION: Verify accordions within 'Build Your Bet' **CORAL**/'Bet Builder' **LADBROKES** tab
        EXPECTED: - Each accordion within the tab corresponds to the Banach league
        EXPECTED: - The order of leagues which appear in BYB is defined by the order defined in CMS->BYB->Banach Leagues
        EXPECTED: - BYB icon is not present
        """
        pass

    def test_006_open_event_from_build_your_bet_coralbet_builder_ladbrokes_tab(self):
        """
        DESCRIPTION: Open event from 'Build Your Bet' **CORAL**/'Bet Builder' **LADBROKES** tab
        EXPECTED: EDP is opened on 'Build Your Bet' **CORAL**/'Bet Builder' **LADBROKES** tab
        """
        pass
