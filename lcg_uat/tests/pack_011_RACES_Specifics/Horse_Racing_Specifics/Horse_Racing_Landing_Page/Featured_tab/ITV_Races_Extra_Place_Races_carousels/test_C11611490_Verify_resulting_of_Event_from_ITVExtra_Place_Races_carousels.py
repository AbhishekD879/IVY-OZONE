import pytest
from time import sleep

from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # event creation
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.mobile_only  # applicable for tablet as well
@pytest.mark.medium
@pytest.mark.safari
@vtest
class Test_C11611490_Verify_resulting_of_Event_from_ITVExtra_Place_Races_carousels(BaseRacing):
    """
    TR_ID: C11611490
    VOL_ID: C11809206
    NAME: Verify resulting of Event from ITV/Extra Place Races carousels
    DESCRIPTION: This test case verifies resulting of Event from ITV/Extra Place Races carousels
    PRECONDITIONS: 1. ITV/Extra Place Races feature toggle should be set to "ON" (CMS->System configuration->Structure->featuredRaces)
    PRECONDITIONS: 2. There should be few Horse Racing events configured with 'Featured Racing Types'(ITV races), 'Extra Place Race'  and with both flags checked in TI.
    PRECONDITIONS: 3. Go to oxygen application and navigate to Featured tab on Horse Racing page.
    PRECONDITIONS: <Module name> - "Offers and Extra place" (Ladbrokes), "Enhanced Races" (Coral)
    PRECONDITIONS: Design for both Brands can be found here: https://jira.egalacoral.com/browse/BMA-35023
    PRECONDITIONS: 'Featured race'(ITV races) - is checked on event level
    PRECONDITIONS: 'Extra Place Race' flag - is checked on market level
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event with enabled 'Featured Racing Types' check box on event level (drilldownTagNames="EVFLAG_FRT") and races should be from different types
        DESCRIPTION: Create event with enabled 'Extra Place Race' check box on market level (drilldownTagNames="MKTFLAG_EPR") and races should be from different types
        DESCRIPTION: Open Horse Racing landing page
        """
        itv_event = self.ob_config.add_UK_racing_event(time_to_start=7, featured_racing_types=True, number_of_runners=1)
        self.__class__.itv_eventID = itv_event.event_id
        self.__class__.itv_event_marketID = itv_event.market_id
        self.__class__.itv_event_selectionID = list(itv_event.selection_ids.values())[0]
        itv_event_name = f'{itv_event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.itv_event_name = itv_event_name[:10] if self.brand == 'ladbrokes' else itv_event_name

        extra_place_event = self.ob_config.add_UK_racing_event(time_to_start=12, market_extra_place_race=True,
                                                               number_of_runners=1)
        self.__class__.extra_eventID = extra_place_event.event_id
        self.__class__.extra_event_marketID = extra_place_event.market_id
        self.__class__.extra_event_selectionID = list(extra_place_event.selection_ids.values())[0]
        extra_event_name = f'{extra_place_event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.extra_event_name = extra_event_name[:10] if self.brand == 'ladbrokes' else extra_event_name

        combined_event = self.ob_config.add_UK_racing_event(time_to_start=17, featured_racing_types=True,
                                                            number_of_runners=1)
        self.__class__.combined_eventID = combined_event.event_id
        self.__class__.combined_event_marketID = combined_event.market_id
        self.__class__.combined_event_selectionID = list(combined_event.selection_ids.values())[0]
        self.ob_config.change_racing_promotion_state(promotion_name='extra_place_race',
                                                     level='market',
                                                     market_id=self.ob_config.market_ids[self.combined_eventID],
                                                     event_id=self.combined_eventID)

        combined_event_name = f'{combined_event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.combined_event_name = combined_event_name[:10] if self.brand == 'ladbrokes' else combined_event_name

        self.__class__.created_itv_events = [self.itv_event_name, self.combined_event_name]
        self.__class__.created_extra_place_events = [self.extra_event_name, self.combined_event_name]

        self.navigate_to_page(name='horse-racing/featured')
        self.site.wait_content_state('Horseracing')

    def test_001_verify_displaying_of__itv_and_extra_place_races_carousels(self):
        """
        DESCRIPTION: Verify displaying of ITV and Extra Place Races carousels
        EXPECTED: * ITV and Extra Place Races carousels are displayed on Horse Racing Featured tab
        EXPECTED: * Events from preconditions are displayed in the related carousels.
        """
        self.__class__.sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found')
        self.assertIn(self.enhanced_races_name, self.sections,
                      msg=f'Cannot find "{self.enhanced_races_name}" module section')
        self.__class__.enhanced_races_section = self.sections[self.enhanced_races_name]

        self.assertTrue(self.enhanced_races_section.has_itv_module(),
                        msg=f'"{self.enhanced_races_name}" module section '
                            f'does not contain "{vec.racing.ITV}" carousel')

        self.assertTrue(self.enhanced_races_section.has_extra_place_module(),
                        msg=f'"{self.enhanced_races_name}" module section '
                            f'does not contain "{vec.racing.EXTRA_PLACE_TITLE}" carousel')

        itv_module_events = self.enhanced_races_section.itv_module.items_as_ordered_dict
        self.assertTrue(itv_module_events,
                        msg=f'There are no events in "{vec.racing.ITV}" module')
        for event in self.created_itv_events:
            self.assertIn(event, itv_module_events.keys(),
                          msg=f'"{event}" cannot be found in "{list(itv_module_events.keys())}"')

        extra_place_module_events = self.enhanced_races_section.extra_place_offer_module.items_as_ordered_dict
        self.assertTrue(extra_place_module_events,
                        msg=f'There are no events in "{vec.racing.EXTRA_PLACE_TITLE}" module')
        for event in self.created_extra_place_events:
            self.assertIn(event, extra_place_module_events.keys(),
                          msg=f'"{event}" cannot be found in "{list(extra_place_module_events.keys())}"')

    def test_002_in_ti_select_event_from_preconditions_with_featured_racing_types_flag_set_results_for_it(self):
        """
        DESCRIPTION: In TI select event from preconditions with 'Featured Racing Types' flag and set results for it
        """
        self.result_event(event_id=self.itv_eventID,
                          market_id=self.itv_event_marketID,
                          selection_ids=self.itv_event_selectionID)

    def test_003_go_to_oxygen_application_and_navigate_to_featured_tab_on_horse_racing_page(self):
        """
        DESCRIPTION: Go to oxygen application and navigate to Featured tab on Horse Racing page.
        DESCRIPTION: Verify that resulted events are removed from module automatically
        EXPECTED: * Resulted event with 'Featured Racing Types' flag is removed from ITV carousel by live update
        EXPECTED: * Resulted event with 'Extra Place Race' flag is removed from Extra Place Races carousel by live update
        EXPECTED: * Resulted event with both 'Featured Racing Types' and ''Extra Place Race' flags is removed from both carousels by live update.
        EXPECTED: * Not resulted events are still displayed in ITV and Extra place
        """
        self.assertTrue(self.sections, msg='No sections found')
        self.assertIn(self.enhanced_races_name, self.sections,
                      msg=f'Cannot find "{self.enhanced_races_name}" module section')

        itv_module_events = self.sections[self.enhanced_races_name].itv_module.items_as_ordered_dict
        self.assertNotIn(self.itv_event_name, itv_module_events.keys(),
                         msg=f'"{self.itv_event_name}" can be found among "{list(itv_module_events.keys())}" events '
                             f'in "{vec.racing.ITV}" module. It should not.')

    def test_004_in_ti_select_event_from_preconditions_with_extra_place_race_flag_and_set_results_for_it(self):
        """
        DESCRIPTION: In TI select event from preconditions with 'Extra Place Race' and set results for it
        """
        self.ob_config.result_selection(selection_id=self.extra_event_selectionID,
                                        market_id=self.extra_event_marketID,
                                        event_id=self.extra_eventID)
        self.ob_config.confirm_result(selection_id=self.extra_event_selectionID, market_id=self.extra_event_marketID,
                                      event_id=self.extra_eventID)

    def test_005_go_to_oxygen_application_and_navigate_to_featured_tab_on_horse_racing_page(self):
        """
        DESCRIPTION: Go to oxygen application and navigate to Featured tab on Horse Racing page.
        DESCRIPTION: Verify that resulted event is removed from module automatically
        EXPECTED: * Resulted event with 'Featured Racing Types' flag is removed from ITV carousel by live update
        EXPECTED: * Resulted event with 'Extra Place Race' flag is removed from Extra Place Races carousel by live update
        """
        sleep(7)  # small delay for application to receive changes from TI
        self.assertTrue(self.sections, msg='No sections found')
        self.assertIn(self.enhanced_races_name, self.sections,
                      msg=f'Cannot find "{self.enhanced_races_name}" module section')

        extra_place_events = self.sections[self.enhanced_races_name].extra_place_offer_module.items_as_ordered_dict
        self.assertNotIn(self.extra_event_name, extra_place_events.keys(),
                         msg=f'"{self.extra_event_name}" can be found among "{list(extra_place_events.keys())}" events '
                             f'in "{vec.racing.EXTRA_PLACE_TITLE}" module. It should not.')

    def test_006_in_ti_select_event_from_preconditions_with_both_flags_checked_and_set_results_for_it(self):
        """
        DESCRIPTION: In TI select event from preconditions with both flags checked and set results for it
        """
        self.result_event(event_id=self.combined_eventID,
                          market_id=self.combined_event_marketID,
                          selection_ids=self.combined_event_selectionID)

    def test_007_go_to_oxygen_application_and_navigate_to_featured_tab_on_horse_racing_page(self):
        """
        DESCRIPTION: Go to oxygen application and navigate to Featured tab on Horse Racing page.
        DESCRIPTION: Verify that resulted events are removed from module automatically
        EXPECTED: * Resulted event with both 'Featured Racing Types' and ''Extra Place Race' flags is removed from both carousels by live update.
        EXPECTED: * Not resulted events are still displayed in ITV and Extra place
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        # Adding if/else because <Module name> can be present due to other events presence
        enhanced_races_section = sections.get(self.enhanced_races_name)
        if enhanced_races_section:
            itv_module_events = self.sections[self.enhanced_races_name].itv_module.items_as_ordered_dict
            self.assertNotIn(self.combined_event_name, itv_module_events.keys(),
                             msg=f'"{self.combined_event_name}" can be found among "{list(itv_module_events.keys())}" '
                                 f'events in "{vec.racing.ITV}" module. It should not.')

            extra_place_events = self.sections[self.enhanced_races_name].extra_place_offer_module.items_as_ordered_dict
            self.assertNotIn(self.combined_event_name, extra_place_events.keys(),
                             msg=f'"{self.combined_event_name}" can be found among "{list(extra_place_events.keys())}" '
                                 f'events in "{vec.racing.EXTRA_PLACE_TITLE}" module. It should not.')
        else:
            self._logger.warning(f'*** "{self.enhanced_races_name}" is not present on page anymore')
