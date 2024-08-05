import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod #Can't create offers in Prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.races
@pytest.mark.free_ride
@vtest
class Test_C62933321_Verify_display_of_automated_betslip_details_in_My_Bets_Page(BaseBetSlipTest):
    """
    TR_ID: C62933321
    NAME: Verify display of automated betslip details in My Bets Page
    DESCRIPTION: This test case verifies display of automated betslip details in My Bets Page
    PRECONDITIONS: 1. Third question with Answers(option1,Option2 and Option3) and Summary message are configured in CMS (Free Ride-&gt; campaign -&gt; Questions)
    PRECONDITIONS: 2. Login to Ladbrokes application with eligible customers for Free Ride
    PRECONDITIONS: 3. Click on 'Launch Banner' in Homepage
    PRECONDITIONS: 4. Click on CTA Button in Splash Page
    PRECONDITIONS: 5. User should select answers for First, Second and Third questions
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Campaign should be created in CMS
        PRECONDITIONS: Offer should be assigned to the user in OB
        """
        self.__class__.username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=self.username)
        self.update_spotlight_events_price(class_id=223)
        campaign_id = self.cms_config.check_update_and_create_freeride_campaign()
        self.__class__.campaign_questions_response = self.cms_config.get_freeride_campaign_details(campaign_id)
        self.__class__.pots = self.cms_config.get_pots(freeride_campaignid=campaign_id)
        self.site.login(username=self.username)
        self.__class__.free_ride_banner = self.site.home.free_ride_banner()
        self.free_ride_banner.click()
        self.__class__.free_ride_dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE,
                                                                    timeout=10,
                                                                    verify_name=False)
        self.assertTrue(self.free_ride_dialog.cta_button.is_displayed(),
                        msg='Splash page with CTA button not displayed')
        self.free_ride_dialog.cta_button.click()
        free_ride_overlay_result = wait_for_result(lambda: self.site.free_ride_overlay is not None,
                                                   timeout=10, name='Waiting for free ride overlay to be displayed')
        self.assertTrue(free_ride_overlay_result, msg='free ride overlay is not displayed')
        self.assertTrue(self.site.free_ride_overlay.welcome_message,
                        msg="welcome Message is not displayed in Free Ride Overlay screen")
        first_question = wait_for_result(lambda: self.site.free_ride_overlay.first_question is not None,

                                         timeout=10, name='Waiting for First Question to be displayed')
        self.assertTrue(first_question, msg='Question is not displayed yet')
        wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                        timeout=20, name='Waiting for options to be displayed')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.values())
        options[0].click()
        second_question = wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                                          timeout=10, name='Waiting for second Question to be displayed')
        self.assertTrue(second_question,
                        msg='Second question is not displayed below to step 2 of 3')
        answers = wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                                  timeout=20, name='Waiting for options to be displayed')
        self.assertTrue(answers,
                        msg='Answers are not displayed for second question')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.values())
        options[0].click()
        third_question = wait_for_result(lambda: self.site.free_ride_overlay.third_question is not None,
                                         timeout=10, name='Waiting for Third Question to be displayed')
        self.assertTrue(third_question,
                        msg='Third question is not displayed below to step 2 of 3')
        answers = wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                                  timeout=20, name='Waiting for options to be displayed')
        self.assertTrue(answers,
                        msg='Answers are not displayed for third question')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.values())
        options[0].click()

    def test_001_verify_display_of_automated_betslip(self):
        """
        DESCRIPTION: Verify display of automated betslip
        EXPECTED: Automated betslip should be successfully generated in Free Ride Overlay
        """
        summary = wait_for_result(lambda: self.site.free_ride_overlay.summary is not None,
                                  timeout=10, name='Waiting for summary to be displayed')
        self.assertTrue(summary, msg='Summary is not displayed')
        result_container = wait_for_result(lambda: self.site.free_ride_overlay.results_container is not None,
                                           timeout=10, name='Waiting for Results container betslip to be displayed')
        self.assertTrue(result_container, msg='Betslip with Results container is not displayed')

    def test_002_verify_the_fields_inautomated_betslip(self):
        """
        DESCRIPTION: Verify the fields in automated betslip
        EXPECTED: Below information should be displayed:
        EXPECTED: * That’s it! We made something for you:
        EXPECTED: * Name of the Horse:
        EXPECTED: * Name of the Jockey
        EXPECTED: * Event Time, Meeting place name
        EXPECTED: * Jockey(kits and crests) logo below to summary details
        EXPECTED: * "CTA TO RACECARD" CTA should be displayed
        """
        self.__class__.result_msg = self.site.free_ride_overlay.results_container
        self.assertIn("Here we go!", self.result_msg, msg="Here we go! content is not present in the resulted betslip")
        self.assertIn(self.campaign_questions_response['eventClassInfo']['marketPlace'][0]['typeName'].upper(),
                      self.result_msg.split(',')[1], msg="Type Name is not present in the Betslip")
        pot_id = vec.bma.EXPECTED_FREE_RIDE_POTS.TopPlayer_BigStrong_GoodChance
        horses = self.pots[pot_id]['horses']
        horses_list = []
        races_time = []
        for horse in horses:
            horses_list.append(horse['horseName'])
            races_time.append(horse['raceTime'])
        self.assertIn(self.result_msg.split('\n')[1], horses_list, msg="Horse is not listed in the betslip")
        self.assertIn(self.result_msg.split('\n')[3].split(',')[0], races_time, msg="Horse is not listed in the betslip")
        self.assertTrue(self.site.free_ride_overlay.jockey_logo.is_displayed(), msg="Jockey Logo is not displayed")
        wait_for_result(lambda: self.site.free_ride_overlay.CTA_button is not None,
                        timeout=10, name='Waiting for First Question to be displayed')
        self.assertTrue(self.site.free_ride_overlay.CTA_button.is_displayed(), msg="CTA button is not displayed")
        self.site.free_ride_overlay.CTA_button.click()
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_003_navigate_to_my_bets_page(self):
        """
        DESCRIPTION: Navigate to My Bets page
        EXPECTED: Automated Betslip details should be displayed in My Bets page
        EXPECTED: * Single @Odds
        EXPECTED: * Receipt No:
        EXPECTED: * Selection Name
        EXPECTED: * Win or Each Way market
        EXPECTED: * Time, Meeting place name
        """
        self.site.open_my_bets_open_bets()
        if self.device_type == 'mobile':
            self.site.wait_content_state(state_name='OpenBets', timeout=20)
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, number_of_bets=1)
        self.assertEqual(bet.bet_type, vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                         msg=f'Bet type "{bet.bet_type}" is not the same as expected "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}"')
        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')
        name, selection = list(bet_legs.items())[0]
        self.assertEqual(selection.outcome_name, self.result_msg.split('\n')[1],
                         msg=f'Selection name "{selection.outcome_name}" is not the same as Expected')
        self.assertEqual(name.split("-")[1].lstrip().split(" ")[0], self.result_msg.split('\n')[3].split(',')[0],
                         msg=f'Race Time is not the same as Expected')
        self.assertEqual(selection.market_name, "Win or Each Way",
                         msg=f'Market name "{selection.market_name}" is not the same as '
                             f'expected "Win or Each Way"')
        self.assertTrue(selection.event_time, msg="Events Time is not found")
        self.assertTrue(selection.odds_value, msg=f'Odds "{selection.odds_value}" is not the found')

    def test_004_verify_display_offree_ride_signposting(self):
        """
        DESCRIPTION: Verify display of Free Ride signposting
        EXPECTED: Free Ride signposting should be displayed to be Betslip details in My Bets page
        EXPECTED: Note:
        EXPECTED: As mentioned by OpenBet, Free Ride signpost display will be available after Promo sign posting implementation.
        """
        # Not yet implemented
