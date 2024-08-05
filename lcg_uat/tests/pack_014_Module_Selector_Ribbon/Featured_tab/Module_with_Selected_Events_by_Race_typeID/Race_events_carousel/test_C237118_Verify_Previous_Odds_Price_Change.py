import pytest
import tests
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from crlat_siteserve_client.siteserve_client import racing_form, price_history, prune, simple_filter
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #cannot create events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.homepage_featured
@vtest
class Test_C237118_Verify_Previous_Odds_Price_Change(BaseRacing, BaseFeaturedTest):
    """
    TR_ID: C237118
    NAME: Verify Previous Odds Price Change
    DESCRIPTION: This test case verify displaying of Previous odds under Price/Odds button
    DESCRIPTION: **NOTE:**
    DESCRIPTION: agreed with Adam Smith
    DESCRIPTION: that Previous Odds functionality is not applied for Featured module for now
    DESCRIPTION: (user can see previous odds appears under Price/Odds button if during live price update Feature module was active but in all other cases previous odds won't be displayed)
    DESCRIPTION: To implement Previous Odd to be displayed on Featured module changes should be made for featured microservice
    DESCRIPTION: no an issue according to comment in https://jira.egalacoral.com/browse/BMA-19508
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) To retrieve an information from Site Server about Previous Odds use link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZZZ?simpleFilter=event.suspendAtTime:greaterThan:####-##-##T##:##:##.###Z&racingForm=outcome&racingForm=event&priceHistory=true&prune=event&prune=market&translationLang=en
    PRECONDITIONS: *X.XX* - current supported version of OpenBet release
    PRECONDITIONS: *ZZZZZZ* - an event id
    PRECONDITIONS: *####-##-##T##:##:##.###Z* - date and time until event won't be suspended
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True
    price = ['1/10', '1/7', '1/5', '1/3', '1/2']

    def get_historic_prices(self, query):
        response = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID, query_builder=query)

        historic_prices = response[0]['event']['children'][0]['market']['children'][0]['outcome']['children']
        live_prices = []
        for price in historic_prices:
            historic_price = price.get('historicPrice')
            if historic_price:
                live_prices.append(f'{historic_price.get("livePriceNum")}/{historic_price.get("livePriceDen")}')

        return live_prices

    def create_events(self):
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, time_to_start=3, lp=True,
                                                          lp_prices={0: self.price[0]})
        race_name = event_params.ss_response['event']['name']
        self.__class__.race_name = race_name if tests.settings.brand == 'bma' else race_name.upper()
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.eventID = event_params.event_id
        event_off_time = event_params.event_off_time
        name = self.horseracing_autotest_uk_name_pattern if self.brand == 'bma' and self.device_type == 'desktop' else \
            self.horseracing_autotest_uk_name_pattern.upper()
        self.__class__.created_event_name = f'{event_off_time} {name}'

        race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id
        self.__class__.is_executed_on_desktop = self.device_type in ['desktop']
        self.__class__.featured_module_name = \
            self.cms_config.add_featured_tab_module(select_event_by='RaceTypeId', id=race_type_id,
                                                    module_time_from_hours_delta=-10,
                                                    events_time_from_hours_delta=-10,
                                                    max_rows=self.max_number_of_events)['title'].upper()

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED:
        """
        self.create_events()
        self.site.wait_content_state("Homepage")
        self.wait_for_featured_module(name=self.featured_module_name)

    def test_002_go_to_module_selector_ribbon___module_created_by_race_type_id(self):
        """
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID
        EXPECTED: * 'Feature' tab is selected by default
        EXPECTED: * Module created by <Race> type ID is shown
        """
        if not self.is_executed_on_desktop:
            featured_module = \
                self.site.home.get_module_content(
                    self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

            self.__class__.section = \
                featured_module.accordions_list.items_as_ordered_dict.get(self.featured_module_name)
            self.assertTrue(self.section, msg=f'Section "{self.featured_module_name}" is not found on FEATURED tab')

        if self.is_executed_on_desktop:
            featured_module = self.site.home.desktop_modules.featured_module
            self.assertTrue(featured_module, msg='"Featured" module is not displayed')

            featured_content = featured_module.tab_content
            featured_modules = featured_content.accordions_list.items_as_ordered_dict.keys()
            self.assertTrue(featured_content.accordions_list, msg='"Featured" module does not contain any accordions')
            self.assertIn(self.featured_module_name, featured_content.accordions_list.items_as_ordered_dict.keys(),
                          msg=f'Module "{self.featured_module_name}" is not displayed. '
                              f'Please check list of all displayed modules:\n"{featured_modules}"')

            self.__class__.section = featured_content.accordions_list.items_as_ordered_dict[self.featured_module_name]
            self.assertTrue(self.section, msg='No accordions displayed in "Featured" section on Home page')

    def test_003_in_the_race_events_carousel_find_event_with_live_price_available(self):
        """
        DESCRIPTION: In the '<Race> events carousel' find event with 'Live Price' available
        EXPECTED: Event is shown
        """
        self.__class__.event = self.section.items_as_ordered_dict.get(self.race_name)
        self.assertTrue(self.event, msg='Event not found')

    def test_004_trigger_price_changing_for_some_outcome_and_check_previous_odds(self):
        """
        DESCRIPTION: Trigger price changing for some outcome and check Previous Odds
        EXPECTED: * 'Price/Odds' button immediately displays new price
        EXPECTED: * Previous price/odd is displayed under Price/odds button immediately
        EXPECTED: * Previous price/odd is displayed in decimal or fractional format (depends upon the users chosen odds display preference)
        """
        self.__class__.selection_name, self.__class__.selection = list(self.event.items_as_ordered_dict.items())[0]
        self.__class__.selection_id = self.selection_ids[self.selection_name]
        self.ob_config.change_price(selection_id=self.selection_id, price=self.price[1])
        result = wait_for_result(lambda: self.selection.previous_price == self.price[0],
                                 name=f'Previous price {self.price[0]} to appear. '
                                      f'Current is {self.selection.previous_price}',
                                 timeout=50)
        self.assertTrue(result, msg='Price was not changed')
        self.assertEqual(self.selection.bet_button.name, self.price[1],
                         msg=f'Bet button price "{self.selection.bet_button.name}" '
                             f'is not the same as expected "{self.price[1]}"')

    def test_005_repeat_step_4_several_times_and_check_previous_odds(self):
        """
        DESCRIPTION: Repeat step №4 several times and check Previous Odds
        EXPECTED: * Previous Odds are updated successfully each time
        EXPECTED: * Only 2 last Previous Odds are displayed in format X/X>X/X (older one goes first)
        """
        expected_previous_price = f'{self.price[0]} > {self.price[1]}'
        self.ob_config.change_price(selection_id=self.selection_id, price=self.price[2])

        result = wait_for_result(lambda: self.selection.previous_price == expected_previous_price,
                                 name=f'Previous price {expected_previous_price} to appear. '
                                      f'Current is {self.selection.previous_price}',
                                 timeout=15)
        self.assertTrue(result, msg='Price was not changed')
        self.assertEqual(self.selection.bet_button.name, self.price[2],
                         msg=f'Bet button price "{self.selection.bet_button.name}" '
                             f'is not the same as expected "{self.price[2]}"')

        expected_previous_price = f'{self.price[1]} > {self.price[2]}'
        self.ob_config.change_price(selection_id=self.selection_id, price=self.price[3])

        result = wait_for_result(lambda: self.selection.previous_price == expected_previous_price,
                                 name=f'Previous price {expected_previous_price} to appear. '
                                      f'Current is {self.selection.previous_price}',
                                 timeout=15)
        self.assertTrue(result, msg='Price was not changed')
        self.assertEqual(self.selection.bet_button.name, self.price[3],
                         msg=f'Bet button price "{self.selection.bet_button.name}" '
                             f'is not the same as expected "{self.price[3]}"')

    def test_006_verify_previous_odds_correctness(self):
        """
        DESCRIPTION: Verify Previous Odds correctness
        EXPECTED: * Previous Odds correspond to **livePriceNum** and **livePriceDen** attributes from tag *<historicPrice .../>*  in fractional format
        EXPECTED: *  Previous Odds correspond to **'livePriceDec'** attributes from tag *<historicPrice .../>*  in decimal format
        EXPECTED: * Previous odds are ordered according to **'displayOrder'** attribute (the biggest - the last)
        """
        query = self.ss_query_builder \
            .add_filter(racing_form(LEVELS.EVENT)) \
            .add_filter(racing_form(LEVELS.OUTCOME)) \
            .add_filter(price_history()) \
            .add_filter(prune()) \
            .add_filter(
             simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, self.start_date_minus))

        result = wait_for_result(lambda: len(self.get_historic_prices(query)) == 3,
                                 name=f'Waiting for all three historic prices are recorded in SiteServe.',
                                 timeout=10)
        self.assertTrue(result, 'Not all historic prices were recorded in SiteServe. '
                                'Expected amount of historic prices is 3')

        live_prices = self.get_historic_prices(query)
        expected_old_price_value = None
        try:
            expected_old_price_value = f'{live_prices[-2]} > {live_prices[-1]}'
        except IndexError as e:
            self._logger.warning(f'*** Overriding exception {e}')
        self.assertEqual(self.selection.previous_price, expected_old_price_value,
                         msg=f'Old price value {self.selection.previous_price} '
                             f'is not the same as retrieved from from SiteServe {expected_old_price_value}')

    def test_007_collapse_featured_module_and_trigger_price_change_for_some_selection(self):
        """
        DESCRIPTION: Collapse featured module and trigger price change for some selection
        EXPECTED: After module is expanded updated Previous Odds are displayed correctly
        """
        if self.is_executed_on_desktop:
            module = self.site.home.desktop_modules.featured_module.tab_content.accordions_list.items_as_ordered_dict[self.featured_module_name]
        else:
            module = self.get_section(section_name=self.featured_module_name)

        module.collapse()
        self.assertFalse(module.is_expanded(expected_result=False),
                         msg=f'"{self.featured_module_name}" module is not collapsed')

        self.ob_config.change_price(selection_id=self.selection_id, price=self.price[4])
        module.expand()
        self.test_002_go_to_module_selector_ribbon___module_created_by_race_type_id()
        self.test_003_in_the_race_events_carousel_find_event_with_live_price_available()
        self.__class__.selection_name, self.__class__.selection = list(self.event.items_as_ordered_dict.items())[0]

        expected_previous_price = f'{self.price[2]} > {self.price[3]}'
        result = wait_for_result(lambda: self.selection.previous_price == expected_previous_price,
                                 name=f'Previous price {expected_previous_price} to appear. '
                                      f'Current is {self.selection.previous_price}',
                                 timeout=50)
        self.assertTrue(result, msg='Price was not changed')
        self.assertEqual(self.selection.bet_button.name, self.price[4],
                         msg=f'Bet button price "{self.selection.bet_button.name}" '
                             f'is not the same as expected "{self.price[4]}"')
