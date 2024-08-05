import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
import voltron.environments.constants as vec
from voltron.utils.helpers import normalize_name


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.promotions
@pytest.mark.football
@pytest.mark.markets
@pytest.mark.ob_smoke
@pytest.mark.promotions_banners_offers
@pytest.mark.desktop
@pytest.mark.cms
@pytest.mark.medium
@vtest
class Test_C884421_Verify_Double_Your_Winnings_Promo_Icon_on_Football_event_details_page(BaseSportTest):
    """
    TR_ID: C884421
    NAME: Verify Double Your Winnings Promo Icon on Football event details page
    """
    keep_browser_open = True
    section_name = tests.settings.football_autotest_league
    event_level_flag, market_level_flag = 'EVFLAG_DYW', 'MKTFLAG_DYW'

    def check_dyw_promotion_for_market(self, market, is_present=True):
        if is_present:
            self.assertTrue(market.promotion_icons.has_double_your_winnings(),
                            msg='Market %s does not have "Double Your Winnings" promotion' % market.name)
            market.promotion_icons.double_your_winnings.click()
            self.check_promotion_dialog_appearance_and_close_it(
                expected_title=vec.dialogs.DIALOG_MANAGER_DOUBLE_YOUR_WINNINGS)
        else:
            self.assertFalse(market.promotion_icons.has_double_your_winnings(expected_result=False),
                             msg='Market %s have "Double Your Winnings" promotion after unchecking on TI' % market.name)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('extra_time_result', {'cashout': True})])
        self.__class__.eventID = event.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.created_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.created_event_name}"')

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0], in_play_tab_slp=True)

        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.ob_config.change_double_your_winnings_promotion_market_state(
            market_id=self.ob_config.market_ids[event.event_id][market_short_name],
            market_template_id=self.ob_config.football_config.autotest_class.autotest_premier_league.market_template_id,
            event_id=event.event_id)

        dialog_name = self.get_promotion_details_from_cms(event_level_flag=self.event_level_flag,
                                                          market_level_flag=self.market_level_flag)['popupTitle'].upper()
        vec.dialogs.DIALOG_MANAGER_DOUBLE_YOUR_WINNINGS = vec.dialogs.DIALOG_MANAGER_DOUBLE_YOUR_WINNINGS.format(dialog_name)

    def test_001_open_event_details_page_of_an_event_with_double_your_winnings_promotion_available(self):
        """
        DESCRIPTION: Open event details page of an event with **Double Your Winnings** promotion available
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_002_check_the_accordion_of_the_market_for_which_the_promotion_is_available(self):
        """
        DESCRIPTION: Check the accordion of the Market, for which the promotion is available
        EXPECTED: The promo icon is displayed on corresponding accordion
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.expected_market_sections.match_result in markets,
                        msg='MATCH RESULT market not present in markets %s' % markets.keys())

        self.check_dyw_promotion_for_market(market=markets[self.expected_market_sections.match_result])

    def test_003_uncheck_the_double_your_winnings_check_box_for_the_market_in_ti_and_save(self):
        """
        DESCRIPTION: Uncheck the "Double Your Winnings" check box for the Market in TI and save
        EXPECTED: Changes are saved
        """
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.ob_config.change_double_your_winnings_promotion_market_state(
            market_id=self.ob_config.market_ids[self.eventID][market_short_name],
            market_template_id=self.ob_config.football_config.autotest_class.autotest_premier_league.market_template_id,
            event_id=self.eventID,
            available=False)

    def test_004_refresh_the_event_details_page(self):
        """
        DESCRIPTION: Refresh the event details page
        EXPECTED: The icon is no longer displayed on the accordion
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.expected_market_sections.match_result, markets,
                      msg='MATCH RESULT market not present in markets %s' % markets.keys())
        self.check_dyw_promotion_for_market(market=markets[self.expected_market_sections.match_result],
                                            is_present=False)

    def test_005_check_off_the_double_your_winnings_check_box_for_any_other_market_for_the_same_event_in_ti_and_save(self):
        """
        DESCRIPTION: Check off the "Double Your Winnings" check box for any other Market (for the same event) in TI and save
        EXPECTED: Changes are saved
        """
        self.ob_config.change_double_your_winnings_promotion_market_state(
            market_id=self.ob_config.market_ids[self.eventID]['extra_time_result'],
            market_template_id=list(self.ob_config.football_config.autotest_class.autotest_premier_league.markets.extra_time_result.values())[0],
            event_id=self.eventID)

    def test_006_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: The promo icon is displayed on the accordion of the Market from step 6
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.expected_market_sections.extra_time_result, markets,
                      msg='EXTRA-TIME RESULT market not present in markets %s' % markets.keys())
        self.check_dyw_promotion_for_market(market=markets[self.expected_market_sections.extra_time_result])

    def test_007_check_the_event_odds_card_in_any_location_where_event_odds_card_is_displayed_and_tap_the_icon_on_the_event_odds_card(self):
        """
        DESCRIPTION: Check the event odds card in any location, where event odds card is displayed
        EXPECTED: Promo icon is not displayed on the event odds card
        """
        self.navigate_to_page(name='sport/football')
        event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
        self.assertFalse(event.promotion_icons.has_double_your_winnings(expected_result=False),
                         msg='Event %s should not have "Double Your Winnings" promotion' % self.created_event_name)
