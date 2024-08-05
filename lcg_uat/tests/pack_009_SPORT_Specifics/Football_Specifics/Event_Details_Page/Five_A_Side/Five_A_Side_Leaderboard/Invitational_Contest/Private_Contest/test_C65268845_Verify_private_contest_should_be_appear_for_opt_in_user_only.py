import pytest
import tests
import time
import voltron.environments.constants as vec
from tests.base_test import vtest
from datetime import datetime
from time import sleep
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod  # Ladbrokes Only
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.five_a_side_leaderboard
@vtest
class Test_C65268845_Verify_private_contest_should_be_appear_for_opt_in_user_only(BaseFiveASide, BaseFeaturedTest):
    """
    TR_ID: C65268845
    NAME: Verify private contest should be appear for opt-in user only
    DESCRIPTION: Verify private contest is displayed in Lobby once user is opt-in for contest
    PRECONDITIONS: Create a private contest
    """
    keep_browser_open = True
    proxy = None
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}//5-a-side/lobby'

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

    def test_000_preconditions(self):
        """
        DESCRIPTION: Contest name: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {event id}
        DESCRIPTION: Size: 1
        DESCRIPTION: Teams: 1
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: invitational Contest : True
        DESCRIPTION: Invitational Contest Display : Private (True)
        DESCRIPTION: Capture the Contest Id
        DESCRIPTION: In Fronend:Navigate to private contest via URL(https://beta-sports.ladbrokes.com/5-a-side/leaderboard/{contest-id}) by using contest-id or
        DESCRIPTION: take the URL from Contest URL field in CMS
        """
        if self.device_type != 'desktop':
            if not self.is_quick_links_enabled():
                raise CmsClientException('"Quick links" module is disabled')
            if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
                raise CmsClientException('"Quick links" module is disabled for homepage')
            self.__class__.quick_link_title = 'Autotest Beta2 Lobby' + '_C65268845'
            date_from = self.get_current_time()
            self.cms_config.create_quick_link(title=self.quick_link_title,
                                              sport_id=self.homepage_id.get('homepage'),
                                              destination=self.destination_url,
                                              date_from=date_from)
        time_format = self.event_card_future_time_format_pattern
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        market_name = vec.yourcall.MARKETS.player_bets
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        event_start_time = event_resp[0]['event']['startTime']
        self.__class__.event_start_time_local = self.convert_time_to_local(
            date_time_str=event_start_time,
            ob_format_pattern=self.ob_format_pattern,
            future_datetime_format=time_format,
            ss_data=True)
        self.__class__.full_event_name = f'{self.event_name} {self.event_start_time_local}'
        self._logger.info(
            f'***Found Football event "{event_id}" "{self.full_event_name}" with market name "{market_name}", '
            f'event id "{self.event_name}", event start time "{self.event_start_time_local}"')
        # Creating contest
        self.cms_config.enable_disable_show_down_overlay(enabled=False)
        self.__class__.contest_name = f"Auto test " + self.event_name + " " + "C65268845"
        contest = self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name, entryStake="0.10",
                                                               size="1",
                                                               teams="1", event_id=event_id,
                                                               isInvitationalContest=True, isPrivateContest=True)
        contest_id = contest['id']
        contest_url = f'{tests.HOSTNAME}/5-a-side/leaderboard/{contest_id}'
        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.user_balance = self.get_balance_by_page('all')
        self.__class__.user_currency = self.site.header.user_balance_section.currency_symbol
        self.device.navigate_to(url=contest_url)
        sleep(10)
        self.site.wait_content_state_changed(timeout=20)

    def test_001_log_in_to_applicaion(self, opt_in=True):
        """
        DESCRIPTION: log in to application
        DESCRIPTION: Navigate to lobby
        EXPECTED: 1.User should be logged in
        EXPECTED: 2.On Lobby page created contest should appear
        """
        # Adding sleep, since contest will take some time to reflect on lobby
        sleep(20)
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')
        if self.device_type == 'mobile':
            featured_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
            self.site.home.module_selection_ribbon.tab_menu.click_button(featured_tab)
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            self.assertIn(self.quick_link_title, list(quick_links.keys()),
                          msg=f'Can not find "{self.quick_link_title}" in "{list(quick_links.keys())}"')
            quick_links.get(self.quick_link_title).click()
        else:
            self.site.header.sport_menu.items_as_ordered_dict.get('LOBBY').click()
        self.site.wait_content_state_changed(timeout=20)
        result = wait_for_result(
            lambda: self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict,
            timeout=20)
        self.assertTrue(result,
                        msg=f'"Lobby page is not displayed on UI"')
        section = self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict.get(self.contest_name)
        if opt_in:
            self.assertTrue(section,
                            msg=f'Private contest: "{self.contest_name}" is not appearing on Lobby after user is Opt-in to it')
        else:
            self.assertFalse(section,
                             msg=f'Private contest: "{self.contest_name}" is appearing on Lobby after login with different user')

    def test_002_logout(self):
        """
        DESCRIPTION: log out
        DESCRIPTION: Navigate to lobby
        DESCRIPTION: Check for created contest
        EXPECTED: 1.User should be logged in
        EXPECTED: 2.On Lobby page should appear
        EXPECTED: 3:On Lobby page created contest should not appear
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(timeout=5), msg='User is not logged out.')
        # Adding sleep, since contest will take some time to reflect on lobby
        sleep(10)
        self.site.login()
        self.test_001_log_in_to_applicaion(opt_in=False)
