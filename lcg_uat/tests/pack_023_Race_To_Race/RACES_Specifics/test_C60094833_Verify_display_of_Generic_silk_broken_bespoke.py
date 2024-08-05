import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
# @pytest.mark.tst2  # Datafabric not available for tst2
# @pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.horseracing
@vtest
class Test_C60094833_Verify_display_of_Generic_silk_broken_bespoke(BaseRacing):
    """
    TR_ID: C60094833
    NAME: Verify display of Generic silk-broken bespoke
    DESCRIPTION: This test case verifies display of Generic silk in horse racing EDP for all horses of all races(UK& IRE and International) when feed is broken
    PRECONDITIONS: 1.Bespoke silk should be present and broken from feed for any one of horse in HR EDP
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    section_skip_list = ['VIRTUAL RACING', 'ENHANCED RACES', 'NEXT RACES', 'Next Races', 'OFFERS & FEATURED RACES',
                         'INDIA', 'EXTRA PLACE OFFER', 'YOURCALL SPECIALS']

    def test_001_login_to_the_application_and_navigate_to_horse_racing_from_header_sub_menuin_mobile_from_sports_ribbonor_in_play___horse_racing(
            self):
        """
        DESCRIPTION: Login to the application and navigate to horse racing from header sub menu(In mobile from sports ribbon)
        DESCRIPTION: or In play - Horse racing
        EXPECTED: Horse racing landing page - meetings tab should display
        EXPECTED: if user is navigate from in play tab in play horse racing events should display
        """
        self.site.login()
        self.site.wait_content_state('homepage')
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing', timeout=20)
        current_tab_name = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Default tab is "{current_tab_name}" not "{vec.racing.RACING_DEFAULT_TAB_NAME}" tab')

    def test_002_click_on_any_event_from_uk_and_ire_for_which_bespoke_silk_is_provided_but_broken_from_feed_for_at_least_one_horse(
            self):
        """
        DESCRIPTION: Click on any event from UK and IRE for which bespoke silk is provided but broken from feed for at least one horse
        EXPECTED: All the horse in EDP should have bespoke silk
        EXPECTED: for the horse which bespoke silk is provided but broken feed should display generic silk
        """
        self.site.wait_splash_to_hide()
        sleep(5)
        sections = list(self.site.horse_racing.tab_content.accordions_list.get_items(
            name=vec.racing.UK_AND_IRE_TYPE_NAME.upper()).values())[0]
        self.assertTrue(sections, msg='UK AND IRISH RACES meeting is not available in Horse Racing SLP')
        meetings = sections.items_as_ordered_dict
        self.assertTrue(meetings,
                        msg=f'Failed to display any meetings for section_name "{vec.racing.UK_AND_IRE_TYPE_NAME}"')

        # code optimization--- verified for single section as it taking time for multiple sections
        # for i in range(len(sections.items())):
        #     sleep(10)
        #     sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        #     found_event = False
        #     section_name, section = list(sections.items())[i]
        #     if section_name not in self.section_skip_list:
        #         self._logger.debug(f'*** In section "{section_name}"')
        #         if not section.is_expanded():
        #             section.expand()
        #         meetings = section.items_as_ordered_dict
        #         self._logger.info(f'Meetings for section_name "{section_name}"')
        found_event = False
        for meeting_name, meeting in meetings.items():
            try:
                events = meeting.items_as_ordered_dict
                self.assertTrue(events,
                                msg=f'Failed to display any event for section_name "{self.uk_and_ire_type_name}"')
            except RuntimeError:
                events = meetings
            for event_name, event in events.items():
                if 'race-on' in event.get_attribute('class'):
                    event.click()
                    sleep(3)
                    if self.site.wait_for_stream_and_bet_overlay():
                        self.site.stream_and_bet_overlay.close_button.click()
                    if self.site.wait_for_my_stable_onboarding_overlay():
                        self.site.my_stable_onboarding_overlay.close_button.click()
                    self.site.wait_splash_to_hide(5)
                    self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
                        vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
                    sleep(2)
                    self.site.wait_content_state_changed(10)
                    found_event = True
                if found_event is True:
                    break
            if found_event is True:
                break
        # if found_event is False:
        #     self._logger.info(f'Did not get race-on event from section "{section_name}"')
        #     continue
        racing_details = self.site.racing_event_details
        result = wait_for_result(
            lambda: racing_details.event_title is not None,
            name='Wait for Event title to display',
            timeout=20)
        self.assertTrue(result, msg=f'Event title is not displayed for section "{self.uk_and_ire_type_name}"')

        for item in racing_details.items:
            self.assertTrue(item.horse_name, msg=f'Failed to display the horse name "{item.horse_name}" '
                                                 f'from section "{self.uk_and_ire_type_name}"')
            # Generic Silk
            if item.horse_name == 'Unnamed Favourite' or item.horse_name == 'Unnamed 2nd Favourite':
                self.assertTrue(item.has_silks,
                                msg=f'Silk is not displayed for the horse "{item.horse_name}" from section "{self.uk_and_ire_type_name}"')
            # No silk at all
            elif item.is_non_runner:
                self.assertTrue(item.has_no_silks,
                                msg=f'Silk is displayed for non-runner horse "{item.horse_name}" from section "{self.uk_and_ire_type_name}"')
            # Bespoke Silk
            elif item.silk:
                self.assertTrue(item.has_bespoke_silks,
                                msg=f'Bespoke silk is not displayed for the horse "{item.horse_name}" from section "{self.uk_and_ire_type_name}"')
            else:  # Generic Silk
                self.assertTrue(item.has_silks,
                                msg=f'Silk is not displayed for the horse "{item.horse_name}" from section "{self.uk_and_ire_type_name}"')

    def test_003_to_confirm_above_step_right_click_on_any_bespoke_silk_and_inspect_and_change_image_id_with_dummy_id_and_see_in_febackground_image_urlhttpsaggregationladbrokescomsilksracingpostxxxx(
            self):
        """
        DESCRIPTION: To confirm above step right click on any bespoke silk and inspect and change image id with dummy id and see in FE
        DESCRIPTION: background-image: url("https://aggregation.ladbrokes.com/silks/racingpost/xxxx
        EXPECTED: In FE generic silk should be displayed
        """
        # Cann't be automated

    def test_004_repeat_above_step_from_below_racesmeeting_tab___race_from_usameeting_tab___race_from_francemeeting_tab___race_from_australiameeting_tab___race_from_international_racesmeeting_tab___race_from_international_tote_carasoulmeeting_tab___race_from_virtual_race_carasoulmeeting_tab___race_from_extra_place_offersmeeting_tab___race_from_ladbrokes_legendsfuture_tab___race_from_flat_tabfuture_tab___race_from_international_tabfuture_tab___race_from_national_hunts_tabany_race_from_next_races_tabany_race_from_special_races_tabinplay_races(
            self):
        """
        DESCRIPTION: Repeat above step from below races
        DESCRIPTION: Meeting tab - race from USA
        DESCRIPTION: Meeting tab - race from FRANCE
        DESCRIPTION: Meeting tab - race from AUSTRALIA
        DESCRIPTION: Meeting tab - race from International races
        DESCRIPTION: Meeting tab - race from international tote carasoul
        DESCRIPTION: Meeting tab - race from Virtual race carasoul
        DESCRIPTION: Meeting tab - race from extra place offers
        DESCRIPTION: Meeting tab - race from Ladbrokes legends
        DESCRIPTION: Future tab - race from flat tab
        DESCRIPTION: Future tab - race from International tab
        DESCRIPTION: Future tab - race from National hunts tab
        DESCRIPTION: Any race from next races tab
        DESCRIPTION: Any race from Special races tab
        DESCRIPTION: Inplay races
        """
        # Covered in Step2
