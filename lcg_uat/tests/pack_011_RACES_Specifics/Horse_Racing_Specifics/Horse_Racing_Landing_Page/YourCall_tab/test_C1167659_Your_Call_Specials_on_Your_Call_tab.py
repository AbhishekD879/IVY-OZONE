from collections import OrderedDict

import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.crl_tst2   # yourcall not in the scope of roxane release
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.your_call
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1167659_Your_Call_Specials_on_Your_Call_tab(BaseRacing):
    """
    TR_ID: C1167659
    VOL_ID: C9698476
    NAME: Your Call Specials on Your Call tab
    DESCRIPTION: This test case verifies the Your Call Specials accordion on YourCall tab for Horse Racing
    PRECONDITIONS: Horse Racing page is loaded and Horse Racing Your Call Specials selections available (Horse Racing Your Call Specials selections should be configured in TI).
    PRECONDITIONS: To retrieve all events with markets and selections for Horse Racing Your Call Specials type:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/TTTT
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: TTTT - Your Call Specials type id (15031)
    PRECONDITIONS: or
    PRECONDITIONS: Create selections if necessary:
    PRECONDITIONS: Under the category Horse Racing (category id = 21) select Daily Racing Specials class (id = 227), then select Your Call Specials Type (id = 15031), then add market created using 'YourCall Specials' market template
    """
    keep_browser_open = True

    prices = {0: '1/4', 1: '1/2'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check Your Call Static Block presence
        DESCRIPTION: Create Horse Racing Your Call Specials event
        EXPECTED: Event is created
        """
        static_block_params = self.cms_config.get_your_call_static_block()
        yc_racing_block = next((block for block in static_block_params if block["title"] == 'yourcall-racing'), None)
        if not yc_racing_block:
            raise CmsClientException('Your Call racing block is not present')
        if not yc_racing_block['htmlMarkup']:
            raise CmsClientException('Your Call racing block is not configured')
        if 'twitter' not in yc_racing_block['htmlMarkup']:
            raise CmsClientException('Your Call racing block is not configured to show twitter button')

        self.ob_config.add_racing_your_call_specials_event(number_of_runners=2, lp_prices=self.prices,
                                                           default_market_name='Featured')
        self.ob_config.add_racing_your_call_specials_event(number_of_runners=1, lp_prices=self.prices,
                                                           default_market_name='Odds On')
        self.ob_config.add_racing_your_call_specials_event(number_of_runners=1, lp_prices=self.prices,
                                                           default_market_name='Events - 5/2, 50/1+')
        self.ob_config.add_racing_your_call_specials_event(number_of_runners=1, lp_prices=self.prices,
                                                           default_market_name='Antepost')

    def test_001_navigate_to_your_call_tab(self):
        """
        DESCRIPTION: Navigate to Your Call tab
        EXPECTED: * Your Call tab is loaded and Your Call Specials section is displayed below 'Tweet Now' button
        EXPECTED: * 'YourCall Specials' accordion is expanded by default and not collapsible
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        self.site.horse_racing.tabs_menu.click_button('YOURCALL')
        selected_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(selected_tab, 'YOURCALL',
                         msg='Selected tab is "%s" instead of "YOURCALL" tab' % selected_tab)
        static_block = self.site.horse_racing.tab_content.accordions_list.static_block
        self.assertTrue(static_block, msg='Can not find Static Block')
        self.assertTrue(static_block.tweet_now_button, msg='Can not find "Tweet Now" button')

        self.__class__.sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.yc_specials_type_name, self.sections.keys())
        self.__class__.your_call_section = self.sections.get(self.yc_specials_type_name)
        self.assertTrue(self.your_call_section.is_expanded(), msg='Section is collapsed')
        self.your_call_section.click()
        self.assertTrue(self.your_call_section.is_expanded(), msg='Section is collapsed')

    def test_002_verify_the_section_header(self):
        """
        DESCRIPTION: Verify the section header
        EXPECTED: * Section header contains # (YourCall) icon and is named "YourCall Specials"
        """
        self.assertIn(self.yc_specials_type_name, self.sections.keys())
        self.assertTrue(self.your_call_section.has_byb_icon(), msg='No yourcall icon for "%s"' % self.yc_specials_type_name)

    def test_003_verify_the_section_content(self):
        """
        DESCRIPTION: Verify the section content
        DESCRIPTION: Verify tab's names
        EXPECTED: * The amount of tabs is the same as amount of markets with selection(s) within response EventToOutcomeForType/<#YourCall type id> from OpenBet
        EXPECTED: * If the number of tabs are 5 or more then switcher to scroll tabs horizontally is available
        EXPECTED: * Tabs are ordered by **dispOrder** parameter for a markets from in EventToOutcomeForType (Type id for YourCall specials for HR) response. The lower the value, the higher the position
        EXPECTED: * Content of first tab is displayed by default
        EXPECTED: * Name of each tab is the same as corresponding market name from response EventToOutcomeForType/<#YourCall type id>
        """
        self.__class__.market_tab_names = self.your_call_section.market_tabs_list.items_as_ordered_dict
        type_id = self.ob_config.horseracing_config.daily_racing_specials.your_call_specials.type_id
        resp = self.ss_req.ss_event_to_outcome_for_type(type_id=type_id)
        outcomes_display_order = self.get_outcomes_display_order_for_type(response=resp)
        ss_market_names = outcomes_display_order.market_names
        self.assertEqual(len(set(ss_market_names)), len(self.market_tab_names))

        outcome_names_prices = OrderedDict(
            [(outcome_name, outcome.bet_button.outcome_price_text) for outcome_name, outcome in
             self.your_call_section.items_as_ordered_dict.items()])
        params = self.get_outcomes_display_order_for_type(response=resp)
        market_names = [b.upper().strip('|') for b in params.market_names]
        self.assertEqual(list(self.your_call_section.market_tabs_list.items_as_ordered_dict.keys()), market_names)
        selected_tab = self.your_call_section.market_tabs_list.current
        ss_outcomes = params.markets_with_outcomes.get(selected_tab.title())
        self.assertEqual(outcome_names_prices.items(), ss_outcomes.items())

    def test_004_verify_the_content_of_tabs(self):
        """
        DESCRIPTION: Verify the content of tabs
        EXPECTED: * Each tab contains selection(s) names and prices from corresponding market from response EventToOutcomeForType/<#YourCall type id>
        EXPECTED: * Selections are ordered by **dispOrder** parameter for a selection from in EventToOutcomeForType (Type id for YourCall specials for HR) response. The lower the value, the higher the position
        EXPECTED: * The name of each selection begins with "#YourCall" label
        """
        selections = self.your_call_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No one market: "%s" selection found' % self.yc_specials_type_name)
        [self.assertIn('#YourCall ', selection.css_property_text()) for selection in selections.values()]

    def test_006_on_mobile_tablet_scroll_content_of_each_tab(self):
        """
        DESCRIPTION: On **Mobile/Tablet** scroll content of each tab
        EXPECTED: * Content of tabs is scrollable
        EXPECTED: * Tabs becomes sticky to the top and fixed below page header 'Horse Racing'
        """
        pass

    def test_007_verify_yourcall_tab_content_if_are_no_yourcall_specials_selections_available(self):
        """
        DESCRIPTION: Verify YourCall tab content if are no YourCall Specials selections available
        EXPECTED: Only the static text block and the 'tweet now' button are displayed
        """
        pass
