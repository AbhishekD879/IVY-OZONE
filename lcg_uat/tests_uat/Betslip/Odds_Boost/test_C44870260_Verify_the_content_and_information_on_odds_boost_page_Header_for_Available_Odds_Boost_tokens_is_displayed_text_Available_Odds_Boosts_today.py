import pytest
import tests
from voltron.environments import constants as vec
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can't executed on prod, Can't add odds boost token on prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870260_Verify_the_content_and_information_on_odds_boost_page_Header_for_Available_Odds_Boost_tokens_is_displayed_text_Available_Odds_Boosts_today(BaseBetSlipTest):
    """
    TR_ID: C44870260
    NAME: "Verify the content and information on odds boost page -Header for Available Odds Boost tokens is displayed, text: 'Available Odds Boost(s) today'
    DESCRIPTION: Place a bet on using Odds boost token and verify the count has been decreased after placing the bet.
    PRECONDITIONS: Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Odds Boost' item is enabled in Right menu in CMS
    PRECONDITIONS: 'My account' (User menu) Feature Toggle is enabled in CMS
    PRECONDITIONS: 'Odds Boost' item is enabled in My account (User menu) in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Odds Boost' Feature Toggle is enabled in CMS
        PRECONDITIONS: Odds Boost' item is enabled in Right menu in CMS
        PRECONDITIONS: 'My account' (User menu) Feature Toggle is enabled in CMS
        PRECONDITIONS: 'Odds Boost' item is enabled in My account (User menu) in CMS
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
        # Right menu is GVC CMS, We don't have access of it, We can't validate(My account, Odds Boost) from CMS
        selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.home_team_selection_id = list(selection_ids.values())[0]
        self.__class__.username = tests.settings.odds_boost_user
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.home_team_selection_id)

    def test_001_navigate_to_my_accounts__offers__free_bets__odds_boost(self):
        """
        DESCRIPTION: Navigate to 'My accounts' > Offers & Free bets > Odds boost
        EXPECTED: My account' (User menu) menu is expanded > Offer & Free bets
        EXPECTED: Odds Boost item is available in the menu
        EXPECTED: Summary value 1 of the number of Odds Boost tokens is displaying in Odds Boost item
        """
        self.site.login(username=self.username)
        self.site.wait_content_state('Homepage')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu items not found')
        right_menu_list = menu_items.keys()
        if self.brand == 'bma':
            self.assertIn(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1], right_menu_list,
                          msg=f'Expected item: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1]}" is not present in'
                              f'Actual items list: "{right_menu_list}"')
            self.site.right_menu.click_item(item_name=vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
            self.site.wait_content_state_changed()
            menu_items = self.site.right_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='Offers menu has no items available.')
            offer_item_list = menu_items.keys()
            ob_count = menu_items.get(vec.odds_boost.PAGE.title.upper())
            self.assertIn(vec.odds_boost.PAGE.title.upper(), offer_item_list,
                          msg=f'Expected item: "{vec.odds_boost.PAGE.title.upper()}" is not present in'
                              f'Actual items list: "{offer_item_list}"')
            self.assertTrue(ob_count.badge_text, msg='Odds boost badge count is not displayed')
            self.site.right_menu.click_item(item_name=vec.odds_boost.PAGE.title.upper())
        else:
            self.assertIn(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[2], right_menu_list,
                          msg=f'Expected item: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[2]}" is not present in'
                              f'Actual items list: "{right_menu_list}"')
            self.site.right_menu.click_item(item_name=vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[2])
            self.site.wait_splash_to_hide(timeout=1)
        self.site.wait_content_state('OddsBoost')

    def test_002_place_a_bet_with_available_information_page_odds_boost_token(self):
        """
        DESCRIPTION: Place a bet with available information page Odds boost token
        EXPECTED: Bet is placed
        EXPECTED: Odds Boost token is used
        EXPECTED: number of Odds boost will be decreased as user had placed another bet.
        """
        odds_boost_sections = list(self.site.odds_boost_page.sections.items_as_ordered_dict.values())
        self.assertTrue(odds_boost_sections, '"Odds boost section" are not displayed')
        available_count = [int(i) for i in odds_boost_sections[0].available_now.name.split() if i.isdigit()]
        self.assertTrue(available_count, msg="Available count is not displayed")

        self.open_betslip_with_selections(selection_ids=self.home_team_selection_id)
        self.site.close_all_dialogs()
        wait_for_result(lambda: self.get_betslip_sections().Singles, timeout=15)
        self.assertTrue(self.site.betslip.odds_boost_header.boost_button.is_displayed(),
                        msg='"Odds boost button" is not displayed')
        self.site.betslip.odds_boost_header.boost_button.click()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = 1
        self.site.betslip.bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

        self.navigate_to_page('oddsboost')
        self.site.wait_content_state(vec.odds_boost.PAGE.title.upper())
        updated_odds_boost_sections = list(self.site.odds_boost_page.sections.items_as_ordered_dict.values())
        self.assertTrue(updated_odds_boost_sections, '"Odds boost section" are not displayed')
        new_available_count = [int(i) for i in updated_odds_boost_sections[0].available_now.name.split()
                               if i.isdigit()]
        self.assertNotEqual(available_count, new_available_count,
                            msg=f'Old available token count: "{available_count}" is '
                            f'equal: "{new_available_count}" new odds boost')
