import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot grant odds boost
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.odds_boost
@vtest
class Test_C2854678_Verify_displaying_Odds_Boost_token_value_in_My_account_User_menu(BaseBetSlipTest):
    """
    TR_ID: C2854678
    NAME: Verify displaying Odds Boost token value in My account (User menu)
    DESCRIPTION: This test case verifies displaying Odds Boost token value in My account (User menu)
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: 'Odds Boost' item is enabled in Right menu in CMS
    PRECONDITIONS: 'My account' (User menu) Feature Toggle is enabled in CMS
    PRECONDITIONS: 'Odds Boost' item is enabled in My account (User menu) in CMS
    PRECONDITIONS: Add Odds Boost token to Any bet to the user
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Generate Upcoming token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to create Upcoming Boosts https://confluence.egalacoral.com/display/SPI/How+to+create+Upcoming+Boosts
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: User should have Odds Boost and Create Event.
        """
        self.__class__.username = tests.settings.default_username
        self.ob_config.grant_odds_boost_token(username=self.username)
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids = self.event.selection_ids[self.event.team1]

    def test_001_navigate_to_the_my_account_user_menu_from_right_menu_for_mobile_and_tablet_onlynavigate_to_my_account_user_menu_from_the_header_of_the_page_for_desktop(self):
        """
        DESCRIPTION: Navigate to the 'My account' (User menu) from Right menu (for mobile and tablet only)
        DESCRIPTION: Navigate to 'My account' (User menu) from the header of the page (for desktop)
        EXPECTED: - 'My account' (User menu) menu is expanded
        EXPECTED: - Odds Boost item is available in the menu
        EXPECTED: - Summary value of the number of Odds Boost tokens is displaying in Odds Boost item
        """
        self.site.login(self.username)
        self.site.wait_content_state(state_name="Homepage")
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        self.__class__.odds_boost_item = self.site.right_menu.items_as_ordered_dict.get(vec.bma.EXPECTED_RIGHT_MENU.odds_boosts)
        self.assertTrue(self.odds_boost_item, msg='"Odds Boost" item is not present in righrt menu.')
        self.__class__.before_odds_boost_count = self.odds_boost_item.badge_text

    def test_002_tap_on_odds_boost_item(self):
        """
        DESCRIPTION: Tap on Odds Boost item
        EXPECTED: User is navigated to the Odds Boost information page
        """
        self.odds_boost_item.click()
        self.site.wait_content_state_changed(timeout=5)
        odds = self.site.odds_boost_page.content_title_text
        self.assertTrue(odds, msg='User not redirected to odds boost information page.')

    def test_003_tap_on_generic_odds_boost_token_which_can_be_used_on_any_bet(self):
        """
        DESCRIPTION: Tap on generic Odds Boost token which can be used on ANY bet
        EXPECTED: User is navigated to the homepage
        """
        all_odds = self.site.odds_boost_page.sections.items_as_ordered_dict.get('BOOSTS AVAILABLE NOW')
        available_odds = list(all_odds.items_as_ordered_dict.values())[0]
        available_odds.click()
        self.site.wait_content_state("Homepage")

    def test_004_add_selection_to_the_betslip_boost_it_and_place_this_boosted_bet(self):
        """
        DESCRIPTION: Add selection to the betslip, boost it and place this boosted bet
        EXPECTED: Bet is placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        odds_boost_header = self.get_betslip_content().odds_boost_header
        odds_boost_header.boost_button.click()
        bet_amount = 0.1
        self.place_single_bet(stake_bet_amounts={self.event.team1: bet_amount})
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_005_navigate_to_the_my_account_user_menu_and_verify_that_summary_value_of_the_number_of_odds_boost_tokens_decreased_on_one_digit(self):
        """
        DESCRIPTION: Navigate to the 'My account' (User menu) and verify that summary value of the number of Odds Boost tokens decreased on one digit
        EXPECTED: Summary value of the number of Odds Boost tokens is updated according to available number of Odds Boost tokens (decreased on one digit)
        """
        self.device.refresh_page()
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        after_odds_boost_count = self.site.right_menu.items_as_ordered_dict.get(vec.bma.EXPECTED_RIGHT_MENU.odds_boosts).badge_text
        self.assertLessEqual(after_odds_boost_count, self.before_odds_boost_count,
                             msg=f'After Count: "{after_odds_boost_count}" is not less than'
                                 f'Before Count: "{self.before_odds_boost_count}"')
