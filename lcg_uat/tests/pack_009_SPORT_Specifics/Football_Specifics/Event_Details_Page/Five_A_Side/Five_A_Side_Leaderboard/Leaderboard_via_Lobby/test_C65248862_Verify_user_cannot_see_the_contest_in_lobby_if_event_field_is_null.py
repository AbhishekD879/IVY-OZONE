import pytest
import tests
from datetime import datetime
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name
from time import sleep, time
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from crlat_ob_client.utils.date_time import get_date_time_as_string


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
class Test_C65248862_Verify_user_cannot_see_the_contest_in_lobby_if_event_field_is_null_in_CMS_navigation_via_lobby(BaseFiveASide, BaseFeaturedTest):
    """
    TR_ID: C65248862
    NAME: Verify user can not see the contest in lobby if event field is null in CMS - navigation via lobby
    DESCRIPTION: Verify user can not see the contest in lobby if event field is null in CMS - navigation via lobby
    PRECONDITIONS: In CMS, quick link should be configured for Lobby
    PRECONDITIONS: Homepage> Quick Links > Create Sports Quick Link.
    PRECONDITIONS: Title: {title} e.g.: Beta2 Lobby
    PRECONDITIONS: Destination: https://beta2-sports.ladbrokes.com/5-a-side/lobby
    PRECONDITIONS: Below contest should be created in CMS:
    PRECONDITIONS: Contest name: {Team1}vs{Team2}(event id)
    PRECONDITIONS: Stake: 1
    PRECONDITIONS: Event: {blank}
    PRECONDITIONS: Size: 2
    PRECONDITIONS: Teams: 1
    PRECONDITION: Display: select the checkbox
    PRECONDITION: User's Allowed: Test Accounts
    PRECONDITION: Capture the Contest Id
    """
    keep_browser_open = True
    proxy = None
    stake_value = 1
    sport_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}//5-a-side/lobby'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: In CMS, quick link should be configured for Lobby
        PRECONDITIONS: Homepage> Quick Links > Create Sports Quick Link.
        PRECONDITIONS: Title: {title} e.g.: Beta2 Lobby
        PRECONDITIONS: Destination: https://beta2-sports.ladbrokes.com/5-a-side/lobby
        PRECONDITIONS: Below contest should be created in CMS:
        PRECONDITION: Contest name: {Team1}vs{Team2}(event id)
        PRECONDITION: Stake: 1
        PRECONDITION: Event: {blank}
        PRECONDITION: Size: 2
        PRECONDITION: Teams: 1
        PRECONDITION: Display: select the checkbox
        PRECONDITION: User's Allowed: Test Accounts
        PRECONDITION: Capture the Contest Id
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
        self.__class__.contest_name = f"Auto test " + event_name + "_" + str(event_id) + "_" + str(
            round(time()))
        self.cms_config.create_five_a_side_show_down(contest_name=self.contest_name,
                                                     entryStake=self.stake_value, size="2",
                                                     teams="1",
                                                     display=True)
        self.site.login(username=tests.settings.betplacement_user)

    def test_001_Click_on_the_Lobby_from_sports_header(self):
        """
        DESCRIPTION: Click on the "LOBBY" from sports header
        EXPECTED: Created Contest should not be displayed.
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
        list_of_contests_in_lobby = self.site.lobby.leaderboard_container.lobby_section.items_as_ordered_dict
        self.assertNotIn(self.contest_name, list_of_contests_in_lobby, msg='created contest is displayed in the lobby')
