import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893591_Verify_if_the_user_is_able_to_view_both_open_and_settled_bets_sections_with_anonymous_user_tracked_bets_along_with_the_account_bets_if_the_user_is_logged_in(BaseBetSlipTest):
    """
    TR_ID: C64893591
    NAME: Verify if the user is able to view both open and settled bets sections with anonymous user tracked bets along with the account bets if the user is logged in
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_url2click_on_grid_tab3click_on_login_button_and_enter_valid_credentials4click_on_my_bets_at_the_bottom_of_the_page4click_on_open_and_settled_bets_tabsexpected_result1sports_url_should_be_launched_sucessfully2user_should_be_able_to_open_grid_tab3user_should_be_logged_in_sucessfully4user_should_be_able_to_access_my_bets_sucessfully4user_must_be_able_to_view_both_open_and_settled_bets_sections_with_anonymous_user_tracked_bets_and_long_with_logged_in_user_account_bets_sucessfully(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports url.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on login button and enter valid credentials.
        DESCRIPTION: 4.Click on "My Bets" at the bottom of the page.
        DESCRIPTION: 4.Click on open and settled bets tabs.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports url should be launched sucessfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be logged in sucessfully.
        DESCRIPTION: 4.User should be able to access "My Bets" sucessfully.
        DESCRIPTION: 4.User must be able to view both open and settled bets sections with anonymous user tracked bets and long with logged in user account bets sucessfully.
        EXPECTED: 1. 1.Sports url should be launched sucessfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be logged in sucessfully.
        EXPECTED: 4.User should be able to access "My Bets" sucessfully.
        EXPECTED: 4.User must be able to view both open and settled bets sections with anonymous user tracked bets and long with logged in user account bets sucessfully.
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
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='"Bet types are not displayed"')
        self.site.open_my_bets_settled_bets()
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='"Bet types are not displayed"')