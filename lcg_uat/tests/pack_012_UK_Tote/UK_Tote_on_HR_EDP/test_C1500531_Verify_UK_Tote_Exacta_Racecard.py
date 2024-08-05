import pytest
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.siteserve_client import racing_form
from tests.base_test import vtest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.uk_tote
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.liveserv_updates
@pytest.mark.races
@vtest
class Test_C1500531_Verify_UK_Tote_Exacta_Racecard(BaseUKTote):
    """
    TR_ID: C1500531
    NAME: Verify UK Tote Exacta Racecard
    DESCRIPTION: This test case verifies the racecard of Exacta pool type of UK Tote
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * The horse racing event should have Exacta markets available
    """
    keep_browser_open = True
    outcomes = []
    racing_form_available = None
    uk_tote_pool_event_id = None
    uk_tote_pool_selection_id = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        ob_config = cls.get_ob_config()
        if cls.uk_tote_pool_selection_id:
            ob_config.change_selection_state(selection_id=cls.uk_tote_pool_selection_id, displayed=True, active=True)

        if cls.eventID:
            ob_config.change_event_state(event_id=cls.eventID, displayed=True, active=True)

    def test_000_find_event_and_navigate_to_horseracing_edp(self):
        """
        DESCRIPTION: Find event with UK Tote Exacta pool available
        DESCRIPTION: Navigate to EPD of selected event
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.eventID = event.event_id
        query = self.ss_query_builder.add_filter(racing_form(LEVELS.EVENT)).add_filter(racing_form(LEVELS.OUTCOME))
        event_to_outcome_for_event = self.ss_req.ss_event_to_outcome_for_event(event_id=event.event_id,
                                                                               query_builder=query)
        self.__class__.racing_form_available = next((True for form in event_to_outcome_for_event
                                                     if 'racingFormOutcome' in form.keys()), False)

        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='UK Tote tab is not opened')

        self.__class__.expected_fixture_headers = ['1ST', '2ND', 'ANY'] if self.brand == 'bma' else ['1st', '2nd', 'ANY']

    def test_001_select_exacta_tab(self):
        """
        DESCRIPTION: Select "Exacta" tab
        EXPECTED: "Exacta" tab is selected
        EXPECTED: Exacta racecard is shown
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        exacta_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.exacta)
        self.assertTrue(exacta_opened, msg='Exacta tab is not opened')
        self.__class__.pool = section.pool

    def test_002_verify_exacta_racecard_for_an_active_event(self):
        """
        DESCRIPTION: Verify Exacta racecard for an **active** event
        EXPECTED: Exacta racecard consists of:
        EXPECTED: Current pool value (only shown if available)
        EXPECTED: "What is Exacta?" clickable link
        EXPECTED: Runner number, name and information for each runner
        EXPECTED: Runner silks (if available) for each runner
        EXPECTED: "1st", "2nd", and "Any" check boxes for each runner (all active by default)
        """
        fixture_headers = self.pool.section_header.items_as_ordered_dict
        self.assertTrue(fixture_headers, msg='No Fixture headers found')
        self.assertListEqual(self.expected_fixture_headers, list(fixture_headers.keys()))

        self.__class__.outcomes = list(self.pool.items_as_ordered_dict.items())
        self.assertTrue(self.outcomes, msg='No outcomes found')
        for outcome_name, outcome in self.outcomes:
            self.assertTrue(outcome.runner_number, msg='No outcome number found for "%s"' % outcome_name)
            self.assertTrue(outcome.has_silks, msg=f'Silks are not available for "{outcome_name}"')
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            self.assertEqual(len(checkboxes), 3,
                             msg='Should be present 3 checkboxes but "%s" are found for "%s"'
                                 % (len(checkboxes), outcome_name))
            for checkbox_name, checkbox in checkboxes.items():
                if not checkbox.non_runner:
                    self.assertTrue(checkbox.is_enabled(), msg='Checkbox "%s" is not enabled for "%s"'
                                                               % (checkbox_name, outcome_name))

    def test_003_click_on_spotlight_and_form_options_under_individual_selections(self):
        """
        DESCRIPTION: Click on spotlight and form options under individual selections
        EXPECTED: The spotlight and form information under the selection are shown to the user
        """
        if self.racing_form_available:
            outcome_name, outcome = self.outcomes[0]
            outcome.show_summary_toggle.click()
            self.assertTrue(outcome.has_spotlight_overview(),
                            msg='Outcome: "%s" spotlight overview was not expanded' % outcome_name)

    def test_004_select_the_1st_check_box_for_any_runner(self):
        """
        DESCRIPTION: Select the **"1st"** check box for any runner
        EXPECTED: The check box is selected
        EXPECTED: All other "1st" check boxes are disabled
        EXPECTED: "2nd" check box **for this runner** is disabled
        EXPECTED: All "Any" check boxes on the racecard are disabled as well
        """
        outcome_name, outcome = self.outcomes[0]
        checkboxes = outcome.items_as_ordered_dict
        self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
        checkbox_name, checkbox = list(checkboxes.items())[0]
        checkbox.click()
        self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                    % (checkbox_name, outcome_name))

        checkbox_name, checkbox = list(checkboxes.items())[1]
        self.assertFalse(checkbox.is_enabled(expected_result=False), msg='Checkbox "%s" is not disabled for "%s"'
                                                                         % (checkbox_name, outcome_name))

        checkbox_name, checkbox = list(checkboxes.items())[2]
        self.assertFalse(checkbox.is_enabled(expected_result=False), msg='Checkbox "%s" is not disabled for "%s"'
                                                                         % (checkbox_name, outcome_name))

        for outcome_name, outcome in self.outcomes[1:]:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[0]
            self.assertFalse(checkbox.is_enabled(expected_result=False), msg='Checkbox "%s" is not disabled for "%s"'
                                                                             % (checkbox_name, outcome_name))

            checkbox_name, checkbox = list(checkboxes.items())[1]
            self.assertTrue(checkbox.is_enabled(), msg='Checkbox "%s" is not enabled for "%s"'
                                                       % (checkbox_name, outcome_name))

            checkbox_name, checkbox = list(checkboxes.items())[2]
            self.assertFalse(checkbox.is_enabled(expected_result=False), msg='Checkbox "%s" is not disabled for "%s"'
                                                                             % (checkbox_name, outcome_name))

    def test_005_uncheck_the_1st_check_box_and_select_the_2nd_check_box_for_any_runner(self):
        """
        DESCRIPTION: Uncheck the "1st" check box and select the **"2nd"** check box for any runner
        EXPECTED: The check box is selected
        EXPECTED: All other "2nd" check boxes are disabled
        EXPECTED: "1st" check box **for this runner** is disabled
        EXPECTED: All "Any" check boxes on the racecard are disabled as well
        """
        outcome_name, outcome = self.outcomes[0]
        checkboxes = outcome.items_as_ordered_dict
        self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
        checkbox_name, checkbox = list(checkboxes.items())[0]
        checkbox.click()
        self.assertFalse(checkbox.is_selected(expected_result=False),
                         msg='Checkbox "%s" is selected for "%s" after click' % (checkbox_name, outcome_name))

        outcome_name, outcome = self.outcomes[1]
        checkboxes = outcome.items_as_ordered_dict
        self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
        checkbox_name, checkbox = list(checkboxes.items())[1]
        checkbox.click()
        self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                    % (checkbox_name, outcome_name))

        checkbox_name, checkbox = list(checkboxes.items())[2]
        self.assertFalse(checkbox.is_enabled(expected_result=False), msg='Checkbox "%s" is not disabled for "%s"'
                                                                         % (checkbox_name, outcome_name))

        outcomes = dict(self.outcomes)
        outcomes.pop(outcome_name)

        for outcome_name, outcome in outcomes.items():
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[0]
            self.assertTrue(checkbox.is_enabled(), msg='Checkbox "%s" is not enabled for "%s"'
                                                       % (checkbox_name, outcome_name))

            checkbox_name, checkbox = list(checkboxes.items())[1]
            self.assertFalse(checkbox.is_enabled(expected_result=False), msg='Checkbox "%s" is not disabled for "%s"'
                                                                             % (checkbox_name, outcome_name))

            checkbox_name, checkbox = list(checkboxes.items())[2]
            self.assertFalse(checkbox.is_enabled(expected_result=False), msg='Checkbox "%s" is not disabled for "%s"'
                                                                             % (checkbox_name, outcome_name))

    def test_006_select_the_1st_and_2nd_check_boxes_together_for_any_runners(self):
        """
        DESCRIPTION: Select the **"1st"**  and **"2nd"** check boxes together for any runners
        EXPECTED: The check boxes are selected
        EXPECTED: All other check boxes on the racecard are disabled
        """
        outcome_name, outcome = self.outcomes[0]
        checkboxes = outcome.items_as_ordered_dict
        self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
        checkbox_name, checkbox = list(checkboxes.items())[0]
        checkbox.click()
        self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                    % (checkbox_name, outcome_name))

        checkbox_name, checkbox = list(checkboxes.items())[1]
        self.assertFalse(checkbox.is_enabled(expected_result=False), msg='Checkbox "%s" is not disabled for "%s"'
                                                                         % (checkbox_name, outcome_name))

        checkbox_name, checkbox = list(checkboxes.items())[2]
        self.assertFalse(checkbox.is_enabled(expected_result=False), msg='Checkbox "%s" is not disabled for "%s"'
                                                                         % (checkbox_name, outcome_name))

        for outcome_name, outcome in self.outcomes[2:]:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            for checkbox_name, checkbox in checkboxes.items():
                self.assertFalse(checkbox.is_enabled(expected_result=False),
                                 msg='Checkbox "%s" is not disabled for "%s"' % (checkbox_name, outcome_name))

    def test_007_uncheck_the_1st_and_2nd_check_boxes(self):
        """
        DESCRIPTION: Uncheck the **"1st"** and **"2nd"** check boxes
        EXPECTED: All check boxes are active again
        """
        outcome_name, outcome = self.outcomes[0]
        checkboxes = outcome.items_as_ordered_dict
        self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
        checkbox_name, checkbox = list(checkboxes.items())[0]
        checkbox.click()
        self.assertFalse(checkbox.is_selected(expected_result=False),
                         msg='Checkbox "%s" is selected for "%s" after click' % (checkbox_name, outcome_name))

        outcome_name, outcome = self.outcomes[1]
        checkboxes = outcome.items_as_ordered_dict
        self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
        checkbox_name, checkbox = list(checkboxes.items())[1]
        checkbox.click()
        self.assertFalse(checkbox.is_selected(expected_result=False),
                         msg='Checkbox "%s" is selected for "%s" after click' % (checkbox_name, outcome_name))

        for outcome_name, outcome in self.outcomes:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            for checkbox_name, checkbox in checkboxes.items():
                self.assertTrue(checkbox.is_enabled(), msg='Checkbox "%s" is not enabled for "%s"'
                                                           % (checkbox_name, outcome_name))

    def test_008_select_any_check_box_for_any_runner(self):
        """
        DESCRIPTION: Select **"Any"** check box for any runner
        EXPECTED: Check box is selected
        EXPECTED: All "1st" and "2nd" check boxes are disabled
        EXPECTED: Others "Any" check boxes on the racecard are enabled
        """
        outcome_name, outcome = self.outcomes[0]
        checkboxes = outcome.items_as_ordered_dict
        self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
        checkbox_name, checkbox = list(checkboxes.items())[2]
        checkbox.click()
        self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                    % (checkbox_name, outcome_name))

        for outcome_name, outcome in self.outcomes:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            for checkbox_name, checkbox in list(checkboxes.items())[:2]:
                self.assertFalse(checkbox.is_enabled(expected_result=False),
                                 msg='Checkbox "%s" is not disabled for "%s"' % (checkbox_name, outcome_name))
            checkbox_name, checkbox = list(checkboxes.items())[2]
            self.assertTrue(checkbox.is_enabled(),
                            msg='Checkbox "%s" is not enabled for "%s"' % (checkbox_name, outcome_name))

    def test_009_select_any_check_boxes_for_2_3_more_runners(self):
        """
        DESCRIPTION: Select **"Any"** check boxes for 2-3 more runners
        EXPECTED: User is able to select "Any" check boxes for multiple runners
        EXPECTED: All "1st" and "2nd" check boxes are still disabled
        """
        for outcome_name, outcome in self.outcomes[1:3]:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[2]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                        % (checkbox_name, outcome_name))

        for outcome_name, outcome in self.outcomes:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            for checkbox_name, checkbox in list(checkboxes.items())[:2]:
                self.assertFalse(checkbox.is_enabled(expected_result=False),
                                 msg='Checkbox "%s" is not disabled for "%s"' % (checkbox_name, outcome_name))

        for outcome_name, outcome in self.outcomes[:3]:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[2]
            checkbox.click()
            self.assertFalse(checkbox.is_selected(expected_result=False),
                             msg='Checkbox "%s" is not deselected for "%s" after click' % (checkbox_name, outcome_name))

    def test_010_verify_exacta_racecard_with_a_suspended_selection(self):
        """
        DESCRIPTION: Verify Exacta racecard with a **suspended selection**
        EXPECTED: All check boxes for suspended selection are disabled
        EXPECTED: All check boxes for active selections are active
        """
        ss_uk_tote_pool = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.eventID,
            query_builder=self.ss_query_builder)
        ss_uk_tote_pool_outcomes = ss_uk_tote_pool[0]['event']['children'][0]['market']['children']
        selection_id, outcome_name = next(((outcome['outcome']['id'], outcome['outcome']['name']) for outcome in ss_uk_tote_pool_outcomes
                                           if 'Unnamed' not in outcome['outcome']['name']), (None, None))
        self.assertTrue(selection_id, msg='Cannot get selection id from SS response')
        self.__class__.uk_tote_pool_selection_id = selection_id
        self.ob_config.change_selection_state(selection_id=selection_id, displayed=True)

        outcome = next((outcome for name, outcome in self.outcomes if name == outcome_name), None)
        self.assertTrue(outcome, msg='Cannot find outcome with name "%s"' % outcome_name)
        checkboxes = outcome.items_as_ordered_dict
        self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
        for checkbox_name, checkbox in checkboxes.items():
            self.assertFalse(checkbox.is_enabled(expected_result=False, timeout=10),
                             msg='Checkbox "%s" is not disabled for "%s"' % (checkbox_name, outcome_name))

        outcomes = dict(self.outcomes)
        outcomes.pop(outcome_name)
        for outcome_name, outcome in outcomes.items():
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            for checkbox_name, checkbox in checkboxes.items():
                self.assertTrue(checkbox.is_enabled(),
                                msg='Checkbox "%s" is not enabled for "%s"' % (checkbox_name, outcome_name))

    def test_011_verify_case_when_the_event_changes_from_active_to_suspended_while_the_user_is_on_the_page(self):
        """
        DESCRIPTION: Verify case when the event changes from active to suspended while the user is on the page
        EXPECTED: The event changes to suspended in real time
        EXPECTED: All check boxes become disabled in real time
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True)
        for outcome_name, outcome in self.outcomes:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            for checkbox_name, checkbox in checkboxes.items():
                self.assertFalse(checkbox.is_enabled(expected_result=False, timeout=5),
                                 msg='Checkbox "%s" is not disabled for "%s"' % (checkbox_name, outcome_name))

    def test_012_verify_case_when_the_event_changes_from_suspended_to_active_while_the_user_is_on_the_page(self):
        """
        DESCRIPTION: Verify case when the event changes from suspended to active while the user is on the page
        EXPECTED: The event changes to active in real time
        EXPECTED: All check boxes become active in real time
        """
        self.ob_config.change_selection_state(selection_id=self.uk_tote_pool_selection_id, displayed=True, active=True)
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        for outcome_name, outcome in self.outcomes:
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            for checkbox_name, checkbox in checkboxes.items():
                self.assertTrue(checkbox.is_enabled(timeout=10),
                                msg='Checkbox "%s" is not enabled for "%s"' % (checkbox_name, outcome_name))
