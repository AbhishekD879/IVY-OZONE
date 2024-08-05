import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.uat
# @pytest.mark.prod  - can't update odds boost CMS configuration on prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.p1
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870269_Place_in_play_pre_play_boosted_bet_and_verify_returns_odd_boost_sign_post_on_bet_receipt_and_my_bets(BaseBetSlipTest):
    """
    TR_ID: C44870269
    NAME: Place in play , pre play boosted bet and verify returns, odd boost sign post on bet receipt and my bets.
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
        # TODO: Add inplay events when actual match start
        selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.home_team_selection_id = list(selection_ids.values())[0]
        username = tests.settings.odds_boost_user
        self.site.login(username=username)
        self.ob_config.grant_odds_boost_token(username=username, level='selection', id=self.home_team_selection_id)
        self.site.wait_content_state('Homepage')

    def test_001_navigate_to_the_odds_boost_token_page(self):
        """
        DESCRIPTION: Navigate to the Odds Boost token page
        EXPECTED: User is navigated to the OB token page
        EXPECTED: The tokens are displayed
        EXPECTED: Tokens are segmented by available now & upcoming
        """
        self.site.header.right_menu_button.avatar_icon.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.BMA.EXPECTED_LIST_OF_RIGHT_MENU[1])
            self.site.wait_splash_to_hide(timeout=2)
            self.site.right_menu.click_item(vec.odds_boost.PAGE.title.upper())
        else:
            self.site.right_menu.click_item(vec.BMA.PROMOTIONS_MENU_ITEMS[1])
        self.site.wait_content_state(vec.odds_boost.PAGE.title.upper())
        self.site.close_all_dialogs()
        sections = self.site.odds_boost_page.sections.items_as_ordered_dict
        self.assertTrue(sections, msg='"available now" & "upcoming" segments are not found')
        available_now = sections.get(vec.odds_boost.PAGE.available_now_section_title)
        self.assertTrue(available_now, msg=f'Expected section "{vec.odds_boost.PAGE.available_now_section_title}" is not found')
        upcoming = sections.get(vec.odds_boost.PAGE.upcoming_boosts)
        self.assertTrue(upcoming, msg=f'Expected Section "{vec.odds_boost.PAGE.upcoming_boosts}" is not found')

    def test_002_verify_that_tokens_for_any_event_are_displayed_at_the_top_of_appropriate_available_now__upcoming_segments(self):
        """
        DESCRIPTION: Verify that tokens for ANY event are displayed at the top of appropriate available now & upcoming segments
        EXPECTED: Available now boosts tokens with ANY category are displayed at the top of 'available now' segment
        EXPECTED: Upcoming boosts tokens with ANY category are displayed at the top of 'upcoming' segment
        """
        odds_boost_sections = list(self.site.odds_boost_page.sections.items_as_ordered_dict.values())
        expected_odds_boost_section = list(self.site.odds_boost_page.sections.items_as_ordered_dict.keys())[0]
        self.assertEqual(expected_odds_boost_section, vec.odds_boost.PAGE.today_odds_boosts,
                         msg=f'Actual : "{expected_odds_boost_section}" is not same as '
                             f'Expected :"{vec.odds_boost.PAGE.today_odds_boosts}"')
        available_count = [int(i) for i in odds_boost_sections[0].available_now.name.split() if i.isdigit()]
        self.assertTrue(available_count, msg='Available count is not displayed')
        upcoming_count = [int(i) for i in odds_boost_sections[0].upcoming_boosts.name.split() if i.isdigit()]
        self.assertTrue(upcoming_count, msg='Upcoming count is not displayed')
        for new_section in odds_boost_sections[1:3]:
            tokens = list(new_section.items_as_ordered_dict.values())
            if len(tokens) > 0:
                self.assertTrue(tokens, msg='"Boost token" is not displayed')
            else:
                self._logger.info(f'****There are no token available')
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')

    def test_003_place_in_playpre_play_boosted_bet_and_verify_bet_receipt_and_my_bets(self):
        """
        DESCRIPTION: Place in-play/Pre play boosted bet and verify bet receipt and my bets
        EXPECTED: odds are boosted and signposting is displayed in the bet receipt.
        """
        self.open_betslip_with_selections(selection_ids=self.home_team_selection_id)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = 1
        actual_odds = stake.odds
        odds_boost_header = self.get_betslip_content().odds_boost_header
        odds_boost_header.boost_button.click()
        boosted_odds = stake.boosted_odds_container.price_value
        self.assertNotEqual(actual_odds, boosted_odds, msg=f'Actual odds "{actual_odds}" is same as boosted price "{boosted_odds}"')
        self.site.betslip.bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.has_odds_boost_signpost(), msg='"odds boost" signpost is not displayed')
