import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # involves creating event and granting odds boost
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C14876463_Vanilla_Verify_displaying_of_odds_boost_counter_next_to_ODDS_BOOST_in_the_OFFERS_menu(BaseBetSlipTest):
    """
    TR_ID: C14876463
    NAME: [Vanilla] Verify displaying of odds boost counter next to 'ODDS BOOST' in the 'OFFERS' menu
    DESCRIPTION: This test case verifies that users are able to see odds boost counter next to 'ODDS BOOST' options
    PRECONDITIONS: User has an Odds Boosts token. Token is NOT expired
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    """
    keep_browser_open = True
    bet_amount = 0.10

    def get_today_odds_boost(self):
        sections = self.site.odds_boost_page.sections.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        today_odds_boost = sections.get(vec.odds_boost.PAGE.today_odds_boosts)
        self.assertTrue(today_odds_boost, msg=f'"{vec.odds_boost.PAGE.today_odds_boosts}" section is not found')
        return today_odds_boost

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)

        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)

    def test_001_login_into_application(self):
        """
        DESCRIPTION: Login into application
        EXPECTED: User is logged in successfully
        EXPECTED: The "Odds Boost" token notification is displayed
        """
        self.site.login(username=self.username, ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        odd_boost_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=40)
        self.assertTrue(odd_boost_dialog,
                        msg='odd boost dialog is not shown for user with odd boost: "%s"' % self.username)

        odd_boost_dialog.header_object.close_button.click()
        self.assertFalse(self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST),
                         msg='odd boost dialog is shown, exepected- odd boost dailog should not appear')

    def test_002_open_main_page_and_click_on_the_avatar_in_the_header(self):
        """
        DESCRIPTION: Open main page and click on the avatar in the header
        EXPECTED: Account MENU is opened with 'OFFERS & FREE BETS' option
        """
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu items not found')
        if self.brand == 'bma':
            offers_free_bets = menu_items.get(vec.bma.EXPECTED_RIGHT_MENU.offers_free_bets)
        else:
            offers_free_bets = menu_items.get(vec.bma.EXPECTED_RIGHT_MENU.promotions)
        self.assertTrue(offers_free_bets, msg=f'"{offers_free_bets}" option not available in right menu items')

    def test_003_click_on_the_offers__free_bets_options(self):
        """
        DESCRIPTION: Click on the 'OFFERS & FREE BETS' options
        EXPECTED: 'Odds Boost' counter is shown next to 'ODDS BOOST' with the number of available odds boosts
        """
        self.navigate_to_page('oddsboost')
        self.site.wait_content_state(state_name='oddsboost')

        today_odds_boost = self.get_today_odds_boost()
        self.__class__.initial_odds_boost = today_odds_boost.available_now.value
        self.assertTrue(self.initial_odds_boost, msg=f'No. of availble odds boost "{self.initial_odds_boost}"')

    def test_004_use_odds_boost_available_for_the_user_and_click_on_the_avatar_in_the_header(self):
        """
        DESCRIPTION: Use Odds Boost available for the user and click on the avatar in the header
        EXPECTED: Account MENU is opened with 'OFFERS & FREE BETS' option
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections, msg=f'"{selections}" is not added to the betslip')

        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        odds_boost_header.boost_button.click()
        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        self.place_single_bet(number_of_stakes=1)
        self.site.bet_receipt.footer.click_done()

    def test_005_click_on_the_offers__free_bets_option(self):
        """
        DESCRIPTION: Click on the 'OFFERS & FREE BETS' option
        EXPECTED: 'Odds Boost' counter is shown next to 'ODDS BOOST' with the updated number of available odds boosts
        """
        self.navigate_to_page('oddsboost')
        self.site.wait_content_state(state_name='oddsboost')

        today_odds_boost = self.get_today_odds_boost()
        updated_odds_boost = today_odds_boost.available_now.value
        self.assertLess(updated_odds_boost, self.initial_odds_boost,
                        msg=f'"{updated_odds_boost}" is not less than {self.initial_odds_boost}')

    def test_006_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        self.site.logout()
        self.site.wait_content_state('Homepage')
