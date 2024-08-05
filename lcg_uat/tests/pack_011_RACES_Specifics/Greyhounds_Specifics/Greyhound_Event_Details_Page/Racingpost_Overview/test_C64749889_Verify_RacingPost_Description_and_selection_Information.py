import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound


# @pytest.mark.tst2 # Racing Post Info is not available
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.greyhounds
@pytest.mark.event_details
@vtest
class Test_C64749889_Verify_RacingPost_Description_and_selection_Information(BaseGreyhound):
    """
    TR_ID: C64749889
    NAME: Verify RacingPost Description and selection Information
    DESCRIPTION: This testcase verifies RacingPost
    DESCRIPTION: Description and selection Information
    PRECONDITIONS: User should have CMS access
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - Racingpost info should be displayed.
    """
    keep_browser_open = True
    win_or_each_way_tab = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get Greyhound Race Event
        """
        racing_datahub_status = self.get_initial_data_system_configuration().get('RacingDataHub')["isEnabledForGreyhound"]
        if not racing_datahub_status:
            self.cms_config.update_system_configuration_structure(config_item='RacingDataHub',
                                                                  field_name='isEnabledForGreyhound',
                                                                  field_value=True)
        params = self.get_event_details(racing_post_pick=True)
        self.__class__.event_id = params.event_id
        self.__class__.outcomes_info = params.outcomes_info
        self.__class__.data_fabric_data = params.datafabric_data

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        # Covered in step test_003

    def test_002_go_to_the_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to the Greyhounds landing page
        EXPECTED: Greyhounds landing page is opened
        """
        # Covered in step test_003

    def test_003_select_event_with_racingpost_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with RacingPost available and go to its details page
        EXPECTED: Event details page is opened
        EXPECTED: * 'Win or E/W' market is selected by default
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='greyhound-racing')
        markets_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list
        if markets_tabs.current != vec.racing.RACING_EDP_MARKET_TABS.win_or_ew:
            markets_tabs.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
            self.site.wait_content_state_changed(timeout=5)

    def test_004_go_to_selection_area_and_verify_for_the_description_of_the_event(self):
        """
        DESCRIPTION: Go to selection area and verify for the description of the event
        EXPECTED: event Selection/description area consists of:
        EXPECTED: * Silk with different colors (for different track and dog identification)
        EXPECTED: * Dog Names
        EXPECTED: * Trainer Details
        EXPECTED: * Dog Form for? last 5 races result
        EXPECTED: * Show more button
        EXPECTED: * and Odds.
        """
        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        self.__class__.outcomes = market.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='Market does not have any items')
        for outcome_name, outcome in list(self.outcomes.items())[:4] if len(self.outcomes) > 4 else self.outcomes.items():
            outcome.scroll_to()
            if 'Unnamed' not in outcome_name and not outcome.is_non_runner:
                self.assertTrue(outcome.has_silks, msg=f'No runner number found for "{outcome_name}"')
                timeform_outcome_info = next((list(outcome_info.values())[0] for outcome_info in self.outcomes_info
                                              if list(outcome_info.keys())[0] in outcome_name), None)

                self.assertTrue(timeform_outcome_info, msg=f'Outcome info not found for "{outcome_name}"')
                trainer_name = timeform_outcome_info.get('trainerName', '')
                if self.brand == 'ladbrokes' and self.device_type == 'mobile':
                    actual_trainer_name = outcome.jockey_trainer_info.split(':')[1].lstrip()
                    self.assertEqual(actual_trainer_name, trainer_name,
                                    msg=f'Actual Trainer name "{actual_trainer_name}" '
                                        f'is not the same as expected "{trainer_name}"')
                    trainer_label = outcome.trainer_label
                else:
                    self.assertEqual(outcome.trainer_name.text, trainer_name,
                                    msg=f'Trainer name "{outcome.trainer_name.text}" '
                                        f'is not the same as expected "{trainer_name}"')
                    trainer_label = outcome.trainer_label.text.split(':')[0]
                self.assertEqual(trainer_label, vec.racing.TRAINER,
                                 msg=f'Label "{trainer_label}" '
                                     f'is not the same as expected "{vec.racing.TRAINER}"')
                self.assertTrue(outcome.has_show_summary_toggle(),
                                msg=f'No summary toggle found for selection "{outcome_name}"')
                self.assertFalse(outcome.has_expanded_summary(expected_result=False),
                                 msg=f'Summary is not collapsed by default for selection "{outcome_name}"')
                self.assertTrue(outcome.bet_button.is_displayed(),
                                msg=f'Odds for selection "{outcome_name}" is not displayed')

    def test_005_verify_trainer_name_correctness(self):
        """
        DESCRIPTION: Verify trainer name correctness
        EXPECTED: Trainer name corresponds to **trainerName** attribute from RacingPost microservice response
        """
        trainer_names = [data_fabric_info['trainerName'] for data_fabric_info in self.data_fabric_data['runners'] if data_fabric_info['dogName'] and 'rating' in data_fabric_info]
        trainer_names_ui = []
        for outcome_name, outcome in self.outcomes.items():
            if 'Unnamed' not in outcome_name and 'N/R' not in outcome_name:
                if self.brand == 'ladbrokes' and self.device_type == 'mobile':
                    actual_trainer_name = outcome.jockey_trainer_info.split(':')[1].lstrip()
                    trainer_names_ui.append(actual_trainer_name)
                else:
                    trainer_names_ui.append(outcome.trainer_name.text)
        self.assertListEqual(sorted(trainer_names_ui), sorted(trainer_names),
                             msg=f'Trainer names in timeform response "{sorted(trainer_names)}" '
                                 f'are not the same as on UI "{sorted(trainer_names_ui)}"')

    def test_006_verify_form_value_correctness(self):
        """
        DESCRIPTION: Verify form value correctness
        EXPECTED: Form value corresponds to **last5Runs** attribute from RacingPost microservice response
        """
        last_5runs = [data_fabric_info['last5Runs'] for data_fabric_info in self.data_fabric_data['runners'] if data_fabric_info['dogName'] and 'rating' in data_fabric_info]
        last_5runs_ui = []
        for outcome_name, outcome in self.outcomes.items():
            if 'Unnamed' not in outcome_name and 'N/R' not in outcome_name:
                if self.brand == 'ladbrokes' and self.device_type == 'mobile':
                    last_5runs_ui.append(outcome.form_value)
                else:
                    last_5runs_ui.append(outcome.form_value.text)
        self.assertListEqual(sorted(last_5runs), sorted(last_5runs_ui),
                             msg=f'Trainer names in timeform response "{sorted(last_5runs)}" '
                                 f'are not the same as on UI "{sorted(last_5runs_ui)}"')

    def test_007_verify_user_can_made_selections(self):
        """
        DESCRIPTION: Verify user can made selections
        EXPECTED: User should be able to made selections.
        """
        list(self.outcomes.values())[0].bet_button.click()
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True), msg='Quick Bet is not present so selection got not selected')
            self.site.quick_bet_panel.header.close_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick bet not closed')

        else:
            self.assertTrue(list(self.outcomes.values())[0].bet_button.is_selected(), msg='selection is not selected')

    def test_008_verify_non_runner_selection_within_racingpost_summary_information(self):
        """
        DESCRIPTION: Verify Non-runner selection within RacingPost Summary Information
        EXPECTED: Non-runner selection is NOT included in RacingPost Summary Information
        """
        for outcome_name, outcome in list(self.outcomes.items()):
            outcome.scroll_to()
            if 'N/R' in outcome_name:
                self.assertTrue(outcome.odds_button.get_attribute('disabled'), msg='Non-runner selection should be disabled')
