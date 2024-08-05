import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.mobile_only
@pytest.mark.adhoc_suite
@pytest.mark.reg167_fix
@vtest
class Test_C65946739_Verify_inplay_tab_in_tier1_SLPmobile(Common):
    """
    TR_ID: C65946739
    NAME: Verify inplay tab in tier1 SLP(mobile)
    DESCRIPTION: This test case Verify inplay tab in tier1 SLP(mobile)
    PRECONDITIONS: 1.Navigate to cms https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2.Sport category->any tier 1 sport->inplay tab(Active)
    """
    keep_browser_open = True
    target_uri = 'sport/football/live'

    def test_001_launch_bma_application(self):
        """
        DESCRIPTION: Launch BMA application
        EXPECTED: Application Launched successfully
        """
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,in_play_event=True)
        if not events:
            raise SiteServeException('Live Events are Not Available for Football')
        self.site.login()

    def test_002_navigate_to_any_tier1_sport_landing_page__click_on_inplay_tab(self):
        """
        DESCRIPTION: Navigate to any tier1 sport Landing page  click on Inplay tab
        EXPECTED: Navigated sport landing page and Iplay tab opened
        """
        pass

    def test_003_verify_inplay_tabs_live_now_upcoming_events_sections_dataloads_with_appropriate_data(self):
        """
        DESCRIPTION: Verify inplay tab's live now ,upcoming events sections data
        DESCRIPTION: loads with appropriate data
        EXPECTED: Inplay tab's live now ,upcoming events sections data loaded
        EXPECTED: with appropriate data
        """
        self.site.open_sport('Football')
        sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        inplay_tab = next((tab for tab_name, tab in sports_tabs.items() if tab_name.upper()=='IN-PLAY'), None)
        self.assertTrue(inplay_tab, 'IN-PLAY tab is not available')
        inplay_tab.click()

    def test_004_verify_live_now__and_upcoming_accordians_are_editable_tocollapse_and_expand(self, type='LIVE NOW'):
        """
        DESCRIPTION: Verify live now  and upcoming accordians are editable to
        DESCRIPTION: collapse and expand
        EXPECTED: live now  and upcoming accordians are editable to collapse
        EXPECTED: and expand
        """
        def get_accordion_list():
            return self.site.sports_page.tab_content.live_now if type == 'LIVE NOW' else self.site.sports_page.tab_content.upcoming

        def accordions_flexibility(accordions, type_of_accordions):
            self._logger.info(f'Verifying accordion behaviour for "{type}" section')
            for accordion_name, accordion in accordions.items():
                if accordion.is_expanded():
                    accordion.collapse()
                    self.assertFalse(accordion.is_expanded(),
                                     f'Football >> {type_of_accordions} : Accordion "{accordion_name}" is not collapsed')
                    accordion.expand()
                    self.assertTrue(accordion.is_expanded(),
                                    f'Football >> {type_of_accordions} : Accordion "{accordion_name}" is not expanded')
                else:
                    accordion.expand()
                    self.assertTrue(accordion.is_expanded(),
                                    f'Football >> {type_of_accordions} : Accordion "{accordion_name}" is not expanded')
                    accordion.collapse()
                    self.assertFalse(accordion.is_expanded(),
                                     f'Football >> {type_of_accordions} : Accordion "{accordion_name}" is not collapsed')

        def event_or_league_navigation(click_on='Event', first_league=None, leagues=None):
            self._logger.info(f'Verifying Navigation when user clicking on "{click_on}" for "{type}" section')
            if click_on == 'League':
                for league in leagues.values():
                    league.expand()
                league_name, league = next(([league_name, league] for league_name, league in leagues.items() if league.group_header.has_see_all_link()), [None, None])
                if not league:
                    self._logger.info(f'No One League Have See All Link in {type}')
                    return
                league.group_header.see_all_link.click()
                self.site.wait_content_state(state_name='CompetitionLeaguePage')
                league_name_on_fe = self.site.competition_league.title_section.type_name.name
                self.assertEqual(league_name.upper().strip().split('\n')[0], league_name_on_fe.upper().strip(),
                                 msg=f'expected league "{first_league_name}" is not same as actual league "{league_name_on_fe}"')
            else:
                first_league.expand()
                events = first_league.items_as_ordered_dict
                first_event_name, first_event = next(iter(events.items()))
                first_event.click() if click_on == 'Event' else first_event.more_markets_link.click()
                self.site.wait_content_state('EventDetails')
                if self.site.wait_for_stream_and_bet_overlay():
                    self.site.stream_and_bet_overlay.close_button.click()
                if self.brand != 'bma':
                    league_name_on_fe = self.site.sport_event_details.header_line.page_title.title
                    self.assertEqual(first_league_name.upper().strip().split('\n')[0], league_name_on_fe.upper().strip(),
                                     msg=f'expected league "{first_league_name}" is not same as actual league "{league_name_on_fe}"')
            self.site.back_button_click()
            self.site.wait_content_state('Football')

        accordions = get_accordion_list().n_items_as_ordered_dict()
        self.softAssert(self.assertTrue, accordions, msg=f'Leagues Not found for "{type}"')
        accordions_flexibility(accordions=accordions, type_of_accordions=type)

        first_league_name, first_league = next(iter(accordions.items()))
        event_or_league_navigation(click_on='Event', first_league=first_league)

        first_league_name, first_league = get_accordion_list().first_item
        event_or_league_navigation(click_on='More Link', first_league=first_league)

        leagues = get_accordion_list().n_items_as_ordered_dict()
        event_or_league_navigation(click_on='League', leagues=leagues)

    def test_005_verify_live_now_and_upcoming_events_are_clickable_andnavigates_to_respective_edp_page(self):
        """
        DESCRIPTION: Verify live now and upcoming events are clickable and
        DESCRIPTION: navigates to respective edp page
        EXPECTED: Live now and upcoming events are clickable and navigating
        EXPECTED: to respective edp page
        """
        self.test_004_verify_live_now__and_upcoming_accordians_are_editable_tocollapse_and_expand(type='UPCOMING')

    def test_006_verify_live_now_and_upcoming_events__leagues_view_all_linkclickable_and_navingating_the_respective_league_page(self):
        """
        DESCRIPTION: Verify live now and upcoming events  leagues view all link
        DESCRIPTION: clickable and navingating the respective league page
        EXPECTED: Live now and upcoming events  leagues view all link clickable
        EXPECTED: and navingating the respective league page
        """
        # covered in above step

    def test_007_verify_live_now_and_upcoming_events__more_link_on_eventsare_clickable_and_navingating_the_respective_edp(self):
        """
        DESCRIPTION: Verify live now and upcoming events  more link on events
        DESCRIPTION: are clickable and navingating the respective EDP
        EXPECTED: Live now and upcoming events  more link on events are
        EXPECTED: clickable and navingating the respective EDP
        """
        # covered in above step

    def test_008_verify_inplay_tab_is_visble_in_log_in_and_logout(self):
        """
        DESCRIPTION: Verify Inplay tab is visble in log in and logout
        EXPECTED: Inplay tab is visble in log in and logout
        """
        self.site.back_button_click()
        self.site.logout()
        self.test_003_verify_inplay_tabs_live_now_upcoming_events_sections_dataloads_with_appropriate_data()
        current_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}/{self.target_uri}'
        self.assertEqual(current_url, expected_url, msg=f'actual url "{current_url}" is not same as expected url "{expected_url}"')
