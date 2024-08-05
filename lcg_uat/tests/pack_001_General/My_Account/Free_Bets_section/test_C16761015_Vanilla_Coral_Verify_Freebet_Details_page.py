import pytest
import tests
import re
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from datetime import datetime


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C16761015_Vanilla_Coral_Verify_Freebet_Details_page(Common):
    """
    TR_ID: C16761015
    NAME: [Vanilla Coral]  Verify Freebet Details page
    DESCRIPTION: This Test Case verified Freebet Details page.
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User have Free Bets available on his account
    PRECONDITIONS: 3. **accountFreebets?freebetTokenType=SPORT** request is used to get a list of all free bets and called on 'My Balance & Freebets' page ONLY (open dev tools -> Network ->XHR tab)
    PRECONDITIONS: 4. 'Freebets' icon is present on the 'My Acount' menu ![](index.php?/attachments/get/25310456)
    """
    keep_browser_open = True
    currency = '£'
    amount = r'(-?[0-9]+(\.[0-9]+)?)'

    def test_001_log_in_to_application(self):
        """
        DESCRIPTION: Log in to application
        EXPECTED: User is logged in
        """
        username = tests.settings.freebet_user
        if tests.settings.backend_env != 'prod':
            self.ob_config.grant_freebet(username=username)
        self.site.login(username=username, async_close_dialogs=False)
        self.site.wait_content_state("HomePage")

    def test_002_tap_account_button_on_the_header(self):
        """
        DESCRIPTION: Tap Account button on the header
        EXPECTED: Account Menu is displayed
        """
        self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')

    def test_003_tap_offers__free_bets_options_from_the_list(self):
        """
        DESCRIPTION: Tap 'OFFERS & FREE BETS' options from the list
        EXPECTED: 'OFFERS & FREE BETS' menu is open
        """
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.EXPECTED_RIGHT_MENU.sports_free_bets)
        else:
            self.site.right_menu.click_item(vec.bma.EXPECTED_RIGHT_MENU.free_bets)
        self.site.wait_content_state('freebets')

    def test_004_tap_sports_free_bets__option(self):
        """
        DESCRIPTION: Tap 'SPORTS FREE BETS ' option
        EXPECTED: 'MY FREEBETS/BONUSES' page is opened that contains list of available free bets with following information:
        EXPECTED: -Freebet name
        EXPECTED: -Freebet value in proper currency (including 2 decimal places)
        EXPECTED: -'Use by' (greater than a week) in date format of DD/MM/YYYY or 'Expires' (less than a week) with number of remaining days
        EXPECTED: -Freebet Icon
        EXPECTED: -Back button
        """
        self.assertTrue(wait_for_result(lambda: self.site.freebets.header_line, timeout=20),
                        msg='User is not navigated to "Free Bets" page')
        freebet_items = self.site.freebets.freebets_content.items_as_ordered_dict
        self.assertTrue(freebet_items, msg='No Free Bets found on page')
        date_now = datetime.utcnow()
        for freebet_item_name, freebet_item in list(freebet_items.items())[:10]:
            self.assertTrue(freebet_item_name, msg='Freebet title is not present')
            if freebet_item.has_expires():
                expiration_date = freebet_item.expires
                self.assertIn(' day', expiration_date)
            else:
                expiration_date = freebet_item.used_by
                self.assertTrue(expiration_date, msg=f'Freebet: "{freebet_item_name}" expiration date is not present')
                self.assertTrue(date_now <= expiration_date,
                                msg=f'Freebet: "{freebet_item_name}" offer is expired')
            self.assertTrue(freebet_item.freebet_value,
                            msg=f'Freebet: "{freebet_item_name}" value is not present')

        if self.brand == 'ladbrokes':
            auto_freebet = list(freebet_items.values())[-1]
            match = re.search(self.amount, auto_freebet.name)
            free_bet_value = f'{self.currency}{match.group()} {vec.bma.FREE_BET.upper()}'
            self.assertEqual(auto_freebet.name, free_bet_value,
                             msg=f'Freebet name "{auto_freebet.name}" is not the same as expected "{free_bet_value}"')
            freebet_title=auto_freebet.freebet_text.split()
            freebet_text=f'{freebet_title[-2]} {freebet_title[-1]}'
            self.assertTrue(freebet_text,
                            msg=f'Freebet text "{freebet_text}" is not displayed')
            self.assertEqual(auto_freebet.freebet_title, free_bet_value,
                             msg=f'Freebet name "{auto_freebet}" is not the same as expected "{free_bet_value}"')
        else:
            free_bet = self.site.freebets.freebets_content.section_header
            auto_freebet = f'{free_bet.total_balance_with_currency} {free_bet.header_title}'
            match = re.search(self.amount, auto_freebet)
            free_bet_value = f'{self.currency}{match.group()} {vec.bma.FREE_BETS.upper()}'
            self.assertTrue(free_bet.has_fb_icon(), msg=f'"Free Bet Icon" is not displayed')
            self.assertTrue(self.site.freebets.header_line.back_button, msg=f'"Back button" is not displayed')
            self.assertEqual(auto_freebet, free_bet_value,
                             msg=f'Freebet name "{auto_freebet}" is not the same as expected "{free_bet_value}"')

    def test_005_tap_on_one_of_the_free_bet_from_the_list(self):
        """
        DESCRIPTION: Tap on one of the free bet from the list
        EXPECTED: 'FREEBET INFORMATION' page is opened that contains information about selected free bet:
        EXPECTED: -Freebet name
        EXPECTED: -Freebet value in proper currency (including 2 decimal places)
        EXPECTED: -'Use by' (greater than a week) in date format of DD/MM/YYYY or 'Expires' (less than a week) with number of remaining days
        EXPECTED: -Freeet Icon
        EXPECTED: -Back button
        EXPECTED: -'Bet Now' button
        """
        if self.brand == 'bma':
            date_now = datetime.utcnow()
            freebet_items = list(self.site.freebets.freebets_content.items_as_ordered_dict.values())[0]
            header_title = self.site.freebets.header_line.page_title.text
            self.assertEqual(header_title, vec.bma.FREEBET_INFORMATION,
                             msg=f'Freebet information"{header_title}" is not the same as expected"{vec.bma.FREEBET_INFORMATION}"')
            self.assertTrue(self.site.freebet_details.title, msg=f'Freebet"{self.site.freebet_details.title}" name is not displayed')
            freebet = self.site.freebet_details
            if freebet.has_expires():
                expiration_date = freebet.expires
                self.assertIn(' day', expiration_date)
            else:
                expiration_date = freebet.used_by
                self.assertTrue(expiration_date, msg=f'Freebet: "{freebet.title}" expiration date is not present')
                self.assertTrue(date_now <= expiration_date,
                                msg=f'Freebet: "{freebet.title}" offer is expired')
            self.assertTrue(freebet.has_fb_icon(), msg=f'"Free Bet Icon" is not displayed')
            self.assertTrue(freebet.value, msg=f'Freebet value is not displayed')
            self.assertTrue(self.site.freebets.header_line.back_button, msg=f'"Back button" is not displayed')
            self.assertTrue(self.site.freebet_details.bet_now, msg=f'"Bet now" button is not displayed')

    def test_006_tap_on_back_button(self):
        """
        DESCRIPTION: Tap on Back button
        EXPECTED: User is navigated to the 'My FREEBETS/BONUSES' page
        """
        if self.brand == 'bma':
            self.site.freebets.header_line.back_button.click()
