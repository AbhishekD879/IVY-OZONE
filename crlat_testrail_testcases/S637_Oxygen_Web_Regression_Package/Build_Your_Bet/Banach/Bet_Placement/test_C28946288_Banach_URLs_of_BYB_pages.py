import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C28946288_Banach_URLs_of_BYB_pages(Common):
    """
    TR_ID: C28946288
    NAME: Banach. URLs of BYB pages
    DESCRIPTION: Test case verifies URLs of **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) pages
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Note:**
    PRECONDITIONS: **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) tab on Homepage/event details page is loaded
    """
    keep_browser_open = True

    def test_001_mobileclick_on_build_your_bet_for_coral_bet_builder_for_ladbrokes_tab_on_homepage(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Click on **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) tab on Homepage
        EXPECTED: **Mobile:**
        EXPECTED: * **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) tab of Homepage is opened
        EXPECTED: * URL has the following structure:
        EXPECTED: https://xxx/home/buildyourbet **Coral**
        EXPECTED: https://xxx/home/betbuilder **Ladbrokes**
        EXPECTED: where
        EXPECTED: **xxx** - Coral or Ladbrokes domain
        """
        pass

    def test_002_mobile__click_on_any_event_of_build_your_bet_for_coral_bet_builder_for_ladbrokes_pagedesktop__scroll_the_homepage_down_to_build_your_bet_for_coral_bet_builder_for_ladbrokes_block__click_on_any_event_of_this_block(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: - Click on any Event of **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) page
        DESCRIPTION: **Desktop:**
        DESCRIPTION: - Scroll the Homepage down to **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) block
        DESCRIPTION: - Click on any Event of this block
        EXPECTED: **Mobile/Desktop:**
        EXPECTED: * Event Details page: **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) tab is opened by default
        EXPECTED: * URL has the following structure:
        EXPECTED: https://xxx/event/football/class/type/yyy/zzz/build-your-bet **Coral**
        EXPECTED: https://xxx/event/football/class/type/yyy/zzz/bet-builder **Ladbrokes**
        EXPECTED: where
        EXPECTED: **xxx** - Coral or Ladbrokes domain
        EXPECTED: **yyy** - Event name
        EXPECTED: **zzz** - Event id
        """
        pass

    def test_003_mobiledesktop__navigate_to_the_football_page_competitions_tab__select_class_and_type_which_include_event_with_available_byb__click_on_event_with_mapped_byb_markets(self):
        """
        DESCRIPTION: **Mobile/Desktop:**
        DESCRIPTION: - Navigate to the Football page: Competitions tab
        DESCRIPTION: - Select Class and Type which include Event with available BYB
        DESCRIPTION: - Click on Event with mapped BYB Markets
        EXPECTED: **Mobile/Desktop:**
        EXPECTED: * Event Details page: **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) tab is opened
        EXPECTED: * URL has the following structure:
        EXPECTED: https://xxx/event/football/ccc/ttt/yyy/zzz/build-your-bet **Coral**
        EXPECTED: https://xxx/event/football/ccc/ttt/yyy/zzz/bet-builder **Ladbrokes**
        EXPECTED: where
        EXPECTED: **xxx** - Coral or Ladbrokes domain
        EXPECTED: **ccc** - Class name
        EXPECTED: **ttt** - Type name
        EXPECTED: **yyy** - Event name
        EXPECTED: **zzz** - Event id
        """
        pass
