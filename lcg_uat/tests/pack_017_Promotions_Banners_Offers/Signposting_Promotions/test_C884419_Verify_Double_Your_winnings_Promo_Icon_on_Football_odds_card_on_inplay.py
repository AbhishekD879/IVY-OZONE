import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result
from voltron.utils.helpers import wait_for_category_in_inplay_ls_structure


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod  # Coral only
# @pytest.mark.crl_hl
@pytest.mark.promotions
@pytest.mark.in_play
@pytest.mark.football
@pytest.mark.featured
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@pytest.mark.login
@pytest.mark.desktop
@vtest
class Test_C884419_Verify_Double_Your_winnings_Promo_Icon_on_Football_odds_card_on_football_and_in_play(BaseSportTest):
    """
    TR_ID: C884419
    VOL_ID: C9698088
    NAME: Verify Double Your winnings Promo Icon on Football odds card on Football and In-Play
    """
    keep_browser_open = True
    today_event_name, tomorrow_event_name, live_event_name = None, None, None
    event = None
    section_name = tests.settings.football_autotest_league
    coupon_name = vec.siteserve.EXPECTED_COUPON_NAME
    event_level_flag, market_level_flag = 'EVFLAG_DYW', 'MKTFLAG_DYW'

    def check_dyw_promotion_for_event(self, event):
        self.assertTrue(event.promotion_icons.has_double_your_winnings(),
                        msg='Event "%s" does not have "Double Your Winnings" promotion' % event.event_name)
        event.promotion_icons.double_your_winnings.click()
        self.check_promotion_dialog_appearance_and_close_it(
            expected_title=vec.dialogs.DIALOG_MANAGER_DOUBLE_YOUR_WINNINGS.upper())

    def test_001_create_test_events(self):
        """
        DESCRIPTION: Create test events with "Double Your winnings" promotion available
        """
        live_start_time = self.get_date_time_formatted_string(seconds=10)
        tomorrow_start_time = self.get_date_time_formatted_string(days=1)

        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=live_start_time,
                                                                          double_your_winnings=True)
        self.__class__.eventID_live = event.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_live,
                                                               query_builder=self.ss_query_builder)
        self.__class__.live_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.live_event_name}"')
        self.__class__.section_name_live = self.get_accordion_name_for_event_from_ss(event=event_resp[0], in_play_tab_slp=True)

        event = self.ob_config.add_autotest_premier_league_football_event(double_your_winnings=True, special=True)
        self.__class__.eventID1 = event.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID1,
                                                               query_builder=self.ss_query_builder)
        self.__class__.today_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.today_event_name}"')

        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        self.ob_config.add_event_to_coupon(market_id=self.ob_config.market_ids[event.event_id][market_short_name],
                                           coupon_name=self.coupon_name)

        event = self.ob_config.add_autotest_premier_league_football_event(double_your_winnings=True,
                                                                          start_time=tomorrow_start_time)
        self.__class__.eventID_tomorrow = event.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_tomorrow,
                                                               query_builder=self.ss_query_builder)
        self.__class__.tomorrow_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.tomorrow_event_name}"')

        self.__class__.section_name_prematch = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

        dialog_name = self.get_promotion_details_from_cms(event_level_flag=self.event_level_flag,
                                                          market_level_flag=self.market_level_flag)['popupTitle'].upper()
        vec.dialogs.DIALOG_MANAGER_DOUBLE_YOUR_WINNINGS = vec.dialogs.DIALOG_MANAGER_DOUBLE_YOUR_WINNINGS.format(dialog_name)

        self.site.login()

    def test_002_check_the_event_with_double_your_winnings_promotion_on_in_play_pages(self):
        """
        DESCRIPTION: Check the event with **Double Your Winnings** promotion on In Play:
        DESCRIPTION: * Football -> In Play
        DESCRIPTION: * In Play page -> All Sports (Football accordion)
        DESCRIPTION: * In Play page -> Football
        DESCRIPTION: and tap the icon in all listed locations
        EXPECTED: Corresponding promo icon is shown on the event odds card
        EXPECTED: Promo footer is displayed after tapping the icon
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        self.site.football.tabs_menu.click_button('IN-PLAY')
        self.assertEqual(self.site.football.tabs_menu.current, 'IN-PLAY', msg='In-Play tab is not active')
        event = self.get_event_from_league(event_id=self.eventID_live, section_name=self.section_name_live)
        self.check_dyw_promotion_for_event(event=event)

        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state(state_name='in-play')
        self.verify_active_sport_on_inplay_page(sport_name=vec.sb.WATCH_LIVE_LABEL)
        wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.football.category_id)

        self.site.inplay.inplay_sport_menu.click_item('FOOTBALL')
        if self.device_type == 'mobile':
            section_name = tests.settings.football_autotest_competition_league
        else:
            section_name = tests.settings.football_autotest_competition + ' - ' + tests.settings.football_autotest_competition_league

        sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one event section found in for Football')
        section = sections[section_name] if section_name in sections.keys() else None
        self.assertTrue(section, msg='Section "%s" is not found in "%s"' % (section_name, ', '.join(sections.keys())))
        section.expand()
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found in section "%s"' % section_name)

        self.assertTrue(self.live_event_name in events)
        self.check_dyw_promotion_for_event(events[self.live_event_name])

    def test_003_check_the_event_with_double_your_winnings_promotion_on_football_pages(self):
        """
        DESCRIPTION: Check the event with **Double Your Winnings** promotion on Football pages:
        DESCRIPTION: * Football -> Matches
        DESCRIPTION: and tap the icon in all listed locations
        EXPECTED: Corresponding promo icon is shown on the event odds card
        EXPECTED: Promo footer is displayed after tapping the icon
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        self.site.football.tabs_menu.click_button(self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                                          self.ob_config.football_config.category_id))
        event = self.get_event_from_league(event_id=self.eventID1, section_name=self.section_name_prematch)
        self.check_dyw_promotion_for_event(event=event)

    def test_004_check_the_event_with_double_your_winnings_promotion_on_football_coupons_tab_tap_the_icon(self):
        """
        DESCRIPTION: Check the event with **Double Your Winnings** promotion on Football -> Coupons tab
        DESCRIPTION: Tap the icon
        EXPECTED: Corresponding promo icon is shown on the event odds card
        EXPECTED: Promo footer is displayed after tapping the icon
        """
        autotest_league = tests.settings.football_autotest_competition_league

        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.coupons)
        self.assertEqual(self.site.football.tabs_menu.current, self.expected_sport_tabs.coupons,
                         msg='Coupons tab is not active')
        coupons = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(coupons, msg='No coupons found')
        if vec.siteserve.EXPECTED_COUPON_NAME not in coupons:
            sleep(1)
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
        coupons = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(coupons, msg='No coupons found')
        coupons_1 = list(coupons.values())[0].items_as_ordered_dict
        self.assertIn(vec.siteserve.EXPECTED_COUPON_NAME, coupons_1,
                      msg='"%s" is not found in list of coupons "%s"'
                          % (self.coupon_name, ', '.join(coupons_1)))
        coupons_1[self.coupon_name].click()

        sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No event groups found on Coupon page')
        self.assertIn(autotest_league, sections,
                      msg='"%s" is not found in sections list "%s"'
                          % (autotest_league, ', '.join(sections.keys())))
        date_groups = sections[autotest_league].items_as_ordered_dict
        self.assertTrue(date_groups, msg='No data groups found in "%s" section'
                                         % autotest_league)
        self.assertIn('Today', date_groups.keys(),
                      msg='Today date group is not found among date groups "%s"'
                          % ', '.join(date_groups.keys()))
        events = date_groups['Today'].items_as_ordered_dict
        self.assertTrue(events, msg='No events found in "%s" section'
                                    % autotest_league)
        self.assertIn(self.today_event_name, events, msg='No event "%s" found in events list "%s"'
                                                         % (self.today_event_name, ', '.join(events)))
        self.check_dyw_promotion_for_event(event=events[self.today_event_name])

    def test_005_check_the_event_with_double_your_winnings_promotion_on_football_competitions_tab_tap_the_icon(self):
        """
        DESCRIPTION: Check the event with **Double Your Winnings** promotion on Football -> Competitions tab
        DESCRIPTION: Tap the icon
        EXPECTED: Corresponding promo icon is shown on the event odds card
        EXPECTED: Promo footer is displayed after tapping the icon
        """
        self.navigate_to_page(name='sport/football/competitions')
        self.site.wait_content_state(state_name='football')
        active_tab = self.site.football.tabs_menu.current
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                     self.ob_config.football_config.category_id)
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'"{active_tab}" tab is active, expected is "{expected_sport_tab}"')
        if self.device_type == 'mobile':
            competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
        else:
            self.site.football.tab_content.grouping_buttons.items_as_ordered_dict.get('A - Z').click()
            competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on page')
        self.assertIn(tests.settings.football_autotest_competition, competitions)
        competition = competitions[tests.settings.football_autotest_competition]
        competition.expand()
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=2)
        competition_league = tests.settings.football_autotest_competition_league
        competition_league = competition_league.title()
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertTrue(competition_league in leagues,
                        msg='League "%s" is not present in list of league in competition "%s"' % (
                            competition_league, competition))
        league = leagues[competition_league]
        league.click()

        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections are present on page')
        events = sections['Tomorrow'].items_as_ordered_dict
        self.assertTrue(events, msg='No events found')
        self.assertIn(self.tomorrow_event_name, events, msg='No event "%s" found in events list "%s"'
                                                            % (self.tomorrow_event_name, ', '.join(events)))
        self.__class__.event = events[self.tomorrow_event_name]
        self.check_dyw_promotion_for_event(event=self.event)

    def test_006_add_the_event_with_double_your_winnings_promotion_to_favorites(self):
        """
        DESCRIPTION: Add the event with **Double Your Winnings** promotion to Favorites
        EXPECTED: Event is added
        """
        self.event.favourite_icon.click()
        self.assertTrue(self.event.favourite_icon.is_selected(), msg='Event favourite icon is not selected')
        if self.device_type == 'mobile':
            count = self.site.football.header_line.favourites_counter
        else:
            count = len(self.site.favourites.items_as_ordered_dict)
        self.assertEqual(int(count), 1, msg="Event is not added to the 'Favourite Matches' page")

    def test_007_check_the_event_with_double_your_winnings_promotion_on_favorites_page_tap_the_icon(self):
        """
        DESCRIPTION: Check the event with **Double Your Winnings** promotion on Favorites page
        DESCRIPTION: Tap the icon
        EXPECTED: Corresponding promo icon is shown on the event odds card
        EXPECTED: Promo footer is displayed after tapping the icon
        """
        if self.device_type == 'mobile':
            self.site.football.header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            sections = self.site.favourites.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='Sections are not found')
            section = list(sections.values())[0]
            events = section.items_as_ordered_dict
        else:
            events = self.site.favourites.items_as_ordered_dict
        self.assertTrue(events, msg='Events are not found')
        self.assertIn(self.tomorrow_event_name, events, msg='No event "%s" found in events list "%s"'
                                                            % (self.tomorrow_event_name, ', '.join(events)))
        self.check_dyw_promotion_for_event(event=events[self.tomorrow_event_name])
