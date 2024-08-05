import pytest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #need to create events with different disporder and start time
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.homepage_featured
@vtest
class Test_C9607562_Verify_Surface_Bets_ordering(BaseFeaturedTest):
    """
    TR_ID: C9607562
    NAME: Verify Surface Bets ordering
    DESCRIPTION: Test case verifies proper Surface Bets ordering
    PRECONDITIONS: 1. There are a few Surface Bet added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_cms_edit_a_surface_bet_add_a_selection_of_the_live_eventin_the_application_refresh_the_slphomepage_verify_the_surface_bet_with_live_event_is_first(self):
        """
        DESCRIPTION: In the CMS edit a Surface Bet: add a selection of the Live event
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify the Surface Bet with Live event is first
        EXPECTED: Selection from the Live event is shown first
        """
        self.__class__.category_id = self.ob_config.football_config.category_id
        cms_surface_bet = self.cms_config.get_sport_module(sport_id=self.category_id,
                                                           module_type='SURFACE_BET')[0]
        if cms_surface_bet['disabled']:
            self.cms_config.change_sport_module_state(sport_module=cms_surface_bet)

        live_event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.upcoming_event = self.ob_config.add_autotest_premier_league_football_event()
        selection_id_live = live_event.selection_ids[live_event.team1]
        selection_id_upcoming = self.upcoming_event.selection_ids[self.upcoming_event.team1]

        surface_bet_with_live_event = self.cms_config.add_surface_bet(selection_id=selection_id_live,
                                                                      categoryIDs=self.category_id)
        surface_bet_with_live_event_title = surface_bet_with_live_event.get('title').upper()

        surface_bet_with_upcoming_event = self.cms_config.add_surface_bet(selection_id=selection_id_upcoming,
                                                                          categoryIDs=self.category_id)
        surface_bet_with_upcoming_event_title = surface_bet_with_upcoming_event.get('title').upper()

        self.__class__.expected_surface_bets = [surface_bet_with_live_event_title, surface_bet_with_upcoming_event_title]
        self.__class__.created_surface_bets_id = [surface_bet_with_live_event.get('id'), surface_bet_with_upcoming_event.get('id')]

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

        result = self.wait_for_surface_bets(name=surface_bet_with_live_event_title, timeout=10, poll_interval=1,
                                            raise_exceptions=False)
        if result is None:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.wait_for_surface_bets(name=surface_bet_with_live_event_title, timeout=15, poll_interval=1)

        surface_bets = list(self.site.home.tab_content.surface_bets.items_as_ordered_dict.keys())
        self.assertEqual(surface_bets, self.expected_surface_bets, msg=f'expected surface bets ordering "{surface_bets}" but actual surface bets ordering "{self.expected_surface_bets}"')
        self.cms_config.update_surface_bet(surface_bet_id=surface_bet_with_live_event.get('id'), disabled=True)
        self.expected_surface_bets.remove(surface_bet_with_live_event_title)
        self.created_surface_bets_id.remove(surface_bet_with_live_event.get('id'))

    def test_002_in_the_ti_change_events_disporder_of_the_the_selection_from_the_surface_betsin_the_application_refresh_the_slphomepage_verify_the_selection_from_the_event_with_the_disporder_is_shown_first(self):
        """
        DESCRIPTION: In the TI change events Disporder of the the selection from the Surface Bets
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify the selection from the event with the Disporder is shown first
        EXPECTED: Selection from the event with less Disporder is shown first
        """
        self.ob_config.update_event_disporder(eventID=self.upcoming_event.event_id, disporder_value=10)
        upcoming_event1 = self.ob_config.add_autotest_premier_league_football_event(disporder_value=0)
        selection_id_upcoming1 = upcoming_event1.selection_ids[upcoming_event1.team1]

        surface_bet_with_upcoming_event1 = self.cms_config.add_surface_bet(selection_id=selection_id_upcoming1,
                                                                           categoryIDs=self.category_id)

        self.wait_for_surface_bets(name=surface_bet_with_upcoming_event1.get('title').upper(), timeout=15, poll_interval=1,
                                   raise_exceptions=False)

        self.expected_surface_bets.insert(0, surface_bet_with_upcoming_event1.get('title').upper())
        self.created_surface_bets_id.append(surface_bet_with_upcoming_event1.get('id'))

        self.device.refresh_page()
        self.wait_for_surface_bets(name=surface_bet_with_upcoming_event1.get('title').upper(), timeout=15,
                                   poll_interval=1,
                                   raise_exceptions=False)

        result = wait_for_result(lambda: list(self.site.home.tab_content.surface_bets.items_as_ordered_dict.keys()) ==
                                 self.expected_surface_bets, timeout=15)
        self.assertTrue(result, msg=f'actual surface bets ordering "{list(self.site.home.tab_content.surface_bets.items_as_ordered_dict.keys())}" '
                                    f'but expected surface bets ordering "{self.expected_surface_bets}"')

        for surface_bet_id in self.created_surface_bets_id:
            self.cms_config.update_surface_bet(surface_bet_id=surface_bet_id, disabled=True)

    def test_003_setup_following_4_surface_bets_selections1_live_event_disporder12_live_event_disporder23_not_live_event_disporder14_not_live_event_disporder2in_the_application_refresh_the_slphomepage_verify_the_order_of_selections(self):
        """
        DESCRIPTION: Setup following 4 Surface Bets selections:
        DESCRIPTION: 1 Live event, Disporder=1
        DESCRIPTION: 2 Live event, Disporder=2
        DESCRIPTION: 3 Not Live event, Disporder=1
        DESCRIPTION: 4 Not Live event, Disporder=2
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify the order of selections
        EXPECTED: Selections from Live events are shown first. Events with less Disporder are shown first within Live and Not Live events separately.
        EXPECTED: Correct Order is:
        EXPECTED: 1 Live event, Disporder=1
        EXPECTED: 2 Live event, Disporder=2
        EXPECTED: 3 Not Live event, Disporder=1
        EXPECTED: 4 Not Live event, Disporder=2
        """
        live_disp1 = self.ob_config.add_autotest_premier_league_football_event(is_live=True, event_disporder=1)
        selection_id_live_disp1 = live_disp1.selection_ids[live_disp1.team1]

        sb_with_live_disp1 = self.cms_config.add_surface_bet(selection_id=selection_id_live_disp1, categoryIDs=self.category_id)

        live_disp2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True, event_disporder=2)
        selection_id_live_disp2 = live_disp2.selection_ids[live_disp2.team1]

        sb_with_live_disp2 = self.cms_config.add_surface_bet(selection_id=selection_id_live_disp2, categoryIDs=self.category_id)

        upcoming_disp1 = self.ob_config.add_autotest_premier_league_football_event(event_disporder=1)
        selection_id_upcoming_disp1 = upcoming_disp1.selection_ids[upcoming_disp1.team1]

        sb_with_upcoming_disp1 = self.cms_config.add_surface_bet(selection_id=selection_id_upcoming_disp1,
                                                                 categoryIDs=self.category_id)

        upcoming_disp2 = self.ob_config.add_autotest_premier_league_football_event(event_disporder=2)
        selection_id_upcoming_disp2 = upcoming_disp2.selection_ids[upcoming_disp2.team1]

        self.__class__.sb_with_upcoming_disp2 = self.cms_config.add_surface_bet(selection_id=selection_id_upcoming_disp2,
                                                                                categoryIDs=self.category_id)
        self.expected_surface_bets.clear()
        self.created_surface_bets_id.clear()
        self.expected_surface_bets = [sb_with_live_disp1.get('title').upper(), sb_with_live_disp2.get('title').upper(),
                                      sb_with_upcoming_disp1.get('title').upper(), self.sb_with_upcoming_disp2.get('title').upper()]
        self.created_surface_bets_id = [sb_with_live_disp1.get('id'), sb_with_live_disp2.get('id'),
                                        sb_with_upcoming_disp1.get('id'), self.sb_with_upcoming_disp2.get('id')]

        self.device.refresh_page()
        self.site.wait_splash_to_hide(timeout=5)
        self.wait_for_surface_bets(name=self.sb_with_upcoming_disp2.get('title').upper(), timeout=10, poll_interval=1,
                                   raise_exceptions=False)

        surface_bets = list(self.site.home.tab_content.surface_bets.items_as_ordered_dict.keys())
        self.assertEqual(surface_bets, self.expected_surface_bets, msg=f'actual surface bets ordering "{surface_bets}" '
                                                                       f'but expected surface bets ordering "{self.expected_surface_bets}"')

        self.cms_config.update_surface_bet(surface_bet_id=sb_with_live_disp1.get('id').upper(), disabled=True)
        self.cms_config.update_surface_bet(surface_bet_id=sb_with_live_disp2.get('id').upper(), disabled=True)
        for surface_bet_id in [sb_with_live_disp1.get('id'), sb_with_live_disp2.get('id')]:
            self.cms_config.update_surface_bet(surface_bet_id=surface_bet_id, disabled=True)

        start_time = self.get_date_time_formatted_string(hours=-1)
        self.ob_config.update_event_start_time(eventID=upcoming_disp2.event_id, start_time=start_time)
        del self.expected_surface_bets[0:2]
        del self.created_surface_bets_id[0:2]

        self.device.refresh_page()
        self.site.wait_splash_to_hide(timeout=5)
        self.wait_for_surface_bets(name=self.sb_with_upcoming_disp2.get('title').upper(), timeout=10, poll_interval=1,
                                   raise_exceptions=False)

        result = wait_for_result(lambda: list(self.site.home.tab_content.surface_bets.items_as_ordered_dict.keys()) !=
                                 self.expected_surface_bets, timeout=15)
        self.assertTrue(result, msg=f'actual surface bets ordering "{surface_bets}" but expected surface bets ordering '
                                    f'"{self.expected_surface_bets}"')

        for surface_bet_id in self.created_surface_bets_id:
            self.cms_config.update_surface_bet(surface_bet_id=surface_bet_id, disabled=True)

    def test_004_in_the_cms_edit_the_surface_bets_use_selections_from_events_with_different_start_datetimein_the_application_refresh_the_slphomepage_verify_the_selection_from_the_soonest_event_is_shown_first(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bets: use selections from events with different Start date/time.
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify the selection from the soonest event is shown first.
        EXPECTED: The selection from the soonest event is shown first
        """
        # covered in above steps

    def test_005_setup_following_4_not_live_surface_bets_selections_from_events1_disporder1_and_sooner_start_time_ex_15002_disporder1_and_later_start_time_ex_19003_disporder2_and_sooner_start_time_ex_15004_disporder2_and_later_start_time_ex_1900in_the_application_refresh_the_slphomepage_verify_the_order_of_selections(self):
        """
        DESCRIPTION: Setup following 4 Not Live Surface Bets selections from events:
        DESCRIPTION: 1 Disporder=1 and sooner start time (ex. 15:00)
        DESCRIPTION: 2 Disporder=1 and later start time (ex. 19:00)
        DESCRIPTION: 3 Disporder=2 and sooner start time (ex. 15:00)
        DESCRIPTION: 4 Disporder=2 and later start time (ex. 19:00)
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify the order of selections
        EXPECTED: Selections from the events with less Disporder are shown first.
        EXPECTED: Start time defines order after Disporder.
        EXPECTED: Correct order is:
        EXPECTED: 1 Disporder=1 and sooner start time (ex. 15:00)
        EXPECTED: 2 Disporder=1 and later start time (ex. 19:00)
        EXPECTED: 3 Disporder=2 and sooner start time (ex. 15:00)
        EXPECTED: 4 Disporder=2 and later start time (ex. 19:00)
        """
        sooner_start_time = self.get_date_time_formatted_string(hours=2)
        later_start_time = self.get_date_time_formatted_string(hours=4)

        sooner_disp1 = self.ob_config.add_autotest_premier_league_football_event(start_time=sooner_start_time, event_disporder=1)
        selection_id_sooner_disp1 = sooner_disp1.selection_ids[sooner_disp1.team1]

        sb_with_sooner_disp1 = self.cms_config.add_surface_bet(selection_id=selection_id_sooner_disp1, categoryIDs=self.category_id)

        later_disp1 = self.ob_config.add_autotest_premier_league_football_event(start_time=later_start_time, event_disporder=1)
        selection_id_later_disp1 = later_disp1.selection_ids[later_disp1.team1]

        sb_with_later_disp1 = self.cms_config.add_surface_bet(selection_id=selection_id_later_disp1, categoryIDs=self.category_id)

        sooner_disp2 = self.ob_config.add_autotest_premier_league_football_event(start_time=sooner_start_time, event_disporder=2)
        selection_id_sooner_disp2 = sooner_disp2.selection_ids[sooner_disp2.team1]

        sb_with_sooner_disp2 = self.cms_config.add_surface_bet(selection_id=selection_id_sooner_disp2, categoryIDs=self.category_id)

        later_disp2 = self.ob_config.add_autotest_premier_league_football_event(start_time=later_start_time, event_disporder=2)
        selection_id_later_disp2 = later_disp2.selection_ids[later_disp2.team1]

        sb_with_later_disp2 = self.cms_config.add_surface_bet(selection_id=selection_id_later_disp2, categoryIDs=self.category_id)

        self.expected_surface_bets.clear()
        self.created_surface_bets_id.clear()
        self.expected_surface_bets = [sb_with_sooner_disp1.get('title').upper(), sb_with_later_disp1.get('title').upper(),
                                      sb_with_sooner_disp2.get('title').upper(), sb_with_later_disp2.get('title').upper()]
        self.created_surface_bets_id = [sb_with_sooner_disp1.get('id'), sb_with_later_disp1.get('id'),
                                        sb_with_sooner_disp2.get('id'), sb_with_later_disp2.get('id')]

        self.device.refresh_page()
        self.site.wait_splash_to_hide(timeout=5)
        self.wait_for_surface_bets(name=sb_with_later_disp2.get('title').upper(), timeout=10, poll_interval=1,
                                   raise_exceptions=False)

        surface_bets = list(self.site.home.tab_content.surface_bets.items_as_ordered_dict.keys())
        self.assertEqual(surface_bets, self.expected_surface_bets, msg=f'actual surface bets ordering "{surface_bets}" '
                                                                       f'but expected surface bets ordering "{self.expected_surface_bets}"')

        for surface_bet_id in self.created_surface_bets_id[2:]:
            self.cms_config.update_surface_bet(surface_bet_id=surface_bet_id, disabled=True)

        del self.expected_surface_bets[2:]

        self.ob_config.update_event_start_time(eventID=sooner_disp1.event_id, start_time=sooner_start_time)
        self.ob_config.update_event_start_time(eventID=later_disp1.event_id, start_time=sooner_start_time)

        self.device.refresh_page()
        self.site.wait_splash_to_hide(timeout=5)
        self.wait_for_surface_bets(name=sb_with_later_disp1.get('title').upper(), timeout=10, poll_interval=1,
                                   raise_exceptions=False)

        result = wait_for_result(lambda: list(self.site.home.tab_content.surface_bets.items_as_ordered_dict.keys()).sort() ==
                                 self.expected_surface_bets.sort(), timeout=15)
        self.assertTrue(result, msg=f'actual surface bets ordering "{list(self.site.home.tab_content.surface_bets.items_as_ordered_dict.keys()).sort()}" '
                                    f'but expected surface bets ordering "{self.expected_surface_bets.sort()}"')

    def test_006_in_the_cms_edit_the_surface_bets_use_selections_from_events_with_the_same_start_datetimein_the_application_refresh_the_slphomepage_verify_surface_bets_are_ordered_by_event_name_in_alphabetical_order(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bets: use selections from events with the same Start date/time.
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify Surface Bets are ordered by event name in alphabetical order.
        EXPECTED: Surface bets are ordered in alphabetical order
        """
        # covered in above steps
