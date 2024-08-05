import json
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.free_bet
@pytest.mark.free_bet_bet_placement
@pytest.mark.adhoc_suite
@pytest.mark.avtar_menu
@vtest
class Test_C65950088_Verify_count_display_for_free_bets_in_avtar_menu(BaseBetSlipTest):
    """
    TR_ID: C65950088
    NAME: Verify count display for free bets in avtar menu
    DESCRIPTION: Test case need to Verify count display for free bets, bet bundles, odds boost in avtar menu
    PRECONDITIONS: 1.User should have vaild login credentials to log into the application
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def test_000_preconditions(self):
        """
        Getting selections for the bet blacements
        """
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,number_of_events=1)[0]
        match_result_market = next((market['market'] for market in event['event']['children'] if
                                    market.get('market').get('templateMarketName') == 'Match Betting'), None)
        outcomes = match_result_market['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.selection_id = list(all_selection_ids.values())[0]

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should loaded succesfully
        """
        self.__class__.username = tests.settings.freebet_user
        if tests.settings.backend_env != 'prod':
            self.ob_config.grant_freebet(username=self.username)
        self.site.login(username=self.username, async_close_dialogs=False)
        self.site.wait_content_state("HomePage")

    def test_002_verify_avatar__icon_in_the__header(self):
        """
        DESCRIPTION: Verify avatar  icon in the  header
        EXPECTED: User with Freebets should able to see top of avtar icon with gift symbol
        """
        # Get the cookie value from local storage as a dictionary using the specified cookie name f'OX.freeBets-{self.username}'
        cookie_value = self.get_local_storage_cookie_value_as_dict(cookie_name=f'OX.freeBets-{self.username}')
        # Deserialize the cookie value into a list of bet tokens
        # Parse the cookie value as a list of bet tokens
        self.__class__.bet_tokens = json.loads(cookie_value)
        # Initialize an empty list to store free bets
        self.__class__.free_bets = []
        # Iterate through the bet tokens and select those with 'Free Bet' type
        for free_bet in self.bet_tokens:
            if free_bet['freeBetType'] == 'Free Bet':
                self.__class__.free_bets.append(free_bet)
        # Check if there are free bets available
        if len(self.free_bets) > 0:
            # If free bets are available, access the avatar and ensure the presence of the free bet icon
            self.__class__.avatar = self.site.header.user_panel.my_account_button
            self.assertTrue(self.avatar.has_freebet_icon(), msg='Free bet icon is not present')
        else:
            # If no free bets are available, raise a VoltronException
            raise VoltronException(f'Free bet is not available for this user {self.username}')

    def test_003_click_on_avatar_menu_icon(self):
        """
        DESCRIPTION: Click on Avatar menu icon
        EXPECTED: User should be able to see avatar menus with the count of free bets  (if there)
        """
        self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')

    def test_004_verify_by_clicking_on_freebets(self):
        """
        DESCRIPTION: Verify by clicking on free bets
        EXPECTED: User should navigate to free bets page
        """
        self.site.right_menu.click_item(vec.bma.EXPECTED_RIGHT_MENU.sports_free_bets if self.brand =="bma" else vec.bma.EXPECTED_RIGHT_MENU.free_bets)
        self.site.wait_content_state('freebets')
        self.assertTrue(wait_for_result(lambda: self.site.freebets.header_line, timeout=20),
                        msg='User is not navigated to "Free Bets" page')

    def test_005_verify_the_total_value_of_freebets_consists(self):
        """
        DESCRIPTION: Verify the total value of free bets consists
        EXPECTED: User should be able to see total value of all free bets on top right side
        """
        # Get the total count of available free bets from the front-end
        total_free_bet_count = int(self.site.freebets.available_free_bets_count)
        # Check if the count of free bets from the backend matches the total free bet count in the front-end
        self.assertEqual(len(self.free_bets), total_free_bet_count,
                         msg=f"Total free count in FE {total_free_bet_count} is not the same as available free count {len(self.free_bets)}")
        # Get the total balance of free bets from the front-end
        total_free_bet_value = self.site.freebets.balance.total_balance
        # Initialize a variable to accumulate the total value of available free bets
        free_bet_value = float(0)
        # Sum the value of each individual free bet
        for free_bet in self.free_bets:
            free_bet_value += float(free_bet.get('freebetTokenValue'))
        # Check if the total value of free bets from the backend matches the rounded sum of available free bets
        self.assertEqual(total_free_bet_value, round(free_bet_value, 2),
                         msg=f"Total free bet value is '{total_free_bet_value}' is not the same as available free value '{round(free_bet_value, 2)}'")

    def test_006_verify_the_freebets_displayed_as_per_sport_catgeroy_wise(self):
        """
        DESCRIPTION: Verify the free bets displayed as per sport catgeroy wise
        EXPECTED: User should be able to see the free bets displayed as per sport catgeroy wise
        """
        # covered in test_008_verify_by_clicking_go_betting_for_all_sports

    def test_007_verify_by_clicking_go_betting_for_specific_sport(self):
        """
        DESCRIPTION: Verify by clicking Go betting for specific sport
        EXPECTED: User should be navigated to respective sport
        """
        # covered in test_008_verify_by_clicking_go_betting_for_all_sports

    def test_008_verify_by_clicking_go_betting_for_all_sports(self):
        """
        DESCRIPTION: Verify by clicking Go betting for All sports
        EXPECTED: User should be navigated to Homepage
        """
        # need different sport free bets to validate this test step
        # Get the free bet items as an ordered dictionary from the front-end
        free_bet_items = self.site.freebets.items_as_ordered_dict
        # Get all sports categories from the CMS configuration and store their uppercase names
        all_sports_categories = self.cms_config.get_sport_categories()
        sport_names = [sport_category['imageTitle'].upper() for sport_category in all_sports_categories]
        # Iterate through the free bet items
        for i in range(len(free_bet_items)):
            # Get the free bet items again (refresh to avoid potential issues)
            free_bet_items = self.site.freebets.items_as_ordered_dict
            # Get the name of the current free bet
            free_bet_name = list(free_bet_items.keys())[i]
            # Check if the free bet name contains "ALL SPORTS"
            if "ALL SPORTS" in free_bet_name:
                # If "ALL SPORTS" is found, navigate to the betting section, wait for the homepage, and go back
                free_bet_items[free_bet_name].go_betting.click()
                self.site.wait_content_state('homepage')
                self.device.go_back()
            else:
                # If the free bet name matches a sport category, navigate to that sport, wait for it, and go back
                for sport_name in sport_names:
                    if sport_name.replace(" ", "") in free_bet_name.replace(" ", "").upper():
                        free_bet_items[free_bet_name].go_betting.click()
                        self.site.wait_content_state(sport_name.lower())
                        self.device.go_back()
                        break

    def test_009_verify_by_placing_bet_using_freebet_and_caluculation(self):
        """
        DESCRIPTION: Verify by placing bet using freebet and caluculation
        EXPECTED: User freebet count need to decreased and used freebets should not be display under bet slip or quick bet.
        """
        # need any sport free bet or football free bet to validate the step
        # Open the betslip with selections based on selection IDs
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        # Get the Singles section from the betslip
        singles_section = self.get_betslip_sections().Singles
        # Extract the name and stake from the first item in the Singles section
        stake_name, stake = list(singles_section.items())[0]
        # Log information about the stake
        self._logger.info(f'*** Verifying stake "{stake_name}"')
        # Check the device type to determine the action flow
        if self.device_type == 'mobile':
            # For mobile devices:
            stake.amount_form.input.click()
            bet_slip = self.get_betslip_content()
            # Ensure the betslip keyboard is displayed
            self.assertTrue(
                bet_slip.keyboard.is_displayed(name='Bet slip keyboard shown', timeout=3),
                msg='Bet slip keyboard is not shown')
            # Enter the amount 'free-bet' using the keyboard
            bet_slip.keyboard.enter_amount_using_keyboard(value='free-bet')
        else:
            # For non-mobile devices:
            # Ensure the presence of the "Use Free Bet" link
            self.assertTrue(stake.has_use_free_bet_link(), msg='"Use Free Bet" link was not found')
            # Click the "Use Free Bet" link
            stake.use_free_bet_link.click()
        # Wait for the dialog related to free bets to appear
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE,
                                           verify_name=False)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" has not appeared')
        # Select the first available free bet in the dialog
        dialog.select_first_free_bet()
        # Wait for the dialog to be closed
        self.assertTrue(dialog.wait_dialog_closed(),
                        msg=f'{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE} was not closed')
        # Click the "Bet Now" button in the betslip content
        self.get_betslip_content().bet_now_button.click()
        # Check if the bet receipt is displayed
        self.check_bet_receipt_is_displayed()
        # Click the "Done" button in the bet receipt footer
        self.site.bet_receipt.footer.click_done()
        # Call test_003_click_on_avatar_menu_icon() and test_004_verify_by_clicking_on_freebets() test methods
        self.test_003_click_on_avatar_menu_icon()
        self.test_004_verify_by_clicking_on_freebets()
        # Get the total count of available free bets from the front-end
        total_free_bet_count = int(self.site.freebets.available_free_bets_count)
        # Compare the count of free bets from the backend with the total free bet count in the front-end
        self.assertEqual(len(self.free_bets) - 1, total_free_bet_count,
                         msg=f"Total free count in FE {total_free_bet_count} is not the same as available free count {len(self.free_bets) - 1}")

