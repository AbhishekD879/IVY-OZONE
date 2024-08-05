import pytest
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.smoke
@pytest.mark.private_markets
@pytest.mark.module_ribbon
@pytest.mark.homepage
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.promotions_banners_offers
@pytest.mark.login
@vtest
class Test_C29431_Your_Enhanced_Markets_tabsection_for_Eligible_User(BasePrivateMarketsTest, BaseUserAccountTest):
    """
    TR_ID: C29431
    NAME: 'Your Enhanced Markets' tab/section for Eligible User
    DESCRIPTION: This test case verifies 'Your Enhanced Markets' tab/section for the user which is eligible for private market offers.
    PRECONDITIONS: 1.  Open Invictus app and log in
    PRECONDITIONS: 2.  User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: 3.  Private market offers should be active (not expired)
    PRECONDITIONS: 4.  To view event information on SS use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?
    PRECONDITIONS: includeRestricted=true&translationLang=LL
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: For setting private markets use the link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Setup+and+Use+Private+Markets?preview=/36604227/
    PRECONDITIONS: 36604228/HowToSetupAndUsePrivateMarkets%20.pdf
    PRECONDITIONS: Place a bet on the configured event by any user with sufficient funds for bet placement and then
    PRECONDITIONS: verify Private Markets on the Homepage. Private Markets will be shown for all users which placed a
    PRECONDITIONS: bet on the configured event.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Places a bet again on the event which triggers Private Market appearance
        EXPECTED: Bet is placed successfully and Bet Receipt is shown
        """
        self.__class__.user = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=self.user, amount=tests.settings.min_deposit_amount)
        self.site.login(username=self.user)
        self.trigger_private_market_appearance(user=self.user,
                                               expected_market_name=self.private_market_name)

    def test_001_load_oxygen_and_login_with_the_user_with_private_markets_available(self):
        """
        DESCRIPTION: Load Oxygen and login with the user with private markets available
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_navigate_to_your_enhanced_markets_tab_section(self):
        """
        DESCRIPTION: Navigate to 'Your Enhanced Markets' tab/section
        EXPECTED: All eligible private markets and associated selections are shown
        EXPECTED: All private market accordions expanded by default
        """
        self.tab_name = self.expected_sport_tabs.private_market

        if self.device_type == 'mobile':
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(tabs, msg='No tabs are displayed at the Home page')
            self.assertIn(self.tab_name, tabs.keys(),
                          msg=f'Tab "{self.tab_name}" is not displayed for the user which is '
                              f'"{tests.settings.user_with_private_market}"')
            self.assertTrue(tabs[self.tab_name].is_selected(), msg=f'"{self.tab_name}" tab is not selected by default')

        private_market_tab_content = self.site.home.get_module_content(self.expected_sport_tabs.private_market)
        self.__class__.markets = private_market_tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No Markets found')

        for market in self.markets.values():
            self.assertTrue(market.is_displayed(),
                            msg='Private markets and associated selections are expected to be shown')
            self.assertTrue(market.is_expanded(),
                            msg='Markets are not expanded by default')

    def test_003_collapse_expand_private_market_accordions(self):
        """
        DESCRIPTION: Collapse/expand private market accordions
        EXPECTED: It is possible to collapse/expand private market accordions
        """
        for market in self.markets.values():
            market.collapse()
            self.assertFalse(market.is_expanded(), msg='Markets are not collapsed after click')
            market.expand()
            self.assertTrue(market.is_expanded(), msg='Markets are not expanded after click')

    def test_004_verify_private_market_image_graphics(self):
        """
        DESCRIPTION: Verify private market image/graphics
        EXPECTED: Private market image/graphics is shown beside each private market line
        """
        for market in self.markets.values():
            self.__class__.selections = market.items_as_ordered_dict
            self.assertTrue(self.selections, msg='There\'s no selections present')
            for selection in self.selections.values():
                self.assertTrue(selection.private_market_icon.is_displayed(),
                                msg='Private market image/graphics is not shown beside each private market line')

    def test_005_verify_name_of_the_private_market(self):
        """
        DESCRIPTION: Verify name of the private market
        EXPECTED: Name of each private market corresponds to **<name>** attribute on market level (e.g. name="Asian Handicap Half-Time Betting")
        """
        for market in self.markets.values():
            self.assertTrue(market.section_header.is_displayed(), msg='Private market name is not shown')

        self.assertTrue(self.private_market_name.upper() in self.markets.keys(),
                        msg=f'There\'s no expected private market name "{self.private_market_name.upper()}"')

    def test_006_verify_market_with_cash_out_label_on_market_section(self):
        """
        DESCRIPTION: Verify Market with 'CASH OUT' label on market section
        EXPECTED: 'CASH OUT' label is shown next to market name ONLY for markets  with **cashoutAvail="Y" **attribute on Market level
        """
        if self.brand == 'bma':
            for market in self.markets.values():
                self.assertTrue(market.section_header.has_cash_out_mark(),
                                msg='"CASH OUT" label is not shown next to market name')

    def test_007_verify_selections_within_the_private_market(self):
        """
        DESCRIPTION: Verify selections within the private market
        EXPECTED: First 3 selections and their respective prices are displayed in the market section
        EXPECTED: Selections Names and Price/Odds values are correct
        EXPECTED: 'Show All' button is displayed below
        """
        for selection_name, selection in self.selections.items():
            self.assertTrue(selection_name,
                            msg='There\'s no selection name')
            self.assertTrue(selection.output_price,
                            msg=f'There\'s no odds value for "{selection_name}"')

    def test_008_verify_show_all_button(self):
        """
        DESCRIPTION: Verify 'Show All' button
        EXPECTED: 'Show All' button is displayed if there are more than 3 selections for a given private market
        EXPECTED: All available selection are shown after tapping on 'Show All' button
        EXPECTED: 'Show All' button is changed to 'Show Less'
        EXPECTED: On tapping 'Show Less' button selection list is collapsed back to showing 3 selections
        EXPECTED: 'Show Less' button is changed to 'Show All' after collapsing
        """
        market = self.markets[self.private_market_name.upper()]
        default_selections = market.items_as_ordered_dict
        self.assertEqual(len(default_selections), 3, msg='Selections are not collapsed by default')

        has_show_all_button = market.has_show_all_button
        self.assertTrue(has_show_all_button, msg='There\'s no show all button')
        market.show_all_button.click()
        bypass_exceptions = (VoltronException, NoSuchElementException, StaleElementReferenceException)
        wait_for_result(lambda: len(market.items_as_ordered_dict) > 3,
                        bypass_exceptions=bypass_exceptions,
                        timeout=3)
        all_selections = market.items_as_ordered_dict
        self.assertNotEqual(len(all_selections), 3,
                            msg='All available selection are not shown after tapping on "Show All" button')
        self.assertTrue(market.has_show_less_button(), msg='There\'s no show less button')
        market.show_less_button.click()
        wait_for_result(lambda: len(market.items_as_ordered_dict) <= 3,
                        bypass_exceptions=bypass_exceptions,
                        timeout=3)
        collapsed_selections = market.items_as_ordered_dict
        self.assertEqual(len(collapsed_selections), 3,
                         msg='Selection list is not collapsed back to showing 3 selections')
        has_show_all_button = market.has_show_all_button
        self.assertTrue(has_show_all_button, msg='There\'s no show all button')

    def test_009_verify_terms_and_conditions_link(self):
        """
        DESCRIPTION: Verify 'Terms and Conditions' link
        EXPECTED: Link is displayed under the last of available market section
        """
        private_market_tab_content = self.site.home.get_module_content(self.expected_sport_tabs.private_market)
        terms_and_conditions = private_market_tab_content.terms_and_conditions
        self.assertTrue(terms_and_conditions.is_displayed(), msg="Link is not displayed")
