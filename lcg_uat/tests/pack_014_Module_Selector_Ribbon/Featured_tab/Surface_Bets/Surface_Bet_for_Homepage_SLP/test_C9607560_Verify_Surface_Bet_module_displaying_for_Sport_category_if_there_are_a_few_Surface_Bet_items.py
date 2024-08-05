import pytest
import tests
from faker import Faker
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot modify cms / create modules on prod
@pytest.mark.critical
@pytest.mark.surface_bets
@pytest.mark.mobile_only
@pytest.mark.featured
@pytest.mark.cms
@vtest
class Test_C9607560_Verify_Surface_Bet_module_displaying_for_Sport_category_if_there_are_a_few_Surface_Bet_items(BaseFeaturedTest):
    """
    TR_ID: C9607560
    VOL_ID: C9858656
    NAME: Verify Surface Bet module displaying for Sport category if there are a few Surface Bet items
    DESCRIPTION: This test case verifies displaying of Surface Bets module when there is a few selections configured for the module in CMS.
    PRECONDITIONS: 1. There are a few Surface Bets added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Content/Was price/Icon for one Surface Bet are not defined
    PRECONDITIONS: 2. Content/Was price/Icon for one Surface Bet are defined
    PRECONDITIONS: 3. Valid Selection Ids are set
    PRECONDITIONS: 4. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Surface Bets to the SLP/Homepage in the CMS
        DESCRIPTION: There are a few Surface Bets added to the SLP/Homepage in the CMS
        DESCRIPTION: Content/Was price/Icon for one Surface Bet are not defined
        DESCRIPTION: Content/Was price/Icon for one Surface Bet are defined
        DESCRIPTION: Open this SLP/Homepage page in the application
        """
        category_id = self.ob_config.football_config.category_id
        cms_surface_bet = self.cms_config.get_sport_module(sport_id=category_id,
                                                           module_type='SURFACE_BET')[0]
        if cms_surface_bet['disabled']:
            if tests.settings.cms_env == 'prd0':
                raise CmsClientException('Surface bets are disabled for Football')
            else:
                self.cms_config.change_sport_module_state(sport_module=cms_surface_bet)

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=category_id)[0]
            self.__class__.eventID = event['event']['id']
            self._logger.info(f'*** Found Football event with id "{self.eventID}"')
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are not available outcomes')
            selection_ids = list({i['outcome']['name']: i['outcome']['id'] for i in outcomes}.values())
            if len(selection_ids) < 3:
                raise SiteServeException('Existing event does not have at least 3 outcomes')
            self.__class__.selection_id1 = selection_ids[0]
            self.__class__.selection_id2 = selection_ids[2]
            self.__class__.marketID = outcomes[0]['outcome']['marketId']
            price_info1 = outcomes[0]['outcome']['children'][0]['price']
            self.__class__.expected_price1 = f'{price_info1["priceNum"]}/{price_info1["priceDen"]}'
            price_info2 = outcomes[2]['outcome']['children'][0]['price']
            self.__class__.expected_price2 = f'{price_info2["priceNum"]}/{price_info2["priceDen"]}'
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_id1 = event.selection_ids[event.team1]
            self.__class__.selection_id2 = event.selection_ids[event.team2]
            self.__class__.expected_price1 = self.ob_config.event.prices['odds_home']
            self.__class__.expected_price2 = self.ob_config.event.prices['odds_away']

        surface_bet_with_content_and_price = self.cms_config.add_surface_bet(selection_id=self.selection_id1,
                                                                             categoryIDs=category_id,
                                                                             content=self.content,
                                                                             priceNum=self.price_num,
                                                                             priceDen=self.price_den
                                                                             )
        self.__class__.surface_bet_with_content_and_price_id = surface_bet_with_content_and_price.get('id')
        self.__class__.surface_bet_with_content_and_price_title = surface_bet_with_content_and_price.get('title').upper()

        surface_bet_without_content_and_price = self.cms_config.add_surface_bet(selection_id=self.selection_id2,
                                                                                categoryIDs=category_id,
                                                                                content=None,
                                                                                priceNum=None,
                                                                                priceDen=None)
        self.__class__.surface_bet_without_content_and_price_id = surface_bet_without_content_and_price.get('id')
        self.__class__.surface_bet_without_content_and_price_title = surface_bet_without_content_and_price.get('title').upper()

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

        result = self.wait_for_surface_bets(name=self.surface_bet_with_content_and_price_title, timeout=1, poll_interval=1,
                                            raise_exceptions=False)
        if result is None:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.wait_for_surface_bets(name=self.surface_bet_with_content_and_price_title, timeout=15, poll_interval=1)

    def test_001_verify_the_surface_bet_carousel(self):
        """
        DESCRIPTION: Verify the Surface Bet carousel
        EXPECTED: * Full first SB card and ~1/4 of the following card are shown
        EXPECTED: * Carousel can be smoothly swiped to the left/right
        """
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertTrue(all((sf_bet in surface_bets for sf_bet in (self.surface_bet_with_content_and_price_title,
                                                                   self.surface_bet_without_content_and_price_title))),
                        msg=f'"{[self.surface_bet_with_content_and_price_title, self.surface_bet_without_content_and_price_title]}" not found in "{list(surface_bets.keys())}"')

    def test_002_verify_the_surface_bet_without_content_was_price_icon_displaying(self):
        """
        DESCRIPTION: Verify the Surface Bet without Content/Was price/Icon displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: * Content placeholder is empty
        EXPECTED: * Was price placeholder is empty, "Was" word isn't displayed
        EXPECTED: * Title is aligned as there is no icon placeholder
        """
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_without_content_and_price_title)
        surface_bet.bet_button.scroll_to()

        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_without_content_and_price_title}" '
                                         f'not found in "{list(surface_bets.keys())}"')

        self.assertTrue(surface_bet.has_bet_button(),
                        msg=f'Bet Button is not shown for {self.surface_bet_without_content_and_price_title}')
        actual_price = surface_bet.bet_button.outcome_price_text

        self.assertEqual(actual_price, self.expected_price2,
                         msg=f'Actual price on UI "{actual_price}" is not the same as on OB {self.expected_price2}')

        self.assertFalse(surface_bet.content, msg='Surface Bet content is not empty')

        self.assertFalse(surface_bet.is_old_price_present(expected_result=False),
                         msg='Placeholder for old price is shown')

        self.assertFalse(surface_bet.header.has_icon(expected_result=False), msg='Icon is shown')

    def test_003_verify_the_surface_bet_with_content_was_price_icon_displaying(self):
        """
        DESCRIPTION: Verify the Surface Bet with Content/Was price/Icon displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Icon, uploaded in the CMS
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: >* Content, defined in the CMS
        EXPECTED: >* Price, defined in the CMS (Coral: price is struck through; Ladbrokes: "Was" and price are struck through)
        """
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_with_content_and_price_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_with_content_and_price_title}" '
                                         f'not found in "{list(surface_bets.keys())}"')
        surface_bet.bet_button.scroll_to()

        self.assertTrue(surface_bet.has_bet_button(),
                        msg=f'Bet Button is not shown for {self.surface_bet_with_content_and_price_title}')
        actual_price = surface_bet.bet_button.outcome_price_text

        self.assertEqual(actual_price, self.expected_price1,
                         msg=f'Actual price on UI "{actual_price}" is not the same as on OB {self.expected_price1}')

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
        import time
        time.sleep(30)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
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

        import time
        time.sleep(30)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
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
        EXPECTED: Long title is shortened with ... and fits the Title area
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_without_content_and_price_id,
                                           title=f'{self.surface_bet_without_content_and_price_title} {self.fake.name_female()*10}')
        import time
        time.sleep(30)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
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
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_with_content_and_price_title)
        surface_bet.scroll_to()
        initial_height = surface_bet.size.get('height')

        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_with_content_and_price_id,
                                           content=f'{self.fake.paragraph(nb_sentences=10)}')
        import time
        time.sleep(30)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_with_content_and_price_title)
        surface_bet.scroll_to()

        new_height = surface_bet.size.get('height')

        self.assertNotEqual(initial_height, new_height,
                            msg=f'Height for "{self.surface_bet_with_content_and_price_title}" was not changed')

        sf_bet_sizes = [sf_bet.size for sf_bet_name, sf_bet in surface_bets.items()]
        self.assertTrue(all(sf_bet_sizes[0] == size for size in sf_bet_sizes),
                        msg=f'All the Surface Bets are not the same size: "{sf_bet_sizes}"')
