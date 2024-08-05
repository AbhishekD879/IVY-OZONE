import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.odds_boost
@pytest.mark.odds_boost_bet_placement
@pytest.mark.adhoc_suite
@pytest.mark.avtar_menu
@vtest
class Test_C65950089_Verify_count_display_for_odds_boost_in_avtar_menu(BaseBetSlipTest):
    """
    TR_ID: C65950089
    NAME: Verify count display for odds boost in avtar menu
    DESCRIPTION: Test case need to  Verify count display for  odds boost in avtar menu
    PRECONDITIONS: 1.User should have vaild login credentials to log into the application
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        Getting selections for the bet blacements
        """
        event = \
        self.get_active_events_for_category(category_id=self.ob_config.tennis_config.category_id, number_of_events=1)[0]
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
        if self.brand !="bma":
            self.__class__.username = tests.settings.betplacement_user
        else:
            self.__class__.username = tests.settings.odd_boost_users
        self.site.wait_content_state("HomePage")
        self.site.login(username=self.username, async_close_dialogs=False)
        self.site.wait_content_state("HomePage")
        cookie_value = self.get_local_storage_cookie_value_as_dict(cookie_name=f'OX.oddsBoostTokens-{self.username}')
        # Initialize an empty list to store free bets
        self.__class__.odd_boosts = []
        # Iterate through the bet tokens and select those with 'Free Bet' type
        for bet_token in cookie_value:
            if bet_token['freebetTokenType'] == 'BETBOOST':
                self.__class__.odd_boosts.append(bet_token)
        if len(self.odd_boosts) <= 0:
            # If no free bets are available, raise a VoltronException
            raise VoltronException(f'odd boost is not available for this user {self.username}')

    def test_002_click_on_avatar_menu_icon(self):
        """
        DESCRIPTION: Click on Avatar menu icon
        EXPECTED: User should be able to see avatar menus with the count of oddboast (if there)
        """
        self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')

    def test_003_verify_by_clicking_odd_boosts(self):
        """
        DESCRIPTION: Verify by clicking odd boosts
        EXPECTED: User should  navigate to odds boast  page
        """

        self.__class__.odds_boost_item = self.site.right_menu.items_as_ordered_dict.get(
            vec.bma.EXPECTED_RIGHT_MENU.odds_boosts)
        self.assertTrue(self.odds_boost_item, msg='"Odds Boost" item is not present in righrt menu.')
        self.__class__.before_odds_boost_count = self.odds_boost_item.badge_text
        self.odds_boost_item.click()
        self.site.wait_content_state(vec.odds_boost.PAGE.title.upper())
        odds = self.site.odds_boost_page.content_title_text
        self.assertTrue(odds, msg='User not redirected to odds boost information page.')

    def test_004_verify_the_odd_boosts_displayed_as_per_sport_catgeroy_wise(self,sport_name="ALL"):
        """
        DESCRIPTION: Verify the odd boosts displayed as per sport catgeroy wise
        EXPECTED: User should be able to see the odd boosts displayed as per sport catgeroy wise
        """
        self.__class__.all_odds = self.site.odds_boost_page.sections.items_as_ordered_dict
        available_odd_boosts = self.all_odds.get('oddsBoostSection.Available')
        sections = available_odd_boosts.section_items_as_ordered_dict
        self.assertTrue(sections, msg="There no odds boost sport wise divided ")
        for section_name, section in sections.items():
            section.scroll_to()
            odd_boost = section.items_as_ordered_dict
            self.assertTrue(odd_boost, msg=f'There are no odds boost under sport section "{section_name} under sport pill sportname {sport_name}"')

    def test_005_verify_by_switching_the_sports_tabs(self):
        """
        DESCRIPTION: Verify by switching the sports tabs
        EXPECTED: User should be able to see to odd boosts with in tab
        """
        # Check if the brand is not "bma"
        if self.brand != "bma":
            # Get the sports switcher items as an ordered dictionary from the odds boost page
            sport_switcher = self.site.odds_boost_page.sections.sports_pills.items_as_ordered_dict
            # Iterate through the sports switcher items
            for i in range(len(sport_switcher)):
                # Get the sports switcher items again (refresh to avoid potential issues)
                sport_switcher = self.site.odds_boost_page.sections.sports_pills.items_as_ordered_dict
                # Get the name of the current sport
                sport_name = list(sport_switcher.keys())[i]
                # Access the specific sport by name, excluding "ALL"
                if sport_name.upper() != "ALL":
                    # Scroll to the sport filter and click it
                    sport = sport_switcher[sport_name]
                    sport.scroll_to()
                    sport.click()
                    # Wait for a moment
                    wait_for_haul(3)
                    # Call the  test method
                    self.test_004_verify_the_odd_boosts_displayed_as_per_sport_catgeroy_wise(sport_name=sport_name)

    def test_006_verify_by_clicking_chevron_beside_the_odd_boost(self):
        """
        DESCRIPTION: Verify by clicking chevron beside the odd boost
        EXPECTED: User should be navigated to the respective url
        """
        # Set class attributes 'tennis' and 'multisport' to False initially
        self.__class__.tennis = False
        self.__class__.multisport = False

        # Check if the brand is not "bma"
        if self.brand != "bma":
            # Get the sports switcher items as an ordered dictionary from the odds boost page
            sport_switcher = self.site.odds_boost_page.sections.sports_pills.items_as_ordered_dict
            # Find and click the "ALL" sports switcher item
            sport = next((sport for sport_name, sport in sport_switcher.items() if sport_name.upper() == "ALL"),None)
            if sport:
                sport.click()
        # Get all sports categories from the CMS configuration and store their uppercase names
        all_sports_categories = self.cms_config.get_sport_categories()
        sport_names = [sport_category['imageTitle'].upper() for sport_category in all_sports_categories]
        # Get available odds boosts from the odds boost section
        available_odd_boosts = self.all_odds.get('oddsBoostSection.Available')
        sections = available_odd_boosts.section_items_as_ordered_dict
        # Ensure there are sections with odds boosts divided by sport
        self.assertTrue(sections, msg="There are no odds boost sport-wise divided")
        # Iterate through the sections
        for i in range(len(sections)):
            # Get all odds boosts as an ordered dictionary
            all_odds = self.site.odds_boost_page.sections.items_as_ordered_dict
            available_odd_boosts = all_odds.get('oddsBoostSection.Available')
            sections = available_odd_boosts.section_items_as_ordered_dict
            # Get the name of the current section
            section_name = list(sections.keys())[i]
            section = sections[section_name]
            # Scroll to the section
            section.scroll_to()
            # Get the odds boosts within the section
            odd_boosts = section.items_as_ordered_dict
            # Ensure there are odds boosts in the section
            self.assertTrue(odd_boosts, msg=f'There are no odds boosts under the sport section "{section_name}"')
            # Find and click the first available odds boost within the section
            odd_boost_name, odd_boost = next(
                ((odd_boost_name, odd_boost) for odd_boost_name, odd_boost in odd_boosts.items() if
                 odd_boost_name is not None), None)
            odd_boost.click()
            # Check if the section name contains 'MULTI-SPORT'
            if 'MULTI-SPORT' in section_name:
                self.site.wait_content_state('homepage')
                self.device.go_back()
                self.__class__.multisport = True
            else:
                # Iterate through sport names to match the section name and set 'tennis' attribute if needed
                for sport_name in sport_names:
                    if sport_name.replace(" ", "") in section_name.replace(" ", "").upper():
                        if 'AMERICANFOOTBALL' in section_name.replace(" ", "").upper():
                            self.site.wait_content_state('american-football')
                        else:
                            self.site.wait_content_state(sport_name.lower())
                        self.device.go_back()
                        if sport_name.replace(" ", "") == "TENNIS":
                            self.__class__.tennis = True
                        break

    def test_007_verify_placing_bet_by__boosting_the_odds(self):
        """
        DESCRIPTION: verify placing bet by  boosting the odds
        EXPECTED: User should be able place bets with boosted odds.
        """
        # please collet user to odd booster to run this step at present we have odd boost for coral
        if self.multisport or self.tennis or self.brand=="bma":
            # Open the betslip with selections based on selection IDs
            self.open_betslip_with_selections(selection_ids=self.selection_id)
            self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
            self.assertTrue(self.odds_boost_header, msg='Odds boost header is not available')
            self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                            msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
            self.assertEqual(self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                             msg='Button text "%s" is not the same as expected "%s"' %
                                 (self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled))
            # Get the Singles section from the betslip
            singles_section = self.get_betslip_sections().Singles
            # Extract the name and stake from the first item in the Singles section
            stake_name, stake = list(singles_section.items())[0]
            # Log information about the stake
            self.enter_stake_amount(stake=(stake_name,stake),stake_bet_amounts={stake_name: 1})
            self._logger.info(f'*** Verifying stake "{stake_name}"')
            self.__class__.before_est_returns = stake.est_returns
            self.assertTrue(self.before_est_returns,
                            msg=f'Est. Returns is not shown for "{stake_name}" stake')
        else:
            raise VoltronException(f'odd boost for multi sport or tennis sport is not available for this user {self.username}')

    def test_008_verify_price_get_changes_when_odds_get_boosted(self):
        """
        DESCRIPTION: Verify price get changes when odds get boosted
        EXPECTED: Boosted button need to replace with reboosted
        """
        self.odds_boost_header.boost_button.click()
        odds_boost_header = self.get_betslip_content().odds_boost_header

        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        if not self.brand == 'ladbrokes':
            self.assertTrue(odds_boost_header.boost_button.has_boost_indicator,
                            msg='Boost button does not have boost indicator')
        elif self.brand == 'ladbrokes':
            self.assertIn('enabled', odds_boost_header.boost_button.boost_indicator,
                          msg='Boost-meter did not animate during odds boosting')
        # Get the Singles section from the betslip
        singles_section = self.get_betslip_sections().Singles
        # Extract the name and stake from the first item in the Singles section
        stake_name, stake = list(singles_section.items())[0]
        self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out')
        boosted_est_returns = stake.est_returns
        self.assertNotEqual(boosted_est_returns,self.before_est_returns,msg=f'Boosted Est. Returns value "{boosted_est_returns}" is the same as initial value "{self.before_est_returns}"')
        # Click the "Bet Now" button in the betslip content
        self.get_betslip_content().bet_now_button.click()
        # Check if the bet receipt is displayed
        self.check_bet_receipt_is_displayed()
        # Click the "Done" button in the bet receipt footer
        self.site.bet_receipt.footer.click_done()

    def test_009_verify_placing_bet_using_reboosting_odds(self):
        """
        DESCRIPTION: Verify placing bet using reboosting odds
        EXPECTED: User should be able place bets with reboosted odds.
        """
        pass

    def test_010_verify_the_count_of_the_oddsboast_after_placing_bets(self):
        """
        DESCRIPTION: verify the count of the oddsboast after placing bets
        EXPECTED: Count need to decresed
        """
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        self.test_002_click_on_avatar_menu_icon()
        odds_boost_item = self.site.right_menu.items_as_ordered_dict.get(
            vec.bma.EXPECTED_RIGHT_MENU.odds_boosts)
        self.assertTrue(self.odds_boost_item, msg='"Odds Boost" item is not present in righrt menu.')
        odds_boost_count = odds_boost_item.badge_text
        self.assertEqual(int(odds_boost_count),int(self.before_odds_boost_count)-1,msg='Odds Boost count is not less than before count after using one booster')
