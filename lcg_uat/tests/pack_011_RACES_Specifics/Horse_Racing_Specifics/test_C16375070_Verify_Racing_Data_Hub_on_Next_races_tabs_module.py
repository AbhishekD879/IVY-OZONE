import pytest
from tests.base_test import vtest
from time import sleep
from voltron.environments import constants as vec
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import do_request
from json import JSONDecodeError


# @pytest.mark.tst2  #Can't get feed for test envts
# @pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C16375070_Verify_Racing_Data_Hub_on_Next_races_tabs_module(BaseUKTote, BaseRacing):
    """
    TR_ID: C16375070
    NAME: Verify Racing Data Hub on Next races tabs/module
    DESCRIPTION: This test case verifies receiving and displaying data from Racing Post API on Next races tabs/modules
    DESCRIPTION: NOTE: Next races tab on HR Landing page available only for Ladbrokes brand
    PRECONDITIONS: - In CMS: Horse Racing (HR) Racing Data Hub toggle is turned on : System-configuration > RacingDataHub > isEnabledForHorseRacing = true
    PRECONDITIONS: - At least one Horse Racing Event from Next Races tab is mapped with DF API data (Racing Post)
    PRECONDITIONS: - List of Aggregation MS environments: https://confluence.egalacoral.com/display/SPI/Aggregation+Java
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get Horse Racing Event
        """
        event_info = self.get_event_details(datafabric_data=True, race_form_info=True, df_event_summary=True)
        self.__class__.event_id = event_info.event_id

    def test_001_open_oxygenladbrokes_app(self):
        """
        DESCRIPTION: Open Oxygen/Ladbrokes app
        EXPECTED:
        """
        self.site.wait_content_state('HomePage')

    def test_002_for_mobile_open_homepage__next_races_tabfor_desktop_open_homepage_and_check_presence_of_next_races_module(
            self):
        """
        DESCRIPTION: [For mobile]: Open Homepage > 'Next races' tab
        DESCRIPTION: [For desktop]: Open Homepage and check presence of 'Next races' module
        EXPECTED: 'Next races' tab/module is displayed
        """
        if self.device_type == 'mobile':
            next_races = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races)
            sleep(3)
            self.site.home.module_selection_ribbon.tab_menu.click_button(next_races)
        if self.brand == 'Ladbrokes':
            current_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEquals(current_tab, vec.racing.RACING_NEXT_RACES_NAME,
                              msg=f'Actual tab opened: "{current_tab}" is not equal to '
                                  f'Expected tab: "{vec.racing.RACING_NEXT_RACES_NAME}"')

    def test_003_check_the_correct_displaying_of_the_information_for_the_event_which_is_mapped_with_df_api_data_racing_post(
            self):
        """
        DESCRIPTION: Check the correct displaying of the information for the event which is mapped with DF API data (Racing Post)
        EXPECTED: Information is available and displayed (data for Jockey Name, Trainer Name, Silks, Runner Number(saddle), Draw, Form is present)
        EXPECTED: ![](index.php?/attachments/get/34237)
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.site.wait_content_state_changed()
        tab_names = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_names
        win_ew_tab_name = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
        self.assertIn(win_ew_tab_name, tab_names,
                      msg=f'Win each way tab "{win_ew_tab_name}" is not in the '
                          f'as tabs "{tab_names}"')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)

        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = markets.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        outcomes = market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found')

        for outcome_name, outcome in outcomes.items():
            outcome.scroll_to()
            if not('Unnamed' in outcome_name and 'Non Runner'in outcome_name  and 'generic'in outcome_name) and not('' is outcome.jockey_trainer_info or 'Non-Runner' is outcome.jockey_trainer_info):
                horse_info = self.get_horse_info_from_datafabric(event_id=self.event_id,
                                                                 horse_name=outcome_name)
                if horse_info.get('jockey'):
                    jockey = vec.racing.JOCKEY_TEXT.format(jockey=horse_info['jockey'])
                    self.assertEqual(jockey, outcome.jockey_name.split('(')[0].strip(),
                                     msg=f'Jockey name "{jockey}" for outcome "{outcome_name}" '
                                         f'is not the same as expected "{outcome.jockey_name.split("(")[0].strip()}"')
                else:
                    jockey = None
                    self._logger.warning(f'*** No jockey for outcome "{outcome_name}" available')

                if horse_info.get('trainer'):
                    trainer = vec.racing.TRAINER_TEXT.format(trainer=horse_info['trainer'])
                    self.assertEqual(trainer, outcome.trainer_name,
                                     msg=f'Trainer name "{trainer}" for outcome "{outcome_name}" '
                                         f'is not the same as expected "{outcome.trainer_name}"')
                else:
                    trainer = None
                    self._logger.warning(f'*** No trainer for outcome "{outcome_name}" available')

                if jockey and trainer:
                    expected_jockey_trainer = vec.racing.JOCKEY_TRAINER_TEXT.format(jockey=horse_info['jockey'],
                                                                                    trainer=horse_info['trainer'])
                    self.assertEqual(outcome.jockey_name.split('(')[0].strip() + ' / ' + outcome.trainer_name, expected_jockey_trainer,
                                     msg=f'Jockey/trainer info "{outcome.jockey_name.split("(")[0].rstrip() + "/" + outcome.trainer_name}" is not the '
                                         f'same as expected "{expected_jockey_trainer}"')
                else:
                    self._logger.warning(f'*** No jockey or trainer for outcome "{outcome_name}" available')

                if horse_info.get('draw'):
                    draw_number = horse_info['draw']
                    self.assertEqual(draw_number, outcome.draw_number,
                                     msg=f'Draw number "{draw_number}" for outcome "{outcome_name}" '
                                         f'is not the same as expected "{outcome.draw_number}"')
                else:
                    self._logger.warning(f'*** No draw number for outcome "{outcome_name}" available')

                if horse_info.get('form'):
                    form = f'Form: {horse_info["formfigs"]}'
                    self.assertEqual(form, outcome.form,
                                     msg=f'Form "{form}" for outcome "{outcome_name}" '
                                         f'is not the same as expected "{outcome.form}"')
                else:
                    self._logger.info(f'*** No form for outcome "{outcome_name}" available')

    def test_004_check_that_data_for_the_race_is_taken_from_aggregation_ms_jockey_name_trainer_name_silks_runner_number_draw_form(
            self):
        """
        DESCRIPTION: Check that data for the race is taken from Aggregation MS (Jockey Name, Trainer Name, Silks, Runner Number, Draw, Form)
        EXPECTED: Displayed data is received from Racing Data Hub in response:
        EXPECTED: e.g. https://ld-prd1.api.datafabric.prod.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/228859733,228864955,228859734,228863900,228865712,228859736/content?locale=en-GB&api-key=LDc7c2ede219f84f95b81f3e87e2800a3c
        """
        actual_url = self.get_response_url('/sportsbook-api/categories')
        response = do_request(method='GET', url=actual_url)
        for event in response["document"]:
            event = response["document"].get(event)
            self.assertTrue(event["horses"], msg="horses attribute is not displayed")
            self.assertTrue(event["raceNo"], msg="raceNo attribute is not displayed")
            for horse_details in event["horses"]:
                self.assertTrue(horse_details["saddle"],
                                msg="saddle attribute is not displayed in "f'{horse_details} {horse_details.keys()}')
                self.assertTrue(horse_details["silk"],
                                msg="silk attribute is not displayed in "f'{horse_details} {horse_details.keys()}')
                self.assertTrue(horse_details["trainer"],
                                msg="trainer attribute is not displayed in "f'{horse_details} {horse_details.keys()}')
                if "draw" in horse_details.keys():
                    self.assertIn("draw", horse_details.keys(),
                                  msg="draw number attribute is not displayed in "f'{horse_details} {horse_details.keys()}')
                if "jockey" not in horse_details.keys():
                    for form in horse_details["form"]:
                        self.assertTrue(form["jockey"],
                                        msg="jockey attribute is not displayed in "f'{form} {form.keys()}')
                else:
                    self.assertIn("jockey", horse_details.keys(),
                                  msg="jockey attribute is not displayed in "f'{horse_details} {horse_details.keys()}')
                self.assertTrue(horse_details["horseName"],
                                msg="horseName attribute is not displayed in "f'{horse_details} {horse_details.keys()}')

    def test_005_repeat_steps_3_4_for_next_races_module_on_hr_landing_page(self):
        """
        DESCRIPTION: Repeat steps 3-4 for Next races module on HR Landing page
        EXPECTED: Results are the same
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')
        if self.brand == 'ladbrokes':
            next_races_tab = self.site.horse_racing.tabs_menu.click_button(
                button_name=vec.racing.RACING_NEXT_RACES_NAME)
            self.assertTrue(next_races_tab,
                            msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')
        else:
            next_races = self.get_next_races_section()
            self.__class__.sections = next_races.items_as_ordered_dict
        self.test_003_check_the_correct_displaying_of_the_information_for_the_event_which_is_mapped_with_df_api_data_racing_post()
        self.test_004_check_that_data_for_the_race_is_taken_from_aggregation_ms_jockey_name_trainer_name_silks_runner_number_draw_form()

    def test_006_for_ladbrokes_brand_only_repeat_steps_3_4_for_next_races_tab_on_hr_landing_page(self):
        """
        DESCRIPTION: [For Ladbrokes brand only]: Repeat steps 3-4 for Next races tab on HR Landing page
        EXPECTED: Results are the same
        """
    # Covered in above step
