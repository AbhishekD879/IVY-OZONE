import pytest

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.helpers import normalize_name
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod  # cannot create CMS modules on prod
@pytest.mark.racing
@pytest.mark.module_ribbon
@pytest.mark.featured
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C2854772_Verify_PriceOdds_for_3_Way_Market(BaseFeaturedTest):
    """
    TR_ID: C2854772
    NAME: Verify Price/Odds for 3-Way Market
    DESCRIPTION: This test case verifies Price/Odds buttons of Pre-Match and BIP event.
    PRECONDITIONS: 1. There is featured module created by <Sport> type id with non-US events
    PRECONDITIONS: 2. In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. In order to determine US/non-US event use **typeFlagCodes="US" **(for US events)
    PRECONDITIONS: 4. User is logged in
    """
    keep_browser_open = True

    def test_000_precondition(self):
        """
        DESCRIPTION: Preconditions
        DESCRIPTION: Create event
        DESCRIPTION: Create Featured Module by type id in CMS
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children']
                             if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            self.__class__.team2 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'A'), None)
            type_id = event['event']['typeId']
        else:
            event = self.ob_config.add_football_event_to_featured_autotest_league()
            self.__class__.eventID = event.event_id
            self.__class__.team1, self.__class__.team2 = event.team1, event.team2
            self.__class__.event_name = f'{self.team1} v {self.team2}'
            self.__class__.selection_ids = event.selection_ids
            type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

        self.__class__.featured_module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', show_expanded=True, id=type_id, show_all_events=True)['title'].upper()

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.login(async_close_dialogs=False)
        self.site.wait_content_state(state_name='HomePage')

    def test_002_go_to_featured_module(self):
        """
        DESCRIPTION: Access featured module
        EXPECTED: Featured module is displayed
        """
        self.wait_for_featured_module(name=self.featured_module_name)
        self.__class__.featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        )
        self.featured_module.scroll_to()
        sections = self.featured_module.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No accordions found on FEATURED tab')
        self.__class__.section = sections.get(self.featured_module_name)
        self.assertTrue(self.section, msg=f'Section "{self.featured_module_name}" is not found on FEATURED tab')

    def test_003_verify_data_of_price_odds_for_verified_event(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified event
        EXPECTED: 'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        """
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.outcomes_resp = event_resp[0]['event']['children'][0]['market']['children']

        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.section.get_bet_button_by_selection_id(selection_id)
            self.assertIsNotNone(bet_button,
                                 msg=f'"{selection_name}" selection bet button is not found within module '
                                     f'"{self.featured_module_name}"')
            price_resp = next((i["outcome"]["children"][0]["price"] for i in self.outcomes_resp
                               if 'price' in i["outcome"]["children"][0].keys() and
                               i["outcome"]['name'] == selection_name), '')
            self.assertTrue(price_resp, msg=f'Price is not found in Siteserve response "{self.outcomes_resp}"')
            lp_price_resp = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}'
            self.assertEqual(bet_button.outcome_price_text, lp_price_resp,
                             msg=f'Price "{bet_button.outcome_price_text}" is '
                                 f'not the same as in response "{lp_price_resp}"')

    def test_004_verify_order_of_price_odds_buttons_for_3_way_market(self):
        """
        DESCRIPTION: Verify order of Price/Odds buttons for 3-Way Market
        EXPECTED: Price/Odds are in **Win/Draw/Win** order according to **Primary**** Market**, where:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home Win
        EXPECTED: *   outcomeMeaningMinorCode="D" is a Draw
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away Win
        """
        header_resp_team1 = next((i["outcome"]["outcomeMeaningMinorCode"] for i in self.outcomes_resp
                                  if i["outcome"]['name'] == self.team1), '')
        self.assertTrue(header_resp_team1,
                        msg=f'Home/Away outcome code for {self.team1} '
                            f'is not found in Siteserve response "{self.outcomes_resp}"')
        header_resp_draw = next((i["outcome"]["outcomeMeaningMinorCode"] for i in self.outcomes_resp
                                 if i["outcome"]['name'] == 'Draw'), '')
        self.assertTrue(header_resp_draw,
                        msg=f'Home/Away outcome code for {"Draw"} '
                            f'is not found in Siteserve response "{self.outcomes_resp}"')
        header_resp_team2 = next((i["outcome"]["outcomeMeaningMinorCode"] for i in self.outcomes_resp
                                  if i["outcome"]['name'] == self.team2), '')
        self.assertTrue(header_resp_team2,
                        msg=f'Home/Away outcome code for {self.team2} '
                            f'is not found in Siteserve response "{self.outcomes_resp}"')
        self.assertEqual('H', header_resp_team1,
                         msg=f'Price for "{self.team1}" is in wrong order,'
                             f'not the same as in Siteserve response "{header_resp_team1}"')
        self.assertEqual('D', header_resp_draw,
                         msg=f'Price for "{"Draw"}" is in wrong order,'
                             f'not the same as in Siteserve response "{header_resp_draw}"')
        self.assertEqual('A', header_resp_team2,
                         msg=f'Price for "{self.team2}" is in wrong order,'
                             f'not the same as in Siteserve response "{header_resp_team2}"')

    def test_005_click_on_price_odds_button_to_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Click on Price/Odds button to add selection to the Betslip
        EXPECTED: Selection is added to the Betslip, button is green
        """
        bet_button = self.section.get_bet_button_by_selection_id(self.selection_ids[self.team1])
        bet_button.scroll_to()
        bet_button.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()

        self.verify_betslip_counter_change(expected_value=1)

        self.assertTrue(bet_button.is_selected(timeout=2),
                        msg=f'Bet button for "{self.team1}" is not highlighted in green')
