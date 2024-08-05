import re
import requests
from collections import namedtuple, OrderedDict
from collections.abc import KeysView, ValuesView, ItemsView
from crlat_ob_client import BackEndSettings
from crlat_ob_client.login import OBLogin
from crlat_ob_client.utils.date_time import get_date_time_object, get_date_time_as_string
from crlat_ob_client.utils.exceptions import OBException
from crlat_ob_client.utils.helpers import generate_name, check_status_code, do_request
from random import randint
from lxml import html

from crlat_ob_client.utils.waiters import wait_for_result
from requests import ReadTimeout

try:
    from urllib import quote, unquote_plus  # Python 2.X
except ImportError:
    from urllib.parse import quote, unquote_plus  # Python 3+


class CreateSportEvent(OBLogin):
    def __init__(self, env, brand, category_id, class_id, type_id, market_template_id=None, market_name=None, *args, **kwargs):
        super(CreateSportEvent, self).__init__(env, brand, *args, **kwargs)
        self.ss_timeout = self.backend.siteserve.general_info.timeout
        self.ss_version = kwargs.get('ss_version', '2.31')
        self.backend = BackEndSettings(backend=env, brand=self.brand)
        self.football_config = self.backend.ti.football
        self.tennis_config = self.backend.ti.tennis
        self.horseracing_config = self.backend.ti.horse_racing
        self.category_id = category_id
        self.class_id = class_id
        self.type_id = type_id
        self.market_template_id = market_template_id
        self.market_name = market_name
        self.team1_name = None
        self.team2_name = None
        self.eventID = None
        self.marketID = None
        self.selectionID = None
        self.default_ew_terms = {'ew_places': 3, 'ew_fac_num': 1, 'ew_fac_den': 8}
        self.prices = OrderedDict([('odds_home', '1/2'),
                                   ('odds_draw', '3/2'),
                                   ('odds_away', '4/1')])
        self.other_sport_prices = OrderedDict([('odds_home', '1/2'),
                                               ('odds_away', '4/1')])
        self.correct_score_prices = [
            ('home', {
                '1-0': '1/5',
                '2-1': '2/7',
                '3-1': '1/4',
                '2-0': '1/5'
            }),
            ('away', {
                '1-0': '1/8',
                '2-1': '5/1',
                '3-1': '3/7',
                '2-0': '1/17',
            }),
            ('Draw', {
                '0-0': '1/9',
                '1-1': '1/16',
                '2-2': '2/23'
            })
        ]

    def _find_disporder_for_market(self, market_template_id):
        """
        Find disporder for market by template id
        :param market_template_id: market template id
        :return: disporder for market
        """
        from crlat_siteserve_client.siteserve_client import SiteServeRequests, query_builder, debug_filter
        s = SiteServeRequests(env=self.env, class_id=self.class_id, version=self.ss_version,
                              category_id=self.category_id, brand=self.brand)
        resp = s.ss_class_to_template_market_for_type(type_id=self.type_id,
                                                      query_builder=query_builder().add_filter(debug_filter(value='all')),
                                                      raise_exceptions=False)
        disporder = None
        try:
            market_templates = resp[0]['class']['children'][0]['type']['children']
            for market in market_templates:
                if market['templateMarket']['id'] == str(market_template_id):
                    disporder = market['templateMarket']['displayOrder']
        except (KeyError, IndexError):
            pass
        if disporder:
            return disporder
        rnd_disporder = randint(100, 5000)
        self._logger.warning(f'Disporder for market with template id "{market_template_id}" was not found, '
                             f'setting random disporder "{rnd_disporder}"')
        return rnd_disporder

    def create_event(self, is_off=None, is_upcoming=False, is_live=False, is_tomorrow=False,
                     cashout=True, **kwargs):
        """
        :kwargs: score handball format for example: "score = {'current': '25-18'}"
        expected: "Dinamik Genclik 25-18 Cevhertepe"
        :kwargs: score and set for valleyball format for example: "score = {'current': '25-18', 'set': '(2):(0)'}
        expected: "Dinamik Genclik (2) 25-18 (0) Cevhertepe"
        """
        url = '{0}/hierarchy/type/{1}'.format(self.site, self.type_id)
        max_bet = kwargs['max_bet'] if 'max_bet' in kwargs else ''
        max_mult_bet = kwargs['max_mult_bet'] if 'max_mult_bet' in kwargs else ''
        min_bet = kwargs['min_bet'] if 'min_bet' in kwargs else ''
        sort = kwargs.get('sort', 'MTCH')

        at_time_string = get_date_time_as_string(time_format='%Y-%m-%d %H:%M:%S', days=1)
        suspend_at = kwargs.get('suspend_at', at_time_string)

        bir_delay = kwargs.get('bir_delay', '2')
        if 'start_time' in kwargs and kwargs['start_time']:
            if self.brand == 'bma':
                event_date_time = quote(kwargs['start_time'])
            else:
                event_date_time = kwargs['start_time']
        else:
            time_format = '%Y-%m-%d %H:%M:%S'
            if self.brand == 'bma':
                event_date_time = get_date_time_as_string(time_format=time_format, url_encode=True) if is_live \
                    else get_date_time_as_string(days=1, hours=1, time_format=time_format, url_encode=True) if is_tomorrow \
                    else get_date_time_as_string(hours=3, time_format=time_format, url_encode=True) if is_upcoming \
                    else get_date_time_as_string(hours=1, minutes=randint(10, 59), time_format=time_format, url_encode=True)
            else:
                event_date_time = get_date_time_as_string(time_format=time_format) if is_live \
                    else get_date_time_as_string(days=1, hours=1, time_format=time_format) if is_tomorrow \
                    else get_date_time_as_string(hours=3, time_format=time_format) if is_upcoming \
                    else get_date_time_as_string(hours=1, minutes=randint(10, 59), time_format=time_format)

        is_off_value = 'Y' if is_live else 'N'
        flag_BL_value = 'Y' if is_live or is_upcoming else 'N'
        flag_NE_value = 'Y' if is_upcoming else 'N'
        flag_ES_value = 'Y' if self.type_id == '2297' else 'N'
        flag_DYW_value = 'N'
        flag_YC_value = 'N'
        flag_RD_value = 'N'
        flag_AVA_value = 'Y' if sort == 'TNMT' else 'N'
        flag_FI_value = kwargs.get('flag_FI','Y')
        flags = 'FI'
        if self.brand == 'bma' and flag_AVA_value == 'Y':
            flags += ',AVA'
        channel_I_value, channel_Q_value = 'Y', 'Y'
        channels_list = 'IPCMQ'
        tv_flags_list = 'AVA%2CFI%2CINT%2CIVA%2CPVA%2CUK%2C'
        flags += ',BL' if is_live or is_upcoming else ''
        flags += ',NE' if is_upcoming else ''
        if 'img_stream' in kwargs and kwargs['img_stream']:
            flag_AVA_value, flag_IVM_value, flag_RD_value, flag_FI_value = 'N', 'Y', 'Y', 'N'
            channel_I_value, channel_Q_value = 'N', 'N'
            channels_list = 'PCM'
            flags += ',IVM,RD'
            tv_flags_list = 'IVA%2CPVA%2CRD'
        else:
            flag_IVM_value = 'N'
        if 'perform_stream' in kwargs and kwargs['perform_stream']:
            flag_PVM_value = 'Y'
            flag_FE_value = 'Y'
            if self.brand == 'bma':
                flag_AVA_value, flag_NE_value, flag_FI_value = 'Y', 'Y', 'N'
                additional_flags = [',AVA', ',FE', ',NE', ',PVM']
                for additional_flag in additional_flags:
                    if additional_flag not in flags:
                        flags += additional_flag
                flags = flags.replace('FI,', '')
            else:
                flag_NE_value = 'N'
                flags += ',FE,PVM'
        else:
            flag_PVM_value = 'N'
            flag_FE_value = 'N'

        if not is_off and not is_live:
            is_off_value = '-'
        if self.brand == 'bma':
            if 'double_your_winnings' in kwargs and kwargs['double_your_winnings']:
                flag_DYW_value = 'Y'
                flags += ',DYW'
            if 'your_call' in kwargs and kwargs['your_call']:
                flag_YC_value = 'Y'
                flags += ',YC'
        self.team1_name = kwargs.get('team1', f'Auto test {generate_name()}')
        self.team2_name = kwargs.get('team2', f'Auto test {generate_name()}')
        if self.brand == 'bma':
            name = quote('|' + self.team1_name + '| |vs| |' + self.team2_name + '|')
        else:
            name = '|' + self.team1_name + '| |vs| |' + self.team2_name + '|'
        if 'score' in kwargs:
            score = kwargs['score']
            if 'current' in score:
                if self.brand == 'bma':
                    name = quote('|' + self.team1_name + '| ' + score['current'] + ' |' + self.team2_name + '|')
                else:
                    name = '|' + self.team1_name + '| ' + score['current'] + ' |' + self.team2_name + '|'
            if 'set' in score:
                set_teams = score['set'].split(':')
                set_team_a = set_teams[0]
                set_team_b = set_teams[1]
                if self.brand == 'bma':
                    name = quote('|' + self.team1_name + '| ' + set_team_a + ' ' + score['current'] + ' '
                                 + set_team_b + ' |' + self.team2_name + '|')
                else:
                    name = '|' + self.team1_name + '| ' + set_team_a + ' ' + score['current'] + ' ' \
                           + set_team_b + ' |' + self.team2_name + '|'
        event_name = kwargs.get('event_name', name)
        cashout_available = 'Y' if cashout else 'N'
        enhanced_odds = kwargs.get('enhanced_odds', 'Y') or 'N'
        flag_mb_value = kwargs.get('money_back', 'N')
        event_disporder = kwargs.get('event_disporder', 0)
        if flag_mb_value is True:
            flag_mb_value = 'Y'
            flags += ',MB,'
        flag_pb_value = kwargs.get('price_boost', 'N')
        if flag_pb_value is True:
            flag_pb_value = 'Y'
            flags += ',PB,'

        if self.brand == 'bma':
            params = '?action=hierarchy::event::H_insert' \
                     '&id=&read_only=N&name={event_name}&type_id={type_id}' \
                     '&class_id={class_id}' \
                     '&category_name=' \
                     '&class_sort=FB' \
                     '&home_team=' \
                     '&away_team=' \
                     '&home_id=' \
                     '&away_id=' \
                     '&displayed=Y' \
                     '&disporder={event_disporder}' \
                     '&status=A' \
                     '&allow_stl=Y' \
                     '&start_time={start_time}' \
                     '&est_start_time=' \
                     '&suspend_at={suspend_at}' \
                     '&feed_updateable=-' \
                     '&bir_delay={bir_delay}' \
                     '&min_bet={min_bet}' \
                     '&max_mult_bet={max_mult_bet}' \
                     '&max_bet={max_bet}' \
                     '&sp_max_bet=' \
                     '&max_place_lp=' \
                     '&max_place_sp=' \
                     '&liability=' \
                     '&ew_factor=' \
                     '&venue=' \
                     '&country=' \
                     '&sort={sort}' \
                     '&mult_key=' \
                     '&ext_key=' \
                     '&domain=-' \
                     '&is_off={is_off}' \
                     '&sett_at_sp_from=' \
                     '&sett_at_sp_to=' \
                     '&late_bet_toll=' \
                     '&on_settl=na' \
                     '&calendar=N' \
                     '&cashout_avail={cashout}' \
                     '&enhanced_odds_avail={enhanced_odds}' \
                     '&blurb_sort=EVENT' \
                     '&blurb_language=all' \
                     '&multi_blurb_all=' \
                     '&multi_blurb_EVENT_lang_en=' \
                     '&multi_blurb_EVENT_lang_wp=' \
                     '&multi_blurb_EVENT_lang_01=' \
                     '&note_channels=P' \
                     '&note_channel_I=' \
                     '&note_channel_P=' \
                     '&note_channel_C=' \
                     '&note_channel_M=' \
                     '&note_channel_Q=' \
                     '&note_channel_D=' \
                     '&note_channel_T=' \
                     '&note_channel_G=' \
                     '&note_channel_W=' \
                     '&note_channel_J=' \
                     '&note_channel_U=' \
                     '&flag_MB={flag_mb_value}' \
                     '&flag_PB={flag_pb_value}' \
                     '&flag_FE={flag_FE_value}' \
                     '&flag_FI={flag_fi_value}' \
                     '&flag_NE={flag_NE_value}' \
                     '&flag_ST=N' \
                     '&flag_BL={flag_bl_value}' \
                     '&flag_ES={flag_es_value}' \
                     '&flag_RD={flag_rd_value}' \
                     '&flag_SP=N' \
                     '&flag_NC=N' \
                     '&flag_PVM={flag_pvm_value}' \
                     '&flag_PDM=N' \
                     '&flag_AVA={flag_ava_value}' \
                     '&flag_IVM={flag_ivm_value}' \
                     '&flag_RF=N' \
                     '&flag_ES=N' \
                     '&flag_SM=N' \
                     '&flag_RB=N&flag_BR=N&flag_BG=N&flag_IS=N&flag_IM=N&flag_SN=N&flag_CP=N&flag_ME=N&flag_MU=N' \
                     '&flag_DYW={flag_DYW_value}'\
                     '&flag_YC={flag_YC_value}'\
                     '&flags_list=' \
                     '&channel_I={ch_i_value}' \
                     '&channel_P=Y' \
                     '&channel_C=Y&channel_M=Y&channel_Q={ch_q_value}&channel_D=N&channel_T=N&channel_G=N' \
                     '&channel_U=N&channel_W=N&channel_J=N&channels_list={ch_list}&tv_channel_34=N&tv_channel_1=N' \
                     '&tv_channel_3=N&tv_channel_4=N&tv_channel_5=N&tv_channel_6=N&tv_channel_2=N' \
                     '&tv_channel_36=N&tv_channel_37=N&tv_channel_7=N&tv_channel_9=N&tv_channel_10=N' \
                     '&tv_channel_11=N&tv_channel_39=N&tv_channel_12=N&tv_channel_8=N&tv_channel_13=N' \
                     '&tv_channel_14=N&tv_channel_15=N&tv_channel_16=N&tv_channel_17=N&tv_channel_18=N' \
                     '&tv_channel_19=N&tv_channel_20=N&tv_channel_35=N&tv_channel_38=N&tv_channel_21=N' \
                     '&tv_channel_22=N&tv_channel_23=N&tv_channel_26=N&tv_channel_40=N&tv_channel_27=N' \
                     '&tv_channel_28=N&tv_channel_29=N&tv_channel_30=N&tv_channel_24=N&tv_channel_25=N' \
                     '&tv_channel_31=N&tv_channel_32=N&tv_channel_33=N&tv_flags_list={tv_flags_list}' \
                     '&flags={flags}' \
                .format(event_name=event_name, type_id=self.type_id, class_id=self.class_id, event_disporder=event_disporder, start_time=event_date_time,
                        max_bet=max_bet, max_mult_bet=max_mult_bet, min_bet=min_bet, is_off=is_off_value,
                        cashout=cashout_available, enhanced_odds=enhanced_odds, flag_bl_value=flag_BL_value, flag_mb_value=flag_mb_value, flag_pb_value=flag_pb_value,
                        flag_ivm_value=flag_IVM_value, flags=flags, tv_flags_list=tv_flags_list,
                        flag_ava_value=flag_AVA_value, flag_rd_value=flag_RD_value, flag_fi_value=flag_FI_value,
                        flag_es_value=flag_ES_value, flag_pvm_value=flag_PVM_value, ch_i_value=channel_I_value,
                        ch_q_value=channel_Q_value, ch_list=channels_list, flag_DYW_value=flag_DYW_value,
                        flag_YC_value=flag_YC_value, sort=sort, bir_delay=bir_delay, flag_NE_value=flag_NE_value,
                        flag_FE_value=flag_FE_value,
                        suspend_at=quote(suspend_at))
            url = url + params.strip(',')
            resp_dict = do_request(url=url, cookies=self.site_cookies)
        else:
            params = (
                ('action', 'hierarchy::event::H_insert'),
                ('id', ''),
                ('read_only', 'N'),
                ('name', event_name),
                ('type_id', self.type_id),
                ('class_id', self.class_id),
                ('category_name', ''),
                ('class_sort', 'FB'),
                ('home_team', ''),
                ('away_team', ''),
                ('home_id', ''),
                ('away_id', ''),
                ('displayed', 'Y'),
                ('disporder', event_disporder),
                ('status', 'A'),
                ('allow_stl', 'Y'),
                ('start_time', event_date_time),
                ('est_start_time', ''),
                ('suspend_at', suspend_at),
                ('feed_updateable', '-'),
                ('bir_delay', bir_delay),
                ('is_off', is_off_value),
                ('liability', ''),
                ('min_bet', min_bet),
                ('max_mult_bet', max_mult_bet),
                ('max_bet', max_bet),
                ('sp_max_bet', ''),
                ('max_bet_lp', kwargs.get('max_bet_lp', '')),
                ('max_place_sp', ''),
                ('least_max_bet', '1.00'),
                ('most_max_bet', kwargs.get('most_max_bet', '500000.00')),
                ('lay_to_lose', ''),
                ('ew_factor', ''),
                ('venue', ''),
                ('country', ''),
                ('sort', sort),
                ('mult_key', ''),
                ('ext_key', ''),
                ('domain', '-'),
                ('sett_at_sp_from', ''),
                ('sett_at_sp_to', ''),
                ('late_bet_toll', ''),
                ('on_settl', 'na'),
                ('calendar', 'N'),
                ('cashout_avail', cashout_available),
                ('enhanced_odds_avail', enhanced_odds),
                ('blurb_sort', 'EVENT'),
                ('blurb_language', 'all'),
                ('multi_blurb_all', ''),
                ('multi_blurb_EVENT_lang_en', ''),
                ('multi_blurb_EVENT_lang_ru', ''),
                ('multi_blurb_EVENT_lang_cn', ''),
                ('multi_blurb_EVENT_lang_it', ''),
                ('multi_blurb_EVENT_lang_es', ''),
                ('multi_blurb_EVENT_lang_sw', ''),
                ('multi_blurb_EVENT_lang_th', ''),
                ('multi_blurb_EVENT_lang_dk', ''),
                ('multi_blurb_EVENT_lang_no', ''),
                ('multi_blurb_EVENT_lang_ie', ''),
                ('multi_blurb_EVENT_lang_de', ''),
                ('multi_blurb_EVENT_lang_gr', ''),
                ('multi_blurb_EVENT_lang_fi', ''),
                ('multi_blurb_EVENT_lang_cs', ''),
                ('multi_blurb_EVENT_lang_as', ''),
                ('multi_blurb_EVENT_lang_tr', ''),
                ('multi_blurb_EVENT_lang_pt', ''),
                ('multi_blurb_EVENT_lang_oo', ''),
                ('multi_blurb_EVENT_lang_pl', ''),
                ('multi_blurb_EVENT_lang_bg', ''),
                ('multi_blurb_EVENT_lang_ro', ''),
                ('multi_blurb_EVENT_lang_ca', ''),
                ('multi_blurb_EVENT_lang_hr', ''),
                ('multi_blurb_EVENT_lang_za', ''),
                ('multi_blurb_EVENT_lang_fr', ''),
                ('multi_blurb_EVENT_lang_f2', ''),
                ('multi_blurb_EVENT_lang_sk', ''),
                ('multi_blurb_EVENT_lang_si', ''),
                ('multi_blurb_EVENT_lang_cz', ''),
                ('multi_blurb_EVENT_lang_hu', ''),
                ('multi_blurb_EVENT_lang_id', ''),
                ('multi_blurb_EVENT_lang_af', ''),
                ('note_channels', 'P'),
                ('note_channel_E', ''),
                ('note_channel_I', channel_I_value),
                ('note_channel_O', ''),
                ('note_channel_T', ''),
                ('note_channel_C', ''),
                ('note_channel_N', ''),
                ('note_channel_W', ''),
                ('note_channel_D', ''),
                ('note_channel_Z', ''),
                ('note_channel_V', ''),
                ('note_channel_P', ''),
                ('note_channel_H', ''),
                ('note_channel_L', ''),
                ('note_channel_U', ''),
                ('note_channel_F', ''),
                ('note_channel_S', ''),
                ('note_channel_X', ''),
                ('note_channel_J', ''),
                ('note_channel_Q', channel_Q_value),
                ('note_channel_R', ''),
                ('note_channel_Y', ''),
                ('note_channel_M', ''),
                ('note_channel_@', ''),
                ('note_channel_K', ''),
                ('note_channel_p', ''),
                ('note_channel_G', ''),
                ('note_channel_t', ''),
                ('note_channel_B', ''),
                ('note_channel_e', ''),
                ('note_channel_f', ''),
                ('note_channel_y', ''),
                ('note_channel_z', ''),
                ('flag_FE', flag_FE_value),
                ('flag_FI', flag_FI_value),
                ('flag_NE', flag_NE_value),
                ('flag_ST', 'N'),
                ('flag_BL', flag_BL_value),
                ('flag_RD', flag_RD_value),
                ('flag_SP', 'N'),
                ('flag_NC', 'N'),
                ('flag_PVM', flag_PVM_value),
                ('flag_PDM', 'N'),
                ('flag_GVM', 'N'),
                ('flag_IVM', flag_IVM_value),
                ('flag_RF', 'N'),
                ('flag_ES', flag_ES_value),
                ('flag_SM', 'N'),
                ('flag_RW', 'N'),
                ('flag_RB', 'N'),
                ('flag_BR', 'N'),
                ('flag_BG', 'N'),
                ('flag_IS', 'N'),
                ('flag_IM', 'N'),
                ('flag_SN', 'N'),
                ('flag_CP', 'N'),
                ('flag_ME', 'N'),
                ('flag_MU', 'N'),
                ('flag_PB', flag_pb_value),
                ('flag_MB', flag_mb_value),
                ('flag_GOP', 'N'),
                ('flag_SI', 'N'),
                ('flag_PR1', 'N'),
                ('flag_PR2', 'N'),
                ('flag_YC', flag_YC_value),
                ('flags_list', ''),
                ('channel_E', 'N'),
                ('channel_I', 'Y'),
                ('channel_O', 'N'),
                ('channel_T', 'N'),
                ('channel_C', 'Y'),
                ('channel_N', 'N'),
                ('channel_W', 'N'),
                ('channel_D', 'N'),
                ('channel_Z', 'N'),
                ('channel_V', 'N'),
                ('channel_P', 'Y'),
                ('channel_H', 'N'),
                ('channel_L', 'N'),
                ('channel_U', 'N'),
                ('channel_F', 'N'),
                ('channel_S', 'N'),
                ('channel_X', 'N'),
                ('channel_J', 'N'),
                ('channel_Q', 'Y'),
                ('channel_R', 'N'),
                ('channel_Y', 'N'),
                ('channel_M', 'Y'),
                ('channel_@', 'N'),
                ('channel_K', 'N'),
                ('channel_p', 'N'),
                ('channel_G', 'N'),
                ('channel_t', 'N'),
                ('channel_B', 'N'),
                ('channel_e', 'N'),
                ('channel_f', 'N'),
                ('channel_y', 'N'),
                ('channel_z', 'N'),
                ('channels_list', channels_list),
                ('tv_channel_34', 'N'),
                ('tv_channel_1', 'N'),
                ('tv_channel_6', 'N'),
                ('tv_channel_3', 'N'),
                ('tv_channel_5', 'N'),
                ('tv_channel_4', 'N'),
                ('tv_channel_2', 'N'),
                ('tv_channel_36', 'N'),
                ('tv_channel_37', 'N'),
                ('tv_channel_51', 'N'),
                ('tv_channel_52', 'N'),
                ('tv_channel_54', 'N'),
                ('tv_channel_7', 'N'),
                ('tv_channel_11', 'N'),
                ('tv_channel_39', 'N'),
                ('tv_channel_12', 'N'),
                ('tv_channel_8', 'N'),
                ('tv_channel_9', 'N'),
                ('tv_channel_13', 'N'),
                ('tv_channel_14', 'N'),
                ('tv_channel_15', 'N'),
                ('tv_channel_53', 'N'),
                ('tv_channel_16', 'N'),
                ('tv_channel_17', 'N'),
                ('tv_channel_18', 'N'),
                ('tv_channel_19', 'N'),
                ('tv_channel_20', 'N'),
                ('tv_channel_35', 'N'),
                ('tv_channel_38', 'N'),
                ('tv_channel_21', 'N'),
                ('tv_channel_22', 'N'),
                ('tv_channel_23', 'N'),
                ('tv_channel_24', 'N'),
                ('tv_channel_25', 'N'),
                ('tv_channel_26', 'N'),
                ('tv_channel_27', 'N'),
                ('tv_channel_28', 'N'),
                ('tv_channel_29', 'N'),
                ('tv_channel_30', 'N'),
                ('tv_channel_40', 'N'),
                ('tv_channel_47', 'N'),
                ('tv_channel_48', 'N'),
                ('tv_channel_50', 'N'),
                ('tv_channel_44', 'N'),
                ('tv_channel_46', 'N'),
                ('tv_channel_42', 'N'),
                ('tv_channel_45', 'N'),
                ('tv_channel_41', 'N'),
                ('tv_channel_49', 'N'),
                ('tv_channel_43', 'N'),
                ('tv_channel_31', 'N'),
                ('tv_channel_32', 'N'),
                ('tv_channel_33', 'N'),
                ('tv_flags_list', tv_flags_list),
                ('flags', flags)
            )
            resp_dict = do_request(url=url, params=params, cookies=self.site_cookies)

        if 'id' not in resp_dict or not resp_dict['id']:
            raise OBException('*** Create event response does not have event_id, response is: %s' % resp_dict)
        self.eventID = resp_dict['id']

        event_date_time = unquote_plus(event_date_time)
        parameters = namedtuple('event_parameters', ['eventID', 'team1_name', 'team2_name', 'event_date_time'])
        event_parameters = parameters(self.eventID, self.team1_name, self.team2_name, event_date_time)
        self._logger.debug('*** Event id is: %s' % event_parameters.eventID)
        return event_parameters

    def get_markets_for_event(self, eventID=None):
        """
        Get all available markets for event
        :param eventID: event ID
        :return: dict with in format {'market_name': market_id}
        """
        eventID = eventID if eventID else self.eventID
        params = (
            ('action', 'hierarchy::event::H_get_markets'),
            ('id', eventID)
        )

        r = do_request(url=self.site, load_response=False, params=params, cookies=self.site_cookies)

        page = html.fromstring(r)
        market_nodes = page.xpath('//*[@id="type_event_market"]/a')
        markets_dict = OrderedDict()
        for node in market_nodes:
            market_id = node.attrib['data-id']
            market_name = node.text
            self._logger.debug(f'*** Parsed market "{market_name}" and id "{market_id}"')
            markets_dict[market_name] = market_id

        return markets_dict

    def update_market_settings(self, market_id, **kwargs):
        market_template_id = kwargs.get('market_template_id', self.market_template_id)
        event_id = kwargs.get('event_id', self.eventID)
        market_display_sort_code = kwargs.get('market_display_sort_code')

        def get_settings_params(**kwargs):
            flags_values = ''
            params = []
            if 'max_mult_bet' in kwargs:
                value = kwargs.get('max_mult_bet')
                params.append(('max_multiple_bet', value))
            if 'min_bet' in kwargs:
                value = kwargs.get('min_bet')
                params.append(('min_bet', value))
            if 'max_bet' in kwargs:
                value = kwargs.get('max_bet')
                params.append(('max_bet', value))
            if 'cashout' in kwargs:
                value = 'Y' if kwargs.get('cashout') else 'N'
                params.append(('cashout_avail', value))
            if 'market_enhanced_odds' in kwargs:
                value = 'Y' if kwargs.get('market_enhanced_odds') else 'N'
                params.append(('enhanced_odds_avail', value))
            if 'bir_delay' in kwargs:
                value = kwargs.get('bir_delay')
                params.append(('bir_delay', value))
            if 'bet_in_run' in kwargs:
                value = kwargs.get('bet_in_run') if kwargs.get('bet_in_run') else 'Y'
                params.append(('bet_in_run', value))
            if 'bir_index' in kwargs:
                value = kwargs.get('bir_index')
                params.append(('bir_index', value))
            if 'ew_terms' in kwargs:
                ew_terms = kwargs.get('ew_terms')
                if ew_terms is False:
                    value = 'N'
                    params.append(('ew_avail', value))
                else:
                    each_way_terms = ew_terms if ew_terms is not None else self.default_ew_terms
                    ew_available, ew_places, ew_fac_num, ew_fac_den = \
                        'Y', each_way_terms['ew_places'], each_way_terms['ew_fac_num'], each_way_terms['ew_fac_den']
                    params.append(('ew_avail', ew_available))
                    params.append(('ew_places', ew_places))
                    params.append(('ew_fac_num', ew_fac_num))
                    params.append(('ew_fac_den', ew_fac_den))
            if 'disporder' in kwargs:
                value = kwargs.get('disporder')
                params.append(('disporder', value))
            if 'market_displayed' in kwargs:
                value = 'Y' if kwargs.get('market_displayed') else 'N'
                params.append(('displayed', value))
            if 'new_market_name' in kwargs:
                value = kwargs.get('new_market_name')
                params.append(('name', value))

            # parameters with flags are below
            if 'private' in kwargs:
                value = 'Y' if kwargs.get('private') else 'N'
                flags_values += 'PVT,'
                params.append(('flag_PVT', value))
            if 'market_money_back' in kwargs:
                value = 'Y' if kwargs.get('market_money_back') else 'N'
                flags_values += 'MB,'
                params.append(('flag_MB', value))
            if 'market_price_boost' in kwargs:
                value = 'Y' if kwargs.get('market_price_boost') else 'N'
                flags_values += 'PB,'
                params.append(('flag_PB', value))
            if 'lp_avail' in kwargs:
                value = 'Y' if kwargs.get('lp_avail') else 'N'
                params.append(('lp_avail', value))
            if 'gp_avail' in kwargs:
                value = 'Y' if kwargs.get('gp_avail') else 'N'
                params.append(('gp_avail', value))
            if 'sp_avail' in kwargs:
                value = 'Y' if kwargs.get('sp_avail') else 'N'
                params.append(('sp_avail', value))
            if flags_values:
                value = flags_values
                params.append(('flags', value))

            return params

        base_params = [
            ('action', 'hierarchy::market::H_update'),
            ('id', market_id),
            ('exact_flags', 'Y'),
            ('ev_id', event_id),
            ('ev_oc_grp_id', market_template_id),
            ('sort', market_display_sort_code),
            ('class_sort', 'FB'),
            ('ew_with_bet', 'N'),
            ('ew_avail', 'N'),
        ]

        additional_params = get_settings_params(**kwargs)
        final_params = tuple(base_params + additional_params)

        resp_dict = do_request(url=self.site, params=final_params, cookies=self.site_cookies)
        for notification_obj in resp_dict.get('notifications'):
            if 'success' not in notification_obj.get('type'):
                raise OBException(f'Cannot create multiple markets and selections. Response is:\n{resp_dict}')

    def create_multiple_markets(self, markets: list, **kwargs):
        market_params = []
        for market in markets:
            generated_params = market.build_params()
            for generated_param in generated_params:
                market_params.append(generated_param)

        data = [
            ('action', 'hierarchy::multiple_markets::H_insert'),
            ('home_team_name', kwargs.get('team1', self.team1_name)),
            ('away_team_name', kwargs.get('team2', self.team2_name)),
            ('home_team_id', ''),
            ('away_team_id', ''),
            ('event_id', kwargs.get('event_id', self.eventID)),
            ('class_sort', 'FB')
        ]

        params = tuple(data + market_params)

        resp_dict = do_request(url=self.site, params=params, cookies=self.site_cookies)
        for notification_obj in resp_dict.get('notifications'):
            if 'success' not in notification_obj.get('type'):
                raise OBException(f'Cannot create multiple markets and selections. Response is:\n{resp_dict}')

    def create_market(self, bet_in_run='Y', cashout=True, bir_index=3, **kwargs):
        """
        :param bet_in_run: N or Y
        :param cashout: either True or False
        :param bir_index:
        :param kwargs: event_id is expected if this is not default event's market
        :param kwargs: market_name is expected if this is not default event's market
        :param kwargs: market_template_id is expected if this is not default event's market
        :param kwargs: private: either True or False.
        :param kwargs: class_id is expected if create event to already existing event
        :return: marketID
        """
        market_name = kwargs['market_name'] if 'market_name' in kwargs else self.market_name
        market_template_id = kwargs['market_template_id'] if 'market_template_id' in kwargs else self.market_template_id
        class_id = kwargs['class_id'] if 'class_id' in kwargs else self.class_id
        event_id = kwargs['event_id'] if 'event_id' in kwargs else self.eventID
        ew_terms = kwargs.get('ew_terms', False)
        bir_delay = kwargs.get('bir_delay', '2')
        flags = ''
        over_under = kwargs['over_under'] if 'over_under' in kwargs.keys() else 2.5
        handicap = kwargs['handicap'] if 'handicap' in kwargs.keys() else 5
        is_over_under = kwargs['is_over_under'] if 'is_over_under' in kwargs.keys() else False
        disporder = kwargs['disporder'] if 'disporder' in kwargs.keys() \
            else self._find_disporder_for_market(market_template_id)
        market_displayed = 'N' if 'market_displayed' in kwargs.keys() and kwargs['market_displayed'] is False else 'Y'

        private = 'Y' if 'private' in kwargs.keys() and kwargs['private'] is True else 'N'
        flags = flags + '&flags=PVT,' if 'private' in kwargs.keys() and kwargs['private'] is True else flags
        flag_mb_value = kwargs.get('market_money_back', 'N')
        if flag_mb_value is True:
            flag_mb_value = 'Y'
            flags += 'MB,'
        flag_pb_value = kwargs.get('price_boost', 'N')
        if flag_pb_value is True:
            flag_pb_value = 'Y'
            flags += 'PB,'
        flag_LD = ""  # Lucky Dip Flag
        disp_sort = '--'
        hcap_value = ''
        bir_index_value = ''
        your_call_values = ''
        ew_available, ew_places, ew_fac_num, ew_fac_den, ew_with_bet = 'N', '', '', '', 'N'
        if any(h in market_name for h in ['|Handicap Match Result', '|Handicap First Half', '|Handicap Second Half',
                                          '|Handicap 3-way']):
            disp_sort = 'MH'
            hcap_value = '&hcap_value=%s&hcap_steal=' % handicap
        elif '|YourCallSpecials' in market_name:
            market_name = market_name.replace('|YourCallSpecials Market|', '')
            disp_sort = '--'
            ew_with_bet = 'Y'
            your_call_values = f'&pl_avail=N&ew_avail={ew_available}&ew_places={ew_places}&ew_fac_num={ew_fac_num}&ew_fac_den={ew_fac_den}&ew_with_bet={ew_with_bet}'
        elif market_name in ['|Match Betting|', '|Match Result|', '|Match Result & Both Teams To Score|',
                             '|Fight Betting|', '|60 Minute Betting|', '|Most 180s|', '|60 Minutes Betting|']:
            if self.category_id == 32:
                disp_sort = 'HH'
            else:
                disp_sort = 'MR'
        elif market_name == '|Draw No Bet|':
            disp_sort = 'DN'
        elif market_name in ['|Match Handicap|', '|Match Handicap 1|', '|Match Handicap 2|', '|Handicap 2-way|', '|Handicap 2-way 2|', '|Handicap 2-way 3|',
                             '|Puck Line|', '|Match Set Handicap|', '|Run Line|', '|Run Line 2|', '|Run Line 3|',
                             '|Puck Line 2|', '|Puck Line 3|', '|Match Set Handicap 2|']:
            hcap_value = '&hcap_value=%s&hcap_steal=' % handicap
            disp_sort = 'WH'
        elif market_name in ['|Total Match Points|', '|Total Match Points1|',
                             '|Total Goals 2-way|', '|Total Points|', '|Total Points1|', '|Total Sixes|', '|Total Sixes 2|',
                             '|Total Sixes 3|', '|Home team total points|', '|Home team total points 2|', '|Away team total points|', '|Away team total points 2|', '|Half Total Points|', '|Half Total Points 2|',
                             '|Quarter Total Points|', '|Quarter Total Points 2|', '|Total Frames Over/Under|', '|Total Runs|', '|Total Runs 1|', '|Team Runs (Main)|',
                             '|Next Over Runs (Main)|', '|Runs At Fall Of Next Wicket|', '|Total Goals 2-way 2|', '|Total Match Points 2|']:
            hcap_value = '&hcap_value=%s&hcap_steal=' % handicap
            disp_sort = 'HL'
        elif market_name in ['|Money Line|', '|Match Betting Head/Head|']:
            disp_sort = 'HH'
        elif market_name == '|Both Teams To Score|':
            disp_sort = 'BO'
        elif market_name == '|Score Goal in Both Halves|':
            disp_sort = '--'
        elif market_name == '|Correct Score|':
            disp_sort = 'CS'
        elif market_name == '|First-Half Result|':
            disp_sort = 'H1'
        elif market_name == '|To Win To Nil|':
            disp_sort = '--'
            bir_index_value = ''
        elif market_name == '|To Win Not To Nil|':
            disp_sort = 'CW'
            bir_index_value = '&bir_index=%s&' % bir_index
        elif market_name in ['|To Qualify|',
                             '|First Goalscorer|',
                             '|Anytime Goalscorer|',
                             '|Goalscorer - 2 Or More|',
                             '|Last Goalscorer|',
                             '|Hat trick|',
                             '|First Goal Scorecast|',
                             '|Last Goal Scorecast|']:
            disp_sort = 'CW'
            bir_index_value = '&bir_index=%s&' % bir_index
        elif 'Total Goals' in market_name:
            if is_over_under:
                hcap_value = '&hcap_value=%s&hcap_steal=' % over_under
                disp_sort = 'HL'
            else:
                market_name_ = '|Total Goals| |Over/Under| |%s|' % over_under
                disp_sort = '--'
        elif ('Over/Under First Half' in market_name) or ('Over/Under Second Half' in market_name) or ('Over/Under' in market_name):
            hcap_value = '&hcap_value=%s&hcap_steal=' % over_under
            disp_sort = 'HL'
        elif market_name in ['|Current Game 1st Point|', '|Set| |1| |Game| |1| |Deuce|', '|Extra-Time Result|',
                                  '|Next Team To Score|', '|Enhanced Multiples|', '|Outright|']:
            disp_sort = '--'
        elif market_name == '|Half-Time/Full-Time|':
            disp_sort = 'HF'
        elif market_name == '|Random Golfer,Random Golfer Assigned,125/1|':
             flag_LD = "LD"
        cashout_available = 'Y' if cashout else 'N'
        enhanced_odds = kwargs.get('enhanced_odds', 'Y') or 'N'
        url = '{0}/hierarchy/event/{1}'.format(self.site, event_id)

        each_way_terms = ew_terms if ew_terms is not None else self.default_ew_terms
        if each_way_terms:
            ew_available, ew_places, ew_fac_num, ew_fac_den = \
                'Y', each_way_terms['ew_places'], each_way_terms['ew_fac_num'], each_way_terms['ew_fac_den']

        if self.brand == 'bma':
            params = '?action=hierarchy::market::H_insert' \
                     '&id=&read_only=N' \
                     '&name={name}' \
                     '&displayed={market_displayed}' \
                     '&disporder={disporder}&status=A' \
                     '&ew_avail={ew_available}' \
                     '&ew_places={ew_places}' \
                     '&ew_fac_num={ew_fac_num}' \
                     '&ew_fac_den={ew_fac_den}' \
                     '&ev_id={eventID}' \
                     '&ev_oc_grp_id={market_template_id}' \
                     '&sort={sort}' \
                     '&clone=' \
                     '&class_id={class_id}' \
                     '&suspend_at=' \
                     '{your_call_values}' \
                     '&liab_limit=' \
                     '&min_bet=&max_multiple_bet=&max_bet=1000.00' \
                     '&sp_max_bet=' \
                     '&win_lp=&win_sp=&win_ep=' \
                     '&place_lp=&place_sp=&place_ep=' \
                     '&ltl_min_bet=&ltl_max_bet=' \
                     '&acc_min=1&acc_max=25&acc_xmul=-' \
                     '&fc_stk_factor=&fc_min_stk_limit=' \
                     '&tc_stk_factor=&tc_min_stk_limit=' \
                     '&ew_factor=&feed_updateable=-' \
                     '&bet_in_run={bet_in_run}' \
                     '&bir_delay={bir_delay}' \
                     '{hcap_value}' \
                     '&gp_terms=' \
                     '&is_ap_mkt=N' \
                     '&cashout_avail={cashout}' \
                     '&enhanced_odds_avail={enhanced_odds}' \
                     '&flag_MB={flag_mb_value}' \
                     '&flag_PB={flag_pb_value}' \
                     '&dbl_res=N&blurb_sort=EV_MKT&blurb_language=all' \
                     '&multi_blurb_all=&multi_blurb_EV_MKT_lang_en=&multi_blurb_EV_MKT_lang_wp=' \
                     '&multi_blurb_EV_MKT_lang_01=&note_channels=P&note_channel_I=&note_channel_P=' \
                     '&note_channel_C=&note_channel_M=&note_channel_Q=&note_channel_D=&note_channel_T=' \
                     '&note_channel_G=&note_channel_W=&note_channel_J=&note_channel_U=' \
                     '&flag_GT=N&flag_SP=N&flag_NRNB=N' \
                     '&flag_PVT={private}' \
                     '&flag_SM=N&flags={flags}' \
                     '&channel_I=Y&channel_P=Y&channel_C=Y&channel_M=Y&channel_Q=Y&channel_D=N' \
                     '&channel_T=N&channel_G=N&channel_W=N&channel_J=N&channel_U=N&channels_list=IPCMQ&ladder_id=' \
                     '&price_ladder_id=&max_rule4=&mult_key_ev_allow=&allow_oc_combi=N&add_variants=&exact_flags=Y' \
                     '{bir_index_value}' \
                .format(name=quote(market_name, safe=''), eventID=event_id,
                        ew_available=ew_available, ew_places=ew_places, ew_fac_num=ew_fac_num,
                        ew_fac_den=ew_fac_den,
                        market_template_id=market_template_id,
                        sort=disp_sort, class_id=class_id, private=private, flags=flags,
                        bet_in_run=bet_in_run, hcap_value=hcap_value, cashout=cashout_available, enhanced_odds=enhanced_odds,
                        bir_index_value=bir_index_value, your_call_values=your_call_values, disporder=disporder,
                        market_displayed=market_displayed, bir_delay=bir_delay, flag_mb_value=flag_mb_value, flag_pb_value=flag_pb_value)
            url = url + params.strip(',')
            resp_dict = do_request(url=url, cookies=self.site_cookies)
        else:
            params = (
                ('action', 'hierarchy::market::H_insert'),
                ('id', ''),
                ('read_only', 'N'),
                ('name', market_name),
                ('displayed', market_displayed),
                ('disporder', disporder),
                ('status', 'A'),
                ('ev_id', event_id),
                ('ev_oc_grp_id', market_template_id),
                ('sort', disp_sort),
                ('class_sort', 'FB'),
                ('can_place', 'N'),
                ('clone', ''),
                ('class_id', self.class_id),
                ('suspend_at', ''),
                ('liab_limit', ''),
                ('min_bet', ''),
                ('max_multiple_bet', ''),
                ('max_bet', ''),
                ('sp_max_bet', ''),
                ('win_lp', ''),
                ('win_sp', ''),
                ('win_ep', ''),
                ('place_lp', ''),
                ('place_sp', ''),
                ('place_ep', ''),
                ('ltl_min_bet', ''),
                ('ltl_max_bet', ''),
                ('acc_min', '1'),
                ('acc_max', '25'),
                ('acc_xmul', '-'),
                ('fc_stk_factor', ''),
                ('fc_min_stk_limit', ''),
                ('tc_stk_factor', ''),
                ('tc_min_stk_limit', ''),
                ('ew_factor', ''),
                ('feed_updateable', '-'),
                ('bet_in_run', bet_in_run),
                ('bir_delay', bir_delay),
                ('is_ap_mkt', 'N'),
                ('cashout_avail', cashout_available),
                ('hcap_steal', ''),
                ('enhanced_odds_avail', enhanced_odds),
                ('gp_terms', ''),
                ('blurb_sort', 'EV_MKT'),
                ('blurb_language', 'all'),
                ('multi_blurb_all', ''),
                ('multi_blurb_EV_MKT_lang_en', ''),
                ('multi_blurb_EV_MKT_lang_ru', ''),
                ('multi_blurb_EV_MKT_lang_cn', ''),
                ('multi_blurb_EV_MKT_lang_it', ''),
                ('multi_blurb_EV_MKT_lang_es', ''),
                ('multi_blurb_EV_MKT_lang_sw', ''),
                ('multi_blurb_EV_MKT_lang_th', ''),
                ('multi_blurb_EV_MKT_lang_dk', ''),
                ('multi_blurb_EV_MKT_lang_no', ''),
                ('multi_blurb_EV_MKT_lang_ie', ''),
                ('multi_blurb_EV_MKT_lang_de', ''),
                ('multi_blurb_EV_MKT_lang_gr', ''),
                ('multi_blurb_EV_MKT_lang_fi', ''),
                ('multi_blurb_EV_MKT_lang_cs', ''),
                ('multi_blurb_EV_MKT_lang_as', ''),
                ('multi_blurb_EV_MKT_lang_tr', ''),
                ('multi_blurb_EV_MKT_lang_pt', ''),
                ('multi_blurb_EV_MKT_lang_oo', ''),
                ('multi_blurb_EV_MKT_lang_pl', ''),
                ('multi_blurb_EV_MKT_lang_bg', ''),
                ('multi_blurb_EV_MKT_lang_ro', ''),
                ('multi_blurb_EV_MKT_lang_ca', ''),
                ('multi_blurb_EV_MKT_lang_hr', ''),
                ('multi_blurb_EV_MKT_lang_za', ''),
                ('multi_blurb_EV_MKT_lang_fr', ''),
                ('multi_blurb_EV_MKT_lang_f2', ''),
                ('multi_blurb_EV_MKT_lang_sk', ''),
                ('multi_blurb_EV_MKT_lang_si', ''),
                ('multi_blurb_EV_MKT_lang_cz', ''),
                ('multi_blurb_EV_MKT_lang_hu', ''),
                ('multi_blurb_EV_MKT_lang_id', ''),
                ('multi_blurb_EV_MKT_lang_af', ''),
                ('note_channels', 'P'),
                ('note_channel_E', ''),
                ('note_channel_I', ''),
                ('note_channel_O', ''),
                ('note_channel_T', ''),
                ('note_channel_C', ''),
                ('note_channel_N', ''),
                ('note_channel_W', ''),
                ('note_channel_D', ''),
                ('note_channel_Z', ''),
                ('note_channel_V', ''),
                ('note_channel_P', ''),
                ('note_channel_H', ''),
                ('note_channel_U', ''),
                ('note_channel_L', ''),
                ('note_channel_F', ''),
                ('note_channel_S', ''),
                ('note_channel_X', ''),
                ('note_channel_J', ''),
                ('note_channel_Q', ''),
                ('note_channel_R', ''),
                ('note_channel_Y', ''),
                ('note_channel_M', ''),
                ('note_channel_@', ''),
                ('note_channel_K', ''),
                ('note_channel_p', ''),
                ('note_channel_G', ''),
                ('note_channel_t', ''),
                ('note_channel_B', ''),
                ('note_channel_e', ''),
                ('note_channel_f', ''),
                ('note_channel_y', ''),
                ('note_channel_z', ''),
                ('flag_GT', 'N'),
                ('flag_SP', 'N'),
                ('flag_NRNB', 'N'),
                ('flag_PVT', private),
                ('flag_SM', 'N'),
                ('flag_PB', flag_pb_value),
                ('flag_MB', flag_mb_value),
                ('flag_GOP', 'N'),
                ('flag_SI', 'N'),
                ('flag_PR1', 'N'),
                ('flag_PR2', 'N'),
                ('flag_EPR', 'N'),
                ('flag_ITV', 'N'),
                ('flag_3E', 'N'),
                ('flag_FI', 'N'),
                ('flag_LD', flag_LD),
                ('flags_list', ''),
                ('channel_E', 'N'),
                ('channel_I', 'Y'),
                ('channel_O', 'Y'),
                ('channel_T', 'Y'),
                ('channel_C', 'Y'),
                ('channel_N', 'Y'),
                ('channel_W', 'Y'),
                ('channel_D', 'Y'),
                ('channel_Z', 'Y'),
                ('channel_V', 'Y'),
                ('channel_P', 'Y'),
                ('channel_H', 'Y'),
                ('channel_L', 'Y'),
                ('channel_U', 'Y'),
                ('channel_F', 'Y'),
                ('channel_S', 'Y'),
                ('channel_X', 'Y'),
                ('channel_J', 'Y'),
                ('channel_Q', 'Y'),
                ('channel_R', 'Y'),
                ('channel_Y', 'Y'),
                ('channel_M', 'Y'),
                ('channel_@', 'Y'),
                ('channel_K', 'Y'),
                ('channel_p', 'Y'),
                ('channel_G', 'Y'),
                ('channel_t', 'Y'),
                ('channel_B', 'Y'),
                ('channel_e', 'N'),
                ('channel_f', 'N'),
                ('channel_y', 'N'),
                ('channel_z', 'N'),
                ('channels_list', 'IOTCNWDZVPHLUFSXJQRYM@KpGtB'),
                ('views_fr', 'Y'),
                ('views_hu', 'Y'),
                ('views_cz', 'Y'),
                ('views_sk', 'Y'),
                ('views_af', 'Y'),
                ('views_id', 'Y'),
                ('views_za', 'Y'),
                ('views_ro', 'Y'),
                ('views_ru', 'Y'),
                ('views_bg', 'Y'),
                ('views_hr', 'Y'),
                ('views_si', 'Y'),
                ('views_seas', 'Y'),
                ('views_sw', 'Y'),
                ('views_dk', 'Y'),
                ('views_fi', 'Y'),
                ('views_de', 'Y'),
                ('views_vs', 'Y'),
                ('views_uk', 'Y'),
                ('views_ie', 'Y'),
                ('views_gr', 'Y'),
                ('views_pt', 'Y'),
                ('views_cs', 'Y'),
                ('views_it', 'Y'),
                ('views_esmd', 'Y'),
                ('views_cn', 'Y'),
                ('views_esvc', 'Y'),
                ('views_es', 'Y'),
                ('views_esmc', 'Y'),
                ('views_esar', 'Y'),
                ('views_esgc', 'Y'),
                ('views_esnc', 'Y'),
                ('views_th', 'Y'),
                ('views_no', 'Y'),
                ('views_beta', 'Y'),
                ('views_oo', 'Y'),
                ('views_pl', 'Y'),
                ('views_ca', 'Y'),
                ('select_linked_ladder_-1_CASHOUT', '-1'),
                ('select_linked_ladder_-1_ODDSBOOST', '-1'),
                ('price_ladder_id', ''),
                ('max_rule4', ''),
                ('mult_key_ev_allow', ''),
                ('allow_oc_combi', 'N'),
                ('add_variants', ''),
                ('exact_flags', 'Y'),
                ('ew_with_bet', ew_with_bet),
                ('ew_avail', ew_available),
                ('ew_places', ew_places),
                ('ew_fac_num', ew_fac_num),
                ('ew_fac_den', ew_fac_den),
                ('flags', flags)
            )
            if bir_index_value:
                params = params + (('bir_index', bir_index),)
            if any(h in market_name for h in
                   ['|Handicap Match Result', '|Handicap First Half', '|Handicap Second Half', '|Handicap 3-way', '|Match Handicap|', '|Match Handicap 1|', '|Match Handicap 2|',
                    '|Match Set Handicap|', '|Handicap 2-way|', '|Total Match Points|', '|Puck Line|', '|Total Goals 2-way|', '|Total Points|', '|Total Points1|', '|Total Sixes|',
                    '|Total Sixes 2|', '|Total Sixes 3|', '|Home team total points|', '|Home team total points 2|', '|Away team total points|', '|Away team total points 2|', '|Half Total Points|', '|Half Total Points 2|',
                    '|Quarter Total Points|', '|Quarter Total Points 2|', '|Run Line|', '|Run Line 2|', '|Run Line 3|', '|Total Runs|', '|Total Runs 1|', '|Team Runs (Main)|', '|Next Over Runs (Main)|',
                    '|Runs At Fall Of Next Wicket|', '|Handicap 2-way 2|', '|Handicap 2-way 3|', '|Total Match Points1|',
                    '|Total Goals 2-way 2|', '|Puck Line 2|', '|Puck Line 3|', '|Match Set Handicap 2|', '|Total Match Points 2|']):
                params = params + (('hcap_value', handicap), ('hcap_steal', ''), )
            elif 'Total Goals' in market_name:
                if is_over_under:
                    params = params + (('hcap_value', over_under), ('hcap_steal', ''),)
            elif ('Over/Under First Half' in market_name) or ('Over/Under Second Half' in market_name) or ('Total 180s Over/Under' in market_name) or ('Total Frames Over/Under' in market_name):
                params = params + (('hcap_value', over_under), ('hcap_steal', ''),)

            resp_dict = do_request(url=url, params=params, cookies=self.site_cookies)
        try:
            marketID = resp_dict['id']
        except KeyError:
            self._logger.info('*** Add market response %s' % resp_dict)
            raise OBException('Marked id can not be found')
        self._logger.debug('*** Market id is: %s' % marketID)
        return marketID

    def add_both_team_to_score_selection(self, marketID=None, selection_names=None, prices=None, **kwargs):
        selections_displayed = 'N' if 'selections_displayed' in kwargs.keys() and kwargs['selections_displayed'] is False else 'Y'
        marketID = marketID if marketID else self.marketID
        max_bet = kwargs['max_bet'] if 'max_bet' in kwargs else 1000.00
        if not isinstance(selection_names, (list, tuple)):
            selection_names = [selection_names, ]
        if not isinstance(prices, (list, tuple)):
            prices = [prices, ]
        for name, odd in zip(selection_names, prices):
            if self.brand == 'bma':
                params = '?action=hierarchy::selection::H_insert' \
                         '&id=&read_only=N' \
                         '&desc={selection_name}' \
                         '&mkt_id={marketID}' \
                         '&displayed={selections_displayed}' \
                         '&disporder=&status=A' \
                         '&lp_price={lp_price}' \
                         '&feed_updateable=Y' \
                         '&win_roll=0&ext_key=' \
                         '&mult_key=&link_key=' \
                         '&risk_info=-&min_bet=' \
                         '&abs_least_max_bet=' \
                         '&max_multiple_bet=&abs_max_bet=' \
                         '&max_bet={max_bet}' \
                         '&sp_max_bet=&lock_stake_lmt=N' \
                         '&lock_stake_win=N&max_place_lp=1000.00' \
                         '&max_place_sp=1000.00&lock_stake_place=N' \
                         '&stk_or_lbt=L&max_total=&fc_stk_limit=&tc_stk_limit=' \
                         '&ew_factor=&acc_min=&fixed_stake_limits=Y' \
                         '&note_channels=P&note_channel_I=&note_channel_P=' \
                         '&note_channel_C=&note_channel_M=&note_channel_Q=' \
                         '&note_channel_D=&note_channel_T=&note_channel_G=' \
                         '&note_channel_W=&note_channel_J=&channel_I=Y' \
                         '&channel_P=Y&channel_C=Y&channel_M=Y&channel_Q=Y' \
                         '&channel_D=N&channel_T=N&channel_G=N&channel_W=N' \
                         '&channel_J=N&channels_list=IPCMQ&exact_flags=Y' \
                    .format(selection_name=name, marketID=marketID, lp_price=quote(odd), max_bet=max_bet,
                            selections_displayed=selections_displayed)
                url = self.site + params
                do_request(url=url, cookies=self.site_cookies, load_response=False)

            else:
                params = (
                    ('action', 'hierarchy::selection::H_insert'),
                    ('id', ''),
                    ('read_only', 'N'),
                    ('desc', name),
                    ('mkt_id', marketID),
                    ('displayed', selections_displayed),
                    ('disporder', ''),
                    ('status', 'A'),
                    ('lp_price', odd),
                    ('feed_updateable', '-'),
                    ('to_event_link_id', ''),
                    ('to_event_link_level', ''),
                    ('evoc_parent_ev_id', ''),
                    ('evoc_ev_linked_ids', ''),
                    ('win_roll', '0'),
                    ('ext_key', ''),
                    ('mult_key', ''),
                    ('link_key', ''),
                    ('risk_info', '-'),
                    ('min_bet', ''),
                    ('abs_least_max_bet', ''),
                    ('max_multiple_bet', ''),
                    ('abs_max_bet', ''),
                    ('max_bet', max_bet),
                    ('sp_max_bet', ''),
                    ('lock_stake_lmt', 'N'),
                    ('lock_stake_win', 'N'),
                    ('max_place_lp', '1000.00'),
                    ('max_place_sp', '1000.00'),
                    ('lock_stake_place', 'N'),
                    ('stk_or_lbt', 'L'),
                    ('max_total', ''),
                    ('fc_stk_limit', ''),
                    ('tc_stk_limit', ''),
                    ('ew_factor', ''),
                    ('acc_min', ''),
                    ('fixed_stake_limits', 'N'),
                    ('note_channels', 'P'),
                    ('note_channel_E', ''),
                    ('note_channel_I', ''),
                    ('note_channel_O', ''),
                    ('note_channel_T', ''),
                    ('note_channel_C', ''),
                    ('note_channel_N', ''),
                    ('note_channel_W', ''),
                    ('note_channel_D', ''),
                    ('note_channel_Z', ''),
                    ('note_channel_V', ''),
                    ('note_channel_P', ''),
                    ('note_channel_H', ''),
                    ('note_channel_L', ''),
                    ('note_channel_U', ''),
                    ('note_channel_F', ''),
                    ('note_channel_S', ''),
                    ('note_channel_X', ''),
                    ('note_channel_J', ''),
                    ('note_channel_Q', ''),
                    ('note_channel_R', ''),
                    ('note_channel_Y', ''),
                    ('note_channel_M', ''),
                    ('note_channel_@', ''),
                    ('note_channel_K', ''),
                    ('note_channel_p', ''),
                    ('note_channel_G', ''),
                    ('note_channel_t', ''),
                    ('note_channel_B', ''),
                    ('note_channel_e', ''),
                    ('note_channel_f', ''),
                    ('note_channel_y', ''),
                    ('note_channel_z', ''),
                    ('channel_E', 'N'),
                    ('channel_I', 'Y'),
                    ('channel_O', 'N'),
                    ('channel_T', 'N'),
                    ('channel_C', 'Y'),
                    ('channel_N', 'N'),
                    ('channel_W', 'N'),
                    ('channel_D', 'N'),
                    ('channel_Z', 'N'),
                    ('channel_V', 'N'),
                    ('channel_P', 'Y'),
                    ('channel_H', 'N'),
                    ('channel_L', 'N'),
                    ('channel_U', 'N'),
                    ('channel_F', 'N'),
                    ('channel_S', 'N'),
                    ('channel_X', 'N'),
                    ('channel_J', 'N'),
                    ('channel_Q', 'Y'),
                    ('channel_R', 'N'),
                    ('channel_Y', 'N'),
                    ('channel_M', 'Y'),
                    ('channel_@', 'N'),
                    ('channel_K', 'N'),
                    ('channel_p', 'N'),
                    ('channel_G', 'N'),
                    ('channel_t', 'N'),
                    ('channel_B', 'N'),
                    ('channel_e', 'N'),
                    ('channel_f', 'N'),
                    ('channel_y', 'N'),
                    ('channel_z', 'N'),
                    ('channels_list', 'IPCMQ'),
                    ('exact_flags', 'Y')
                )
                url = self.site
                do_request(url=url, params=params, cookies=self.site_cookies, load_response=False)
        selection_ids = self.get_selection_ids(marketID=marketID)
        if not selection_ids:
            raise OBException(f'Not all selections were added to market id {marketID}')
        return selection_ids

    def add_selections(self, prices, marketID=None, **kwargs):
        max_bet = kwargs['max_bet'] if 'max_bet' in kwargs else 1000.00
        selections_displayed = 'N' if 'selections_displayed' in kwargs.keys() and kwargs['selections_displayed'] is False else 'Y'
        marketID = marketID if marketID else self.marketID
        if 'team1' in kwargs.keys() and 'team2' in kwargs.keys():
            self.team1_name = kwargs['team1']
            self.team2_name = kwargs['team2']
        selection_names = kwargs.get('selection_names', None)
        if isinstance(selection_names, str):
            if self.brand == 'bma':
                selection_names = [quote(kwargs['selection_names']), ]
            else:
                selection_names = [(kwargs['selection_names']), ]
        elif isinstance(selection_names, (list, tuple)):
            if self.brand == 'bma':
                selection_names = [quote(name) for name in selection_names]
            else:
                selection_names = [name for name in selection_names]
        if self.brand == 'bma':
            team1, team2 = quote(self.team1_name), quote(self.team2_name)
        else:
            team1, team2 = self.team1_name, self.team2_name

        if selection_names is None:
            selection_names = ['|%s|' % team1, '|Draw|', '|%s|' % team2] if self.category_id in [9, 10, 16, 20, 53, 31, 30, 54, 18, 13] else \
                ['|%s|' % team1, '|%s|' % team2]
        selection_types = kwargs.get('selection_types', None)
        if isinstance(selection_types, str):
            if self.brand == 'bma':
                selection_types = [quote(kwargs['selection_types']), ]
            else:
                selection_types = [(kwargs['selection_types']), ]
        elif isinstance(selection_types, (list, tuple)):
            if self.brand == 'bma':
                selection_types = [quote(name) for name in selection_types]
            else:
                selection_types = [(name) for name in selection_types]
        if selection_types is None:
            selection_types = ['H', 'D', 'A'] if self.category_id in [9, 10, 16, 20, 53, 31, 30, 54, 18, 13] else ['H', 'A']
        if isinstance(prices, (list, tuple)):
            odds = prices
        elif isinstance(prices, (KeysView, ValuesView, ItemsView)):
            odds = list(prices)
        elif isinstance(prices, dict):
            odds = prices.values()
        else:
            odds = prices
        for selection_type, selection_name, odd in zip(selection_types, selection_names, odds):
            if self.brand == 'bma':
                params = '?action=hierarchy::selection::H_insert' \
                         '&id=' \
                         '&read_only=N' \
                         '&desc={selection_name}' \
                         '&mkt_id={marketID}' \
                         '&displayed={selections_displayed}' \
                         '&disporder=' \
                         '&status=A' \
                         '&lp_price={lp_price}' \
                         '&feed_updateable=Y' \
                         '&win_roll=0&ext_key=' \
                         '&mult_key=&link_key=' \
                         '&risk_info=-&min_bet=' \
                         '&abs_least_max_bet=' \
                         '&max_multiple_bet=&abs_max_bet=' \
                         '&max_bet={max_bet}' \
                         '&sp_max_bet=&lock_stake_lmt=N' \
                         '&lock_stake_win=N&max_place_lp=1000.00' \
                         '&max_place_sp=1000.00&lock_stake_place=N' \
                         '&stk_or_lbt=L&max_total=&fc_stk_limit=&tc_stk_limit=' \
                         '&ew_factor=&acc_min=&fixed_stake_limits=Y' \
                         '&fb_result={selection_type}' \
                         '&note_channels=P&note_channel_I=&note_channel_P=' \
                         '&note_channel_C=&note_channel_M=&note_channel_Q=' \
                         '&note_channel_D=&note_channel_T=&note_channel_G=' \
                         '&note_channel_W=&note_channel_J=&channel_I=Y' \
                         '&channel_P=Y&channel_C=Y&channel_M=Y&channel_Q=Y' \
                         '&channel_D=N&channel_T=N&channel_G=N&channel_W=N' \
                         '&channel_J=N&channels_list=IPCMQ&exact_flags=Y' \
                    .format(selection_name=selection_name, marketID=marketID, lp_price=quote(odd),
                            max_bet=max_bet, selection_type=selection_type, selections_displayed=selections_displayed)
                if selection_type == 'YC':
                    params = params.replace('&fb_result=YC', '')
                    params = params.replace('&stk_or_lbt=L', '&stk_or_lbt=S')
                url = self.site + params
                do_request(url=url, load_response=False, cookies=self.site_cookies)
            else:
                params = (
                    ('action', 'hierarchy::selection::H_insert'),
                    ('id', ''),
                    ('read_only', 'N'),
                    ('desc', selection_name),
                    ('name', ''),
                    ('mkt_id', marketID),
                    ('displayed', selections_displayed),
                    ('disporder', '0'),
                    ('status', 'A'),
                    ('lp_price', odd),
                    ('feed_updateable', 'Y'),
                    ('to_event_link_id', ''),
                    ('to_event_link_level', ''),
                    ('evoc_parent_ev_id', self.eventID),
                    ('evoc_ev_linked_ids', ''),
                    ('win_roll', '0'),
                    ('ext_key', ''),
                    ('mult_key', ''),
                    ('link_key', ''),
                    ('risk_info', '-'),
                    ('min_bet', ''),
                    ('abs_least_max_bet', ''),
                    ('max_multiple_bet', ''),
                    ('abs_max_bet', ''),
                    ('max_bet', max_bet),
                    ('sp_max_bet', ''),
                    ('lock_stake_lmt', 'N'),
                    ('lock_stake_win', 'N'),
                    ('max_place_lp', ''),
                    ('max_place_sp', ''),
                    ('lock_stake_place', 'N'),
                    ('stk_or_lbt', 'S' if selection_type == 'YC' else 'L'),
                    ('max_total', ''),
                    ('fc_stk_limit', ''),
                    ('tc_stk_limit', ''),
                    ('ew_factor', ''),
                    ('acc_min', ''),
                    ('fixed_stake_limits', 'N'),
                    ('fb_result', selection_type),
                    ('note_channels', 'P'),
                    ('note_channel_E', ''),
                    ('note_channel_I', ''),
                    ('note_channel_O', ''),
                    ('note_channel_T', ''),
                    ('note_channel_C', ''),
                    ('note_channel_N', ''),
                    ('note_channel_W', ''),
                    ('note_channel_D', ''),
                    ('note_channel_Z', ''),
                    ('note_channel_V', ''),
                    ('note_channel_P', ''),
                    ('note_channel_H', ''),
                    ('note_channel_L', ''),
                    ('note_channel_U', ''),
                    ('note_channel_F', ''),
                    ('note_channel_S', ''),
                    ('note_channel_X', ''),
                    ('note_channel_J', ''),
                    ('note_channel_Q', ''),
                    ('note_channel_R', ''),
                    ('note_channel_Y', ''),
                    ('note_channel_M', ''),
                    ('note_channel_@', ''),
                    ('note_channel_K', ''),
                    ('note_channel_p', ''),
                    ('note_channel_G', ''),
                    ('note_channel_t', ''),
                    ('note_channel_B', ''),
                    ('note_channel_e', ''),
                    ('note_channel_f', ''),
                    ('note_channel_y', ''),
                    ('note_channel_z', ''),
                    ('channel_E', 'N'),
                    ('channel_I', 'Y'),
                    ('channel_O', 'N'),
                    ('channel_T', 'N'),
                    ('channel_C', 'Y'),
                    ('channel_N', 'N'),
                    ('channel_W', 'N'),
                    ('channel_D', 'N'),
                    ('channel_Z', 'N'),
                    ('channel_V', 'N'),
                    ('channel_P', 'Y'),
                    ('channel_H', 'N'),
                    ('channel_L', 'N'),
                    ('channel_U', 'Y'),
                    ('channel_F', 'N'),
                    ('channel_S', 'N'),
                    ('channel_X', 'N'),
                    ('channel_J', 'N'),
                    ('channel_Q', 'Y'),
                    ('channel_R', 'N'),
                    ('channel_Y', 'N'),
                    ('channel_M', 'Y'),
                    ('channel_@', 'N'),
                    ('channel_K', 'N'),
                    ('channel_p', 'N'),
                    ('channel_G', 'N'),
                    ('channel_t', 'N'),
                    ('channel_B', 'N'),
                    ('channel_e', 'Y'),
                    ('channel_f', 'Y'),
                    ('channel_y', 'N'),
                    ('channel_z', 'N'),
                    ('channels_list', 'ICPUQMef'),
                    ('exact_flags', 'Y')
                )
                if selection_type == 'YC':
                    params = tuple(x for x in params if 'fb_result' not in x)
                do_request(url=self.site, params=params, load_response=False, cookies=self.site_cookies)
        selection_ids = self.get_selection_ids(marketID=marketID)
        if len(selection_ids) < len(selection_types):
            raise OBException(f'Not all selections were added to market id {marketID}')
        return selection_ids

    def add_enhanced_multiples_selection(self, odds, selection_name, marketID=None, **kwargs):
        max_bet = kwargs['max_bet'] if 'max_bet' in kwargs else 1000.00
        selections_displayed = 'N' if 'selections_displayed' in kwargs.keys() and kwargs['selections_displayed'] is False else 'Y'
        marketID = marketID if marketID else self.marketID
        if self.brand == 'bma':
            params = '?action=hierarchy::selection::H_insert' \
                     '&id=' \
                     '&read_only=N' \
                     '&desc={selection_name}' \
                     '&mkt_id={marketID}' \
                     '&displayed={selections_displayed}' \
                     '&disporder=' \
                     '&status=A' \
                     '&lp_price={lp_price}' \
                     '&feed_updateable=Y' \
                     '&win_roll=0&ext_key=' \
                     '&mult_key=&link_key=' \
                     '&risk_info=-&min_bet=' \
                     '&abs_least_max_bet=' \
                     '&max_multiple_bet=&abs_max_bet=' \
                     '&max_bet={max_bet}' \
                     '&sp_max_bet=&lock_stake_lmt=N' \
                     '&lock_stake_win=N&max_place_lp=1000.00' \
                     '&max_place_sp=1000.00&lock_stake_place=N' \
                     '&stk_or_lbt=L&max_total=&fc_stk_limit=&tc_stk_limit=' \
                     '&ew_factor=&acc_min=&fixed_stake_limits=Y' \
                     '&note_channels=P&note_channel_I=&note_channel_P=' \
                     '&note_channel_C=&note_channel_M=&note_channel_Q=' \
                     '&note_channel_D=&note_channel_T=&note_channel_G=' \
                     '&note_channel_W=&note_channel_J=&channel_I=Y' \
                     '&channel_P=Y&channel_C=Y&channel_M=Y&channel_Q=Y' \
                     '&channel_D=N&channel_T=N&channel_G=N&channel_W=N' \
                     '&channel_J=N&channels_list=IPCMQ&exact_flags=Y' \
                .format(selection_name=selection_name, marketID=marketID, lp_price=quote(odds),
                        max_bet=max_bet, selections_displayed=selections_displayed)
            url = self.site + params
            do_request(url=url, load_response=False, cookies=self.site_cookies)
        else:
            params = (
                ('action', 'hierarchy::selection::H_insert'),
                ('id', ''),
                ('read_only', 'N'),
                ('desc', selection_name),
                ('mkt_id', marketID),
                ('displayed', selections_displayed),
                ('disporder', ''),
                ('status', 'A'),
                ('lp_price', odds),
                ('feed_updateable', '-'),
                ('to_event_link_id', ''),
                ('to_event_link_level', ''),
                ('evoc_parent_ev_id', ''),
                ('evoc_ev_linked_ids', ''),
                ('win_roll', '0'),
                ('ext_key', ''),
                ('mult_key', ''),
                ('link_key', ''),
                ('risk_info', '-'),
                ('min_bet', ''),
                ('abs_least_max_bet', ''),
                ('max_multiple_bet', ''),
                ('abs_max_bet', ''),
                ('max_bet', max_bet),
                ('sp_max_bet', ''),
                ('lock_stake_lmt', 'N'),
                ('lock_stake_win', 'N'),
                ('max_place_lp', ''),
                ('max_place_sp', ''),
                ('lock_stake_place', 'N'),
                ('stk_or_lbt', 'L'),
                ('max_total', ''),
                ('fc_stk_limit', ''),
                ('tc_stk_limit', ''),
                ('ew_factor', ''),
                ('acc_min', ''),
                ('fixed_stake_limits', 'N'),
                ('note_channels', 'P'),
                ('note_channel_E', ''),
                ('note_channel_I', ''),
                ('note_channel_O', ''),
                ('note_channel_T', ''),
                ('note_channel_C', ''),
                ('note_channel_N', ''),
                ('note_channel_W', ''),
                ('note_channel_D', ''),
                ('note_channel_Z', ''),
                ('note_channel_V', ''),
                ('note_channel_P', ''),
                ('note_channel_H', ''),
                ('note_channel_L', ''),
                ('note_channel_U', ''),
                ('note_channel_F', ''),
                ('note_channel_S', ''),
                ('note_channel_X', ''),
                ('note_channel_J', ''),
                ('note_channel_Q', ''),
                ('note_channel_R', ''),
                ('note_channel_Y', ''),
                ('note_channel_M', ''),
                ('note_channel_@', ''),
                ('note_channel_K', ''),
                ('note_channel_p', ''),
                ('note_channel_G', ''),
                ('note_channel_t', ''),
                ('note_channel_B', ''),
                ('note_channel_e', ''),
                ('note_channel_f', ''),
                ('note_channel_y', ''),
                ('note_channel_z', ''),
                ('channel_E', 'N'),
                ('channel_I', 'Y'),
                ('channel_O', 'N'),
                ('channel_T', 'N'),
                ('channel_C', 'Y'),
                ('channel_N', 'N'),
                ('channel_W', 'N'),
                ('channel_D', 'N'),
                ('channel_Z', 'N'),
                ('channel_V', 'N'),
                ('channel_P', 'Y'),
                ('channel_H', 'N'),
                ('channel_L', 'N'),
                ('channel_U', 'N'),
                ('channel_F', 'N'),
                ('channel_S', 'N'),
                ('channel_X', 'N'),
                ('channel_J', 'N'),
                ('channel_Q', 'Y'),
                ('channel_R', 'N'),
                ('channel_Y', 'N'),
                ('channel_M', 'Y'),
                ('channel_@', 'N'),
                ('channel_K', 'N'),
                ('channel_p', 'N'),
                ('channel_G', 'N'),
                ('channel_t', 'N'),
                ('channel_B', 'N'),
                ('channel_e', 'N'),
                ('channel_f', 'N'),
                ('channel_y', 'N'),
                ('channel_z', 'N'),
                ('channels_list', 'IPCMQ'),
                ('exact_flags', 'Y')
            )
            do_request(url=self.site, params=params, load_response=False, cookies=self.site_cookies)

        selection_ids = self.get_selection_ids(marketID=marketID)
        if not selection_ids:
            raise OBException(f'Not all selections were added to market id {marketID}')
        return selection_ids

    def add_correct_score_selections(self, prices, marketID=None, **kwargs):
        selections_displayed = 'N' if 'selections_displayed' in kwargs.keys() and kwargs['selections_displayed'] is False else 'Y'
        if 'team1' in kwargs.keys() and 'team2' in kwargs.keys():
            self.team1_name = kwargs['team1']
            self.team2_name = kwargs['team2']
        marketID = marketID if marketID else self.marketID
        for team_name, team_prices in prices:
            for score, odd in team_prices.items():
                score_ = score.split('-')
                if team_name == 'away':
                    score_ = score_[::-1]
                    name, score_home, score_away = self.team2_name, score_[0], score_[1]
                elif team_name == 'home':
                    name, score_home, score_away = self.team1_name, score_[0], score_[1]
                else:
                    name, score_home, score_away = team_name, score_[0], score_[1]
                selection_name = '|{team_name} {score}|'.format(team_name=name, score=score)
                if self.brand == 'bma':
                    params = '?action=hierarchy::selection::H_insert' \
                             '&id=' \
                             '&read_only=N' \
                             '&desc={selection_name}' \
                             '&mkt_id={market_id}' \
                             '&displayed={selections_displayed}' \
                             '&disporder=' \
                             '&status=A' \
                             '&lp_price={odd}' \
                             '&feed_updateable=-' \
                             '&win_roll=0' \
                             '&ext_key=' \
                             '&mult_key=' \
                             '&link_key=' \
                             '&risk_info=-' \
                             '&min_bet=' \
                             '&abs_least_max_bet=' \
                             '&max_multiple_bet=' \
                             '&abs_max_bet=' \
                             '&max_bet=' \
                             '&sp_max_bet=' \
                             '&lock_stake_lmt=N' \
                             '&lock_stake_win=N' \
                             '&max_place_lp=' \
                             '&max_place_sp=' \
                             '&lock_stake_place=N' \
                             '&stk_or_lbt=S' \
                             '&max_total=' \
                             '&fc_stk_limit=' \
                             '&tc_stk_limit=' \
                             '&ew_factor=' \
                             '&acc_min=' \
                             '&fixed_stake_limits=Y' \
                             '&fb_result=S' \
                             '&cs_home={score_home}' \
                             '&cs_away={score_away}' \
                             '&note_channels=P' \
                             '&note_channel_I=' \
                             '&note_channel_P=' \
                             '&note_channel_C=' \
                             '&note_channel_M=' \
                             '&note_channel_Q=' \
                             '&note_channel_D=' \
                             '&note_channel_T=' \
                             '&note_channel_G=' \
                             '&note_channel_W=' \
                             '&note_channel_J=' \
                             '&channel_I=Y' \
                             '&channel_P=Y' \
                             '&channel_C=Y' \
                             '&channel_M=Y' \
                             '&channel_Q=Y' \
                             '&channel_D=N' \
                             '&channel_T=N' \
                             '&channel_G=N' \
                             '&channel_W=N' \
                             '&channel_J=N' \
                             '&channels_list=IPCMQ' \
                             '&exact_flags=Y'.format(selection_name=selection_name, market_id=marketID,
                                                     odd=odd, score_home=score_home, score_away=score_away,
                                                     selections_displayed=selections_displayed)
                    url = self.site + params
                    do_request(url=url, load_response=False, cookies=self.site_cookies)
                else:
                    params = (
                        ('action', 'hierarchy::selection::H_insert'),
                        ('id', ''),
                        ('read_only', 'N'),
                        ('desc', selection_name),
                        ('mkt_id', marketID),
                        ('displayed', selections_displayed),
                        ('disporder', ''),
                        ('status', 'A'),
                        ('lp_price', odd),
                        ('feed_updateable', '-'),
                        ('to_event_link_id', ''),
                        ('to_event_link_level', ''),
                        ('evoc_parent_ev_id', ''),
                        ('evoc_ev_linked_ids', ''),
                        ('win_roll', '0'),
                        ('ext_key', ''),
                        ('mult_key', ''),
                        ('link_key', ''),
                        ('risk_info', '-'),
                        ('min_bet', ''),
                        ('abs_least_max_bet', ''),
                        ('max_multiple_bet', ''),
                        ('abs_max_bet', ''),
                        ('max_bet', ''),
                        ('sp_max_bet', ''),
                        ('lock_stake_lmt', 'N'),
                        ('lock_stake_win', 'N'),
                        ('max_place_lp', ''),
                        ('max_place_sp', ''),
                        ('lock_stake_place', 'N'),
                        ('stk_or_lbt', 'L'),
                        ('max_total', ''),
                        ('fc_stk_limit', ''),
                        ('tc_stk_limit', ''),
                        ('ew_factor', ''),
                        ('acc_min', ''),
                        ('fixed_stake_limits', 'N'),
                        ('fb_result', 'S'),
                        ('cs_home', score_home),
                        ('cs_away', score_away),
                        ('note_channels', 'P'),
                        ('note_channel_E', ''),
                        ('note_channel_I', ''),
                        ('note_channel_O', ''),
                        ('note_channel_T', ''),
                        ('note_channel_C', ''),
                        ('note_channel_N', ''),
                        ('note_channel_W', ''),
                        ('note_channel_D', ''),
                        ('note_channel_Z', ''),
                        ('note_channel_V', ''),
                        ('note_channel_P', ''),
                        ('note_channel_H', ''),
                        ('note_channel_L', ''),
                        ('note_channel_U', ''),
                        ('note_channel_F', ''),
                        ('note_channel_S', ''),
                        ('note_channel_X', ''),
                        ('note_channel_J', ''),
                        ('note_channel_Q', ''),
                        ('note_channel_R', ''),
                        ('note_channel_Y', ''),
                        ('note_channel_M', ''),
                        ('note_channel_@', ''),
                        ('note_channel_K', ''),
                        ('note_channel_p', ''),
                        ('note_channel_G', ''),
                        ('note_channel_t', ''),
                        ('note_channel_B', ''),
                        ('note_channel_e', ''),
                        ('note_channel_f', ''),
                        ('note_channel_y', ''),
                        ('note_channel_z', ''),
                        ('channel_E', 'N'),
                        ('channel_I', 'Y'),
                        ('channel_O', 'N'),
                        ('channel_T', 'N'),
                        ('channel_C', 'Y'),
                        ('channel_N', 'N'),
                        ('channel_W', 'N'),
                        ('channel_D', 'N'),
                        ('channel_Z', 'N'),
                        ('channel_V', 'N'),
                        ('channel_P', 'Y'),
                        ('channel_H', 'N'),
                        ('channel_L', 'N'),
                        ('channel_U', 'N'),
                        ('channel_F', 'N'),
                        ('channel_S', 'N'),
                        ('channel_X', 'N'),
                        ('channel_J', 'N'),
                        ('channel_Q', 'Y'),
                        ('channel_R', 'N'),
                        ('channel_Y', 'N'),
                        ('channel_M', 'Y'),
                        ('channel_@', 'N'),
                        ('channel_K', 'N'),
                        ('channel_p', 'N'),
                        ('channel_G', 'N'),
                        ('channel_t', 'N'),
                        ('channel_B', 'N'),
                        ('channel_e', 'N'),
                        ('channel_f', 'N'),
                        ('channel_y', 'N'),
                        ('channel_z', 'N'),
                        ('channels_list', 'ICPUQM'),
                        ('exact_flags', 'Y')
                    )
                    do_request(url=self.site, params=params, load_response=False, cookies=self.site_cookies)

        selection_ids = self.get_selection_ids(marketID=marketID)
        if not selection_ids:
            raise OBException(f'Not all selections were added to market id {marketID}')
        return selection_ids

    def add_handicap_selection(self, marketID=None, odds_home='1/2', odds_draw='3/2', odds_away='4/1', **kwargs):
        selections_displayed = 'N' if 'selections_displayed' in kwargs.keys() and kwargs['selections_displayed'] is False else 'Y'
        if 'team1' in kwargs.keys() and 'team2' in kwargs.keys():
            self.team1_name = kwargs['team1']
            self.team2_name = kwargs['team2']
        marketID = marketID if marketID else self.marketID
        selection_types = ['H', 'L', 'A']
        if self.brand == 'bma':
            selection_names = [quote('|%s|' % self.team1_name), '|Tie|', quote('|%s|' % self.team2_name)]
        else:
            selection_names = ['|%s|' % self.team1_name, '|Tie|', '|%s|' % self.team2_name]
        odds = [odds_home, odds_draw, odds_away]
        for selection_type, selection_name, odd in zip(selection_types, selection_names, odds):

            if self.brand == 'bma':
                params = '?action=hierarchy::selection::H_insert' \
                         '&id=&read_only=N' \
                         '&desc={selection_name}' \
                         '&mkt_id={marketID}' \
                         '&displayed={selections_displayed}' \
                         '&disporder=' \
                         '&status=A' \
                         '&lp_price={lp_price}' \
                         '&feed_updateable=-' \
                         '&win_roll=0&ext_key=' \
                         '&mult_key=&link_key=' \
                         '&risk_info=-&min_bet=' \
                         '&abs_least_max_bet=' \
                         '&max_multiple_bet=&abs_max_bet=' \
                         '&max_bet=1000.00&sp_max_bet=&lock_stake_lmt=N' \
                         '&lock_stake_win=N&max_place_lp=1000.00' \
                         '&max_place_sp=1000.00&lock_stake_place=N' \
                         '&stk_or_lbt=L&max_total=&fc_stk_limit=&tc_stk_limit=' \
                         '&ew_factor=&acc_min=&fixed_stake_limits=Y' \
                         '&fb_result={selection_type}' \
                         '&note_channels=P&note_channel_I=&note_channel_P=' \
                         '&note_channel_C=&note_channel_M=&note_channel_Q=' \
                         '&note_channel_D=&note_channel_T=&note_channel_G=' \
                         '&note_channel_W=&note_channel_J=&channel_I=Y' \
                         '&channel_P=Y&channel_C=Y&channel_M=Y&channel_Q=Y' \
                         '&channel_D=N&channel_T=N&channel_G=N&channel_W=N' \
                         '&channel_J=N&channels_list=IPCMQ&exact_flags=Y' \
                    .format(selection_name=selection_name, marketID=marketID, lp_price=quote(odd),
                            selection_type=selection_type, selections_displayed=selections_displayed)
                url = self.site + params
                do_request(url=url, load_response=False, cookies=self.site_cookies)
            else:
                params = (
                    ('action', 'hierarchy::selection::H_insert'),
                    ('id', ''),
                    ('read_only', 'N'),
                    ('desc', selection_name),
                    ('mkt_id', marketID),
                    ('displayed', selections_displayed),
                    ('disporder', ''),
                    ('status', 'A'),
                    ('lp_price', odd),
                    ('feed_updateable', '-'),
                    ('to_event_link_id', ''),
                    ('to_event_link_level', ''),
                    ('evoc_parent_ev_id', ''),
                    ('evoc_ev_linked_ids', ''),
                    ('win_roll', '0'),
                    ('ext_key', ''),
                    ('mult_key', ''),
                    ('link_key', ''),
                    ('risk_info', '-'),
                    ('min_bet', ''),
                    ('abs_least_max_bet', ''),
                    ('max_multiple_bet', ''),
                    ('abs_max_bet', ''),
                    ('max_bet', ''),
                    ('sp_max_bet', ''),
                    ('lock_stake_lmt', 'N'),
                    ('lock_stake_win', 'N'),
                    ('max_place_lp', ''),
                    ('max_place_sp', ''),
                    ('lock_stake_place', 'N'),
                    ('max_total', ''),
                    ('fc_stk_limit', ''),
                    ('tc_stk_limit', ''),
                    ('ew_factor', ''),
                    ('acc_min', ''),
                    ('fixed_stake_limits', 'N'),
                    ('fb_result', selection_type),
                    ('note_channels', 'P'),
                    ('note_channel_E', ''),
                    ('note_channel_I', ''),
                    ('note_channel_O', ''),
                    ('note_channel_T', ''),
                    ('note_channel_C', ''),
                    ('note_channel_N', ''),
                    ('note_channel_W', ''),
                    ('note_channel_D', ''),
                    ('note_channel_Z', ''),
                    ('note_channel_V', ''),
                    ('note_channel_P', ''),
                    ('note_channel_H', ''),
                    ('note_channel_L', ''),
                    ('note_channel_U', ''),
                    ('note_channel_F', ''),
                    ('note_channel_S', ''),
                    ('note_channel_X', ''),
                    ('note_channel_J', ''),
                    ('note_channel_Q', ''),
                    ('note_channel_R', ''),
                    ('note_channel_Y', ''),
                    ('note_channel_M', ''),
                    ('note_channel_@', ''),
                    ('note_channel_K', ''),
                    ('note_channel_p', ''),
                    ('note_channel_G', ''),
                    ('note_channel_t', ''),
                    ('note_channel_B', ''),
                    ('note_channel_e', ''),
                    ('note_channel_f', ''),
                    ('note_channel_y', ''),
                    ('note_channel_z', ''),
                    ('channel_E', 'N'),
                    ('channel_I', 'Y'),
                    ('channel_O', 'N'),
                    ('channel_T', 'N'),
                    ('channel_C', 'Y'),
                    ('channel_N', 'N'),
                    ('channel_W', 'N'),
                    ('channel_D', 'N'),
                    ('channel_Z', 'N'),
                    ('channel_V', 'N'),
                    ('channel_P', 'Y'),
                    ('channel_H', 'N'),
                    ('channel_L', 'N'),
                    ('channel_U', 'N'),
                    ('channel_F', 'N'),
                    ('channel_S', 'N'),
                    ('channel_X', 'N'),
                    ('channel_J', 'N'),
                    ('channel_Q', 'Y'),
                    ('channel_R', 'N'),
                    ('channel_Y', 'N'),
                    ('channel_M', 'Y'),
                    ('channel_@', 'N'),
                    ('channel_K', 'N'),
                    ('channel_p', 'N'),
                    ('channel_G', 'N'),
                    ('channel_t', 'N'),
                    ('channel_B', 'N'),
                    ('channel_e', 'N'),
                    ('channel_f', 'N'),
                    ('channel_y', 'N'),
                    ('channel_z', 'N'),
                    ('channels_list', 'IPCMQ'),
                    ('exact_flags', 'Y')
                )
                do_request(url=self.site, params=params, load_response=False, cookies=self.site_cookies)

        selection_ids = self.get_selection_ids(marketID=marketID)
        if not selection_ids:
            raise OBException(f'Not all selections were added to market id {marketID}')
        return selection_ids

    def get_selection_ids(self, marketID=None):
        marketID = marketID if marketID else self.marketID
        params = '?action=hierarchy::market::H_get_selections&id=%s&clone=N' % marketID
        url = self.site + params
        r = requests.post(url=url, cookies=self.site_cookies, verify=False)
        check_status_code(r)
        page = html.fromstring(r.content)
        selections = page.xpath('//a[not(contains(@href, "result"))]')
        selections_dict = OrderedDict()
        for i, link in enumerate(selections):
            find = re.search(r'(\d+)', link.attrib['href'])
            selection_name = link.text.replace('|', '')
            selection_id = find.group(1) if find is not None else None
            self._logger.debug(f'*** Selection #{i + 1}: name {selection_name}, id: {selection_id}')
            selections_dict[selection_name] = selection_id

        from crlat_siteserve_client.siteserve_client import SiteServeRequests
        s = SiteServeRequests(env=self.env, brand=self.brand)

        # Comparing that # of selections in SS is the same as added into TI
        wait_for_result(lambda: sum([len(market.get('market', {}).get('children', []))
                                     for market in s.ss_events_to_outcome_for_markets(market_ids=[marketID],
                                                                                      raise_exceptions=False,
                                                                                      timeout=50)[0].get('event', {}).get('children', [])
                                     if str(market.get('market', {}).get('id')) == str(marketID)]) == len(selections_dict),
                        name='Selections to appear in SS',
                        bypass_exceptions=(KeyError, IndexError, AttributeError, ReadTimeout),
                        poll_interval=2,
                        timeout=self.ss_timeout)

        selections = OrderedDict(sorted(selections_dict.items(), key=lambda x: int(x[1])))
        return selections

    def add_lucky_dip_market_and_selection(self, **kwargs):
        market_id = self.create_market(event_id=kwargs.get('event_id'),
                                       market_name=kwargs.get('market_name'),
                                       market_template_id=kwargs.get('market_template_id'),
                                       disporder=kwargs.get('disporder'),
                                       bet_in_run=kwargs.get('bet_in_run'),
                                       market_displayed=kwargs.get('market_displayed')
                                       )
        return (market_id, self.add_lucky_dip_selections(marketID=market_id, max_bet=kwargs.get('max_bet', 10.0),
                                                         selection_names=kwargs.get('selections_names'),
                                                         odds=kwargs.get('odds', '125/1')))

    def add_lucky_dip_selections(self, selection_names, marketID, max_bet, odds='125/1'):
        selection_ids = {}
        not_diplayed_selection = selection_names[:-1]
        displayed_selection = selection_names[-1]
        selection_types = ['A'] * len(not_diplayed_selection)  # actually, selection_types is not needed at all, but otherwise add_selections will fail
        prices = [f"{odds}"] * len(not_diplayed_selection)
        selection_ids["not_diplayed_selection"] = self.add_selections(marketID=marketID, max_bet=max_bet,
                                                                      selection_names=not_diplayed_selection,
                                                                      selection_types=selection_types, prices=prices,
                                                                      selections_displayed=False)
        selection_ids["diplayed_selection"] = self.add_selections(marketID=marketID, max_bet=max_bet,
                                                                  selection_names=displayed_selection,
                                                                  selection_types="A", prices=[f"{odds}"],
                                                                  selections_displayed=True)
        return selection_ids


class CreateRacingEvent(CreateSportEvent):
    def __init__(self, env, brand, category_id, class_id, type_id, event_name_pattern=None,
                 market_template_id=None, market_name=None, *args, **kwargs):
        CreateSportEvent.__init__(self, env, brand, category_id, class_id, type_id, market_template_id, market_name, *args, **kwargs)
        self.event_name_pattern = event_name_pattern
        self.default_ew_terms = {'ew_places': 3, 'ew_fac_num': 1, 'ew_fac_den': 8}

    def create_event(self, is_live=False, is_tomorrow=False, cashout=True, **kwargs):
        """
        :param is_live: if event is live now
        :param is_tomorrow: if event is tomorrow event
        :param is_antepost: if event is antepost event
        :param cashout: if event has cashout enabled
        :param kwargs: time_to_start in minutes, should be applied to live event
        :return:
        """
        if 'start_time' in kwargs and kwargs['start_time']:
            event_off_time = re.search(r'\d{1,2}:\d{2}', kwargs['start_time']).group()
            if self.brand == 'bma':
                event_start_time_url = quote(kwargs['start_time'])
            else:
                event_start_time_url = kwargs['start_time']
        else:
            time_to_start = kwargs.get('time_to_start', randint(1, 240))
            if is_live:
                event_date_time_obj = get_date_time_object(minutes=time_to_start)
            elif is_tomorrow:
                event_date_time_obj = get_date_time_object(days=1, minutes=time_to_start)
            else:
                event_date_time_obj = get_date_time_object(hours=0 if 'time_to_start' in kwargs else 1,
                                     minutes=time_to_start)  # if event has time_to_start in minutes then obviously user don't want extra hour
            if self.brand == 'bma':
                event_start_time_url = get_date_time_as_string(date_time_obj=event_date_time_obj, time_format="%Y-%m-%d %H:%M:%S", url_encode=True)
            else:
                event_start_time_url = get_date_time_as_string(date_time_obj=event_date_time_obj,
                                                               time_format="%Y-%m-%d %H:%M:%S")
            event_off_time = event_date_time_obj.strftime("%H:%M")

        if self.brand == 'bma':
            if self.type_id == self.horseracing_config.daily_racing_specials.enhanced_multiples.type_id:
                event_name = quote('|%s|' % self.event_name_pattern)
            else:
                event_name = quote('|%s %s|' % (event_off_time, self.event_name_pattern))
        else:
            if self.type_id == self.horseracing_config.daily_racing_specials.enhanced_multiples.type_id:
                event_name = '|%s|' % self.event_name_pattern
            else:
                event_name = '|%s %s|' % (event_off_time, self.event_name_pattern)

        flags = 'NE,'

        if 'at_races_stream' in kwargs and kwargs['at_races_stream']:
            flag_AVA_value = 'Y'
            flags += 'AVA,'
        else:
            flag_AVA_value = 'N'

        at_time_string = get_date_time_as_string(time_format='%Y-%m-%d %H:%M:%S', days=1)
        suspend_at = kwargs.get('suspend_at', at_time_string)

        is_off_value = 'Y' if is_live else 'N'
        flag_BL_value = 'Y' if is_live else 'N'
        flags = flags + 'BL,' if is_live else flags
        max_bet = kwargs['max_bet'] if 'max_bet' in kwargs else ''
        max_mult_bet = kwargs['max_mult_bet'] if 'max_mult_bet' in kwargs else ''
        min_bet = kwargs['min_bet'] if 'min_bet' in kwargs else ''

        is_antepost = True if 'is_antepost' in kwargs and kwargs['is_antepost'] else False
        if is_antepost:
            flag_AP_value, flag_APR_value = 'Y', 'Y'
            flags += 'AP,APR,'
        else:
            flag_AP_value, flag_APR_value = 'N', 'N'

        is_national_hunt = True if 'is_national_hunt' in kwargs and kwargs['is_national_hunt'] else False

        if is_national_hunt:
            flag_NH_value, flag_AP_value, flag_APR_value = 'Y', 'Y', 'Y'
            flags += 'NH,AP,APR'
        else:
            flag_NH_value ='N'

        is_flat = True if 'is_flat' in kwargs and kwargs['is_flat'] else False
        if is_flat:
            flag_FT_value, flag_AP_value, flag_APR_value = 'Y', 'Y', 'Y'
            flags += 'FT,AP,APR,'
        else:
            flag_FT_value = 'N'

        is_inplay_horse_race = True if 'is_inplay_horse_race' in kwargs and kwargs['is_inplay_horse_race'] else False
        if is_inplay_horse_race:
            flag_IHR_value = 'Y'
            flags += 'IHR,'
        else:
            flag_IHR_value = 'N'

        is_international = True if 'is_international' in kwargs and kwargs['is_international'] else False
        if is_international:
            flag_IT_value, flag_AP_value, flag_APR_value = 'Y', 'Y', 'Y'
            flags += 'IT,AP,APR,'
        else:
            flag_IT_value = 'N'

        flag_FIN_value, flag_BBL_value, flag_EPR_value, flag_FRT_value = 'N', 'N', 'N', 'N'  # for promotions
        if 'fallers_insurance' in kwargs and kwargs['fallers_insurance']:
            flag_FIN_value = 'Y'
            flags += 'FIN,'
        if 'beaten_by_a_length' in kwargs and kwargs['beaten_by_a_length']:
            flag_BBL_value = 'Y'
            flags += 'BBL,'
        if 'extra_place_race' in kwargs and kwargs['extra_place_race']:
            flag_EPR_value = 'Y'
            flags += 'EPR,'
        if 'featured_racing_types' in kwargs and kwargs['featured_racing_types']:
            flag_FRT_value = 'Y'
            flags += 'FRT,'

        cashout = 'Y' if cashout else 'N'
        enhanced_odds = kwargs.get('enhanced_odds', 'Y') or 'N'
        flag_mb_value = kwargs.get('money_back', 'N')
        if flag_mb_value is True:
            flag_mb_value = 'Y'
            flags += ',MB,'
        flag_pb_value = kwargs.get('price_boost', 'N')
        if flag_pb_value is True:
            flag_pb_value = 'Y'
            flags += ',PB,'
        url = '{0}/hierarchy/type/{1}'.format(self.site, self.type_id)
        if self.brand == 'bma':
            params = '?action=hierarchy::event::H_insert' \
                     '&id=&read_only=N' \
                     '&name={name}' \
                     '&type_id={type_id}' \
                     '&class_id={class_id}' \
                     '&category_name=' \
                     '&class_sort=HR' \
                     '&home_team=&away_team=&home_id=&away_id=' \
                     '&displayed=Y&disporder=0&status=A&allow_stl=Y' \
                     '&start_time={start_time}' \
                     '&est_start_time=' \
                     '&suspend_at={suspend_at}' \
                     '&feed_updateable=-' \
                     '&bir_delay=' \
                     '&min_bet={min_bet}' \
                     '&max_mult_bet={max_mult_bet}' \
                     '&max_bet={max_bet}' \
                     '&sp_max_bet={max_bet}' \
                     '&max_place_lp={max_bet}' \
                     '&max_place_sp={max_bet}' \
                     '&liability=&ew_factor=&venue=&country=&sort=MTCH' \
                     '&mult_key=&ext_key=&' \
                     'is_off={is_off_value}' \
                     '&sett_at_sp_from=&sett_at_sp_to=&late_bet_toll=&on_settl=na' \
                     '&calendar=N' \
                     '&cashout_avail={cash_out}&blurb_sort=EVENT' \
                     '&enhanced_odds_avail={enhanced_odds}' \
                     '&blurb_language=all&multi_blurb_all=&multi_blurb_EVENT_lang_en=' \
                     '&multi_blurb_EVENT_lang_wp=&multi_blurb_EVENT_lang_01=&note_channels=P' \
                     '&note_channel_I=&note_channel_P=&note_channel_C=&note_channel_M=&note_channel_Q=&note_channel_D=' \
                     '&note_channel_T=&note_channel_G=&note_channel_W=&note_channel_J=&' \
                     'flag_HC=N&flag_ST=N' \
                     '&flag_BL={flag_bl_value}' \
                     '&flag_MB={flag_mb_value}' \
                     '&flag_PB={flag_pb_value}' \
                     '&flag_FE=N' \
                     '&flag_FI=N' \
                     '&flag_FT={flag_FT_value}' \
                     '&flag_NH={flag_NH_value}' \
                     '&flag_IT={flag_IT_value}' \
                     '&flag_NE=Y' \
                     '&flag_RD=N' \
                     '&flag_AP={flag_AP_value}' \
                     '&flag_RVA=N' \
                     '&flag_AVA={flag_AVA_value}' \
                     '&flag_FRT=N' \
                     '&flag_RF=N&flag_ES=N&flag_SM=N' \
                     '&flag_APR={flag_APR_value}' \
                     '&flag_IHR={flag_IHR_value}' \
                     '&flag_AIR=N&flag_EWP=N&flag_NRNB=N&flag_GVM=N' \
                     '&flag_FIN={flag_FIN_value}' \
                     '&flag_BBL={flag_BBL_value}' \
                     '&flag_EPR={flag_EPR_value}' \
                     '&flag_FRT={flag_FRT_value}' \
                     '&flags_list=' \
                     '&channel_I=Y' \
                     '&channel_P=Y&channel_C=Y&channel_M=Y&channel_Q=Y' \
                     '&channel_D=N&channel_T=N&channel_G=N&channel_W=N&channel_J=N&channels_list=IPCMQ&tv_channel_34=N' \
                     '&tv_channel_1=N&tv_channel_3=N&tv_channel_4=N&tv_channel_5=N&tv_channel_6=N&tv_channel_2=N' \
                     '&tv_channel_36=N&tv_channel_37=N' \
                     '&tv_channel_7=N&tv_channel_9=N&tv_channel_10=N&tv_channel_11=N&tv_channel_39=N&tv_channel_12=N' \
                     '&tv_channel_8=N&tv_channel_13=N&tv_channel_14=N' \
                     '&tv_channel_15=N&tv_channel_16=N&tv_channel_17=N&tv_channel_18=N&tv_channel_19=N&tv_channel_20=N' \
                     '&tv_channel_35=N&tv_channel_38=N&tv_channel_21=N&tv_channel_22=N&tv_channel_23=N&tv_channel_26=N' \
                     '&tv_channel_40=N&tv_channel_27=N&tv_channel_28=N&tv_channel_29=N&tv_channel_30=N&tv_channel_24=N' \
                     '&tv_channel_25=N&tv_channel_31=N&tv_channel_32=N&tv_channel_33=N' \
                     '&tv_flags_list=AVA%2CNE%2CQL%2CUK%2C&flags={flags}' \
                .format(name=event_name, type_id=self.type_id, class_id=self.class_id, start_time=event_start_time_url,
                        max_mult_bet=max_mult_bet, max_bet=max_bet, min_bet=min_bet, cash_out=cashout, enhanced_odds=enhanced_odds, is_off_value=is_off_value,
                        flag_bl_value=flag_BL_value, flags=flags, flag_AP_value=flag_AP_value, flag_APR_value=flag_APR_value,
                        flag_FIN_value=flag_FIN_value, flag_BBL_value=flag_BBL_value, flag_EPR_value=flag_EPR_value,
                        flag_FRT_value=flag_FRT_value, flag_FT_value=flag_FT_value, flag_NH_value=flag_NH_value,
                        flag_IT_value=flag_IT_value, flag_mb_value=flag_mb_value, flag_pb_value=flag_pb_value, flag_AVA_value=flag_AVA_value, suspend_at=suspend_at, flag_IHR_value=flag_IHR_value)
            url = url + params.strip(',')
            resp_dict = do_request(url=url, cookies=self.site_cookies)
        else:
            params = (
                ('action', 'hierarchy::event::H_insert'),
                ('id', ''),
                ('read_only', 'N'),
                ('name', event_name),
                ('type_id', self.type_id),
                ('class_id', self.class_id),
                ('category_name', ''),
                ('class_sort', 'HR'),
                ('home_team', ''),
                ('away_team', ''),
                ('home_id', ''),
                ('away_id', ''),
                ('displayed', 'Y'),
                ('disporder', ''),
                ('status', 'A'),
                ('allow_stl', 'Y'),
                ('start_time', event_start_time_url),
                ('est_start_time', ''),
                ('suspend_at', suspend_at),
                ('feed_updateable', '-'),
                ('bir_delay', ''),
                ('is_off', is_off_value),
                ('liability', ''),
                ('min_bet', min_bet),
                ('max_mult_bet', max_mult_bet),
                ('max_bet', max_bet),
                ('sp_max_bet', ''),
                ('max_place_lp', ''),
                ('max_place_sp', ''),
                ('least_max_bet', '1.00'),
                ('most_max_bet', '500000.00'),
                ('lay_to_lose', ''),
                ('ew_factor', ''),
                ('venue', ''),
                ('country', ''),
                ('sort', 'MTCH'),
                ('mult_key', ''),
                ('ext_key', ''),
                ('domain', '-'),
                ('sett_at_sp_from', ''),
                ('sett_at_sp_to', ''),
                ('late_bet_toll', ''),
                ('on_settl', 'na'),
                ('calendar', 'N'),
                ('cashout_avail', cashout),
                ('enhanced_odds_avail', enhanced_odds),
                ('blurb_sort', 'EVENT'),
                ('blurb_language', 'all'),
                ('multi_blurb_all', ''),
                ('multi_blurb_EVENT_lang_en', ''),
                ('multi_blurb_EVENT_lang_ru', ''),
                ('multi_blurb_EVENT_lang_cn', ''),
                ('multi_blurb_EVENT_lang_it', ''),
                ('multi_blurb_EVENT_lang_es', ''),
                ('multi_blurb_EVENT_lang_sw', ''),
                ('multi_blurb_EVENT_lang_th', ''),
                ('multi_blurb_EVENT_lang_dk', ''),
                ('multi_blurb_EVENT_lang_no', ''),
                ('multi_blurb_EVENT_lang_ie', ''),
                ('multi_blurb_EVENT_lang_de', ''),
                ('multi_blurb_EVENT_lang_gr', ''),
                ('multi_blurb_EVENT_lang_fi', ''),
                ('multi_blurb_EVENT_lang_cs', ''),
                ('multi_blurb_EVENT_lang_as', ''),
                ('multi_blurb_EVENT_lang_tr', ''),
                ('multi_blurb_EVENT_lang_pt', ''),
                ('multi_blurb_EVENT_lang_oo', ''),
                ('multi_blurb_EVENT_lang_pl', ''),
                ('multi_blurb_EVENT_lang_bg', ''),
                ('multi_blurb_EVENT_lang_ro', ''),
                ('multi_blurb_EVENT_lang_ca', ''),
                ('multi_blurb_EVENT_lang_hr', ''),
                ('multi_blurb_EVENT_lang_za', ''),
                ('multi_blurb_EVENT_lang_fr', ''),
                ('multi_blurb_EVENT_lang_f2', ''),
                ('multi_blurb_EVENT_lang_sk', ''),
                ('multi_blurb_EVENT_lang_si', ''),
                ('multi_blurb_EVENT_lang_cz', ''),
                ('multi_blurb_EVENT_lang_hu', ''),
                ('multi_blurb_EVENT_lang_id', ''),
                ('multi_blurb_EVENT_lang_af', ''),
                ('note_channels', 'P'),
                ('note_channel_E', ''),
                ('note_channel_I', ''),
                ('note_channel_O', ''),
                ('note_channel_T', ''),
                ('note_channel_C', ''),
                ('note_channel_N', ''),
                ('note_channel_W', ''),
                ('note_channel_D', ''),
                ('note_channel_Z', ''),
                ('note_channel_V', ''),
                ('note_channel_P', ''),
                ('note_channel_H', ''),
                ('note_channel_L', ''),
                ('note_channel_U', ''),
                ('note_channel_F', ''),
                ('note_channel_S', ''),
                ('note_channel_X', ''),
                ('note_channel_J', ''),
                ('note_channel_Q', ''),
                ('note_channel_R', ''),
                ('note_channel_Y', ''),
                ('note_channel_M', ''),
                ('note_channel_@', ''),
                ('note_channel_K', ''),
                ('note_channel_p', ''),
                ('note_channel_G', ''),
                ('note_channel_t', ''),
                ('note_channel_B', ''),
                ('note_channel_e', ''),
                ('note_channel_f', ''),
                ('note_channel_y', ''),
                ('note_channel_z', ''),
                ('flag_HC', 'N'),
                ('flag_ST', 'N'),
                ('flag_BL', flag_BL_value),
                ('flag_FE', 'N'),
                ('flag_FI', 'N'),
                ('flag_NE', 'Y'),
                ('flag_RD', 'N'),
                ('flag_AP', flag_AP_value),
                ('flag_RVA', 'N'),
                ('flag_AVA', 'Y'),
                ('flag_FRT', 'N'),
                ('flag_RF', 'N'),
                ('flag_ES', 'N'),
                ('flag_SM', 'N'),
                ('flag_APR', flag_APR_value),
                ('flag_AIR', 'N'),
                ('flag_EWP', 'N'),
                ('flag_NRNB', 'N'),
                ('flag_GVM', 'N'),
                ('flag_RW', 'N'),
                ('flag_EPR', flag_EPR_value),
                ('flag_PB', flag_pb_value),
                ('flag_MB', 'N'),
                ('flag_PR1', 'N'),
                ('flag_PR2', 'N'),
                ('flag_3E', 'N'),
                ('flag_FIN', flag_FIN_value),
                ('flag_YC', 'N'),
                ('flags_list', ''),
                ('flag_IHR', flag_IHR_value),
                ('channel_E', 'N'),
                ('channel_I', 'Y'),
                ('channel_O', 'N'),
                ('channel_T', 'N'),
                ('channel_C', 'Y'),
                ('channel_N', 'N'),
                ('channel_W', 'N'),
                ('channel_D', 'N'),
                ('channel_Z', 'N'),
                ('channel_V', 'N'),
                ('channel_P', 'Y'),
                ('channel_H', 'N'),
                ('channel_L', 'N'),
                ('channel_U', 'N'),
                ('channel_F', 'N'),
                ('channel_S', 'N'),
                ('channel_X', 'N'),
                ('channel_J', 'N'),
                ('channel_Q', 'Y'),
                ('channel_R', 'N'),
                ('channel_Y', 'N'),
                ('channel_M', 'Y'),
                ('channel_@', 'N'),
                ('channel_K', 'N'),
                ('channel_p', 'N'),
                ('channel_G', 'N'),
                ('channel_t', 'N'),
                ('channel_B', 'N'),
                ('channel_e', 'N'),
                ('channel_f', 'N'),
                ('channel_y', 'N'),
                ('channel_z', 'N'),
                ('channels_list', 'IPCMQ'),
                ('tv_channel_34', 'N'),
                ('tv_channel_1', 'N'),
                ('tv_channel_6', 'N'),
                ('tv_channel_3', 'N'),
                ('tv_channel_5', 'N'),
                ('tv_channel_4', 'N'),
                ('tv_channel_2', 'N'),
                ('tv_channel_36', 'N'),
                ('tv_channel_37', 'N'),
                ('tv_channel_51', 'N'),
                ('tv_channel_52', 'N'),
                ('tv_channel_54', 'N'),
                ('tv_channel_7', 'N'),
                ('tv_channel_11', 'N'),
                ('tv_channel_39', 'N'),
                ('tv_channel_12', 'N'),
                ('tv_channel_8', 'N'),
                ('tv_channel_9', 'N'),
                ('tv_channel_13', 'N'),
                ('tv_channel_14', 'N'),
                ('tv_channel_15', 'N'),
                ('tv_channel_53', 'N'),
                ('tv_channel_16', 'N'),
                ('tv_channel_17', 'N'),
                ('tv_channel_18', 'N'),
                ('tv_channel_19', 'N'),
                ('tv_channel_20', 'N'),
                ('tv_channel_35', 'N'),
                ('tv_channel_38', 'N'),
                ('tv_channel_21', 'N'),
                ('tv_channel_22', 'N'),
                ('tv_channel_23', 'N'),
                ('tv_channel_24', 'N'),
                ('tv_channel_25', 'N'),
                ('tv_channel_26', 'N'),
                ('tv_channel_27', 'N'),
                ('tv_channel_28', 'N'),
                ('tv_channel_29', 'N'),
                ('tv_channel_30', 'N'),
                ('tv_channel_40', 'N'),
                ('tv_channel_47', 'N'),
                ('tv_channel_48', 'N'),
                ('tv_channel_50', 'N'),
                ('tv_channel_44', 'N'),
                ('tv_channel_46', 'N'),
                ('tv_channel_42', 'N'),
                ('tv_channel_45', 'N'),
                ('tv_channel_41', 'N'),
                ('tv_channel_49', 'N'),
                ('tv_channel_43', 'N'),
                ('tv_channel_31', 'N'),
                ('tv_channel_32', 'N'),
                ('tv_channel_33', 'N'),
                ('tv_flags_list', 'AVA,NE,QL,UK,'),
                ('flags', flags)
            )
            resp_dict = do_request(url=url, params=params, cookies=self.site_cookies)

        if 'id' not in resp_dict or not resp_dict['id']:
            raise OBException(f'Create event response does not have event_id, response is: {resp_dict}')
        self.eventID = resp_dict['id']

        event_date_time = unquote_plus(event_start_time_url)
        parameters = namedtuple('event_parameters', ['eventID', 'event_off_time', 'event_date_time'])
        event_with_params = parameters(self.eventID, event_off_time, event_date_time)
        self._logger.debug('*** Event id is: %s' % event_with_params.eventID)
        return event_with_params

    def create_event_with_participant_id(self, type_id, event_name, start_time, selection_count, external_comp_id, **kwargs):
        """
        Creates an event with a specified number of participant IDs and sends a request to the backend.

        Args:
            type_id (str): The type ID for the event.
            event_name (str): The name of the event.
            start_time (str): The start time of the event in the format 'YYYY-MM-DD HH:MM:SS'.
            selection_count (int): The number of participants to include in the event.
            external_comp_id (list): List of numbers which are unique to a specific horses.
            **kwargs: Optional parameters to customize the event and participants.

        Note: The length of external_comp_id should be greater than or equal to selection_count.

        Returns:
            tuple: A tuple containing the response from the backend request and the list of remaining external competition IDs if any.
        """
        url = self.backend.feeds.hostname
        headers = {'Content-Type': 'application/xml'}

        # Extract or set default values for optional parameters
        event_status = kwargs.get('event_status', 'active')
        event_displayed = kwargs.get('event_displayed', 'yes')
        event_bet_limits_min = kwargs.get('event_bet_limits_min', '1')
        event_bet_limits_max = kwargs.get('event_bet_limits_max', '50000')
        max_potential_win = kwargs.get('max_potential_win', '50000')
        channel = kwargs.get('channel', 'I')
        hold_settlement = kwargs.get('hold_settlement', 'no')
        market_status = kwargs.get('market_status', 'active')
        market_name = kwargs.get('market_name', '|Win or Each Way|')
        market_displayed = kwargs.get('market_displayed', 'yes')
        market_pricing_live = kwargs.get('market_pricing_live', 'yes')
        market_pricing_starting = kwargs.get('market_pricing_starting', 'no')
        market_pricing_guaranteed = kwargs.get('market_pricing_guaranteed', 'no')
        ew_avail = kwargs.get('ew_avail', 'yes')
        ew_places = kwargs.get('ew_places', '2')
        ew_fac_num = kwargs.get('ew_fac_num', '1')
        ew_fac_den = kwargs.get('ew_fac_den', '4')
        pl_avail = kwargs.get('pl_avail', 'yes')
        liability_limit = kwargs.get('liability_limit', '25000')
        accumulator_min = kwargs.get('accumulator_min', '1')
        accumulator_max = kwargs.get('accumulator_max', '25')
        bet_limits_max_multiple = kwargs.get('bet_limits_max_multiple', '50000.00')
        bet_limits_max_potential_win = kwargs.get('bet_limits_max_potential_win', '50000')
        ante_post = kwargs.get('ante_post', 'no')
        auto_traded = kwargs.get('auto_traded', 'no')
        betting_in_running_active = kwargs.get('betting_in_running_active', 'no')
        betting_in_running_delay = kwargs.get('betting_in_running_delay', '0')
        selection_status = kwargs.get('selection_status', 'active')
        selection_display = kwargs.get('selection_display', 'yes')
        market_bet_limits_min = kwargs.get('market_bet_limits_min', '0.01')
        market_bet_limits_max = kwargs.get('market_bet_limits_max', '50000.00')
        selection_bet_limits_min = kwargs.get('selection_bet_limits_min', '0.01')
        selection_bet_limits_max = kwargs.get('selection_bet_limits_max', '50000.00')

        if selection_count > len(external_comp_id):
            raise OBException(
                f'selection_count: {selection_count} should be less than or equal the length of external_comp_id: {len(external_comp_id)}')

        # Build selectionInsert XML blocks dynamically based on selection_count
        selection_inserts = ""

        for i in range(selection_count):
            count = i + 1
            selection_inserts += f'''<selectionInsert>
                           <form provider="Amelco_PA" formUpdateable="yes">
                               <externalCompId>{external_comp_id.pop()}</externalCompId>
                           </form>
                           <selectionName>|{event_name} S{count}|</selectionName>
                           <price type="fractional">{count}/10</price>
                           <status>{selection_status}</status>
                           <display displayed="{selection_display}" />
                           <runnerNumber>{count}</runnerNumber>
                           <betLimits min="{selection_bet_limits_min}" max="{selection_bet_limits_max}"/>
                       </selectionInsert>'''

        data = f'''<?xml version="1.0" encoding="UTF-8"?>
        <oxiFeedRequest version="1.0">
            <auth username="{self.user}" password="{self.password}" />
            <eventInsert distance="480mtrs">
                <typeId>
                    <openbetId>{type_id}</openbetId>
                </typeId>
                <eventName>{event_name}</eventName>
                <startTime isOff="undefined">{start_time}</startTime>
                <status>{event_status}</status>
                <display displayed="{event_displayed}" />
                <eventSort>match</eventSort>
                <betLimits min="{event_bet_limits_min}" max="{event_bet_limits_max}" maxPotentialWin="{max_potential_win}">0</betLimits>
                <autoTraded>{auto_traded}</autoTraded>
                <channel>{channel}</channel>
                <holdSettlement>{hold_settlement}</holdSettlement>
                <marketInsert>
                    <status>{market_status}</status>
                    <marketSort code="--" name="{market_name}" />
                    <display displayed="{market_displayed}" order="0" />
                    <pricing live="{market_pricing_live}" starting="{market_pricing_starting}" guaranteed="{market_pricing_guaranteed}" />
                    <ewAvail>{ew_avail}</ewAvail>
                    <ewPlaces>{ew_places}</ewPlaces>
                    <ewFacNum>{ew_fac_num}</ewFacNum>
                    <ewFacDen>{ew_fac_den}</ewFacDen>
                    <plAvail>{pl_avail}</plAvail>
                    <liability limit="{liability_limit}" />
                    <accumulator min="{accumulator_min}" max="{accumulator_max}">0</accumulator>
                    <betLimits min="{market_bet_limits_min}" max="{market_bet_limits_max}"  maxMultiple="{bet_limits_max_multiple}" maxPotentialWin="{bet_limits_max_potential_win}">0</betLimits>
                    <antepost>{ante_post}</antepost>
                    <autoTraded>{auto_traded}</autoTraded>
                    <bettingInRunning active="{betting_in_running_active}" delay="{betting_in_running_delay}" />
                    {selection_inserts}
                </marketInsert>
                <raceLength units="FR">4.60</raceLength>
            </eventInsert>
        </oxiFeedRequest>'''

        return do_request(url, method='POST', data=data, headers=headers, cookies=self.site_cookies,
                          load_response=False), external_comp_id

    def create_market(self, bet_in_run='N', forecast_available=False, tricast_available=False,
                   cashout=True, ew_terms=None, specials=False, **kwargs):
        """
        :param ew_terms: dictionary with the following keys:
            ew_places, ew_fac_num, ew_fac_den
        :param forecast_available: 'Y' or 'N'
        :param tricast_available: 'Y' or 'N'
        """
        class_sort = 'HR' if self.category_id == self.horseracing_config.category_id else 'GR'
        market_name = kwargs['market_name'] if 'market_name' in kwargs else self.market_name
        market_template_id = kwargs['market_template_id'] if 'market_template_id' in kwargs else self.market_template_id
        class_id = kwargs['class_id'] if 'class_id' in kwargs else self.class_id
        event_id = kwargs['event_id'] if 'event_id' in kwargs else self.eventID
        market_displayed = 'N' if 'market_displayed' in kwargs.keys() and kwargs['market_displayed'] is False else 'Y'
        forecast_available = 'Y' if forecast_available else 'N'
        tricast_available = 'Y' if tricast_available else 'N'
        cashout_available = 'Y' if cashout else 'N'
        enhanced_odds = kwargs.get('enhanced_odds', 'Y') or 'N'
        is_antepost = any(param for param in ('is_antepost', 'is_national_hunt', 'is_flat', 'is_international')
                          if param in kwargs and kwargs[param])
        is_antepost_value = 'Y' if is_antepost else 'N'
        bet_in_run_value = 'Y' if bet_in_run or ('is_upcoming_bet_in_run' in kwargs and kwargs['is_upcoming_bet_in_run']) else 'N'
        market_extra_place_race = 'Y' if 'market_extra_place_race' in kwargs and kwargs['market_extra_place_race'] else 'N'
        market_beaten_by_a_length = 'Y' if kwargs.get('market_beaten_by_a_length') else 'N'
        lp_available = 'Y' if kwargs.get('lp', False) else 'N'
        sp_available = 'Y' if kwargs.get('sp', True) else 'N'
        disporder = kwargs['disporder'] if 'disporder' in kwargs.keys() \
            else self._find_disporder_for_market(market_template_id)
        if kwargs.get('gp', False):
            gp_available, lp_available, sp_available = 'Y', 'Y', 'Y'
        else:
            gp_available= 'N'
        ep_available = 'Y' if kwargs.get('ep', False) else 'N'
        flags = ''
        url = '{0}/hierarchy/event/{1}'.format(self.site, event_id)

        each_way_terms = ew_terms if ew_terms is not None else self.default_ew_terms
        if each_way_terms:
            ew_available, ew_places, ew_fac_num, ew_fac_den = \
                'Y', each_way_terms['ew_places'], each_way_terms['ew_fac_num'], each_way_terms['ew_fac_den']
        else:
            ew_available, ew_places, ew_fac_num, ew_fac_den = 'N', '', '', ''
        flag_SP = 'Y' if specials else 'N'
        flags += 'SP,' if specials else ''
        flags += 'EPR,' if 'market_extra_place_race' in kwargs and kwargs['market_extra_place_race'] else ''
        flags += 'BBAL,' if kwargs.get('market_beaten_by_a_length') else ''
        flag_mb_value = kwargs.get('money_back', 'N')
        if flag_mb_value is True:
            flag_mb_value = 'Y'
            flags += 'MB,'
        flag_pb_value = kwargs.get('price_boost', 'N')
        if flag_pb_value is True:
            flag_pb_value = 'Y'
            flags += 'PB,'

        if self.brand == 'bma':
            params = '?action=hierarchy::market::H_insert' \
                     '&id=&read_only=N' \
                     '&name={name}' \
                     '&class_sort={class_sort}' \
                     '&displayed={market_displayed}' \
                     '&disporder={disporder}&status=A' \
                     '&ev_id={event_id}' \
                     '&ev_oc_grp_id={market_template_id}' \
                     '&sort=--&clone=' \
                     '&class_id={class_id}' \
                     '&suspend_at=&' \
                     'lp_avail={lp_available}' \
                     '&sp_avail={sp_available}' \
                     '&gp_avail={gp_available}' \
                     '&ep_active={ep_available}' \
                     '&fc_avail={forecast_available}' \
                     '&tc_avail={tricast_available}' \
                     '&pl_avail=N' \
                     '&ew_avail={ew_available}' \
                     '&ew_places={ew_places}' \
                     '&ew_fac_num={ew_fac_num}' \
                     '&ew_fac_den={ew_fac_den}' \
                     '&ew_with_bet=N&liab_limit=' \
                     '&liab_limit_ep=&min_bet=&max_multiple_bet=&max_bet=&sp_max_bet=&win_lp=&win_sp=&win_ep=' \
                     '&place_lp=&place_sp=&place_ep=&ltl_min_bet=&ltl_max_bet=&acc_min=1&acc_max=25&acc_xmul=-' \
                     '&fc_stk_factor=&fc_min_stk_limit=&tc_stk_factor=&tc_min_stk_limit=&ew_factor=' \
                     '&feed_updateable=-&bet_in_run={bet_in_run}' \
                     '&bir_delay=&is_ap_mkt={is_antepost_value}' \
                     '&cashout_avail={cashout_available}' \
                     '&enhanced_odds_avail={enhanced_odds}' \
                     '&template_id=--' \
                     '&dbl_res=N&gp_terms=&blurb_sort=EV_MKT&blurb_language=all&multi_blurb_all=' \
                     '&multi_blurb_EV_MKT_lang_en=&multi_blurb_EV_MKT_lang_wp=&multi_blurb_EV_MKT_lang_01=' \
                     '&note_channels=P&note_channel_I=&note_channel_P=&note_channel_C=&note_channel_M=' \
                     '&note_channel_Q=&note_channel_D=&note_channel_T=&note_channel_G=&note_channel_W=' \
                     '&note_channel_J=' \
                     '&flag_MB={flag_mb_value}' \
                     '&flag_PB={flag_pb_value}' \
                     '&flag_GT=N' \
                     '&flag_SP={flag_SP}' \
                     '&flag_NRNB=N' \
                     '&flag_PVT=N' \
                     '&flag_SM=N' \
                     '&flag_EPR={market_extra_place_race}' \
                     '&flag_BBAL={market_beaten_by_a_length}' \
                     '&flags={flags}' \
                     '&channel_I=Y&channel_P=Y&channel_C=Y&channel_M=Y&channel_Q=Y&channel_D=N&channel_T=N' \
                     '&channel_G=N&channel_W=N&channel_J=N&channels_list=IPCMQ&price_ladder_id=&max_rule4=' \
                     '&mult_key_ev_allow=&allow_oc_combi=N&add_variants=&exact_flags=Y&flags={flags}' \
                .format(name=quote(market_name), event_id=event_id, market_template_id=market_template_id,
                        class_id=class_id, ew_available=ew_available, ew_places=ew_places, ew_fac_num=ew_fac_num,
                        ew_fac_den=ew_fac_den, lp_available=lp_available, sp_available=sp_available,
                        gp_available=gp_available, ep_available=ep_available, bet_in_run=bet_in_run_value,
                        cashout_available=cashout_available, enhanced_odds=enhanced_odds, forecast_available=forecast_available,
                        flag_SP=flag_SP, market_extra_place_race=market_extra_place_race, flags=flags, tricast_available=tricast_available,
                        is_antepost_value=is_antepost_value, market_displayed=market_displayed, flag_mb_value=flag_mb_value, flag_pb_value=flag_pb_value,
                        market_beaten_by_a_length=market_beaten_by_a_length, disporder=disporder, class_sort=class_sort)
            url = url + params.strip(',')
            resp_dict = do_request(url=url, cookies=self.site_cookies)
        else:
            flag_mb_value = kwargs.get('money_back', 'N')
            if flag_mb_value is True:
                flag_mb_value = 'Y'
            flag_pb_value = kwargs.get('price_boot', 'N')
            if flag_pb_value is True:
                flag_pb_value = 'Y'
            params = (
                ('action', 'hierarchy::market::H_insert'),
                ('id', ''),
                ('read_only', 'N'),
                ('name', market_name),
                ('displayed', market_displayed),
                ('disporder', disporder),
                ('status', 'A'),
                ('ev_id', event_id),
                ('ev_oc_grp_id', market_template_id),
                ('sort', '--'),
                ('class_sort', 'HR'),
                ('can_place', 'Y'),
                ('clone', ''),
                ('class_id', class_id),
                ('suspend_at', ''),
                ('lp_avail', lp_available),
                ('sp_avail', sp_available),
                ('gp_avail', gp_available),
                ('ep_active', ep_available),
                ('fc_avail', forecast_available),
                ('tc_avail', tricast_available),
                ('pl_avail', 'N'),
                ('ew_avail', ew_available),
                ('ew_places', ew_places),
                ('ew_fac_num', ew_fac_num),
                ('ew_fac_den', ew_fac_den),
                ('ew_with_bet', 'N'),
                ('liab_limit', ''),
                ('liab_limit_ep', ''),
                ('min_bet', ''),
                ('max_multiple_bet', ''),
                ('max_bet', ''),
                ('sp_max_bet', ''),
                ('win_lp', ''),
                ('win_sp', ''),
                ('win_ep', ''),
                ('place_lp', ''),
                ('place_sp', ''),
                ('place_ep', ''),
                ('ltl_min_bet', ''),
                ('ltl_max_bet', ''),
                ('acc_min', '1'),
                ('acc_max', '25'),
                ('acc_xmul', '-'),
                ('fc_stk_factor', ''),
                ('fc_min_stk_limit', ''),
                ('tc_stk_factor', ''),
                ('tc_min_stk_limit', ''),
                ('ew_factor', ''),
                ('feed_updateable', '-'),
                ('bet_in_run', bet_in_run_value),
                ('bir_delay', ''),
                ('is_ap_mkt', is_antepost_value),
                ('cashout_avail', cashout_available),
                ('enhanced_odds_avail', enhanced_odds),
                ('template_id', '--'),
                ('gp_terms', ''),
                ('blurb_sort', 'EV_MKT'),
                ('blurb_language', 'all'),
                ('multi_blurb_all', ''),
                ('multi_blurb_EV_MKT_lang_en', ''),
                ('multi_blurb_EV_MKT_lang_ru', ''),
                ('multi_blurb_EV_MKT_lang_cn', ''),
                ('multi_blurb_EV_MKT_lang_it', ''),
                ('multi_blurb_EV_MKT_lang_es', ''),
                ('multi_blurb_EV_MKT_lang_sw', ''),
                ('multi_blurb_EV_MKT_lang_th', ''),
                ('multi_blurb_EV_MKT_lang_dk', ''),
                ('multi_blurb_EV_MKT_lang_no', ''),
                ('multi_blurb_EV_MKT_lang_ie', ''),
                ('multi_blurb_EV_MKT_lang_de', ''),
                ('multi_blurb_EV_MKT_lang_gr', ''),
                ('multi_blurb_EV_MKT_lang_fi', ''),
                ('multi_blurb_EV_MKT_lang_cs', ''),
                ('multi_blurb_EV_MKT_lang_as', ''),
                ('multi_blurb_EV_MKT_lang_tr', ''),
                ('multi_blurb_EV_MKT_lang_pt', ''),
                ('multi_blurb_EV_MKT_lang_oo', ''),
                ('multi_blurb_EV_MKT_lang_pl', ''),
                ('multi_blurb_EV_MKT_lang_bg', ''),
                ('multi_blurb_EV_MKT_lang_ro', ''),
                ('multi_blurb_EV_MKT_lang_ca', ''),
                ('multi_blurb_EV_MKT_lang_hr', ''),
                ('multi_blurb_EV_MKT_lang_za', ''),
                ('multi_blurb_EV_MKT_lang_fr', ''),
                ('multi_blurb_EV_MKT_lang_f2', ''),
                ('multi_blurb_EV_MKT_lang_sk', ''),
                ('multi_blurb_EV_MKT_lang_si', ''),
                ('multi_blurb_EV_MKT_lang_cz', ''),
                ('multi_blurb_EV_MKT_lang_hu', ''),
                ('multi_blurb_EV_MKT_lang_id', ''),
                ('multi_blurb_EV_MKT_lang_af', ''),
                ('note_channels', 'P'),
                ('note_channel_E', ''),
                ('note_channel_I', ''),
                ('note_channel_O', ''),
                ('note_channel_T', ''),
                ('note_channel_C', ''),
                ('note_channel_N', ''),
                ('note_channel_W', ''),
                ('note_channel_D', ''),
                ('note_channel_Z', ''),
                ('note_channel_V', ''),
                ('note_channel_P', ''),
                ('note_channel_H', ''),
                ('note_channel_L', ''),
                ('note_channel_U', ''),
                ('note_channel_F', ''),
                ('note_channel_S', ''),
                ('note_channel_X', ''),
                ('note_channel_J', ''),
                ('note_channel_Q', ''),
                ('note_channel_R', ''),
                ('note_channel_Y', ''),
                ('note_channel_M', ''),
                ('note_channel_@', ''),
                ('note_channel_K', ''),
                ('note_channel_p', ''),
                ('note_channel_G', ''),
                ('note_channel_t', ''),
                ('note_channel_B', ''),
                ('note_channel_e', ''),
                ('note_channel_f', ''),
                ('note_channel_y', ''),
                ('note_channel_z', ''),
                ('flag_GT', 'N'),
                ('flag_SP', flag_SP),
                ('flag_NRNB', 'N'),
                ('flag_PVT', 'N'),
                ('flag_SM', 'N'),
                ('flag_PB', flag_pb_value),
                ('flag_MB', flag_mb_value),
                ('flag_GOP', 'N'),
                ('flag_SI', 'N'),
                ('flag_PR1', 'N'),
                ('flag_PR2', 'N'),
                ('flag_EPR', market_extra_place_race),
                ('flag_ITV', 'N'),
                ('flag_3E', 'N'),
                ('flag_FI', 'N'),
                ('flags_list', ''),
                ('channel_E', 'N'),
                ('channel_I', 'Y'),
                ('channel_O', 'N'),
                ('channel_T', 'Y'),
                ('channel_C', 'Y'),
                ('channel_N', 'N'),
                ('channel_W', 'N'),
                ('channel_D', 'N'),
                ('channel_Z', 'N'),
                ('channel_V', 'N'),
                ('channel_P', 'Y'),
                ('channel_H', 'N'),
                ('channel_L', 'N'),
                ('channel_U', 'Y'),
                ('channel_F', 'N'),
                ('channel_S', 'N'),
                ('channel_X', 'N'),
                ('channel_J', 'N'),
                ('channel_Q', 'Y'),
                ('channel_R', 'N'),
                ('channel_Y', 'N'),
                ('channel_M', 'Y'),
                ('channel_@', 'N'),
                ('channel_K', 'N'),
                ('channel_p', 'N'),
                ('channel_G', 'N'),
                ('channel_t', 'N'),
                ('channel_B', 'N'),
                ('channel_e', 'N'),
                ('channel_f', 'N'),
                ('channel_y', 'N'),
                ('channel_z', 'N'),
                ('channels_list', 'ITCPUQM'),
                ('views_fr', 'N'),
                ('views_hu', 'N'),
                ('views_cz', 'N'),
                ('views_sk', 'N'),
                ('views_af', 'N'),
                ('views_id', 'N'),
                ('views_za', 'N'),
                ('views_ro', 'N'),
                ('views_ru', 'N'),
                ('views_bg', 'N'),
                ('views_hr', 'N'),
                ('views_si', 'N'),
                ('views_seas', 'N'),
                ('views_sw', 'N'),
                ('views_dk', 'N'),
                ('views_fi', 'N'),
                ('views_de', 'N'),
                ('views_vs', 'N'),
                ('views_uk', 'N'),
                ('views_ie', 'N'),
                ('views_gr', 'N'),
                ('views_pt', 'N'),
                ('views_cs', 'N'),
                ('views_it', 'N'),
                ('views_esmd', 'N'),
                ('views_cn', 'N'),
                ('views_esvc', 'N'),
                ('views_es', 'N'),
                ('views_esmc', 'N'),
                ('views_esar', 'N'),
                ('views_esgc', 'N'),
                ('views_esnc', 'N'),
                ('views_th', 'N'),
                ('views_no', 'N'),
                ('views_beta', 'N'),
                ('views_oo', 'N'),
                ('views_pl', 'N'),
                ('views_ca', 'N'),
                ('select_linked_ladder_-1_CASHOUT', '-1'),
                ('select_linked_ladder_-1_ODDSBOOST', '-1'),
                ('price_ladder_id', ''),
                ('max_rule4', ''),
                ('mult_key_ev_allow', ''),
                ('allow_oc_combi', 'N'),
                ('add_variants', ''),
                ('exact_flags', 'Y'),
                ('flags', flags)
             )
            resp_dict = do_request(url=url, params=params, cookies=self.site_cookies)
        try:
            self.marketID = resp_dict['id']
        except KeyError:
            raise OBException('Marked id can not be found')
        return self.marketID

    def add_selections(self, market_id=None, runner_number=1, price=None, name=None, **kwargs):
        max_bet = kwargs['max_bet'] if 'max_bet' in kwargs else 1000.00
        min_bet = kwargs.get('min_bet', '')
        selections_displayed = 'N' if 'selections_displayed' in kwargs.keys() and kwargs['selections_displayed'] is False else 'Y'
        lp_price = price if price else ''
        market_id = market_id if market_id else self.marketID
        runner_num_param = '' if runner_number == '-' else '&runner_num=%s' % runner_number
        if self.brand == 'bma':
            params = '?action=hierarchy::selection::H_insert' \
                     '&id=&read_only=N' \
                     '&desc={name}' \
                     '&mkt_id={marketID}' \
                     '&displayed={selections_displayed}' \
                     '&disporder=0' \
                     '&status=A' \
                     '{runner_num_param}' \
                     '&lp_price={lp_price}' \
                     '&feed_updateable=Y' \
                     '&sp_guide_price=&win_roll=0&ext_key=&mult_key=&link_key=' \
                     '&risk_info=-&min_bet={min_bet}&abs_least_max_bet=&max_multiple_bet=' \
                     '&abs_max_bet=&max_bet=&sp_max_bet=&ep_max_bet=&lock_stake_lmt=N' \
                     '&lock_stake_win=N&max_place_lp=&max_place_sp=&max_place_ep=' \
                     '&lock_stake_place=N&stk_or_lbt=L&max_total=&fc_stk_limit=&tc_stk_limit=' \
                     '&ew_factor=&acc_min=&fixed_stake_limits=Y&fb_result=-&note_channels=P' \
                     '&note_channel_I=&note_channel_P=&note_channel_C=&note_channel_M=' \
                     '&note_channel_Q=&note_channel_D=&note_channel_T=&note_channel_G=&note_channel_W=' \
                     '&note_channel_J=&channel_I=Y&channel_P=Y&channel_C=Y&channel_M=Y&channel_Q=Y' \
                     '&channel_D=N&channel_T=N&channel_G=N&channel_W=N&channel_J=N&channels_list=IPCMQ' \
                     '&exact_flags=Y'\
                .format(name=name, marketID=market_id, runner_num_param=runner_num_param,
                        lp_price=lp_price, selections_displayed=selections_displayed, min_bet=min_bet)
            url = self.site + params
            do_request(url=url, cookies=self.site_cookies)
        else:
            params = (
                ('action', 'hierarchy::selection::H_insert'),
                ('id', ''),
                ('read_only', 'N'),
                ('desc', name),
                ('mkt_id', market_id),
                ('displayed', selections_displayed),
                ('disporder', '0'),
                ('status', 'A'),
                ('runner_num', '' if runner_number == '-' else runner_number),
                ('lp_price', lp_price),
                ('feed_updateable', 'Y'),
                ('to_event_link_id', ''),
                ('to_event_link_level', ''),
                ('evoc_parent_ev_id', ''),
                ('evoc_ev_linked_ids', ''),
                ('win_roll', '0'),
                ('ext_key', ''),
                ('mult_key', ''),
                ('link_key', ''),
                ('risk_info', '-'),
                ('min_bet', min_bet),
                ('abs_least_max_bet', ''),
                ('max_multiple_bet', ''),
                ('abs_max_bet', ''),
                ('max_bet', max_bet),
                ('sp_max_bet', ''),
                ('ep_max_bet', ''),
                ('lock_stake_lmt', 'N'),
                ('lock_stake_win', 'N'),
                ('max_place_lp', ''),
                ('max_place_sp', ''),
                ('max_place_ep', ''),
                ('lock_stake_place', 'N'),
                ('stk_or_lbt', 'S'),
                ('max_total', ''),
                ('fc_stk_limit', ''),
                ('tc_stk_limit', ''),
                ('ew_factor', ''),
                ('acc_min', ''),
                ('fixed_stake_limits', 'N'),
                ('fb_result', '-'),
                ('note_channels', 'P'),
                ('note_channel_E', ''),
                ('note_channel_I', ''),
                ('note_channel_O', ''),
                ('note_channel_T', ''),
                ('note_channel_C', ''),
                ('note_channel_N', ''),
                ('note_channel_W', ''),
                ('note_channel_D', ''),
                ('note_channel_Z', ''),
                ('note_channel_V', ''),
                ('note_channel_P', ''),
                ('note_channel_H', ''),
                ('note_channel_L', ''),
                ('note_channel_U', ''),
                ('note_channel_F', ''),
                ('note_channel_S', ''),
                ('note_channel_X', ''),
                ('note_channel_J', ''),
                ('note_channel_Q', ''),
                ('note_channel_R', ''),
                ('note_channel_Y', ''),
                ('note_channel_M', ''),
                ('note_channel_@', ''),
                ('note_channel_K', ''),
                ('note_channel_p', ''),
                ('note_channel_G', ''),
                ('note_channel_t', ''),
                ('note_channel_B', ''),
                ('note_channel_e', ''),
                ('note_channel_f', ''),
                ('note_channel_y', ''),
                ('note_channel_z', ''),
                ('channel_E', 'N'),
                ('channel_I', 'Y'),
                ('channel_O', 'N'),
                ('channel_T', 'N'),
                ('channel_C', 'Y'),
                ('channel_N', 'N'),
                ('channel_W', 'N'),
                ('channel_D', 'N'),
                ('channel_Z', 'N'),
                ('channel_V', 'N'),
                ('channel_P', 'Y'),
                ('channel_H', 'N'),
                ('channel_L', 'N'),
                ('channel_U', 'Y'),
                ('channel_F', 'N'),
                ('channel_S', 'N'),
                ('channel_X', 'N'),
                ('channel_J', 'N'),
                ('channel_Q', 'Y'),
                ('channel_R', 'N'),
                ('channel_Y', 'N'),
                ('channel_M', 'Y'),
                ('channel_@', 'N'),
                ('channel_K', 'N'),
                ('channel_p', 'N'),
                ('channel_G', 'N'),
                ('channel_t', 'N'),
                ('channel_B', 'N'),
                ('channel_e', 'Y'),
                ('channel_f', 'Y'),
                ('channel_y', 'N'),
                ('channel_z', 'N'),
                ('channels_list', 'IPCMQ'),
                ('exact_flags', 'Y')
            )
            do_request(url=self.site, params=params, load_response=False, cookies=self.site_cookies)
        selection_ids = self.get_selection_ids(marketID=market_id)
        if not selection_ids:
            raise OBException(f'Not all selections were added to market id {market_id}')
        return selection_ids

    def change_racing_selection_type(self, id, unnamed_favorites_position='-'):
        params = '?action=hierarchy::selection::H_update&id={id}&fb_result={unnamed_favorites_position}&exact_flags=Y'\
            .format(id=id, unnamed_favorites_position=unnamed_favorites_position)
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)

    def add_dividend(self):
        pass


class Coupon(OBLogin):

    def add_market_to_coupon(self, coupon_id=None, market_id=None):
        url = '{0}/hierarchy/coupon/{0}/markets'.format(self.site)
        params = '?id={0}' \
                 '&addMarkets={1}' \
                 '&action=hierarchy%3A%3Acoupon_market%3A%3AH_update'.format(coupon_id, market_id)
        url = url + params
        do_request(url=url, cookies=self.site_cookies)
