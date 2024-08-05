import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't grant odds boost tokens on prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C59928279_Verify_selection_isnt_automatically_boosted_in_Quickbet_Betslip_after_placing_boosted_bet_from_Betslip(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C59928279
    NAME: Verify selection isn't automatically boosted in Quickbet/Betslip after placing boosted bet from Betslip
    DESCRIPTION: This test case verifies selection in Quick Bet isn't boosted after placing boosted bet from Betslip
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has several Odds Boost tokens added (https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token)
    """
    keep_browser_open = True
    bet_amount = 1

    def test_000_pre_conditions(self):
        """
        DESCRIPTION: Login with user and place bet with boosting odds
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')

        username = tests.settings.default_username
        self.ob_config.grant_odds_boost_token(username=username)
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id
        self.__class__.all_selection_ids = list(event_params.selection_ids.values())
        market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')
        self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

        self.site.login(username=username)

    def test_001_add_one_selection_to_quick_bet_skip_for_desktop(self):
        """
        DESCRIPTION: Add one selection to Quick Bet (skip for Desktop)
        EXPECTED: Selection is added to Quick Bet
        EXPECTED: Boost button is displayed unselected
        """
        self.navigate_to_edp(event_id=self.eventID)
        if self.device_type == 'mobile':
            self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)
            quick_bet = self.site.quick_bet_panel
            self.assertTrue(quick_bet.has_odds_boost_button(),
                            msg='Odds boost button is present on Quickbet panel')
            self.assertFalse(quick_bet.selection.content.has_boosted_odds, msg=f'Boosted odds is showing up')
        else:
            self.open_betslip_with_selections(selection_ids=self.all_selection_ids[1])

    def test_002_add_selection_from_quick_bet_to_betslip(self):
        """
        DESCRIPTION: Add selection from Quick Bet to Betslip
        EXPECTED: Selection is added to betslip
        EXPECTED: Boost button is displayed unselected
        """
        if self.device_type == 'mobile':
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.open_betslip()
        self.site.wait_content_state_changed(timeout=20)
        sleep(2)
        self.assertTrue(self.get_betslip_content().has_odds_boost_header,
                        msg='Odds Boost header is not displayed on betslip')
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertFalse(stake.has_boosted_odds, msg=f'for "{stake_name}" Boosted odds is showing up')

    def test_003_click_boost_button_enter_stake_into_stake_field_and_place_bet(self):
        """
        DESCRIPTION: Click Boost button, enter stake into stake field and place bet
        EXPECTED: Slection is boosted after clicking  Boost sutton, new odds displayed
        EXPECTED: Bet is placed and Bet receipt displayed with boosted odds.
        """
        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        self.assertTrue(odds_boost_header, msg='Odds boost header is not available')
        self.assertEqual(odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                         msg='Button text "%s" is not the same as expected "%s"' %
                             (odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled))
        odds_boost_header.boost_button.click()
        singles_section = self.get_betslip_sections().Singles
        new_stake = list(singles_section.values())[0]
        boosted_price = new_stake.boosted_odds_container.price_value
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Bet receipt sections not found')
        single_sections = sections.get(vec.betslip.SGL)
        self.assertTrue(single_sections, msg='Double sections not found')
        sleep(2)
        boosted_value = single_sections.item_odds
        self.assertEqual(
            boosted_value.split('@')[0].strip() if self.brand == 'ladbrokes' else boosted_value.split('@')[1].strip(),
            boosted_price,
            msg=f'Boosted odds "{boosted_value}" are not the same as expected "{boosted_price}"')

    def test_004_mobile_close_bet_receipt_by_clicking_x_button_at_the_betslip_headerthen_add_same_or_different_selection_to_quick_betdesktop_dont_close_bet_receipt_add_same_or_other_selection_to_betslip(self):
        """
        DESCRIPTION: (Mobile): Close Bet Receipt by clicking 'X' button at the Betslip header
        DESCRIPTION: Then add same or different selection to Quick Bet
        DESCRIPTION: (Desktop): Don't Close Bet Receipt. Add same or other selection to betslip
        EXPECTED: Mobile: Selection is added to Quick Bet. Boost button is displayed unselected, odds are NOT boosted.
        EXPECTED: Desktop: Selection is added to Betslip. Boost button is displayed unselected, odds are NOT boosted
        """
        if self.device_type == 'mobile':
            self.site.bet_receipt.close_button.click()
        self.__class__.expected_betslip_counter_value = 0
        self.test_001_add_one_selection_to_quick_bet_skip_for_desktop()
        self.test_002_add_selection_from_quick_bet_to_betslip()
