import pytest
from time import sleep

from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # event creation
# @pytest.mark.hl
@pytest.mark.races
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.mobile_only  # applicable for tablet as well
@pytest.mark.medium
@vtest
class Test_C2592701_Verify_displaying_of_ITVExtra_Place_Races_carousels(BaseRacing):
    """
    TR_ID: C2592701
    VOL_ID: C11547285
    NAME: Verify displaying of ITV/Extra Place Races carousels
    PRECONDITIONS: 1. ITV/Extra Place Races feature toggle should be set to "ON" (CMS->System configuration->Structure->featuredRaces)
    PRECONDITIONS: 2. There should be NO Horse Racing events with 'Featured Racing Types'(ITV races) or 'Extra Place Race' flags checked in TI
    PRECONDITIONS: 3. Go to oxygen application and navigate to Featured tab on Horse Racing page.
    PRECONDITIONS: <Module name> - "Offers and Extra place" (Ladbrokes), "Enhanced Races" (Coral)
    PRECONDITIONS: Design for both Brands can be found here: https://jira.egalacoral.com/browse/BMA-35023
    PRECONDITIONS: 'Featured race'(ITV races) - is checked on event level
    PRECONDITIONS: 'Extra Place Race' flag - is checked on market level
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event without 'Featured Racing Types'(ITV races) or 'Extra Place Race' flags
        DESCRIPTION: Go to oxygen application and navigate to Featured tab on Horse Racing page.
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms,
                                                   time_to_start=111)  # for making event unique, please not change
        self.__class__.eventID = event.event_id
        self.__class__.event_time = event.event_off_time
        self.__class__.event_name = f'{self.event_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.event_name_on_landing_page = self.event_name[:10] if self.brand == 'ladbrokes' \
            else self.event_name

        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab "{current_tab}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')

    def test_001_verify_module_displaying(self):
        """
        DESCRIPTION: Verify <Module name> module displaying
        EXPECTED: * <Module name> Module is not displayed on Featured tab
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        # Presence of <Module name> is not a bug, since there can be other events for the module
        if self.enhanced_races_name in sections:
            self._logger.debug(f'*** "{self.enhanced_races_name}" found!')

    def test_002_go_to_ti_and_check_featured_racing_types_flag_on_any_horse_racing_event(self):
        """
        DESCRIPTION: Go to TI and check 'Featured Racing Types' flag on any Horse Racing event
        """
        self.ob_config.change_racing_promotion_state(promotion_name='featured_racing_types',
                                                     level='event',
                                                     market_id=self.ob_config.market_ids[self.eventID],
                                                     event_id=self.eventID)

    def test_003_go_back_to_oxygen_application_and_refresh_the_page_and_verify_module_displaying(self):
        """
        DESCRIPTION: Go back to oxygen application and refresh the page.
        DESCRIPTION: Verify <Module name> module displaying.
        EXPECTED: * <Module name> Module is displayed
        EXPECTED: * Module can be expanded/collapsed
        EXPECTED: * ITV carousel is displayed
        EXPECTED: * Extra Place Races carousel is not displayed
        """
        sleep(5)  # Sometimes update from TI is not received quick enough
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        self.assertIn(self.enhanced_races_name, sections,
                      msg=f'Cannot find "{self.enhanced_races_name}" module section')
        self.__class__.enhanced_races_section = sections[self.enhanced_races_name]

        self.enhanced_races_section.collapse()
        self.assertFalse(self.enhanced_races_section.is_expanded(expected_result=False),
                         msg=f'"{self.enhanced_races_name}" module section is not collapsed')

        self.enhanced_races_section.expand()
        self.assertTrue(self.enhanced_races_section.is_expanded(),
                        msg=f'"{self.enhanced_races_name}" module section is not expanded')

        self.assertTrue(self.enhanced_races_section.has_itv_module(timeout=5),
                        msg=f'"{self.enhanced_races_name}" module section '
                            f'does not contain "{vec.racing.ITV}" carousel')

        self._logger.warning('*** Cannot verify absence of "Extra Place Races" carousel, '
                             'since other events, not created in test, can be present there')

    def test_004_verify_displaying_of_events_in_itv_carousel(self):
        """
        DESCRIPTION: Verify displaying of events in ITV carousel
        EXPECTED: * Event with 'Featured Racing Types' flag is present in ITV carousel
        EXPECTED: * Event is clickable(user is navigated to the race card of the event on click)
        EXPECTED: * CORAL: Carousel header is displayed. Event race time and meeting name are displayed
        EXPECTED: * LADBROKES: Carousel header and ITV/Extra Place icons are displayed. Event race time and first 4 letters of meeting name are displayed
        """
        itv_module_events = self.enhanced_races_section.itv_module.items_as_ordered_dict
        itv_event = itv_module_events.get(self.event_name_on_landing_page)
        self.assertTrue(itv_event, msg=f'"{self.event_name_on_landing_page}" not found in '
                                       f'"{vec.racing.ITV}" among: {list(itv_module_events.keys())}')

        if self.brand == 'ladbrokes':
            actual_header_name = self.enhanced_races_section.itv_module.header_name.text
            self.assertEqual(actual_header_name, vec.racing.ITV,
                             msg=f'Actual carousel header name, "{actual_header_name}", '
                                 f'is not equal to expected: "{vec.racing.ITV}"')

            actual_meeting_time, actual_meeting_name = itv_event.name.split(' ')
            expected_meeting_name = self.horseracing_autotest_uk_name_pattern[:4]
            self.assertEqual(actual_meeting_name, expected_meeting_name,
                             msg=f'Actual meeting name in event name: "{actual_meeting_name}" '
                                 f'is not equal to expected: "{expected_meeting_name}"')
            self.assertEqual(actual_meeting_time, self.event_time,
                             msg=f'Actual meeting time "{actual_meeting_time}" '
                                 f'is not equal to expected "{self.event_time}"')

            self.assertTrue(self.enhanced_races_section.itv_module.has_itv_icon(),
                            msg='Cannot find icon for "ITV Races" module')
        else:
            self.assertEqual(itv_event.card_name.upper(), vec.racing.ITV,
                             msg=f'Found "{itv_event.card_name.upper()}" carousel name, '
                                 f'expected was: "{vec.racing.ITV}"')

        itv_event.click()
        self.site.wait_content_state(state_name='RacingEventDetails')
        event_title = self.site.racing_event_details.tab_content.race_details.event_title
        self.assertEqual(event_title, self.event_name,
                         msg=f'Wrong EDP page opened.\nActual: "{event_title}"\nExpected: "{self.event_name}"')

        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_005_go_to_ti_select_event_from_step_2_and_check_extra_place_race_flag_on_the_market_level_of_the_selected_event(self):
        """
        DESCRIPTION: Go to TI, select event from step 2 and check 'Extra Place Race' flag on the market level of the selected event.
        """
        self.ob_config.change_racing_promotion_state(promotion_name='extra_place_race',
                                                     level='market',
                                                     market_id=self.ob_config.market_ids[self.eventID],
                                                     event_id=self.eventID)

    def test_006_go_back_to_oxygen_application_and_refresh_the_page_and_verify_module_displaying(self):
        """
        DESCRIPTION: Go back to oxygen application and refresh the page.
        DESCRIPTION: Verify <Module name> module displaying.
        EXPECTED: * <Module name> Module is displayed
        EXPECTED: * ITV carousel is displayed
        EXPECTED: * Extra Place Races carousel is displayed
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        self.assertIn(self.enhanced_races_name, sections,
                      msg=f'Cannot find "{self.enhanced_races_name}" module section')
        self.__class__.enhanced_races_section = sections[self.enhanced_races_name]

        self.assertTrue(self.enhanced_races_section.has_itv_module(),
                        msg=f'"{self.enhanced_races_name}" module section '
                            f'does not contain "{vec.racing.ITV}" carousel')

        self.assertTrue(self.enhanced_races_section.has_extra_place_module(timeout=5),
                        msg=f'"{self.enhanced_races_name}" module section '
                            f'does not contain "{vec.racing.EXTRA_PLACE_TITLE}" carousel')

    def test_007_verify_displaying_of_events_in_itv_and_extra_place_races_carousels(self):
        """
        DESCRIPTION: Verify displaying of events in ITV and Extra Place Races carousels
        EXPECTED: * Event is present in Extra Place Races carousel
        EXPECTED: * Event is clickable(user is navigated to the race card of the event on click)
        EXPECTED: * CORAL: Carousel header is displayed. Event race time and meeting name are displayed
        EXPECTED: * LADBROKES: Carousel header and ITV/Extra Place icons are displayed. Event race time and first 4 letters of meeting name are displayed
        """
        extra_place_module_events = self.enhanced_races_section.extra_place_offer_module.items_as_ordered_dict
        self.assertTrue(extra_place_module_events,
                        msg=f'There are no events in Extra Place Races module section')
        extra_place_event = extra_place_module_events.get(self.event_name_on_landing_page)
        if not extra_place_event:  # Sometimes update from TI is not received quick enough
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
            self.__class__.enhanced_races_section = sections[self.enhanced_races_name]
            extra_place_module_events = self.enhanced_races_section.extra_place_offer_module.items_as_ordered_dict
            extra_place_event = extra_place_module_events.get(self.event_name_on_landing_page)

        self.assertTrue(extra_place_event,
                        msg=f'"{self.event_name_on_landing_page}" not found in '
                            f'"{vec.racing.EXTRA_PLACE_TITLE}" module among: {list(extra_place_module_events.keys())}')

        if self.brand == 'ladbrokes':
            actual_header_name = self.enhanced_races_section.extra_place_offer_module.header_name.text
            self.__class__.expected_header_name = vec.racing.EXTRA_PLACE_TITLE.title()
            self.assertEqual(actual_header_name, self.expected_header_name,
                             msg=f'Actual carousel header name, "{actual_header_name}",  '
                                 f'is not equal to expected: "{self.expected_header_name}"')

            actual_meeting_time, actual_meeting_name = extra_place_event.name.split(' ')
            expected_meeting_name = self.horseracing_autotest_uk_name_pattern[:4]
            self.assertEqual(actual_meeting_name, expected_meeting_name,
                             msg=f'Actual meeting name in event name: "{actual_meeting_name}" '
                                 f'is not equal to expected: "{expected_meeting_name}"')
            self.assertEqual(actual_meeting_time, self.event_time,
                             msg=f'Actual meeting time "{actual_meeting_time}" '
                                 f'is not equal to expected "{self.event_time}"')

            self.assertTrue(self.enhanced_races_section.extra_place_offer_module.has_extra_place_races_icon(),
                            msg='Cannot find icon for "Extra Place Offer" module')
        else:
            self.assertEqual(extra_place_event.card_name.upper(), vec.racing.EXTRA_PLACE_TITLE,
                             msg=f'Found "{extra_place_event.card_name.upper()}" carousel name, '
                                 f'expected was: "{vec.racing.EXTRA_PLACE_TITLE}"')

        extra_place_event.click()
        self.site.wait_content_state(state_name='RacingEventDetails')
        event_title = self.site.racing_event_details.tab_content.race_details.event_title
        self.assertEqual(event_title, self.event_name,
                         msg=f'Wrong EDP page opened.\nActual: "{event_title}"\nExpected: "{self.event_name}"')

        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_008_go_to_ti_and_uncheck_featured_racing_types_flag_for_event_from_step_2_that_had_this_flag_checked(self):
        """
        DESCRIPTION: Go to TI and uncheck 'Featured Racing Types' flag for event from Step 2 that had this flag checked
        """
        self.ob_config.change_racing_promotion_state(promotion_name='featured_racing_types',
                                                     level='event',
                                                     market_id=self.ob_config.market_ids[self.eventID],
                                                     event_id=self.eventID,
                                                     available=False)

    def test_009_go_back_to_oxygen_application_and_refresh_the_pageverify_module_displaying(self):
        """
        DESCRIPTION: Go back to oxygen application and refresh the page.
        DESCRIPTION: Verify <Module name> module displaying.
        EXPECTED: * <Module name> Module is displayed
        EXPECTED: * ITV carousel is NOT displayed
        EXPECTED: * Extra Place Races carousel is displayed
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        self.assertIn(self.enhanced_races_name, sections,
                      msg=f'Cannot find "{self.enhanced_races_name}" module section')
        self.__class__.enhanced_races_section = sections[self.enhanced_races_name]

        self._logger.warning('*** Cannot verify absence of "ITV" carousel, '
                             'since other events, not created in test, can be present there')

        self.assertTrue(self.enhanced_races_section.has_extra_place_module(),
                        msg=f'"{self.enhanced_races_name}" module section '
                            f'does not contain "{vec.racing.EXTRA_PLACE_TITLE}" carousel')

    def test_010_verify_displaying_of_events_in_itv_and_extra_place_races_carousels(self):
        """
        DESCRIPTION: Verify displaying of events in ITV and Extra Place Races carousels
        EXPECTED: * Event with 'Extra Place Race' flag is present in Extra Place Race carousel
        EXPECTED: * CORAL: Carousel header is displayed. Event race time and meeting name are displayed
        EXPECTED: * LADBROKES: Carousel header and ITV/Extra Place icons are displayed. Event race time and first 4 letters of meeting name are displayed
        """
        itv_module_events = self.enhanced_races_section.itv_module.items_as_ordered_dict
        itv_event = itv_module_events.get(self.event_name_on_landing_page)
        if itv_event:  # Sometimes update from TI is not received quick enough
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
            self.__class__.enhanced_races_section = sections[self.enhanced_races_name]
            itv_module_events = self.enhanced_races_section.itv_module.items_as_ordered_dict
            itv_event = itv_module_events.get(self.event_name_on_landing_page)

        self.assertFalse(itv_event, msg=f'"{self.event_name_on_landing_page}" found in '
                                        f'"{vec.racing.ITV}" module. It should not be there')

        enhanced_races_events = self.enhanced_races_section.extra_place_offer_module.items_as_ordered_dict
        extra_place_event = enhanced_races_events.get(self.event_name_on_landing_page)
        self.assertTrue(extra_place_event,
                        msg=f'"{self.event_name_on_landing_page}" not found in '
                            f'"{vec.racing.EXTRA_PLACE_TITLE}" module among: {list(enhanced_races_events.keys())}')

        if self.brand == 'ladbrokes':
            actual_header_name = self.enhanced_races_section.extra_place_offer_module.header_name.text
            self.assertEqual(actual_header_name, self.expected_header_name,
                             msg=f'Actual header name of Extra Place Offer "{actual_header_name}" carousel '
                                 f'is not equal to expected: "{self.expected_header_name}"')

            actual_meeting_time, actual_meeting_name = extra_place_event.name.split(' ')
            expected_meeting_name = self.horseracing_autotest_uk_name_pattern[:4]
            self.assertEqual(actual_meeting_name, expected_meeting_name,
                             msg=f'Actual meeting name in event name: "{actual_meeting_name}" '
                                 f'is not equal to expected: "{expected_meeting_name}"')
            self.assertEqual(actual_meeting_time, self.event_time,
                             msg=f'Actual meeting time "{actual_meeting_time}" '
                                 f'is not equal to expected "{self.event_time}"')

            self.assertTrue(self.enhanced_races_section.extra_place_offer_module.has_extra_place_races_icon(),
                            msg='Cannot find icon for "Extra Place Offer" module')
        else:
            self.assertEqual(extra_place_event.card_name.upper(), vec.racing.EXTRA_PLACE_TITLE,
                             msg=f'Found "{extra_place_event.card_name.upper()}" carousel , '
                                 f'expected was: "{vec.racing.EXTRA_PLACE_TITLE}"')

    def test_011_go_to_ti_and_uncheck_extra_place_race_flag_for_event_from_step_5_that_had_this_flag_checked(self):
        """
        DESCRIPTION: Go to TI and uncheck 'Extra Place Race' flag for event from Step 5 that had this flag checked
        """
        self.ob_config.change_racing_promotion_state(promotion_name='extra_place_race',
                                                     level='market',
                                                     market_id=self.ob_config.market_ids[self.eventID],
                                                     event_id=self.eventID,
                                                     available=False)

    def test_012_go_to_oxygen_application_and_navigate_to_featured_tab_on_horse_racing_page(self):
        """
        DESCRIPTION: Go to oxygen application and navigate to Featured tab on Horse Racing page.
        DESCRIPTION: Verify that resulted events are removed from module automatically
        EXPECTED: * <Module name> module is NOT displayed
        EXPECTED: ITV and Extra Place Races carousels are NOT displayed
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        # Adding if/else because <Module name> can be present due to other events presence
        enhanced_races_section = sections.get(self.enhanced_races_name)
        if enhanced_races_section:
            itv_module_events = enhanced_races_section.itv_module.items_as_ordered_dict
            itv_event = itv_module_events.get(self.event_name_on_landing_page)
            self.assertFalse(itv_event, msg=f'"{self.event_name_on_landing_page}" found in '
                                            f'"{vec.racing.ITV}" module. It should not be there')

            enhanced_races_events = enhanced_races_section.extra_place_offer_module.items_as_ordered_dict
            extra_place_event = enhanced_races_events.get(self.event_name_on_landing_page)
            if extra_place_event:  # Sometimes update from TI is not received quick enough
                self.device.refresh_page()
                self.site.wait_splash_to_hide()
                sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
                enhanced_races_events = sections[self.enhanced_races_name].extra_place_offer_module.items_as_ordered_dict
                extra_place_event = enhanced_races_events.get(self.event_name_on_landing_page)

            self.assertFalse(extra_place_event, msg=f'"{self.event_name_on_landing_page}" found in '
                                                    f'"{vec.racing.EXTRA_PLACE_TITLE}" module. It should not be there')
        else:
            self._logger.warning(f'*** "{self.enhanced_races_name}" is not present on page anymore')
