import voltron.environments.constants as vec
import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.safari
@vtest
class Test_C28864_Verify_Unnamed_Favourite_Selections_on_the_Bet_Slip(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C28864
    NAME: Verify Unnamed Favourite Selections on the Bet Slip
    DESCRIPTION: This test case verifies how Favourite selections added to the Bet Slip are displayed
    PRECONDITIONS: 'Unnamed Favourite' and 'Unnamed 2nd Favourite' selections are present in Race event
    """
    selection_names = ['Unnamed Favourite', 'Unnamed 2nd Favourite']
    expected_market_name = 'Win or Each Way'
    keep_browser_open = True

    def test_001_add_the_following_selections_to_the_betslip_unnamed_favourite_unnamed_2nd_favourite(self):
        """
        DESCRIPTION: Add the following selections to the Betslip:
        DESCRIPTION: *   'Unnamed Favourite'
        DESCRIPTION: *   'Unnamed 2nd Favourite'
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = []
            additional_filter.append(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES,
                                                                               OPERATORS.INTERSECTS, 'SP')))
            additional_filter.append(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.RUNNER_NUMBER, OPERATORS.IS_EMPTY))
            sp_events = self.get_active_events_for_category(additional_filters=additional_filter,
                                                            category_id=self.ob_config.horseracing_config.category_id,
                                                            all_available_events=True)
            event, outcomes_resp = None, None
            for event in sp_events:
                for market in event['event']['children']:
                    if market['market'].get('children') and market.get('market').get(
                            'templateMarketName') == 'Win or Each Way':
                        for outcome in market['market']['children']:
                            if not outcome['outcome'].get(
                                    'children') and 'Unnamed' in outcome['outcome'].get(
                                    'name'):  # outcomes that does not have children are usually outcomes with SP prices
                                outcomes_resp = market['market']['children']
                                break
                        break
                if outcomes_resp:
                    break
            if not outcomes_resp:
                raise SiteServeException('There are no selections with Unnamed runners')
            self.__class__.event_id = event['event']['id']
            self.__class__.created_event_name = event['event']['name']
            market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
            outcomes_resp = market['market']['children']
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id']
                                            for i in outcomes_resp if 'Unnamed' in i['outcome']['name']}
        else:
            event_params = self.ob_config.add_UK_racing_event(unnamed_favorites=True, number_of_runners=1)
            self.__class__.selection_ids, self.__class__.event_id = event_params.selection_ids, event_params.event_id
            self.__class__.event_off_time = event_params.event_off_time
            self.__class__.created_event_name = '%s %s' % (self.event_off_time, self.horseracing_autotest_uk_name_pattern)
            self._logger.info('*** Created Event id: %s, event off time: %s, selection ids: %s'
                              % (event_params.event_id, event_params.event_off_time, event_params.selection_ids.values()))
        self.open_betslip_with_selections(selection_ids=[self.selection_ids[self.selection_names[0]],
                                          self.selection_ids[self.selection_names[1]]])

    def test_002_open_bet_slip_and_verify_display_of_both_selections(self):
        """
        DESCRIPTION: Open Bet Slip and verify display of both selections
        EXPECTED: The following correct information is displayed for each selection in 'Singles' section:
        EXPECTED: *  'Unnamed Favourite'/'Unnamed 2nd Favourite' selection name
        EXPECTED: *  Market Name (e.g. Win or Each Way)
        EXPECTED: *  Event Start Time and Name (e.g. 12:40 Newbury)
        EXPECTED: *  NO E/W text and checkbox is displayed**
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertEqual(singles_section.keys(), self.selection_names,
                         msg=f'Selection names "{singles_section.keys()} is not equal to expected "{self.selection_names}"')

        for stake_name, stake in singles_section.items():
            self.assertEqual(stake.event_name, self.created_event_name,
                             msg=f'Event name "{stake.event_name}" is not equal to created "{self.created_event_name}"')
            self.assertEqual(singles_section.name, vec.betslip.BETSLIP_SINGLES_NAME,
                             msg=f'Section title "{singles_section.name}" is not the same as expected "{vec.betslip.BETSLIP_SINGLES_NAME}"')
            self.assertEqual(stake.market_name, self.expected_market_name,
                             msg=f'Market name "{stake.market_name}" is not equal to expected "{self.expected_market_name}"')
            self.assertFalse(stake.has_each_way_checkbox(expected_result=False),
                             msg=f'Win or each way is displayed for selection: "{stake_name}"')
