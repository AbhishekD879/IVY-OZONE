from time import sleep

import pytest
from faker import Faker

from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.homepage_featured
@pytest.mark.mobile_only
@pytest.mark.slow
@vtest
class Test_C9770789_Verify_Surface_Bet_module_displaying_on_Event_Details_Page_if_there_is_one_Surface_Bet(BaseFeaturedTest):
    """
    TR_ID: C9770789
    VOL_ID: C12519961
    NAME: Verify Surface Bet module displaying on Event Details Page if there is one Surface Bet
    DESCRIPTION: This test case verifies displaying of Surface Bets module when there is only one selection configured for the module in CMS.
    PRECONDITIONS: 1. There is a single Surface Bet added to the Event Details page (EDP).
    PRECONDITIONS: 2. Content/Was price/Icon are not defined
    PRECONDITIONS: 3. Valid Selection Id is set
    PRECONDITIONS: 4. Display on Highlights tab is unticked
    PRECONDITIONS: 5. Show on Sports options are unticked
    PRECONDITIONS: 6. Open this EDP in Oxygen application.
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    f = Faker()
    timeout = 60
    keep_browser_open = True
    price = {'priceDen': f.random.randint(10, 99),
             'priceNum': f.random.randint(10, 99)}

    def random_string(self, length=10):
        return self.f.text(length).replace("\n", '')

    def retrieve_surface_bet(self, bet_title: str):
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertEqual(len(surface_bets), 1, msg='Single surface bet is not displayed on the page')

        ui_surface_bet = surface_bets.get(bet_title)
        self.assertIsNotNone(ui_surface_bet, msg=f'Specified surface bet "{bet_title}" cannot be found')
        return ui_surface_bet

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. There is a single Surface Bet added to the Event Details page (EDP).
        PRECONDITIONS: 2. Content/Was price/Icon are not defined
        PRECONDITIONS: 3. Valid Selection Id is set
        PRECONDITIONS: 4. Display on Highlights tab is unticked
        PRECONDITIONS: 5. Show on Sports options are unticked
        PRECONDITIONS: 6. Open this EDP in Oxygen application.
        PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids, self.__class__.team1 = event.selection_ids, event.team1
        self.__class__.eventID = event.event_id
        self.__class__.price_button_text = self.ob_config.event.prices['odds_home']

        self.__class__.api_surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_ids[self.team1],
                                                                         content=None,
                                                                         eventIDs=self.eventID,
                                                                         edpOn=True,
                                                                         priceDen=None,
                                                                         priceNum=None)

        self.__class__.surface_bet_title = self.api_surface_bet.get('title').upper()

        sleep(self.timeout)  # there's delay between putting values on CMS and appearance on UI

        self.navigate_to_edp(self.eventID)

    def test_001_verify_the_single_surface_bet_displaying(self):
        """
        DESCRIPTION: Verify the single Surface Bet displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: * Surface Bet is of the regular size, centered
        EXPECTED: * Content placeholder is empty
        EXPECTED: * Was price placeholder is empty, "Was" word isn't displayed
        EXPECTED: * Title is aligned as there is no icon placeholder
        """
        ui_surface_bet = self.retrieve_surface_bet(self.surface_bet_title)

        expected_title = self.surface_bet_title
        actual_title = ui_surface_bet.name
        self.assertEqual(expected_title, actual_title,
                         msg=f"Expected surface bet title '{expected_title}' isn't equal to actual '{actual_title}'")

        self.assertTrue(ui_surface_bet.bet_button.is_displayed(),
                        msg="Betslip button isn't displayed")

        expected_price = self.price_button_text
        actual_price = ui_surface_bet.bet_button.outcome_price_text
        self.assertEqual(expected_price, actual_price,
                         msg=f'Expected price "{expected_price}" is not equal to actual "{actual_price}"')

        self.assertFalse(ui_surface_bet.content, msg='Content is not empty, but was expected to be empty')

        is_present = ui_surface_bet.is_old_price_present(expected_result=False)
        self.assertFalse(is_present, msg='Was price placeholder is present, but was not expected to be present')

        is_icon_present = ui_surface_bet.header.has_icon(expected_result=False)
        self.assertFalse(is_icon_present, msg='Surface bet icon is present, but was not expected to be present')

    def test_002_in_the_cms_edit_the_surface_bet_add_content_upload_icon_add_price_both_numerator_and_denominator(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet, add content, upload icon, add price (both numerator and denominator)
        """
        expected_content = self.random_string()
        self.__class__.api_surface_bet = self.cms_config.update_surface_bet(self.api_surface_bet['id'],
                                                                            content=expected_content,
                                                                            priceDen=self.price['priceDen'],
                                                                            priceNum=self.price['priceNum'])
        sleep(self.timeout)  # there's delay between putting values on CMS and appearance on UI

        # icon can't be tested

    def test_003_in_the_application_refresh_the_edpverify_the_single_surface_bet_displaying(self):
        """
        DESCRIPTION: In the application: Refresh the EDP
        DESCRIPTION: Verify the single Surface Bet displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Icon, uploaded in the CMS
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: >* Content, defined in the CMS
        EXPECTED: >* Price, defined in the CMS (Coral: price is struck through; Ladbrokes: "Was" and price are struck through)
        EXPECTED: * Surface Bet is fit the full width of the screen
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        # icon can't be tested

        ui_surface_bet = self.retrieve_surface_bet(self.surface_bet_title)

        expected_title = self.surface_bet_title
        actual_title = ui_surface_bet.name
        self.assertEqual(expected_title, actual_title,
                         msg=f"Expected surface bet title '{expected_title}' isn't equal to actual '{actual_title}'")

        button = ui_surface_bet.bet_button
        self.assertTrue(button.is_displayed(),
                        msg="Betslip button isn't displayed")

        expected_price = self.price_button_text
        actual_price = button.outcome_price_text
        self.assertEqual(expected_price, actual_price,
                         msg=f'Expected price "{expected_price}" is not equal to actual "{actual_price}"')

        expected_content = self.api_surface_bet.get('content')
        actual_content = ui_surface_bet.content

        self.assertEqual(expected_content, actual_content,
                         msg=f'Actual content "{actual_content}" is not equal to expected content "{expected_content}"')

        is_price_crossout = ui_surface_bet.old_price.is_strike_through
        self.assertTrue(is_price_crossout, msg='Price is not struck through, but was expected to be')

    def test_004_verify_price_and_was__word_are_not_displayed_if_the_following_conditions_numerator_isnt_set_and_denominator_is_set_numerator_is_set_and_denominator_isnt_set(self):
        """
        DESCRIPTION: Verify price and "Was " word are not displayed if the following conditions:
        DESCRIPTION: * Numerator isn't set and denominator is set
        DESCRIPTION: * Numerator is set and denominator isn't set
        EXPECTED: Price and "Was " word are not displayed if numerator or denominator are not defined
        """
        self.cms_config.update_surface_bet(self.api_surface_bet['id'],
                                           priceNum=None,
                                           priceDen=self.price['priceDen'])
        sleep(self.timeout)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        was_text_is_present = self.retrieve_surface_bet(self.surface_bet_title).is_old_price_present(expected_result=False)
        self.assertFalse(was_text_is_present, msg='Was price placeholder is present, but was not expected to be present')

        self.cms_config.update_surface_bet(self.api_surface_bet['id'],
                                           priceNum=self.price['priceNum'],
                                           priceDen=None)
        sleep(self.timeout)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        was_text_is_present = self.retrieve_surface_bet(self.surface_bet_title).is_old_price_present(expected_result=False)
        self.assertFalse(was_text_is_present, msg='Was price placeholder is present, but was not expected to be present')

    def test_005_verify_the_long_title_is_shortened_properly(self):
        """
        DESCRIPTION: Verify the long title is shortened properly
        EXPECTED: Long title is shortened and fits the Title area
        """
        long_title = self.random_string(100)

        self.cms_config.update_surface_bet(self.api_surface_bet['id'],
                                           title=long_title)
        sleep(self.timeout)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        ui_surface_bet = self.retrieve_surface_bet(long_title.upper())
        self.assertTrue(ui_surface_bet.header.is_title_truncated(),
                        msg=f'Title "{long_title}" is not truncated, but was expected to be truncated')

    def test_006_verify_content_with_a_long_text_is_shown_properly(self):
        """
        DESCRIPTION: Verify content with a long text is shown properly
        EXPECTED: The height of the Surface Bet card is increased to fit the text
        EXPECTED: Content is properly shown within the Content area
        """
        long_content = self.random_string(300)

        self.cms_config.update_surface_bet(self.api_surface_bet['id'],
                                           content=long_content,
                                           title=self.surface_bet_title)
        sleep(self.timeout)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        ui_surface_bet = self.retrieve_surface_bet(self.surface_bet_title)
        self.assertFalse(ui_surface_bet.is_content_truncated(),
                         msg='Content is truncated, but was not expected to be truncated')
        ui_content = ui_surface_bet.content
        self.assertEqual(long_content, ui_content,
                         msg=f'Expected content "{long_content}" is not equal to actual content from UI "{ui_content}"')
