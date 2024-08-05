import pytest
from collections import OrderedDict
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_details_information
@pytest.mark.timeout(2000)
@vtest
class Test_C66132230_Verify_GA_Tracking_for_betdetails_expand_and_collapse_state_in_Build_your_race_card_and_Mybets_EDP_page(BaseBetSlipTest, BaseDataLayerTest, BaseRacing):
    """
    TR_ID: C66132230
    NAME: Verify GA Tracking for betdetails expand and collapse state in Build your race card and Mybets EDP page
    DESCRIPTION: This test case Verify GA Tracking for betdetails expand and collapse state in Build your race card and Mybets EDP page
    PRECONDITIONS: Bets should be available in mybets EDP
    PRECONDITIONS: User should place bets using Build your race card(Desktop only)
    """
    keep_browser_open = True
    hr_my_bets_tab = 'MY BETS'

    def get_expected_data_layer_reponce(self, action=None, tab_name=None):
        data_layer_responce = {
            "event": "Event.Tracking",
            "component.categoryevent": "betslip",
            "component.LabelEvent": "bet details",
            "component.ActionEvent": action,
            "component.PositionEvent": tab_name,
            "component.LocationEvent": tab_name,
            "component.EventDetails": "Sports",
            "component.URLClicked": "not applicable",
            "component.contentPosition": 1
        }
        return data_layer_responce

    def test_000_preconditions(self):
        """
        Get selections to place bets
        """
        number_of_events = 1
        hr_event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        number_of_events=number_of_events)[0]
        self.__class__.hr_event_id = hr_event['event']['id']
        match_result_market = next((market['market'] for market in hr_event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Win or Each Way'), None)
        outcomes = match_result_market['children']
        hr_all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes if
                                'Unnamed' not in i['outcome']['name']}
        self.__class__.hr_selection_id = list(hr_all_selection_ids.values())[0]

    def test_001_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application ladbrokes/coral
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_002_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        # Covered in above step

    def test_003_place_singlemutiple_bets__from_sportsraces(self):
        """
        DESCRIPTION: Place single/Mutiple bets  from Sports/Races
        EXPECTED: Bets should be placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.hr_selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_go_to_mybets_edp_page_and_check_the_bets_placed(self):
        """
        DESCRIPTION: Go to Mybets EDP page and check the bets placed
        EXPECTED: Bets should be available in My bets EDP page
        """
        self.navigate_to_edp(event_id=self.hr_event_id, sport_name='horse-racing')
        self.site.racing_event_details.event_user_tabs_list.open_tab(tab_name=self.hr_my_bets_tab)
        self.__class__.bet = list(self.site.racing_event_details.my_bets.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(self.bet.has_bet_details(), msg=f'Bet Details section is not displayed under {self.hr_event_id} event details My Bets tab')

    def test_005_click_on_chevron_to_expand_the_bet_details_and_check_the_ga_tracking(self):
        """
        DESCRIPTION: Click on Chevron to expand the bet details and check the Ga tracking
        EXPECTED: Bet details should be expanded
        EXPECTED: **Check the below tags in expand state for bet details:**
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betslip',
        EXPECTED: component.LabelEvent: 'bet details',
        EXPECTED: component.ActionEvent:{expand/collapse},
        EXPECTED: component.PositionEvent: {tab name} or MyBets in the EDP  // Build Your Racecard // EZnav ex: Open tab // Cash Out tab // Settled tab,
        EXPECTED: component.LocationEvent: {bet location} ex: mybets // MyBets in the EDP  // Build Your Racecard // EZnav,
        EXPECTED: component.EventDetails: {bet category type} ex: Sports // Lottos // Pools,
        EXPECTED: component.URLClicked: '{url/not applicable}' ,
        EXPECTED: component.contentPosition: {position of the bet} ex:1,2,3etc,
        EXPECTED: }]
        EXPECTED: });
        """
        self.bet.bet_details.chevron_arrow.click()
        self.assertTrue(self.bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details section is not expanded after clicking on Bet Details chevron under {self.hr_event_id} event details My Bets tab')

        actual_data_layer_response = self.get_data_layer_specific_object(object_key='event',
                                                                         object_value='Event.Tracking')
        excepted_data_layer_responce = self.get_expected_data_layer_reponce(action='expand', tab_name="MyBets in the EDP")
        self.compare_json_response(excepted_data_layer_responce, actual_data_layer_response)

    def test_006_click_on_chevron_to_collapse_the_bet_details_and_check_the_ga_tracking(self):
        """
        DESCRIPTION: Click on Chevron to collapse the bet details and check the Ga tracking
        EXPECTED: Bet details should be collapsed
        EXPECTED: **Check the below tags in collapse state for bet details:**
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betslip',
        EXPECTED: component.LabelEvent: 'bet details',
        EXPECTED: component.ActionEvent:{expand/collapse},
        EXPECTED: component.PositionEvent: {tab name} or MyBets in the EDP  // Build Your Racecard // EZnav ex: Open tab // Cash Out tab // Settled tab,
        EXPECTED: component.LocationEvent: {bet location} ex: mybets // MyBets in the EDP  // Build Your Racecard // EZnav,
        EXPECTED: component.EventDetails: {bet category type} ex: Sports // Lottos // Pools,
        EXPECTED: component.URLClicked: '{url/not applicable}' ,
        EXPECTED: component.contentPosition: {position of the bet} ex:1,2,3etc,
        EXPECTED: }]
        EXPECTED: });
        """
        self.bet.bet_details.chevron_arrow.click()
        self.assertFalse(self.bet.bet_details.is_expanded(expected_result=False),
                         msg=f'Bet Details section is not collapsed after clicking on Bet Details chevron under {self.hr_event_id} event details My Bets tab')
        actual_data_layer_response = self.get_data_layer_specific_object(object_key='event',
                                                                         object_value='Event.Tracking')
        excepted_data_layer_responce = self.get_expected_data_layer_reponce(action='collapse', tab_name="MyBets in the EDP")
        self.compare_json_response(excepted_data_layer_responce, actual_data_layer_response)

    def test_007_repeat_above_steps_for_build_your_race_card(self):
        """
        DESCRIPTION: Repeat above steps for Build your Race card
        EXPECTED:
        """
        if self.device_type == 'desktop':
            meetings_tab = vec.racing.RACING_DEFAULT_TAB_NAME.upper()
            self.navigate_to_page(name='horse-racing')
            self.site.wait_content_state('Horseracing')

            current_tab = self.site.horse_racing.tabs_menu.current.upper()
            self.assertEqual(current_tab, meetings_tab,
                             msg=f'{current_tab} tab is selected by default instead of {meetings_tab}')

            self.site.horse_racing.tab_content.build_card.build_race_card_button.click()
            exit_builder_enabled = self.site.horse_racing.tab_content.build_card.exit_builder_button.is_enabled()
            self.assertTrue(exit_builder_enabled,
                            msg="'BUILD A RACECARD' button is not replaced by 'EXIT BUILDER'")

            sections = self.site.horse_racing.tab_content.accordions_list.get_items(name=self.uk_and_ire_type_name)
            uk_and_irish_section = sections.get(self.uk_and_ire_type_name)
            try:
                self.assertTrue(uk_and_irish_section, msg=f'Failed to display {self.uk_and_ire_type_name} section')
                wait_for_result(lambda: next(iter(list(uk_and_irish_section.items_as_ordered_dict.values())), None) is not None,
                                timeout=15)
                meeting = next(iter(list(uk_and_irish_section.items_as_ordered_dict.values())), None)
            except:
                sections = self.site.horse_racing.tab_content.accordions_list.get_items(name=self.international_type_name)
                international_races_section = sections.get(self.international_type_name)
                self.assertTrue(international_races_section, msg=f'Failed to display {self.international_type_name} section')
                wait_for_result(
                    lambda: next(iter(list(international_races_section.items_as_ordered_dict.values())), None) is not None,
                    timeout=15)
                meeting = next(iter(list(international_races_section.items_as_ordered_dict.values())), None)
            events = meeting.items_as_ordered_dict
            for event_name, event in events.items():
                if event.has_checkbox():
                    event.scroll_to()
                    event.check_box.value = True
                    self.assertTrue(event.check_box.value,
                                    msg=f'Event checkbox is not ticked')
                    break
            self.assertTrue(self.site.horse_racing.tab_content.build_card.build_your_race_card_button.is_selected(),
                            msg="'BUILD YOUR RACECARD' button is not clickable after selecting the event checbox")
            self.site.horse_racing.tab_content.build_card.build_your_race_card_button.click()

            breadcrumbs = OrderedDict((key.strip().upper(), self.site.build_your_own_race_card.breadcrumbs.items_as_ordered_dict[key])
                                      for key in self.site.build_your_own_race_card.breadcrumbs.items_as_ordered_dict)
            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')
            build_your_own_race_card_title = vec.sb_desktop.BUILD_YOUR_OWN_RACE_CARD.upper()
            self.assertIn(build_your_own_race_card_title, breadcrumbs,
                          msg=f'"{build_your_own_race_card_title}" was not found in breadcrumbs "{breadcrumbs.keys()}"')

            selected_race_cards = self.site.build_your_own_race_card.tab_content.accordions_list.items_as_ordered_dict
            horse_name, horse = next(iter(selected_race_cards.items()), (None, None))
            horse.bet_button.click()
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()

            self.site.build_your_own_race_card.event_user_tabs_list.open_tab(tab_name=self.hr_my_bets_tab)
            bet = \
            list(self.site.build_your_own_race_card.my_bets.accordions_list.items_as_ordered_dict.values())[0]
            self.assertTrue(bet.has_bet_details(),
                            msg=f'Bet Details section is not displayed in Build Your Own Racecard >> My Bets tab')

            bet.bet_details.chevron_arrow.click()
            self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                            msg=f'Bet Details section is not expanded after clicking on Bet Details chevron in Build Your Own Racecard >> My Bets tab')

            actual_data_layer_response = self.get_data_layer_specific_object(object_key='event',
                                                                             object_value='Event.Tracking')
            excepted_data_layer_responce = self.get_expected_data_layer_reponce(action='expand',
                                                                                tab_name="Build Your Racecard")
            self.compare_json_response(excepted_data_layer_responce, actual_data_layer_response)

            bet.bet_details.chevron_arrow.click()
            self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                             msg=f'Bet Details section is not collapsed after clicking on Bet Details chevron in Build Your Own Racecard >> My Bets tab')
            actual_data_layer_response = self.get_data_layer_specific_object(object_key='event',
                                                                             object_value='Event.Tracking')
            excepted_data_layer_responce = self.get_expected_data_layer_reponce(action='collapse',
                                                                                tab_name="Build Your Racecard")
            self.compare_json_response(excepted_data_layer_responce, actual_data_layer_response)