import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_011_RACES_Specifics.Bet_Filter.base_horseracing_bet_filter_test import BaseHorseRacingBetFilterTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_beta2
@pytest.mark.bet_filter
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.low
@vtest
class Test_C357005_Verify_Bet_Filter_Screen_Texting(BaseHorseRacingBetFilterTest):
    """
    TR_ID: C357005
    NAME: Verify Bet Finder screen texting
    DESCRIPTION: This test case verifies info messages present at the Bet Finder page
    PRECONDITIONS: Jira ticket:
    PRECONDITIONS: - HMN-2438 - Web: Apply UI to Bet Finder
    PRECONDITIONS: - HMN-2833 - Web: Amend Bet Finder
    PRECONDITIONS: Use:
    PRECONDITIONS: https://connect-app-tst1.coral.co.uk/bet-finder (Connect app)
    PRECONDITIONS: https://connect-invictus.coral.co.uk/bet-finder (Oxygen)
    """
    keep_browser_open = True

    def test_001_verify_breadcrumb_and_navigation(self):
        """
        DESCRIPTION: Verify breadcrumb and navigation
        EXPECTED: * breadcrumb text '< BET FILTER'
        EXPECTED: * Tap on '< BET FILTER' redirects user to Horse Racing page
        """
        self.openBetFilterPage()
        actual_title = self.site.horseracing_bet_filter.page_title.text
        self.assertEqual(actual_title, vec.bet_finder.BF_HEADER_TITLE,
                         msg=f'Bet finder page\'s title is incorrect.\n '
                         f'Expected is "{vec.bet_finder.BF_HEADER_TITLE}", '
                         f'Actual is {actual_title}')
        if self.brand == 'bma':
            self.assertTrue(self.site.horseracing_bet_filter.page_title.is_bold,
                            msg='Bet finder\'s page title should be in bold')

    def test_002_verify_the_texting_above_the_filters(self):
        """
        DESCRIPTION: Verify the texting above the filters
        EXPECTED: [Connect] / [Oxygen]
        EXPECTED: * Top text block should read:
        EXPECTED: BET FILTER [in bold]
        EXPECTED: Use filters or Coral's Digital Tipster to find your best bets, also save your selection for future use.
        EXPECTED: Create your search below:
        """
        if self.brand == 'bma':
            self.assertEqual(self.site.horseracing_bet_filter.title.text, vec.bet_finder.BF_HEADER_TITLE,
                             msg=f'Bet finder page\'s title is incorrect.\n '
                             f'Expected is "{self.site.horseracing_bet_filter.title.text,}", '
                             f'Actual is "{vec.bet_finder.BF_HEADER_TITLE}"')

            self.assertTrue(self.site.horseracing_bet_filter.title.is_bold,
                            msg='Bet finder\'s page title should be in bold')

        self.assertEqual(self.site.horseracing_bet_filter.description.text, vec.bet_finder.BF_HEADER_TEXT,
                         msg=f'Bet finder page\'s title is incorrect.\n '
                         f'Expected is "{self.site.horseracing_bet_filter.description.text}", '
                         f'Actual is "{vec.bet_finder.BF_HEADER_TEXT}"')

        self.assertFalse(self.site.horseracing_bet_filter.description.is_bold,
                         msg='Bet finder\'s page description shouldn\'t be in bold')

        self.assertEqual(self.site.horseracing_bet_filter.header_message.text, vec.bet_finder.BF_HEADER_MESSAGE_HORSERACING,
                         msg=f'Bet finder page\'s title is incorrect.\n '
                         f'Expected is "{vec.bet_finder.BF_HEADER_MESSAGE_HORSERACING}", '
                         f'Actual is "{self.site.horseracing_bet_filter.header_message.text}"')

        self.assertTrue(self.site.horseracing_bet_filter.header_message.is_bold,
                        msg='Bet finder\'s header message should be in bold')

    def test_003_verify_the_find_bets_bar_is_sticky_to_the_bottom_of_the_page(self):
        """
        DESCRIPTION: Verify the 'Find Bets' bar is sticky to the bottom of the page
        EXPECTED: - The bar should never be hidden while user scrolls up/down
        """
        self.site.horseracing_bet_filter.scroll_to_we(self.site.horseracing_bet_filter.stars_container)
        self.assertTrue(self.site.horseracing_bet_filter.find_bets_button.is_displayed(),
                        msg='Find Bets bar should be sticky to the bottom of the page')
