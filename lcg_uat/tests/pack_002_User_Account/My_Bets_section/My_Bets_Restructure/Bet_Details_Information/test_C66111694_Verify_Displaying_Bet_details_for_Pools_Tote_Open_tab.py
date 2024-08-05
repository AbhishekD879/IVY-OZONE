import pytest
from datetime import datetime
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tzlocal import get_localzone


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_details_information
@vtest
class Test_C66111694_Verify_Displaying_Bet_details_for_Pools_Tote_Open_tab(BaseBetSlipTest, BaseDataLayerTest):
    """
    TR_ID: C66111694
    NAME: Verify Displaying Bet details for Pools /Tote Open tab
    DESCRIPTION: This test case verify Displaying Bet details for Pools /Tote Open tab
    PRECONDITIONS: Bets should be available in open/cashout tabs
    """
    keep_browser_open = True
    selection_outcomes = []
    num_of_selections = 1
    timezone = str(get_localzone())

    def get_expected_data_layer_reponce(self, action=None, tab_name='Open tab'):
        data_layer_responce = {
            "event": "Event.Tracking",
            "component.categoryevent": "betslip",
            "component.LabelEvent": "bet details",
            "component.ActionEvent": action,
            "component.PositionEvent": tab_name,
            "component.LocationEvent": "mybets",
            "component.EventDetails": "Pools",
            "component.URLClicked": "not applicable",
            "component.contentPosition": 1
        }
        return data_layer_responce

    def verify_bet_details_section_content(self, bet=None, tab_name=None):
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded by default under {tab_name}')
        self.assertTrue(bet.has_bet_details(expected_result=True),
                        msg=f'Bet Details section is not displayed under {tab_name}')
        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                         msg=f'Bet Details section is not collapsed by default under {tab_name}')
        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details section is not expanded after click on Bet Details chevron under {tab_name}')

        actual_data_layer_response = self.get_data_layer_specific_object(object_key='event',
                                                                         object_value='Event.Tracking')
        excepted_data_layer_responce = self.get_expected_data_layer_reponce(action='expand')
        self.compare_json_response(excepted_data_layer_responce, actual_data_layer_response)

        bet.bet_details.chevron_arrow.click()
        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                         msg=f'Bet Details section is not collapsed after clicking on Bet Details chevron under {tab_name}')

        actual_data_layer_response = self.get_data_layer_specific_object(object_key='event',
                                                                         object_value='Event.Tracking')
        excepted_data_layer_responce = self.get_expected_data_layer_reponce(action='collapse')
        self.compare_json_response(excepted_data_layer_responce, actual_data_layer_response)

        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details is not expanded after click on Bet Details chevron under {tab_name}')

        actual_bet_receipt_id = bet.bet_details.bet_receipt.text.replace('\n', '').upper()
        actual_bet_datetime = bet.bet_details.bet_date_time.replace('\n', '').upper()
        actual_bet_number_of_lines = bet.bet_details.bet_number_of_lines.replace('\n', '').upper()
        actual_bet_stake_per_line = bet.bet_details.bet_stake_per_line.replace('\n', '').upper()
        actual_bet_total_stake = bet.bet_details.bet_total_stake.replace('\n', '').upper()
        actual_bet_potential_returns = bet.bet_details.bet_potential_returns.replace('\n', '').upper()
        self.assertEqual(f'BET RECEIPT:  {self.expected_bet_receipt_id.upper()}', actual_bet_receipt_id)
        self.assertEqual(f'BET PLACED:  {self.expected_bet_datetime.upper()}', actual_bet_datetime)
        self.assertEqual(f'NUMBER OF LINES: {self.num_of_selections}', actual_bet_number_of_lines)
        self.assertEqual(f'STAKE PER LINE:  £1.00', actual_bet_stake_per_line)
        self.assertEqual(f'TOTAL STAKE:  £1.00', actual_bet_total_stake)
        self.exp_bet_potential_returns = f'POTENTIAL RETURNS: N/A' if self.expected_bet_potential_returns == 'N/A' else f'POTENTIAL RETURNS: £{self.expected_bet_potential_returns}'
        self.assertEqual(f'{self.exp_bet_potential_returns}', actual_bet_potential_returns)

    def test_001_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_002_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        # Covered in above step

    def test_003_navigate_horsing__page_and_go_to_tote_pools(self):
        """
        DESCRIPTION: Navigate Horsing  page and go to Tote pools
        EXPECTED: Tote  page should be opened
        """
        base_uk_tote_instance = BaseUKTote()
        event = base_uk_tote_instance.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.eventID = event.event_id
        self.__class__.bet_amount = event.min_total_stake
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='Tote Pool tab is not opened')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        exacta_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.exacta)
        self.assertTrue(exacta_opened, msg='Exacta tab is not opened')
        self.__class__.outcomes = list(section.pool.items_as_ordered_dict.items())
        self.assertTrue(self.outcomes, msg='No outcomes found')
        for index, (outcome_name, outcome) in enumerate(self.outcomes[:2]):
            self.__class__.selection_outcomes.append(f'{index + 1} {outcome_name}')
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg=f'No checkboxes found for "{outcome_name}"')
            checkbox_name, checkbox = list(checkboxes.items())[index]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(),
                            msg=f'Checkbox "{checkbox_name}" is not selected for "{outcome_name}" after click')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')
        bet_builder.summary.add_to_betslip_button.click()
        self.site.open_betslip()

        bet_info = self.place_and_validate_single_bet()
        bet_receipt = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict.get('Single')
        self.__class__.expected_bet_receipt_id = bet_receipt.bet_id
        bet_datetime = self.site.bet_receipt.receipt_header.bet_datetime
        time_obj = datetime.strptime(bet_datetime, '%d/%m/%Y, %H:%M')
        self.__class__.expected_bet_datetime = get_date_time_as_string(date_time_obj=time_obj, tz_region='UTC',
                                                                       time_format='%H:%M - %d %b')
        current_time = get_date_time_as_string(time_format='%H:%M', url_encode=False)
        current_time = datetime.strptime(current_time, '%H:%M')
        # If the timezone is UTC, adjust the current time by 60 minutes
        europe_london = get_date_time_as_string(time_format='%H:%M', url_encode=False, tz_region='EUROPE/LONDON')
        europe_london = datetime.strptime(europe_london, '%H:%M')
        time_difference = abs(current_time - europe_london)
        if time_difference.total_seconds() / 3600 >= 1:
            self.__class__.expected_bet_datetime = get_date_time_as_string(date_time_obj=time_obj, tz_region='UTC',
                                                                           time_format='%H:%M - %d %b', hours=1)
        self.__class__.expected_bet_total_stake = bet_info.get('total_stake')
        self.__class__.expected_bet_potential_returns = bet_info.get('total_estimate_returns')
        parts = str(self.expected_bet_potential_returns).split('.')
        if len(parts) > 1 and len(parts[1]) == 1:
            self.__class__.expected_bet_potential_returns = f"{parts[0]}.{parts[1]}0"

    def test_004_place_bets__on_tote(self):
        """
        DESCRIPTION: Place bets  on Tote
        EXPECTED: Bets should be placed successfully
        """
        # Covered in above step

    def test_005_tap_on_my_bets(self):
        """
        DESCRIPTION: Tap on 'My bets'
        EXPECTED: My bets page/Betslip widget is opened
        """
        # Covered in below step

    def test_006_click_on_open_tab(self):
        """
        DESCRIPTION: Click on Open tab
        EXPECTED: Open'  tab is selected by default
        EXPECTED: Placed bet is displayed
        """
        # Covered in below step

    def test_007_check_new_section_with_bet_detail_area_available(self):
        """
        DESCRIPTION: Check new section with bet detail area available
        EXPECTED: Bet detail area is available with expand and collapse
        """
        self.site.open_my_bets_open_bets()
        result = self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.POOLS_TAB_NAME)
        self.assertTrue(result, msg=f'{vec.bet_history.POOLS_TAB_NAME} tab is not opened')
        open_pools_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=2).values())),
            None)
        self.assertIsNotNone(open_pools_tab_bet, msg='Bet is not available under Open >> Pools tab')
        self.verify_bet_details_section_content(bet=open_pools_tab_bet, tab_name='Open >> Pools tab')

    def test_008_check_the_bet_detail_information__for_poolstote___bets_placed(self):
        """
        DESCRIPTION: Check the bet detail information  for pools/tote   bets placed
        EXPECTED: Bet detail information should be as per Figma for pools/tote bets
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/c6e6ddf9-66ad-4540-ac62-4c061834e532)
        """
        # Covered in above step