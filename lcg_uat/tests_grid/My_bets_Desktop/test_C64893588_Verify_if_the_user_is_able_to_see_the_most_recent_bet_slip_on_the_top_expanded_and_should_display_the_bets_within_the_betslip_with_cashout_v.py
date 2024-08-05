import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.grid
@vtest
class Test_C64893588_Verify_if_the_user_is_able_to_see_the_most_recent_bet_slip_on_the_top_expanded_and_should_display_the_bets_within_the_betslip_with_cashout_value_if_it_is_having_any(BaseBetSlipTest):
    """
    TR_ID: C64893588
    NAME: Verify if the user is able to see the most recent bet slip on the top expanded and should display the bets within the betslip with cashout value if it is having any.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_url2click_on_grid_tab3click_on_my_bets_at_the_botton_of_the_pageexpected_result1sports_url_should_be_launched_sucessfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_access_my_bets_sucessfully4user_should_be_able_to_see_the_most_recent_bet_slip_on_the_top_expanded_and_should_display_the_bets_present_in_the_betslip_with_cashout_value_if_that_bet_slip_is_having_any(self):
        """
        DESCRIPTION: 1.Launch Ladbrokes sports url.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on "My Bets" at the botton of the page.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports url should be launched sucessfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to access "My Bets" sucessfully.
        DESCRIPTION: 4.User should be able to see the most recent bet slip on the top expanded and should display the bets present in the betslip with cashout value if that bet slip is having any.
        EXPECTED: 1. 1.Sports url should be launched sucessfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to access "My Bets" sucessfully.
        EXPECTED: 4.User should be able to see the most recent bet slip on the top expanded and should display the bets present in the betslip with cashout value if that bet slip is having any.
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        additional_filters=cashout_filter)[0]
            eventID = event.get('event').get('id')
            outcomes = next(((market['market'].get('children')) for market in event['event'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('No outcomes available')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self._logger.info(f'*** Found Football event with id "{eventID}" with selection ids: "{selection_ids}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
            selection_ids = event.selection_ids
            self._logger.info(f'*** Created Football event with selection ids: "{selection_ids}"')

        self.site.login()
        self.site.wait_content_state(state_name="Homepage")
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.open_sport(name=vec.retail.TITLE)
        self.site.wait_content_state(state_name='thegrid')
        self.site.navigation_menu.click_item(vec.bet_history.TAB_TITLE)
        self.site.open_my_bets_cashout()
        bet = list(self.site.cashout.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(bet.buttons_panel.has_full_cashout_button(),
                        msg='"FULL CASHOUT" button is not present')
