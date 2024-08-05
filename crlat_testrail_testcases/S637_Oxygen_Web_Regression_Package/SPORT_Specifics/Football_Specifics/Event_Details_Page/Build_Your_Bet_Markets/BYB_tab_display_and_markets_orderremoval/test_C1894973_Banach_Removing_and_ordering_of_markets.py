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
class Test_C1894973_Banach_Removing_and_ordering_of_markets(Common):
    """
    TR_ID: C1894973
    NAME: Banach. Removing and ordering of markets
    DESCRIPTION: Test case verifies removing and ordering of markets on the app
    PRECONDITIONS: Request for Banach leagues : https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: 1. Build Your Bet tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: 2. Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: 3. Event belonging to Banach league is mapped (on Banach side) and created in OpenBet (T.I.)
    PRECONDITIONS: 4. BYB markets are added in CMS -> BYB -> BYB Markets
    PRECONDITIONS: Guide for Banach CMS configuration: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Banach
    """
    keep_browser_open = True

    def test_001_remove_any_of_the_market_title_in_cms_eg_match_betting(self):
        """
        DESCRIPTION: Remove any of the 'Market Title' in CMS (e.g. Match betting)
        EXPECTED: Market accordion (e.g. MATCH BETTING) is removed on the app
        """
        pass

    def test_002_verify_ordering_of_market_titles_on_the_app(self):
        """
        DESCRIPTION: Verify ordering of 'Market Titles' on the app
        EXPECTED: 'Market Titles' on the app should be displayed according to order in CMS (BYB > BYB Markets)
        """
        pass

    def test_003_move_any_of_market_title_eg_double_chance_to_the_top_of_the_list_in_cms(self):
        """
        DESCRIPTION: Move any of 'Market Title' (e.g. Double Chance) to the top of the list in CMS
        EXPECTED: Moved Market (e.g. Double Chance) should be displayed on the top of the list on the app
        """
        pass
