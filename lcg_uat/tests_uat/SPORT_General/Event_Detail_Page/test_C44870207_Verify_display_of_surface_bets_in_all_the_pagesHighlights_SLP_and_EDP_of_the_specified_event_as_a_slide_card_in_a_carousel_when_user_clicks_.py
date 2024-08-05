import pytest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from faker import Faker
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Not applicable for PROD as need to create new event, selection suspension & price change
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870207_Verify_display_of_surface_bets_in_all_the_pagesHighlights_SLP_and_EDP_of_the_specified_event_as_a_slide_card_in_a_carousel_when_user_clicks_on_the_odds_button_the_selection_is_added_to_the_quick_bet_bet_slip(BaseFeaturedTest, BaseBetSlipTest):
    """
    TR_ID: C44870207
    NAME: Verify display of surface bets in all the pages(Highlights, SLP and EDP of the specified event) as a slide/card in a carousel, when user clicks on the odds button the selection is added  to the quick bet/ bet slip
    DESCRIPTION: Verify display of surface bets in all the pages(Highlights, SLP and EDP of the specified event) as a slide/card in a carousel, when user clicks on the odds button the selection is added  to the quick bet/ bet slip
    PRECONDITIONS: -There is a  Surface Bet added to the Event Details page (EDP).
    PRECONDITIONS: -Content/Was price/Icon
    PRECONDITIONS: -Display on Highlights tab
    PRECONDITIONS: -Open this EDP in Oxygen application.
    PRECONDITIONS: -CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True

    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)
    changed_price = '1/1'

    def random_string(self, length=10):
        return self.f.text(length).replace("\n", '')

    def retrieve_surface_bet(self, bet_title: str):
        self.navigate_to_page(name='sport/football')
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')

        ui_surface_bet = surface_bets.get(bet_title)
        self.assertIsNotNone(ui_surface_bet, msg=f'Specified surface bet "{bet_title}" cannot be found')
        return ui_surface_bet

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: Home page opened
        """
        self.site.login()
        self.site.wait_content_state('Homepage')
        self.device.driver.implicitly_wait(1)

    def test_002_verify_display_of_surface_bets_on_highlights_sports_landing_page_and_event_detail_page(self):
        """
        DESCRIPTION: Verify display of surface bets on highlights, Sports landing page and Event detail page
        EXPECTED: Surface bets are displayed on highlights tab, sports landing page and event detail page
        """
        self.__class__.category_id = self.ob_config.football_config.category_id
        cms_surface_bet = self.cms_config.get_sport_module(sport_id=self.category_id,
                                                           module_type='SURFACE_BET')[0]
        if cms_surface_bet['disabled']:
            self.cms_config.change_sport_module_state(sport_module=cms_surface_bet)

        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_id = event.selection_ids[event.team1]
        self.__class__.eventID = event.event_id
        self.__class__.price_button_text = self.ob_config.event.prices['odds_home']

        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_id,
                                                                     categoryIDs=self.category_id,
                                                                     content=self.content,
                                                                     eventIDs=self.eventID,
                                                                     edpOn=True,
                                                                     priceNum=self.price_num,
                                                                     priceDen=self.price_den
                                                                     )
        self.__class__.surface_bet_title = self.surface_bet.get('title').upper()

        if self.device_type in ['mobile', 'tablet']:
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state('football')

            result = self.wait_for_surface_bets(name=self.surface_bet_title, timeout=1, poll_interval=1, raise_exceptions=False)

            if result is None:
                self.device.refresh_page()
                self.site.wait_splash_to_hide()
                self.wait_for_surface_bets(name=self.surface_bet_title, timeout=5, poll_interval=1)

        self.navigate_to_edp(self.eventID, timeout=15)
        self.assertTrue(self.site.sport_event_details.tab_content.has_surface_bets(),
                        msg=f'Surface Bet module is not shown on the EDP with event_id: "{self.eventID}"')

    def test_003_verify_the_surface_bet_carousel(self):
        """
        DESCRIPTION: Verify the Surface Bet carousel
        EXPECTED: Carousel can be smoothly swiped to the left/right
        """
        if self.device_type in ['mobile', 'tablet']:
            self.navigate_to_page(name='sport/football')
            self.__class__.surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        else:
            self.navigate_to_edp(self.eventID)
            self.__class__.surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(self.surface_bets, msg='No Surface Bets found')
        if len(self.surface_bets) > 2:
            last_surface_bet = list(self.surface_bets.values())[-1]
            first_surface_bet = list(self.surface_bets.values())[0]
            self.assertTrue(last_surface_bet.is_displayed(),
                            msg='Carousel couldnot swiped from first to the last surface bet')
            self.assertTrue(first_surface_bet.is_displayed(),
                            msg='Carousel couldnot swiped from last to the first surface bet')

    def test_004_verify_the_surface_bet_with_contentwas_priceicon_displaying(self):
        """
        DESCRIPTION: Verify the Surface Bet with Content/Was price/Icon displaying
        EXPECTED: Contents, price, was price and icon are displayed
        """
        if self.device_type in ['mobile', 'tablet']:
            self.__class__.ui_surface_bet = self.retrieve_surface_bet(self.surface_bet_title)
        else:
            self.__class__.ui_surface_bet = self.surface_bets.get(self.surface_bet_title)
        expected_title = self.surface_bet_title
        actual_title = self.ui_surface_bet.name
        self.assertEqual(expected_title, actual_title,
                         msg=f"Expected surface bet title '{expected_title}' isn't equal to actual '{actual_title}'")

        button = self.ui_surface_bet.bet_button
        self.assertTrue(button.is_displayed(), msg=f"Betslip button isn't displayed for surface bet '{expected_title}'")

        expected_price = self.price_button_text
        actual_price = button.outcome_price_text
        self.assertEqual(expected_price, actual_price,
                         msg=f'Expected price "{expected_price}" is not equal to actual "{actual_price}"')

        expected_content = self.surface_bet.get('content')
        actual_content = self.ui_surface_bet.content

        self.assertEqual(expected_content, actual_content,
                         msg=f'Actual content "{actual_content}" is not equal to expected content "{expected_content}"')

        is_price_crossout = self.ui_surface_bet.old_price.is_strike_through
        self.assertTrue(is_price_crossout, msg='Price is not struck through, but was expected to be')

    def test_005_verifies_that_expireddisableddeleted_surface_bet_is_not_shown_on_highlighs_tab_sports_landing_page_and_event_detail_page(self):
        """
        DESCRIPTION: Verifies that expired/disabled/deleted surface bet is not shown on Highlighs tab, sports landing page and Event detail page
        EXPECTED: expired/disabled/deleted surface bet are not displayed
        """
        cms_surface_bets = self.cms_config.get_surface_bets_for_page(reference_id=self.category_id, related_to='sport')
        actual_surface_bets = list(self.surface_bets.keys())

        expired_surface_bets = [s_bets['title'] for s_bets in cms_surface_bets if
                                s_bets['references'][1]['refId'] == self.category_id and
                                (s_bets['displayTo'] is None or s_bets['displayTo'] < get_date_time_as_string(
                                    time_format="%Y-%m-%dT%H:%M:%S", hours=-1))]

        for expired_sb in expired_surface_bets:
            self.assertNotIn(expired_sb, actual_surface_bets, msg=f'Expired surface bet "{expired_sb}" showing on UI')

    def test_006_verify_that_suspendedfuture_surface_bet_is_shown_on_the_edp(self):
        """
        DESCRIPTION: Verify that Suspended/future Surface Bet is shown on the EDP
        EXPECTED: Suspended surface bet are greyed out
        EXPECTED: Future surface bets are displayed on EDP
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, active=False, displayed=True)
        if self.device_type not in ['mobile', 'tablet']:
            self.device.refresh_page()
            self.site.wait_splash_to_hide(4)
            surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
            self.ui_surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertFalse(self.ui_surface_bet.bet_button.is_enabled(expected_result=False, timeout=30),
                         msg=f'Bet button is not disabled for "{self.surface_bet_title}"')
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True,
                                              active=True)
        if self.device_type not in ['mobile', 'tablet']:
            self.device.refresh_page()
            self.site.wait_splash_to_hide(4)
            surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
            self.ui_surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(self.ui_surface_bet.bet_button.is_enabled(expected_result=True, timeout=30),
                        msg=f'Bet button is not enabled for "{self.surface_bet_title}"')

    def test_007_verify_live_updates_on_surface_bets(self):
        """
        DESCRIPTION: Verify Live updates on surface bets
        EXPECTED: Price updates without page refresh
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.changed_price)
        self.wait_for_price_update_from_live_serv(selection_id=self.selection_id, price=self.changed_price)

        if self.device_type in ['mobile', 'tablet']:
            self.ui_surface_bet = self.retrieve_surface_bet(self.surface_bet_title)
        else:
            self.device.refresh_page()  # BMA-55571 - Prices are not updated automatically for price change
            self.site.wait_splash_to_hide(4)
            surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
            self.ui_surface_bet = surface_bets.get(self.surface_bet_title)

        surfacebet_button = self.ui_surface_bet.bet_button
        self.assertTrue(surfacebet_button.is_displayed(), msg=f"Betslip button isn't displayed on surface bet '{self.surface_bet_title}'")

        ui_changed_price = surfacebet_button.outcome_price_text
        self.assertNotEquals(self.price_button_text, ui_changed_price,
                             msg=f'Expected price "{self.price_button_text}" is not equal to actual "{ui_changed_price}"')
        self.ui_surface_bet.bet_button.click()

    def test_008_place_the_bet_using_price_button_of_the_surface_bet_from_the_quickbetbetslip_verify_bet_is_placed_successfully(self):
        """
        DESCRIPTION: Place the bet using Price button of the Surface bet from the Quickbet/Betslip. Verify bet is placed successfully
        EXPECTED: Bet is placed successfully
        """
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet panel is not opened')
            quick_bet = self.site.quick_bet_panel.selection
            quick_bet.content.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
            self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(), msg='Bet Receipt is not displayed')
        else:
            singles_section = self.get_betslip_sections().Singles
            self.assertTrue(singles_section, msg='Selections are not displayed in betslip')
            stake_name, stake = list(singles_section.items())[0]
            stake.amount_form.input.value = '0.10'
            self.get_betslip_content().bet_now_button.click()
            self.check_bet_receipt_is_displayed()
