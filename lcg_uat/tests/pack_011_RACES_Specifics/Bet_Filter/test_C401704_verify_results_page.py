import random
import pytest
from tests.base_test import vtest
from tests.pack_011_RACES_Specifics.Bet_Filter.base_horseracing_bet_filter_test import BaseHorseRacingBetFilterTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.lad_beta2
@pytest.mark.races
@pytest.mark.connect
@pytest.mark.bet_filter
@pytest.mark.desktop
@pytest.mark.medium
@vtest
class Test_C401704_Verify_Results_page(BaseHorseRacingBetFilterTest):
    """
    TR_ID: C401704
    NAME: Verify Results page
    PRECONDITIONS: Jira ticket:
    PRECONDITIONS: - HMN-2439 - Web: Results page
    PRECONDITIONS: Use
    PRECONDITIONS: Connect app:
    PRECONDITIONS: https://connect-app-tst1.coral.co.uk/bet-finder
    PRECONDITIONS: for testing in desktop browser
    PRECONDITIONS: Sportsbook/Coral:
    PRECONDITIONS: https://connect-invictus.coral.co.uk/bet-finder/
    """
    keep_browser_open = True

    def test_001_apply_some_filtering_tap_find_bets_button(self):
        """
        DESCRIPTION: Apply some filtering. Tap 'Find bets' button
        DESCRIPTION: Verify the proper details are shown for the result items
        EXPECTED: - Verify user is redirected to Bet Filter Results screen;
        EXPECTED: - Verify [< Bet Filter Results] at the breadcrumb;
        EXPECTED: - Verify "# Results" label is shown beneath the breadcrumb;
        EXPECTED: - Verify filtering [Sort by TIME/ODDS] (for Sportsbook version only);
        EXPECTED: - Verify the correct # of the results is shown;
        EXPECTED: - Verify the results match the filtering parameters applied.
        DESCRIPTION: Verify the proper details are shown for the result items
        EXPECTED: The following details should be provided:
        EXPECTED: - Jockey, Trainer, Form, Price, Silks, Time selection is running, Runner Number
        EXPECTED: - Draw (for Sportsbook version only)
        """
        cms_config = self.get_initial_data_system_configuration().get('BetFilterHorseRacing')
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('BetFilterHorseRacing')
        if not cms_config:
            raise CmsClientException('"BetFilterHorseRacing" is absent in CMS')
        if not cms_config.get('enabled'):
            raise CmsClientException('"Horseracing Bet Filter" is disabled')
        self.get_bets()
        self.openBetFilterPage()
        button = random.randint(0, 16)
        self.site.horseracing_bet_filter.items[button].click()
        self._logger.info(msg=f'*** Selected [{self.site.horseracing_bet_filter.items[button].name}] button')

        if not self.site.horseracing_bet_filter.find_bets_button.is_enabled():
            for iteration in range(0, 16):
                self.site.horseracing_bet_filter.items[button].click()
                self._logger.info(msg=f'*** Unselected [{self.site.horseracing_bet_filter.items[button].name}] button')
                button = iteration
                self.site.horseracing_bet_filter.items[button].click()
                self._logger.info(msg=f'*** Selected [{self.site.horseracing_bet_filter.items[button].name}] button')
                if self.site.horseracing_bet_filter.find_bets_button.is_enabled():
                    break

        self.assertTrue(self.site.horseracing_bet_filter.find_bets_button.is_enabled(),
                        msg='Find Bets button is disabled')
        self.site.horseracing_bet_filter.find_bets_button.click()
        self.site.wait_splash_to_hide()

        time = self.site.racing_bet_filter_results_page.items[0].time.text

        for item in self.site.racing_bet_filter_results_page.items:
            horse_name = item.horse_name.text
            self._logger.info(msg=f'*** Verifying item with horse name "{horse_name}"')
            item.scroll_to_we()
            self.assertTrue(item.runner_number.is_displayed(), msg='Failed to display the number')
            self.softAssert(self.assertTrue, item.has_silks, msg='Failed to display the silk')
            self.assertTrue(item.horse_name.is_displayed(), msg='Failed to display the horse name')
            self.assertTrue(item.jockey_name.is_displayed(), msg='Failed to display jockey name')
            self.assertTrue(item.trainer_name.is_displayed(), msg='Failed to display trainer name')
            self.assertTrue(item.course.is_displayed(), msg='Failed to display the course')

            try:
                self.assertTrue(item.form.is_displayed())
            except AttributeError:
                self.assertTrue(self.get_formstring_value(horse_name=horse_name) == '',
                                msg=f'Failed to display the form for horse name "{horse_name}"')

            self.assertTrue(item.time.text >= time, msg=f'Items are not sorted by time.')
            time = item.time.text

        if self.brand != 'ladbrokes' or self.device_type != 'mobile':
            odds = 0.0
            self.site.racing_bet_filter_results_page.odds_sorting_link.click()
            self.site.racing_bet_filter_results_page.scroll_to_top()
            for item in self.site.racing_bet_filter_results_page.items:
                price = item.get_odds_price(odds_text=item.odds.text)
                self.assertTrue(price >= odds, msg=f'Items are not sorted by odds. Compare [{item.odds.text}] and [{odds}]')
                odds = price
