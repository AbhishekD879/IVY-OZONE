import pytest

import tests
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.favourites
@pytest.mark.bet_placement
@pytest.mark.betslip
@pytest.mark.sports
@pytest.mark.login
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-50433')  # Coral only
class Test_C28605_Verify_adding_removing_matches_to_from_favourites_on_Betslip(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28605
    NAME: Verify adding/removing matches to from favourites on Betslip
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True
    receipt = None
    sport_name = 'Football'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event for test
        """
        if self.cms_config.get_widgets(widget_type='favourites')[0]['disabled']:
            raise CmsClientException('"Favourites" widget is disabled in CMS')

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=1)

            self.__class__.eventID = events[0]['event']['id']
            self.__class__.event_name = normalize_name(events[0]['event']['name'])
            outcomes = next(((market['market']['children']) for market in events[0]['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.team1 = list(self.selection_ids.keys())[0]
            self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=events[0])

            self._logger.info(f'*** First football event with id "{self.eventID}" name "{self.event_name}" and '
                              f'selection_ids "{self.selection_ids}"')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID, self.__class__.team1, self.__class__.selection_ids =\
                event_params.event_id, event_params.team1, event_params.selection_ids

            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                   query_builder=self.ss_query_builder)
            event_name = normalize_name(event_resp[0]['event']['name'])
            self._logger.info(f'*** Created Football event "{event_name}"')
            self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

    def test_001_load_oxygen_application_and_login(self):
        """
        DESCRIPTION: Load Oxygen application
        DESCRIPTION: Login as a user that has sufficient funds to place a bet
        EXPECTED: Homepage is opened
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_add_selections_to_the_betslip_and_navigate_to_the_betslip_page(self):
        """
        DESCRIPTION: Add selection(s) to the Betslip
        EXPECTED: The selection(s) is/are added
        EXPECTED: Navigate to the Betslip page
        EXPECTED: Betslip page is opened
        EXPECTED: Added selection(s) is/are present
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_003_enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: Bet Receipt is shown
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_tap_on_the_favourite_matches_star_icon_near_event_team_a_v_team_b(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' star icon near 'Event (Team A v Team B)'
        EXPECTED: The star icon becomes bold
        EXPECTED: The event is added to the 'Favourite Matches' page
        """
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section_name, section = list(betreceipt_sections.items())[0]
        receipts = section.items_as_ordered_dict
        self.assertTrue(receipts, msg='No Receipts found')
        receipt_name, receipt = list(receipts.items())[0]
        receipt.favourite_icon.click()
        self.assertTrue(receipt.favourite_icon.is_selected(), msg='Favourite button is not selected after click')
        if self.device_type == 'mobile':
            self.device.navigate_to(url='%s/%s' % (tests.HOSTNAME, 'favourites'))
            self.site.wait_splash_to_hide()
            self.site.wait_content_state('Favourites', timeout=3)
            self.verify_event_on_favourites_page()
        else:
            favourites = self.site.favourites.items_as_ordered_dict
            self.assertTrue(favourites, msg='Sections are not found')
            self.assertIn(self.event_name, favourites.keys(),
                          msg=f'Event: "{self.event_name}" is not added to "Favourites"')

    def test_005_go_to_the_homepage(self):
        """
        DESCRIPTION: Go to the Homepage
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state('Homepage')

    def test_006_tap_football_icon_from_sports_menu_ribbon_find_event(self):
        """
        DESCRIPTION: Tap Football Icon From Sports Menu Ribbon Find Event
        """
        self.site.open_sport(name=self.sport_name)
        event = self.get_event_from_league(section_name=self.section_name, event_id=self.eventID)
        self.assertTrue(event.favourite_icon.is_selected(), msg='Favourite button is not selected on Football page')
        event.favourite_icon.click()
        self.assertFalse(event.favourite_icon.is_selected(expected_result=False),
                         msg='Favourite button is not deselected after click')
        event.click()
        self.site.wait_content_state('EventDetails')

    def test_007_tap_on_the_favourite_matches_icon_star_icon_in_event_details_page(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' icon (star icon) in Event details page
        EXPECTED: The star icon appeared in bold
        EXPECTED: The event is added to the 'Favourites Matches' page
        """
        fav_icon = self.site.sport_event_details.favourite_icon
        fav_icon.click()
        self.assertTrue(fav_icon.is_selected(), msg='Favourite button is not selected after click')
        if self.device_type == 'mobile':
            header_line = self.site.sport_event_details.header_line
            count = header_line.favourites_counter
            self.assertTrue(count, msg='Favourites count seems to be empty')
            self.assertEqual(int(count), 1, msg='The event is not added to the "Favourite Matches" page')
            header_line.go_to_favourites_page.click()
            self.site.wait_content_state('Favourites', timeout=3)
            self.verify_event_on_favourites_page()
        else:
            favourites = self.site.favourites.items_as_ordered_dict
            self.assertTrue(favourites, msg='Sections are not found')
            self.assertIn(self.event_name, favourites.keys(),
                          msg=f'Event: "{self.event_name}" is not added to "Favourites"')

    def test_008_add_selection_to_the_bet_slip_of_the_same_event(self):
        """
        DESCRIPTION: Add selection to the Bet Slip (of the same Event)
        EXPECTED: The selection is added
        EXPECTED: The counter on Betslip bubble is increased appropriately
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_009_enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: Bet is placed successfully
        EXPECTED: Bet Receipt is shown
        EXPECTED: 'Favourites matches' star icon is displayed as bold
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section_name, section = list(betreceipt_sections.items())[0]
        receipts = section.items_as_ordered_dict
        self.assertTrue(receipts, msg='No Receipts found')
        receipt_name, self.__class__.receipt = list(receipts.items())[0]
        self.assertTrue(self.receipt.favourite_icon.is_selected(), msg='Favourite button is not selected')

    def test_010_tap_on_the_favourite_matches_star_icon_near_the_same_event(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' star icon near the same Event
        EXPECTED: The star icon becomes unselected
        EXPECTED: The event becomes removed from favourites & from 'Favourite Matches' page appropriately
        """
        self.receipt.favourite_icon.click()
        self.assertFalse(self.receipt.favourite_icon.is_selected(expected_result=False),
                         msg='Favourite button is not deselected after click')

    def test_011_tap_on_the_event_name(self):
        """
        DESCRIPTION: Tap on the Event name
        EXPECTED: User is redirected to Event details page
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_012_verify_favourite_matches_star_icon_within_event_section(self):
        """
        DESCRIPTION: Verify 'Favourite Matches' star icon within Event section
        EXPECTED: 'Favourite Matches' star icon is not bold anymore
        """
        self.assertFalse(self.site.sport_event_details.favourite_icon.is_selected(expected_result=False),
                         msg='Favourite button is selected but should not be')

    def test_013_go_to_favourite_matches_page_and_verify_presence_of_the_event(self):
        """
        DESCRIPTION: Go to 'Favourite Matches' page and verify presence of the Event
        EXPECTED: The Event is not displayed on 'Favourite Matches' page
        """
        if self.device_type == 'mobile':
            self.site.sport_event_details.header_line.go_to_favourites_page.click()
            self.site.wait_content_state('Favourites')
            self.assertTrue(self.site.favourites.has_info_label,
                            msg='No info label displayed')
            self.assertEqual(self.site.favourites.info_label, vec.sb_desktop.NO_FAVOURITE_MATCHES,
                             msg=f'\nNo-favorite actual message: \n"{self.site.favourites.info_label}" '
                             f'\nis not equal to expected: \n"{vec.sb_desktop.NO_FAVOURITE_MATCHES}"')
        else:
            favourites = self.site.favourites.items_as_ordered_dict
            self.assertFalse(favourites, msg='"Favourites" section is not empty')
            actual_text = self.site.favourites.widget_text_logged.replace('\n', '').rstrip()
            self.assertEqual(actual_text, vec.sb_desktop.NO_FAVOURITE_MATCHES,
                             msg=f'\nNo-favorite actual message: \n"{actual_text}" '
                             f'\nis not equal to expected: \n"{vec.sb_desktop.NO_FAVOURITE_MATCHES}"')
