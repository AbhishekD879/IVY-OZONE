import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.other
@pytest.mark.featured
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.uat
@vtest
class Test_C44870167_Verify_In_play_and_Featured_modules_on_Highlights_tab(Common):
    """
    TR_ID: C44870167
    NAME: Verify In-play and Featured modules on Highlights tab
    DESCRIPTION: "Verify below functions in the featured page,
    DESCRIPTION: - InPlay module with list of Inplay(Sports/Racing) and sublisted with events.
    DESCRIPTION: - Price updates by live push
    DESCRIPTION: - Check SEE ALL  and chevron on in the tap to  navigate to correct page
    DESCRIPTION: - Verify when there is no Inplay sport, Inplay module should not be displayed
    DESCRIPTION: - Check events arranged into competition types and each type is collapsable
    DESCRIPTION: - Check highlight carousel in the featured tab (check the event navigations,bet placement)
    PRECONDITIONS: Configure Featured tab module in CMS
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True
    inplay_event_name, edp_event_name, ENTERED_INPLAY = None, None, None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Configure Featured tab module in CMS
        DESCRIPTION: User should be logged in
        EXPECTED: User should successfully logged into application
        """
        # CMS verification cannot be done on Prod
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        self.__class__.sport_name = vec.football.FOOTBALL_TITLE
        self.site.login()

    def test_001_load_application(self):
        """
        DESCRIPTION: Load Application
        EXPECTED: Application page is loaded and user is landed on Home page with Highlights tab expanded by default
        EXPECTED: For Logged in User : If user has any Private Markets, 'Your Enhanced Markets' tab will be opened by default.
        """
        self.site.wait_content_state('Homepage')

    def test_002_verify_in_play_module(self):
        """
        DESCRIPTION: Verify In-Play module
        EXPECTED: User should see the In-Play events grouped on sport type.  If there are No In-Play events, user should not see the In-Play module.
        """
        if self.is_mobile:
            if self.site.home.tab_content.has_in_play_module():
                self.__class__.ENTERED_INPLAY = True
                self.__class__.in_play_module = self.site.home.tab_content.in_play_module
                self.assertTrue(self.in_play_module.has_in_play_header(),
                                msg=f'There is no "{vec.BMA.IN_PLAY}" header on the page')
                inplay_module_items = self.in_play_module.items_as_ordered_dict
                if self.brand == 'bma':
                    sports = self.sport_name
                else:
                    sports = self.sport_name.upper()
                self.assertIn(sports, inplay_module_items.keys(),
                              msg=f'"{sports}" container is not displayed')
        else:
            inplay_module_items = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            if self.brand == 'bma':
                sports = self.sport_name.upper()
            else:
                sports = self.sport_name

            self.assertIn(sports, inplay_module_items.keys(),
                          msg=f'"{sports}" container is not displayed')

    def test_003_verify_the_price_updates_for_in_play_events(self):
        """
        DESCRIPTION: Verify the price updates for In-Play events
        EXPECTED: User should see the price updates with live push for all the listed In-Play events
        """
        # Don't have prod OB access so can't automate this step.

    def test_004_click_on_see_all_next_to_the_in_play_events(self):
        """
        DESCRIPTION: Mobile: Click on 'SEE ALL' next to the In-Play events
        NOTE: This step is applicable for mobile only, N/A for Desktop
        EXPECTED: User should navigate to the In-Play page which lists all In-Play events for different sports.
        """
        if self.is_mobile:
            if self.ENTERED_INPLAY is True:
                see_all_link = self.in_play_module.see_all_link
                self.assertTrue(see_all_link.is_displayed(),
                                msg=f'"See all" link is not located in the header of "{vec.BMA.IN_PLAY}" module')
                see_all_link.click()
                self.site.wait_content_state(state_name='in-play')

    def test_005_click_back_on_in_play_page(self):
        """
        DESCRIPTION: Mobile: Click 'Back' on In-Play page
        NOTE: This step is applicable for mobile only, N/A for Desktop
        EXPECTED: User should navigate back to the Home page.
        """
        if self.is_mobile:
            if self.ENTERED_INPLAY is True:
                self.site.back_button.click()
            self.site.wait_content_state('Homepage')

    def test_006_click_on_any_chevron_of_a_given_event(self):
        """
        DESCRIPTION: Click on any chevron of a given event
        EXPECTED: User should navigate to the corresponding event Landing page
        """
        if self.ENTERED_INPLAY is True:
            if self.is_mobile:
                in_play_section = self.site.home.tab_content.in_play_module.items_as_ordered_dict
                self.assertTrue(in_play_section, msg=f'{in_play_section} is blank')
                for sport in in_play_section.keys():
                    sport_section = in_play_section.get(sport)
                    self.assertTrue(sport_section, msg=f'"{sport}" section not found')
                    events = sport_section.items_as_ordered_dict
                    self.assertTrue(events, msg=f'No events were found under "{sport}" section')
                    event_list = list(events.values())
                    for event in event_list:
                        self.inplay_event_name = event.name
                        event.more_markets_link.click()
                        self.site.wait_content_state(state_name='EventDetails')
                        self.edp_event_name = self.site.sport_event_details.event_name_team_home + ' V ' + \
                            self.site.sport_event_details.event_name_team_away
                        break
                    break
            else:
                in_play_section = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
                for sport in in_play_section.keys():
                    sport_section = in_play_section.get(sport)
                    self.assertTrue(sport_section, msg=f'"{sport}" section not found')
                    leagues = self.site.home.tab_content.accordions_list.items_as_ordered_dict
                    self.assertTrue(leagues, msg=f'Sports :{sport_section} has no leagues :{leagues} in it')
                    for league in leagues.keys():
                        league = leagues.get(league)
                        events = league.items_as_ordered_dict
                        self.assertTrue(events, msg=f'No events were found under "{sport}" section')
                        event_list = list(events.values())
                        for event in event_list:
                            self.inplay_event_name = event.name.upper()
                            event.more_markets_link.click()
                            self.site.wait_content_state(state_name='EventDetails')
                            self.edp_event_name = self.site.sport_event_details.event_name_team_home + ' V ' + \
                                self.site.sport_event_details.event_name_team_away
                            break
                        break
                    break
            self.assertEqual(self.inplay_event_name.upper(), self.edp_event_name.upper(),
                             msg=f'Actual event name:"{self.inplay_event_name.upper()}" is not'
                                 f'matched with EDP event name: "{self.edp_event_name.upper()}"')

    def test_007_click_back(self):
        """
        DESCRIPTION: Click 'Back'
        EXPECTED: User should navigate back to the Home page.
        """
        if self.ENTERED_INPLAY is True:
            self.site.back_button.click()
            self.site.wait_content_state('Homepage')

    def test_008_verify_recently_played_games_carousal(self):
        """
        DESCRIPTION: verify Recently played Games carousal
        NOTE: This step is applicable for mobile only, N/A for Desktop
        EXPECTED: Recently Played Games carousal is displayed only for Logged in Users, if the user has played any games in the past
        """
        if self.is_mobile:
            if self.site.has_recently_played_games():
                self.assertTrue(self.site.recently_played_games.is_displayed(timeout=3),
                                msg='Recently Played Games Widget is not displayed!')

    def test_009_repeat_steps_1_7_for_a_logged_out_user(self):
        """
        DESCRIPTION: Repeat steps 1-7 for a logged out user
        """
        self.site.logout()
        self.test_001_load_application()
        self.test_002_verify_in_play_module()
        self.test_003_verify_the_price_updates_for_in_play_events()
        self.test_004_click_on_see_all_next_to_the_in_play_events()
        self.test_005_click_back_on_in_play_page()
        self.test_006_click_on_any_chevron_of_a_given_event()
        self.test_007_click_back()
