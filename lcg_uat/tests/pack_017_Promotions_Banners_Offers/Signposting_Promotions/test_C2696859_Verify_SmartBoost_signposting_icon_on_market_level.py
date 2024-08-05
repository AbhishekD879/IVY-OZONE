import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod   # cannot find events with cashout and smart boost
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C2696859_Verify_SmartBoost_signposting_icon_on_market_level(Common):
    """
    TR_ID: C2696859
    NAME: Verify SmartBoost signposting icon on market level
    DESCRIPTION: This test case verifies that the Smart Boost signposting icon is displayed on market level.
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: [BMA-33496 Promo / Signposting : Price Boost : EDP] [1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-33496
    DESCRIPTION: [BMA-43178 Redesign Promo Icons] [2]
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-43178
    PRECONDITIONS: 'PriceBoost' promo flag should be added to the Football Event on market level.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Created events
        """
        pb_event = self.ob_config.add_autotest_premier_league_football_event(price_boost=True, market_price_boost=True, cashout=True)
        self.__class__.pb_event_id = pb_event.event_id
        no_pb_event = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        self.__class__.no_pb_event_id = no_pb_event.event_id

    def test_001_navigate_to_edp_of_event(self):
        """
        DESCRIPTION: Navigate to EDP of event
        EXPECTED: * Price Boost icon is displayed on the right side of market header (eg. 'Match Result')
        """
        self.navigate_to_edp(event_id=self.pb_event_id)
        self.__class__.market = list(self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(self.market.promotion_icons.has_price_boost(), msg=' "Price Boost" icon is not displayed')

    def test_002_navigate_to_edp_of_event_with_price_boost_flag_ticked_at_market_level__cashout_flag_available(self):
        """
        DESCRIPTION: Navigate to EDP of event with Price Boost flag ticked at market level & cashout flag available
        EXPECTED: * Cashout icon is present
        EXPECTED: * Price Boost icon is displayed after it
        """
        self.assertTrue(self.market.section_header.has_cash_out_mark(), msg='"Cashout" icon is not displayed')
        price_boost_coordinates = self.market.promotion_icons.price_boost.location.get('x')
        cash_out_coordinates = self.market.section_header.cash_out_label.location.get('x')
        self.assertTrue(price_boost_coordinates > cash_out_coordinates,
                        msg=f'PriceBoost icon is not displayed after Cashout. PriceBosst coordinates is: '
                            f'{price_boost_coordinates}, Cashout coordinates is: {cash_out_coordinates}')

    def test_003_expandcollapse_market_header(self):
        """
        DESCRIPTION: Expand/Collapse market header
        EXPECTED: * Price Boost icon remains displayed on the right side of market header
        """
        if self.market.is_expanded():
            self.market.collapse()
        else:
            self.market.expand()
        self.assertTrue(self.market.promotion_icons.price_boost.is_displayed(),
                        msg=' "Price Boost" icon is not displayed')

    def test_004_navigate_to_edp_of_event_with_price_boost_flag_not_ticked(self):
        """
        DESCRIPTION: Navigate to EDP of event with Price Boost flag not ticked
        EXPECTED: * Price Boost icon is not displayed
        """
        self.navigate_to_edp(event_id=self.no_pb_event_id)
        market = list(self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertFalse(market.promotion_icons.has_price_boost(),
                         msg=' "Price Boost" icon is not displayed')
