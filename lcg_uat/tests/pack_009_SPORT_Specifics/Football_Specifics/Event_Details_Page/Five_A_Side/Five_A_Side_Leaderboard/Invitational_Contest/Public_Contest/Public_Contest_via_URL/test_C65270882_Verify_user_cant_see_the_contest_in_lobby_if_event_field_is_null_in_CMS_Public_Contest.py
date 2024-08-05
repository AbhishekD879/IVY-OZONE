import pytest
import time
import tests
from time import sleep, time
from datetime import datetime
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.bet_placements
@pytest.mark.event_details
@pytest.mark.five_a_side_leaderboard
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.login
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.cms
@pytest.mark.banach
@vtest
class Ttest_C65270882_Verify_user_cant_see_the_contest_in_lobby_if_event_field_is_null_in_CMS_Public_Contest(BaseFiveASide, BaseFeaturedTest):
    """
    TR_ID: C65270882
    NAME: Verify user cann't see the contest in lobby if event field is null in CMS - Public Contest
    DESCRIPTION: Verify user cann't see the contest in lobby if event field is null in CMS - Public Contest
    PRECONDITIONS: Below contest should be created in CMS:
    PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: {blank}
    PRECONDITIONS: Size: 2
    PRECONDITIONS: Teams: 1
    PRECONDITIONS: User's Allowed: Test Account
    PRECONDITIONS: Invitational Contest : True
    PRECONDITIONS: Invitational Contest Display : Public (True)
    PRECONDITIONS: Capture the Contest Id
    PRECONDITIONS: In Fronend:
    PRECONDITIONS: Navigate to private contest via URL(https://beta-sports.ladbrokes.com/5-a-side/leaderboard/{contest-id}) by using contest-id or take the URL from Contest URL    PRECONDITIONS: field in CMS
    PRECONDITIONS: Click on Build Team
    """
    keep_browser_open = True
    proxy = None
    stake_value = 1
    sport_id = {'homepage': 0}
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
        DESCRIPTION: Below contest should be created in CMS:
        DESCRIPTION: Contest name: {Team1}vs{Team2}(event id)
        DESCRIPTION: Stake: 1
        DESCRIPTION: Event: {blank}
        DESCRIPTION: Size: 2
        DESCRIPTION: Teams: 1
        DESCRIPTION: User's Allowed: Test Account
        DESCRIPTION: Invitational Contest : True
        DESCRIPTION: Invitational Contest Display : Public (True)
        DESCRIPTION: Capture the Contest Id
        DESCRIPTION: In Fronend:
        DESCRIPTION: Navigate to private contest via URL(https://beta-sports.ladbrokes.com/5-a-side/leaderboard/{contest-id}) by using contest-id or take the URL from Contest URL    DESCRIPTION: field in CMS
        DESCRIPTION: Click on Build Team
        """
        self.__class__.quick_link_name = "Autotest_" + str(round(time()))
        if self.device_type != 'desktop':
            if not self.is_quick_links_enabled():
                raise CmsClientException('"Quick links" module is disabled')
            if self.is_quick_link_disabled_for_sport_category(sport_id=self.sport_id.get('homepage')):
                raise CmsClientException('"Quick links" module is disabled for homepage')
            now = datetime.now()
            time_format = '%Y-%m-%dT%H:%M:%S.%f'
            date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                days=-1,
                                                minutes=-1)[:-3] + 'Z'
            date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                              days=3)[:-3] + 'Z'
            self.cms_config.create_quick_link(title=self.quick_link_name,
                                              sport_id=self.sport_id.get('homepage'),
                                              destination=self.destination_url,
                                              date_from=date_from, date_to=date_to)
        time_format = self.event_card_future_time_format_pattern
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        market_name = vec.yourcall.MARKETS.player_bets
        event_name = normalize_name(event_resp[0]['event']['name'])
        event_start_time = event_resp[0]['event']['startTime']
        event_start_time_local = self.convert_time_to_local(
            date_time_str=event_start_time,
            ob_format_pattern=self.ob_format_pattern,
            future_datetime_format=time_format,
            ss_data=True)
        full_event_name = f'{event_name} {event_start_time_local}'
        self._logger.info(
            f'***Found Football event "{event_id}" "{full_event_name}" with market name "{market_name}", '
            f'event id "{event_name}", event start time "{event_start_time_local}"')
        self.cms_config.enable_disable_show_down_overlay(enabled=False)
        self.__class__.contest_name = f"Auto test " + event_name + "_" + str(event_id) + "_" + str(round(time()))
        self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name,
                                                     entryStake=1, size="2", teams="1",
                                                     display=True,
                                                     isInvitationalContest=True, isPrivateContest=True)
        self.site.login(username=tests.settings.betplacement_user)

    def test_001_navigate_to_lobby(self):
        """
        DESCRIPTION: Navigate to Lobby.
        EXPECTED: Contest should not be displayed on Lobby Page.
        """
        if self.device_type == 'mobile':
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            self.assertIn(self.quick_link_name, list(quick_links.keys()),
                          msg=f'Can not find "{self.quick_link_name}" in "{list(quick_links.keys())}"')
            quick_links.get(self.quick_link_name).click()
        else:
            self.site.header.sport_menu.items_as_ordered_dict.get('LOBBY').click()
        self.site.wait_content_state_changed(timeout=20)
        sleep(6)
        section = self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict
        self.assertNotIn(self.contest_name, section.keys(), msg="In active Contest is displayed")
