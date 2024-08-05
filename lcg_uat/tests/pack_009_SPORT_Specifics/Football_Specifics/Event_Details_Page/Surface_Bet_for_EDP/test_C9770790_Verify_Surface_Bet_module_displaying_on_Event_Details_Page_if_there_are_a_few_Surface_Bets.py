from time import sleep

import pytest
from faker import Faker

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.critical
@pytest.mark.event_details
@pytest.mark.surface_bets
@pytest.mark.mobile_only
@vtest
class Test_C9770790_Verify_Surface_Bet_module_displaying_on_Event_Details_Page_if_there_are_a_few_Surface_Bets(BaseFeaturedTest):
    """
    TR_ID: C9770790
    VOL_ID: C15755563
    NAME: Verify Surface Bet module displaying on Event Details Page if there are a few Surface Bets
    DESCRIPTION: This test case verifies displaying of Surface Bets module when there is a few selections configured for the module in CMS.
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)

    def get_actual_prices_from_ss(self, event):
        outcomes = next(((market['market']['children']) for market in event['event']['children']
                         if market['market'].get('children')), None)
        price_resp = next(((i['outcome']['children'][0]['price']) for i in outcomes
                           if 'price' in i['outcome']['children'][0].keys()), None)
        price_resp_2 = outcomes[1]['outcome']['children'][0]['price']
        self.__class__.expected_price_away = f'{price_resp_2["priceNum"]}/{price_resp_2["priceDen"]}' \
            if price_resp_2 else 'SP'  # if price response is empty -> SP
        self.__class__.expected_price_home = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}' \
            if price_resp else 'SP'  # if price response is empty -> SP

    def test_000_preconditions(self):
        """
        PRECONDITIONS: There are a few Surface Bets added to the Event Details page (EDP).
        PRECONDITIONS: Content/Was price/Icon for one Surface Bet are not defined
        PRECONDITIONS: Content/Was price/Icon for one Surface Bet are defined
        PRECONDITIONS: Valid Selection Ids are set
        PRECONDITIONS: Open this EDP in Oxygen application.
        """
        category_id = self.ob_config.football_config.category_id
        if tests.settings.backend_env == 'prod':
            self.__class__.event = self.get_active_events_for_category(category_id=category_id)[0]
            self.__class__.eventID = self.event['event']['id']
            self._logger.info(f'*** Found Football event with id "{self.eventID}"')
            outcomes = next(((market['market']['children']) for market in self.event['event']['children']
                             if market['market'].get('children')), None)
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(selection_ids.values())[0]
            selection_id_2 = list(selection_ids.values())[1]
            self.get_actual_prices_from_ss(event=self.event)

            self._logger.info(f'*** First selection id "{selection_id}" and price "{self.expected_price_home}"')
            self._logger.info(f'*** Second selection id "{selection_id_2}" and price "{self.expected_price_away}"')

        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event.event_id
            selection_id = event.selection_ids[event.team1]
            selection_id_2 = event.selection_ids[event.team2]
            self.__class__.expected_price_away = self.ob_config.event.prices['odds_away']
            self.__class__.expected_price_home = self.ob_config.event.prices['odds_home']
            self.__class__.event = event.ss_response

        surface_bet_with_content_and_price = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                                             categoryIDs=category_id,
                                                                             eventIDs=self.eventID,
                                                                             edpOn=True,
                                                                             content=self.content,
                                                                             priceNum=self.price_num,
                                                                             priceDen=self.price_den
                                                                             )
        self.__class__.surface_bet_with_content_and_price_id = surface_bet_with_content_and_price.get('id')
        self.__class__.surface_bet_with_content_and_price_title = surface_bet_with_content_and_price.get('title').upper()

        surface_bet_without_content_and_price = self.cms_config.add_surface_bet(selection_id=selection_id_2,
                                                                                categoryIDs=category_id,
                                                                                eventIDs=self.eventID,
                                                                                edpOn=True,
                                                                                content=None,
                                                                                priceNum=None,
                                                                                priceDen=None)
        self.__class__.surface_bet_without_content_and_price_id = surface_bet_without_content_and_price.get('id')
        self.__class__.surface_bet_without_content_and_price_title = surface_bet_without_content_and_price.get('title').upper()

        self.navigate_to_edp(self.eventID)

        sleep(30)  # there's delay between putting values on CMS and appearance on UI

    def test_001_verify_the_surface_bet_carousel(self):
        """
        DESCRIPTION: Verify the Surface Bet carousel
        EXPECTED: * Full first SB card and ~1/4 of the following card are shown
        EXPECTED: * Carousel can be smoothly swiped to the left/right
        """
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertTrue(all((sf_bet in surface_bets for sf_bet in (self.surface_bet_with_content_and_price_title,
                                                                   self.surface_bet_without_content_and_price_title))),
                        msg=f'"{[self.surface_bet_with_content_and_price_title, self.surface_bet_without_content_and_price_title]}" not found in "{list(surface_bets.keys())}"')

    def test_002_verify_the_surface_bet_without_contentwas_priceicon_displaying(self):
        """
        DESCRIPTION: Verify the Surface Bet without Content/Was price/Icon displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: * Content placeholder is empty
        EXPECTED: * Was price placeholder is empty, "Was" word isn't displayed
        EXPECTED: * Title is aligned as there is no icon placeholder
        """
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_without_content_and_price_title)

        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_without_content_and_price_title}" '
                                         f'not found in "{list(surface_bets.keys())}"')

        self.assertTrue(surface_bet.has_bet_button(),
                        msg=f'Bet Button is not shown for {self.surface_bet_without_content_and_price_title}')
        surface_bet.bet_button.scroll_to()
        actual_price = surface_bet.bet_button.outcome_price_text
        self.assertEqual(actual_price, self.expected_price_away,
                         msg=f'Actual price on UI "{actual_price}" is not the same as on OB "{self.expected_price_away}"')

        self.assertFalse(surface_bet.content, msg='Surface Bet content is not empty')

        self.assertFalse(surface_bet.is_old_price_present(expected_result=False),
                         msg='Placeholder for old price is shown')

        self.assertFalse(surface_bet.header.has_icon(expected_result=False), msg='Icon is shown')

    def test_003_verify_the_surface_bet_with_contentwas_priceicon_displaying(self):
        """
        DESCRIPTION: Verify the Surface Bet with Content/Was price/Icon displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Icon, uploaded in the CMS
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: >* Content, defined in the CMS
        EXPECTED: >* Price, defined in the CMS (Coral: price is struck through; Ladbrokes: "Was" and price are struck through)
        """
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_with_content_and_price_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_with_content_and_price_title}" '
                                         f'not found in "{list(surface_bets.keys())}"')

        self.assertTrue(surface_bet.has_bet_button(),
                        msg=f'Bet Button is not shown for {self.surface_bet_with_content_and_price_title}')
        surface_bet.bet_button.scroll_to()
        actual_price = surface_bet.bet_button.outcome_price_text
        self.get_actual_prices_from_ss(event=self.event)
        self.assertEqual(actual_price, self.expected_price_home,
                         msg=f'Actual price on UI "{actual_price}" is not the same as on OB {self.expected_price_home}')

        self.assertEqual(surface_bet.content, self.content, msg=f'Text on UI:\n"{surface_bet.content}"\ndoes not match '
                                                                f'with text set in CMS:\n{self.content}')
        self.assertTrue(surface_bet.is_old_price_present(), msg='Old price is not displayed')
        self.assertEqual(surface_bet.old_price.text, f'Was {self.price_num}/{self.price_den}')
        self.assertTrue(surface_bet.old_price.is_strike_through, msg='Old price is not strike through')

    def test_004_verify_price_and_was__word_are_not_displayed_if_the_following_conditions_numerator_isnt_set_and_denominator_is_set_numerator_is_set_and_denominator_isnt_set(self):
        """
        DESCRIPTION: Verify price and "Was " word are not displayed if the following conditions:
        DESCRIPTION: * Numerator isn't set and denominator is set
        DESCRIPTION: * Numerator is set and denominator isn't set
        EXPECTED: Price and "Was " word are not displayed if numerator or denominator are not defined
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_without_content_and_price_id,
                                           priceNum=None,
                                           priceDen=self.price_den
                                           )
        sleep(30)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_without_content_and_price_title)
        surface_bet.scroll_to()
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_without_content_and_price_title}" '
                                         f'not found in "{list(surface_bets.keys())}"')
        self.assertFalse(surface_bet.is_old_price_present(expected_result=False),
                         msg='Placeholder for old price is shown')

        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_without_content_and_price_id,
                                           priceNum=self.price_num,
                                           priceDen=None
                                           )

        sleep(30)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_without_content_and_price_title)
        surface_bet.scroll_to()
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_without_content_and_price_title}" '
                                         f'not found in "{list(surface_bets.keys())}"')
        self.assertFalse(surface_bet.is_old_price_present(expected_result=False),
                         msg='Placeholder for old price is shown')

    def test_005_verify_the_long_title_is_shortened_properly(self):
        """
        DESCRIPTION: Verify the long title is shortened properly
        EXPECTED: Long title is shortened and fits the Title area
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_without_content_and_price_id,
                                           title=f'{self.surface_bet_without_content_and_price_title} {self.fake.name_female()*10}')
        sleep(30)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = next((sf_bet for sf_bet_name, sf_bet in surface_bets.items() if self.surface_bet_without_content_and_price_title in sf_bet_name), None)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_without_content_and_price_title}" '
                                         f'not found in "{list(surface_bets.keys())}"')
        surface_bet.scroll_to()
        self.assertTrue(surface_bet.header.is_title_truncated(),
                        msg=f'Title for "{self.surface_bet_without_content_and_price_title}" is not truncated')

    def test_006_verify_content_with_a_long_text_is_shown_properly(self):
        """
        DESCRIPTION: Verify content with a long text is shown properly
        EXPECTED: The height of the Surface Bet card is increased to fit the text
        EXPECTED: Content is properly shown within the Content area
        EXPECTED: All the Surface Bets are of the same size
        """
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_with_content_and_price_title)
        surface_bet.scroll_to()
        initial_height = surface_bet.size.get('height')

        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_with_content_and_price_id,
                                           content=f'{self.fake.paragraph(nb_sentences=10)}')
        sleep(30)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_with_content_and_price_title)
        surface_bet.scroll_to()

        new_height = surface_bet.size.get('height')

        self.assertNotEqual(initial_height, new_height,
                            msg=f'Height for "{self.surface_bet_with_content_and_price_title}" was not changed')

        sf_bet_sizes = [sf_bet.size for sf_bet_name, sf_bet in surface_bets.items()]
        self.assertTrue(all(sf_bet_sizes[0] == size for size in sf_bet_sizes),
                        msg=f'All the Surface Bets are not the same size: "{sf_bet_sizes}"')
