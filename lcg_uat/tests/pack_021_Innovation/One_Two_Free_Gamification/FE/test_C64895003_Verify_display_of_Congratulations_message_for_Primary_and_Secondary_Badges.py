import voltron.environments.constants as vec
import pytest
import datetime as dt
from voltron.utils.helpers import do_request
from time import sleep
from crlat_cms_client.utils.exceptions import CMSException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.utils.helpers import get_response_url


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.one_two_free
@pytest.mark.one_two_free_gamification
@pytest.mark.reg165_fix
@vtest
# This TestCase Covers C64894998, C64894999, C65221825, C65268978, C65581390
class Test_C64895003_Verify_display_of_Congratulations_message_for_Primary_and_Secondary_Badges(Common):
    """
    TR_ID: C64895003
    NAME: Verify display of Congratulations message for Primary and Secondary Badges
    DESCRIPTION: This test case verifies display of Congratulations message for primary and secondary badges
    DESCRIPTION: Creating Game View/Season/Gamification in CMS
    DESCRIPTION: Verifies the My Badges tab in UI before and after login
    DESCRIPTION: Verifies 'My Badges' tab view as per the zeplin designs
    DESCRIPTION: Verifies Primary and Secondary badges Popup on UI as per the number of badges configured in CMS
    DESCRIPTION: Verifies Primary and Secondary Badges display in My Badges tab on UI as per the events configured in CMS
    DESCRIPTION: Verifies the Non PL teams display on UI as per the configuration in CMS
    PRECONDITIONS: My Badges and Season should be configured in CMS
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    pl_checkbox = [[True, False], [False, False], [False, False]]
    cms_game_scores = [[1, 0], [1, 1], [1, 0]]


    def create_game(self, active_season):
        """
        Description: Create Game View
        """
        game_response = self.cms_config.create_gameView(active_season.get('id'))
        game_id = game_response.get('id')
        self.navigate_to_page('/competitions/football/english/premier-league', timeout=10)
        event_to_outcome_response = get_response_url(self,
            'EventToOutcomeForType/442?simpleFilter=event.eventSortCode:notIntersects')
        sportsbook_api_response = do_request(method='GET',
                                             url=event_to_outcome_response.rstrip('childCount=event')[:-1])["SSResponse"]["children"]
        if not event_to_outcome_response:
            raise SiteServeException('No event data available for english premier league for football sport')
        english_premier_league_event_id_list = []
        for event_data in sportsbook_api_response:
            try:
                event_id = event_data['event']['id']
                english_premier_league_event_id_list.append(event_id)
            except KeyError:
                continue
        self.cms_config.add_prediction_to_game_view(game_id, english_premier_league_event_id_list, pl_checkbox=self.pl_checkbox)
        game_response = self.cms_config.update_game_view_status(game_id, enabled=True)
        self.__class__.event_Ids = [event["eventId"] for event in game_response["events"]]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create the Game View, Season, Gamification in CMS
        """
        one_two_free_my_badges = self.cms_config.get_one_two_free_my_badges()
        if not one_two_free_my_badges['viewBadges'] or not one_two_free_my_badges['lastUpdatedFlag']:
            self.cms_config.update_one_two_free_my_badges(viewBadges=True, lastUpdatedFlag=True)

        flag = 0
        get_games = self.cms_config.get_games()
        self.__class__.active_game = next((game for game in get_games if
                                           game.get('enabled') is True and game.get('displayFrom') <= dt.datetime.utcnow().isoformat() <= game.get('displayTo')), None)
        if not self.active_game:
            getSeasons = self.cms_config.get_seasons()
            active_season = next((season for season in getSeasons if
                                  season.get(
                                      'displayFrom') <= dt.datetime.utcnow().isoformat() <= season.get(
                                      'displayTo')), None)
            if not active_season:
                inactive_season = next((season for season in getSeasons if
                                        (int(season.get('displayFrom').split("-")[2].split('T')[
                                         0]) <= dt.datetime.utcnow().day <= int(season.get('displayTo').split("-")[2].split('T')[0])) and
                                        (int(season.get('displayFrom').split("-")[1]) <= dt.datetime.utcnow().month <= int(season.get('displayTo').split("-")[1]))),
                                       None)
                if inactive_season:
                    if inactive_season.get('gamificationLinked'):
                        get_gamification = self.cms_config.get_gamification()
                        inactive_gamification = next((gamification for gamification in get_gamification if
                                                      gamification.get('seasonName') == inactive_season.get(
                                                          'seasonName')), None)
                        self.cms_config.delete_gamification(inactive_gamification.get('id'))
                    self.cms_config.delete_season(inactive_season.get('id'))
                active_season = self.cms_config.create_season()
                flag = 1
            get_gamification = self.cms_config.get_gamification()
            self.__class__.active_gamification = next((gamification for gamification in get_gamification if
                                                       gamification.get('seasonName') == active_season.get('seasonName') and
                                                       gamification.get('displayFrom') <= dt.datetime.utcnow().isoformat() <= gamification.get('displayTo')), None)
            if flag == 0 and not self.active_gamification:
                raise CMSException("There is already active season.So gamification cannot be created")
            if not self.active_gamification and flag == 1:
                self.active_gamification = self.cms_config.create_gamification(active_season.get('id'))
            if flag == 1 and self.active_gamification:
                self.cms_config.update_season(active_season)
        else:
            self.cms_config.delete_game_view(self.active_game.get('id'))
            getSeasons = self.cms_config.get_seasons()
            active_season = next((season for season in getSeasons if
                                  season.get(
                                      'displayFrom') <= dt.datetime.utcnow().isoformat() <= season.get(
                                      'displayTo')), None)
            get_gamification = self.cms_config.get_gamification()
            self.__class__.active_gamification = next((gamification for gamification in get_gamification if
                                                       gamification.get('seasonName') == active_season.get(
                                                           'seasonName') and
                                                       gamification.get(
                                                           'displayFrom') <= dt.datetime.utcnow().isoformat() <= gamification.get(
                                                           'displayTo')), None)
        self.create_game(active_season)

    def test_001_login_to_ladbrokes(self):
        """
        DESCRIPTION: Login to Ladbrokes
        EXPECTED: User should be able to login successfully
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, timeout=15)

    def test_002_click_on_1_2_free_tab(self):
        """
        DESCRIPTION: Click on '1-2 Free' tab
        EXPECTED: User should be navigated to 1-2 Free page
        """
        self.navigate_to_page('1-2-free')
        if self.device_type == 'mobile':
            one_two_free = self.site.one_two_free
            wait_for_result(lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed())
            one_two_free.one_two_free_welcome_screen.play_button.click()
        self.__class__.one_two_free = self.site.one_two_free
        wait_for_result(lambda:
                        self.one_two_free.one_two_free_current_screen.submit_button.is_enabled(
                            expected_result=True),
                        timeout=15)

    def test_003_verify_display_of_my_badges_tab(self):
        """
        DESCRIPTION: Verify display of 'My Badges' tab
        EXPECTED: User should be able to view 'My Badges' tab
        """
        self.__class__.tab_names = self.one_two_free.one_two_free_current_screen.tab_items.items_as_ordered_dict
        self.__class__.my_badges = self.cms_config.get_one_two_free_my_badges().get("label").strip()
        self.assertIn(self.my_badges, self.tab_names, msg="My Badges tab is not present in 1-2 Free")

    def test_004_click_on_my_badges_tab(self):
        """
        DESCRIPTION: Click on 'My Badges' tab
        EXPECTED: User should be able to view team jerseys
        """
        self.tab_names.get(self.my_badges).click()
        current = self.one_two_free.one_two_free_current_screen.tab_items.current
        self.assertEqual(current, self.my_badges, msg=f'Actual tab: {current} is not same as'
                         f'Expected tab: {self.my_badges}')

    def test_005_trigger_number_of_primary_badges_collected_by_the_user_is_equal_to_the_primary_badges_values_mentioned_in_cms(self):
        """
        DESCRIPTION: Trigger number of primary badges collected by the user is equal to the Primary Badges values mentioned in CMS
        EXPECTED:
        """
        tab_name_configuration = self.cms_config.get_one_two_free_tab_name_configuration()
        self.__class__.current_tab_label = tab_name_configuration["currentTabLabel"].strip().upper()
        self.tab_names.get(self.current_tab_label).click()
        match = list(self.one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())
        for score in match:
            score_switchers = score.score_selector_container.items
            for score_switcher in score_switchers:
                self.assertTrue(score_switcher.increase_score_up_arrow.is_displayed(),
                                msg=f'Upper arrow not displayed for "{score.name}".')
                score_switcher.increase_score_up_arrow.click()
                sleep(1)
                actual_score = score_switcher.score
                self.assertEqual(actual_score, '1',
                                 msg=f'Actual Score "{actual_score}" is not the same as expected "1"')
                break

        self.one_two_free.one_two_free_current_screen.submit_button.click()
        self.one_two_free.one_two_free_you_are_in.view_my_badge_button.click()

    def test_006_verify_display_of_primary_congratulations_message(self):
        """
        DESCRIPTION: Verify display of Primary congratulations message
        EXPECTED: Primary congratulations message should be displayed as per the message configured in CMS
        """
        primary_numberOfBadges = self.active_gamification['badgeTypes'][0]['numberOfBadges']
        secondary_numberOfBadges = self.active_gamification['badgeTypes'][1]['numberOfBadges']
        PLTeam_Count = 0
        for pl_check in self.pl_checkbox:
            PLTeam_Count = PLTeam_Count + pl_check.count(True)
        sleep(2)
        get_games = self.cms_config.get_games()
        active_game = next((game for game in get_games if
                            game.get('enabled') is True and game.get(
                                'displayFrom') <= dt.datetime.utcnow().isoformat() <= game.get(
                                'displayTo')), None)
        ui_primary_badges = ((len(active_game['events']) + 2) - PLTeam_Count)
        if primary_numberOfBadges <= ui_primary_badges:
            dialog = self.one_two_free.primary_badge_popup
            self.assertTrue(dialog.description, msg="Primary Badge Popup description is not appeared")
            dialog.exit_button.click()
        self.tab_names.get(self.current_tab_label).click()

        self.cms_config.set_score_for_event(active_game.get('id'), self.event_Ids[0], 0, self.cms_game_scores[0])
        self.cms_config.set_score_for_event(active_game.get('id'), self.event_Ids[1], 1, self.cms_game_scores[1])
        self.cms_config.set_score_for_event(active_game.get('id'), self.event_Ids[2], 2, self.cms_game_scores[2])
        get_scores = []
        for eventId in self.event_Ids:
            get_scores.append(self.cms_config.get_score_of_event(eventId))
        ui_scores = [[1, 0], [1, 0], [1, 0]]
        self.__class__.primaryTeams = []
        self.__class__.secondaryTeams = []
        self.__class__.nonPLTeam = []
        count = 0
        for i in range(0, len(active_game['events'])):
            self.primaryTeams.append(active_game['events'][i]['home']['name'])
            self.primaryTeams.append(active_game['events'][i]['away']['name'])
            if ui_scores[count] == get_scores[count]:
                if active_game['events'][i]['home']['isNonPLTeam']:
                    self.nonPLTeam.append(active_game['events'][i]['home']['name'])
                else:
                    self.secondaryTeams.append(active_game['events'][i]['home']['name'])
                if active_game['events'][i]['away']['isNonPLTeam']:
                    self.nonPLTeam.append(active_game['events'][i]['away']['name'])
                else:
                    self.secondaryTeams.append(active_game['events'][i]['away']['name'])
            count = count + 1
        for pl_team in self.nonPLTeam:
            if pl_team in self.primaryTeams:
                self.primaryTeams.remove(pl_team)
        self.device.refresh_page()
        tab_names = self.one_two_free.one_two_free_current_screen.tab_items.items_as_ordered_dict
        tab_names.get(self.my_badges).click()
        if secondary_numberOfBadges <= (len(self.secondaryTeams) - len(self.nonPLTeam)):
            dialog = self.site.one_two_free.secondary_badge_popup
            self.assertTrue(dialog.description, msg="Primary Badge Popup description is not appeared")
            dialog.exit_button.click()

    def test_007_trigger_number_of_secondary_badges_collected_by_the_user_is_equal_to_the_secondary_badges_values_mentioned_in_cms(self):
        """
        DESCRIPTION: Trigger number of secondary badges collected by the user is equal to the secondary Badges values mentioned in CMS
        EXPECTED: Secondary congratulations message should be displayed as per the message configured in CMS
        """
        self.assertTrue(self.one_two_free.one_two_free_current_screen.my_badges.last_updated, msg="Last Updated date is not displayed")
        self.assertTrue(self.one_two_free.one_two_free_current_screen.my_badges.my_badges_text, msg="My Badges description is not displayed")
        team_names = self.one_two_free.one_two_free_current_screen.my_badges.items_as_ordered_dict
        for key, value in team_names.items():
            self.assertTrue(value.silk_icon, msg="Team image is not displayed")
            if key in self.primaryTeams:
                self.assertTrue(value.primary_silk, msg=f'"Primary silk badge is not tagged for {key}"')
            if key in self.secondaryTeams:
                self.assertTrue(value.secondary_silk, msg=f'"Secondary Silk badge is not tagged for {key}"')
            if value.name in self.nonPLTeam:
                self.assertIsNone(value.primary_silk, msg=f'"Primary silk badge is tagged to PL Team {key}"')
                self.assertIsNone(value.secondary_silk, msg=f'"Secondary silk badge is tagged to PL Team {key}"')

    def test_008_verify_the_view_of_my_badges_tab(self):
        """
        DESCRIPTION: Verify the view of 'My Badges' tab
        EXPECTED: Design of My Badges tab should be as per the zeplin
        EXPECTED: https://app.zeplin.io/project/5b5f6d56008921750a2b9a82
        """
        my_badges = self.site.one_two_free.one_two_free_current_screen.my_badges.my_badges_element
        self.assertIn(vec.onetwofree.MY_BADGES_FONT_FAMILY, my_badges.css_property_value('font-family'),
                      msg='Font family not matched')
        self.assertEqual(vec.onetwofree.MY_BADGES_FONT_SIZE, my_badges.css_property_value('font-size'),
                         msg='Font size not matched')
        self.assertEqual(vec.onetwofree.MY_BADGES_FONT_WEIGHT, my_badges.css_property_value('font-weight'),
                         msg='Font weight not matched')
        self.assertEqual(vec.onetwofree.MY_BADGES_FONT_STYLE, my_badges.css_property_value('font-style'),
                         msg='Font style not matched')

    def test_009_verify_the_font_color_and_dimensions_of_terms_conditions_displayed_in_the_my_badges_tab(self):
        """
        DESCRIPTION: Verify the font, color and dimensions of Rules text displayed in the 'My Badges' tab
        EXPECTED: Font and dimensions of rules text should be as mentioned in zeplin
        """
        my_badges_text = self.site.one_two_free.one_two_free_current_screen.my_badges.my_badges_text_element
        self.assertIn(vec.onetwofree.RULES_TEXT_FONT_FAMILY, my_badges_text.css_property_value('font-family'),
                      msg='Font family not matched')
        self.assertEqual(vec.onetwofree.RULES_TEXT_FONT_SIZE, my_badges_text.css_property_value('font-size'),
                         msg='Font size not matched')
        self.assertEqual(vec.onetwofree.RULES_TEXT_FONT_WEIGHT, my_badges_text.css_property_value('font-weight'),
                         msg='Font weight not matched')
        self.assertEqual(vec.onetwofree.RULES_TEXT_FONT_STYLE, my_badges_text.css_property_value('font-style'),
                         msg='Font style not matched')

    def test_010_logout_from_the_ladbrokes_application(self):
        """
        DESCRIPTION: Logout from the Ladbrokes application
        EXPECTED: User should be able to logout successfully
        """
        self.site.logout()

    def test_011_click_on_1_2_free_tab(self):
        """
        DESCRIPTION: Click on '1-2 Free' tab
        EXPECTED: User should be navigated to 1-2 Free page
        """
        self.navigate_to_page('1-2-free')
        self.site.wait_content_state('1-2-free')

    def test_012_verify_display_of_my_badges_tab(self):
        """
        DESCRIPTION: Verify display of 'My Badges' tab
        EXPECTED: 'My Badges' tab should not be displayed to the user
        """
        self.assertTrue(self.site.one_two_free.login_to_play_button.is_displayed(),
                        msg="login to play button is not displayed")
