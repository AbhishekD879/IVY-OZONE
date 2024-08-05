import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.event_details
@pytest.mark.markets
@pytest.mark.promotions
@pytest.mark.money_back
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@pytest.mark.login
@vtest
class Test_C2807909_Verify_MoneyBack_signposting_icon_on_Football_market_level(BaseRacing):
    """
    TR_ID: C2807909
    NAME: Verify MoneyBack signposting icon on EDP
    DESCRIPTION: This test case verifies that the MoneyBack signposting icon is displayed on markets
    with MoneyBack flag available on the events details page
    PRECONDITIONS: Events with MoneyBack flag & Cashout flag ticked at market levels available
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events and login
        """
        event_1 = self.ob_config.add_autotest_premier_league_football_event(is_live=True, market_money_back=True,
                                                                            cashout=False)
        self.__class__.eventID_1 = event_1.event_id

        event_2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                            cashout=True,
                                                                            market_money_back=True)
        self.__class__.eventID_2 = event_2.event_id

        event_3 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID_3 = event_3.event_id

        self.site.login()

    def test_001_navigate_to_edp_of_event_with_moneyback_flag_ticked_at_market_level(self):
        """
        DESCRIPTION: Navigate to EDP of event with MoneyBack flag ticked at market level
        EXPECTED: * MoneyBack icon is displayed on the right side of market header
        """
        self.navigate_to_edp(event_id=self.eventID_1)
        events = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found on EDP {self.eventID_1} page')
        market = events.get(self.expected_market_sections.match_result)
        self.assertTrue(market, msg=f'{self.expected_market_sections.match_result} '
                                    f'market is not found on EDP {self.eventID_1} page')
        market_width = market.market_section_header.size["width"]
        money_back_icon_location = market.promotion_icons.money_back.location.get('x')
        self.assertTrue(market_width / 2 < money_back_icon_location,
                        msg='MoneyBack icon is not displayed on the right side of market header')

    def test_002_navigate_to_edp_of_event_with_moneyback_flag_ticked_at_market_level_cashout_flag_available(self):
        """
        DESCRIPTION: Navigate to EDP of event with MoneyBack flag ticked at market level & cashout flag availablelabel
        EXPECTED: * Cashout icon is present
        EXPECTED: * MoneyBack icon is displayed before it
        """
        self.navigate_to_edp(event_id=self.eventID_2)
        events = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found on EDP {self.eventID_2} page')
        self.__class__.market = events.get(self.expected_market_sections.match_result)
        self.assertTrue(self.market, msg=f'{self.expected_market_sections.match_result} '
                                         f'market is not found on EDP {self.eventID_2} page')
        self.assertTrue(self.market.market_section_header.has_cash_out_mark(),
                        msg=f'Cashout icon is not present on market {self.expected_market_sections.match_result}')
        money_back_coordinates = self.market.promotion_icons.money_back.location.get('x')
        cash_out_coordinates = self.market.market_section_header.cash_out_mark.location.get('x')
        self.assertTrue(money_back_coordinates > cash_out_coordinates,
                        msg=f'MoneyBack icon is not displayed after Cashout. MoneyBack coordinates is: '
                            f'{money_back_coordinates}, Cashout coordinates is: {cash_out_coordinates}')

    def test_003_expand_collapse_market_header(self):
        """
        DESCRIPTION: Expand/Collapse market header
        EXPECTED: * MoneyBack icon remains displayed on the right side of market header
        """
        self.market.collapse()
        market_width = self.market.market_section_header.size["width"]
        money_back_icon_location = self.market.promotion_icons.money_back.location.get('x')
        self.assertTrue(market_width / 2 < money_back_icon_location,
                        msg='MoneyBack icon is not displayed on the right side of market header')
        self.market.expand()
        market_width = self.market.market_section_header.size["width"]
        money_back_icon_location = self.market.promotion_icons.money_back.location.get('x')
        self.assertTrue(market_width / 2 < money_back_icon_location,
                        msg='MoneyBack icon is not displayed on the right side of market header')

    def test_004_navigate_to_edp_of_event_with_moneyback_flag_not_ticked(self):
        """
        DESCRIPTION: Navigate to EDP of event with MoneyBack flag not ticked
        EXPECTED: * MoneyBack icon is not displayed
        """
        self.navigate_to_edp(event_id=self.eventID_3)
        events = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found on EDP {self.eventID_3} page')
        market = events.get(self.expected_market_sections.match_result)
        self.assertTrue(market, msg=f'{self.expected_market_sections.match_result} '
                                    f'market is not found on EDP {self.eventID_3} page')
        self.assertFalse(market.promotion_icons.has_money_back(expected_result=False),
                         msg='MoneyBack icon is displayed')
