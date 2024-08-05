import re

import voltron.environments.constants as vec
from crlat_ob_client.utils.waiters import wait_for_result
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest


class BaseFiveASide(BaseBanachTest):
    stat_keys = ['stat1', 'stat2', 'stat3', 'stat4', 'stat5']
    stake_value = 0.5
    time_format = '%H:%M, %d %b'

    @classmethod
    def custom_setUp(cls, **kwargs):
        five_a_side_config = cls.get_initial_data_system_configuration().get('FiveASide')
        if not five_a_side_config:
            five_a_side_config = cls.get_cms_config().get_system_configuration_item('FiveASide')
        if not five_a_side_config.get('enabled'):
            raise CmsClientException('5-A-Side is disabled in CMS')

    def get_web_socket_response(self, response_id):
        """
        Get Web Socket response info based on required response ID
        """
        response = wait_for_result(lambda: self.get_web_socket_response_by_id(response_id=response_id, delimiter='42'),
                                   name=f'WS message with code {response_id} to appear',
                                   timeout=30,
                                   poll_interval=1)
        self.assertTrue(response, msg=f'Response with frame ID #"{response_id}" not received')
        return response

    def convert_outcome_names(self, outcomes_list) -> list:
        """
        Convert outcome names for Open Bets
        :param outcomes_list: 5-A-Side outcomes list
        :return: list of converted outcome names
        """
        converted_outcomes = []
        for outcome in outcomes_list:
            name = 'To Have'
            if name not in outcome:
                name = 'To Make'
            num = ''.join(re.findall(r'\d*\+', outcome))
            market = re.split(r'\d*\+', outcome)[1].strip(' ')
            player = outcome.split(name)[0].split('.')[1].strip(' ')
            converted_outcomes.append(f' {player} {name} {num} {market}')
        return converted_outcomes

    def open_players_list(self, market, market_name) -> dict:
        """
        Open and get Players list
        :param market: 5-A-Side market container
        :param market_name: 5-A-Side market name
        :return: dictionary which contains all players from players list
        """
        market.icon.click()
        self._logger.info(f'Selecting players for market "{market_name}"')
        tab_content = self.site.sport_event_details.tab_content
        self.assertTrue(tab_content.wait_for_players_overlay(),
                        msg='Players Overlay is not shown')
        if market.added_player_name != 'Keeper':
            switchers = tab_content.players_overlay.switchers.items_as_ordered_dict
            self.assertTrue(switchers, msg='Cannot find Players switchers on the Players Overlay')
            home_switcher = switchers.get(vec.five_a_side.HOME_SWITCHER)
            self.assertTrue(home_switcher, msg=f'Switcher "{vec.five_a_side.HOME_SWITCHER}" '
                                               f'not found among switchers: "{switchers.keys()}')
            home_switcher.click()
            self.assertTrue(home_switcher.is_selected(timeout=10), msg='Home switcher is not selected')
        return self.site.sport_event_details.tab_content.players_overlay.players_list.items_as_ordered_dict
