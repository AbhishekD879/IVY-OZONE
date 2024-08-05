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
class Test_C2022257_Build_Your_Bet__Selections_saving_on_Banach_event(Common):
    """
    TR_ID: C2022257
    NAME: Build Your Bet - Selections saving on Banach event
    DESCRIPTION: Test case describes Remember selections feature
    DESCRIPTION: AUTOTEST [C48912786], [C48921973]
    PRECONDITIONS: Guide for Banach CMS configuration: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: HL requests:
    PRECONDITIONS: Request for Banach leagues: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/leagueshttps://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: - Open the app (site)
    PRECONDITIONS: - Navigate to Event details page (EDP) with Banach markets available from:
    PRECONDITIONS: Module Ribbon Tab on the Home page ( 'BUILD YOUR BET' tab name for **CORAL** / 'BET BUILDER' tab name for **LADBROKES** )
    PRECONDITIONS: or
    PRECONDITIONS: Football Sport Landing page
    PRECONDITIONS: or
    PRECONDITIONS: 'BUILD YOUR BET' module **CORAL** / 'BET BUILDER' module **LADBROKES** on the Home page ( **DESKTOP** )
    """
    keep_browser_open = True

    def test_001_tap_on_the_build_your_bet_coral__bet_builder_ladbrokes_edp_market_nameif_we_navigate_from_module_ribbon_tab_or_module__desktop__it_will_redirect_to_build_your_bet_coral__bet_builder_ladbrokes_edp_market_by_default(self):
        """
        DESCRIPTION: Tap on the 'BUILD YOUR BET' **CORAL** / 'BET BUILDER' **LADBROKES** edp market name
        DESCRIPTION: (if we navigate from Module ribbon tab or module ( **Desktop** ) it will redirect to 'BUILD YOUR BET' **CORAL** / 'BET BUILDER' **LADBROKES** edp market by default)
        EXPECTED: 'BUILD YOUR BET' **CORAL** / 'BET BUILDER' **LADBROKES** edp market is opened
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/59007988)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/59007989)
        """
        pass

    def test_002_add_few_combinable_selections_to_bybbet_builder_dashboard_from_different_markets_accordionsmatch_betting_or_both_teams_to_scoreoverunder_marketscorrect_score_etc(self):
        """
        DESCRIPTION: Add few combinable selections to BYB/Bet Builder Dashboard from different markets accordions:
        DESCRIPTION: Match Betting or Both teams to score
        DESCRIPTION: Over/Under markets
        DESCRIPTION: Correct Score etc
        EXPECTED: - Selected selections are highlighted within accordions
        EXPECTED: - 'Build Your Bet' (for **Coral** )/ 'Bet Builder' (for **Ladbrokes** ) Dashboard appears with slide animation and is displayed in an expanded state (only when the page is accessed and selections are added for the first time): on mobile in the bottom of the screen over footer menu on tablet/desktop in the bottom of the market area and above footer menu (if market area is too long to be shown within screen)
        """
        pass

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: - Selections stay highlighted after page refresh
        EXPECTED: - 'Build Your Bet' (for **Coral** ) / 'Bet Builder' (for **Ladbrokes** ) Dashboard is displayed after page refresh
        """
        pass

    def test_004_navigate_between_tabs_of_event_details_page_and_app_modules_and_then_return_back_to_the_same_banach_event(self):
        """
        DESCRIPTION: Navigate between tabs of Event Details page and app modules and then return back to the same Banach event
        EXPECTED: - Selections stay highlighted after navigation
        EXPECTED: - 'Build Your Bet' (for **Coral** ) / 'Bet Builder' (for **Ladbrokes** ) Dashboard is displayed after navigation
        """
        pass

    def test_005_close_the_browser_tab_kill_the_app_then_open_tab_app_again_and_navigate_to_the_same_banach_event(self):
        """
        DESCRIPTION: Close the browser tab (kill the app), then open tab (app) again and navigate to the same Banach event
        EXPECTED: - Selections stay highlighted after tab (app) was closed and restored
        EXPECTED: - 'Build Your Bet' (for **Coral** ) / 'Bet Builder' (for **Ladbrokes** ) Dashboard is displayed tab (app) was closed and restored
        """
        pass
