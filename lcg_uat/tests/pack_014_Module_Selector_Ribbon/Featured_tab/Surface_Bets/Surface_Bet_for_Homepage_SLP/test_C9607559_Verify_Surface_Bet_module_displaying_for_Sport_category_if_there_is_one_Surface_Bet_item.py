import pytest
import tests
from tests.base_test import vtest
from faker import Faker
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod  # cannot modify cms / create modules on prod
@pytest.mark.high
@pytest.mark.surface_bets
@pytest.mark.mobile_only
@pytest.mark.featured
@pytest.mark.cms
@pytest.mark.slow
@vtest
class Test_C9607559_Verify_Surface_Bet_module_displaying_for_Sport_category_if_there_is_one_Surface_Bet_item(BaseFeaturedTest):
    """
    TR_ID: C9607559
    VOL_ID: C9776316
    NAME: Verify Surface Bet module displaying for Sport category if there is one Surface Bet item
    DESCRIPTION: This test case verifies displaying of Surface Bets module when there is only one selection configured for the module in CMS.
    PRECONDITIONS: 1. There is a single Surface Bet added to the SLP/Homepage in CMS.
    PRECONDITIONS: 2. Content/Was price/Icon are not defined
    PRECONDITIONS: 3. Valid Selection Id is set
    PRECONDITIONS: 4. Open this SLP/Homepage in Oxygen application.
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True
    surface_bet_id = None
    tennis_surface_bet_ids = []
    surface_bet_title = ''
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms = cls.get_cms_config()
        if cls.tennis_surface_bet_ids:
            [cms.update_surface_bet(surface_bet_id=sf_bet, disabled=False)
             for sf_bet in cls.tennis_surface_bet_ids]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Disable all Surface Bets on page
        DESCRIPTION: Add Surface Bet to the SLP/Homepage in the CMS
        DESCRIPTION: Open this SLP/Homepage page in the application
        """
        tennis_category_id = self.ob_config.tennis_config.category_id

        cms_surface_bet = self.cms_config.get_sport_module(sport_id=tennis_category_id,
                                                           module_type='SURFACE_BET')[0]
        if cms_surface_bet['disabled']:
            if tests.settings.cms_env == 'prd0':
                raise CmsClientException('Surface bets are disabled for Tennis')
            else:
                self.cms_config.change_sport_module_state(sport_module=cms_surface_bet)

        surface_bets_for_tennis = self.cms_config.get_surface_bets_for_page(reference_id=tennis_category_id,
                                                                            related_to='sport')
        if surface_bets_for_tennis:
            for sf_bet in surface_bets_for_tennis:
                self.__class__.tennis_surface_bet_ids.append(sf_bet.get('id'))
                self.cms_config.update_surface_bet(surface_bet_id=sf_bet.get('id'),
                                                   disabled=True)
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=tennis_category_id)[0]
            self.__class__.eventID = event['event']['id']
            self._logger.info(f'*** Found Tennis event with id "{self.eventID}"')
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are not available outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(selection_ids.values())[0]
            self.__class__.marketID = outcomes[0]['outcome']['marketId']
            price_info = outcomes[0]['outcome']['children'][0]['price']
            self.__class__.expected_price = f'{price_info["priceNum"]}/{price_info["priceDen"]}'
        else:
            event = self.ob_config.add_tennis_event_to_autotest_trophy()
            self.__class__.selection_id = event.selection_ids[event.team1]
            self.__class__.expected_price = self.ob_config.event.prices['odds_home']
        surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_id,
                                                      categoryIDs=tennis_category_id,
                                                      content=None,
                                                      priceNum=None,
                                                      priceDen=None)
        self.__class__.surface_bet_id = surface_bet.get('id')
        self.__class__.surface_bet_cms = surface_bet
        self.__class__.surface_bet_title = surface_bet.get('title').upper()

        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state('tennis')

        result = self.wait_for_surface_bets(name=self.surface_bet_title, delimiter='42/34,', timeout=1,
                                            poll_interval=1, raise_exceptions=False)
        if result is None:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.wait_for_surface_bets(name=self.surface_bet_title, delimiter='42/34,', timeout=15, poll_interval=1)

    def test_001_verify_the_single_surface_bet_displaying(self):
        """
        DESCRIPTION: Verify the single Surface Bet displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: * Surface Bet is fit the full width of the screen
        EXPECTED: * Content placeholder is empty
        EXPECTED: * Was price placeholder is empty, "Was" word isn't displayed
        EXPECTED: * Title is aligned as there is no icon placeholder
        """
        surface_bets = self.site.tennis.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertEqual(1, len(surface_bets), msg=f'Only one Surface Bet should be shown not "{len(surface_bets)}"')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')

        self.assertTrue(surface_bet.has_bet_button(), msg=f'Bet Button is not shown for {self.surface_bet_title}')
        actual_price = surface_bet.bet_button.outcome_price_text
        self.assertEqual(actual_price, self.expected_price,
                         msg=f'Actual price on UI "{actual_price}" is not the same as on OB {self.expected_price}')

        self.assertFalse(surface_bet.content, msg='Surface Bet content is not empty')

        self.assertFalse(surface_bet.is_old_price_present(expected_result=False),
                         msg='Placeholder for old price is shown')

        self.assertFalse(surface_bet.header.has_icon(expected_result=False), msg='Icon is shown')

    def test_002_in_the_cms_edit_the_surface_bet_add_content_upload_icon_add_price_both_numerator_and_denominator(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet, add content, upload icon, add price (both numerator and denominator)
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           content=self.content,
                                           priceNum=self.price_num,
                                           priceDen=self.price_den
                                           )

    def test_003_in_the_application_refresh_the_category_homepage_page_verify_the_single_surface_bet_displaying(self):
        """
        DESCRIPTION: In the application: Refresh the category/homepage page
        DESCRIPTION: Verify the single Surface Bet displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Icon, uploaded in the CMS
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: >* Content, defined in the CMS
        EXPECTED: >* Price, defined in the CMS (Coral: price is struck through; Ladbrokes: "Was" and price are struck through)
        EXPECTED: * Surface Bet is fit the full width of the screen
        """
        import time
        time.sleep(60)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.tennis.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertEqual(1, len(surface_bets), msg=f'Only one Surface Bet should be shown not "{len(surface_bets)}"')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
        self.assertTrue(surface_bet.has_bet_button(), msg=f'Bet Button is not shown for {self.surface_bet_title}')
        actual_price = surface_bet.bet_button.outcome_price_text

        self.assertEqual(actual_price, self.expected_price,
                         msg=f'Actual price on UI "{actual_price}" is not the same as on OB {self.expected_price}')
        self.assertEqual(surface_bet.content, self.content,
                         msg=f'Text on UI:\n"{surface_bet.content}"\ndoes not match with text set in CMS:\n"{self.content}"')
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
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           priceNum=None,
                                           priceDen=self.price_den
                                           )
        import time
        time.sleep(60)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.tennis.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertEqual(1, len(surface_bets), msg=f'Only one Surface Bet should be shown not "{len(surface_bets)}"')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
        self.assertFalse(surface_bet.is_old_price_present(expected_result=False),
                         msg='Placeholder for old price is shown')

        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           priceNum=self.price_num,
                                           priceDen=None
                                           )
        import time
        time.sleep(60)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.tennis.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertEqual(1, len(surface_bets), msg=f'Only one Surface Bet should be shown not "{len(surface_bets)}"')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
        self.assertFalse(surface_bet.is_old_price_present(expected_result=False),
                         msg='Placeholder for old price is shown')

    def test_005_verify_the_long_title_is_shortened_properly(self):
        """
        DESCRIPTION: Verify the long title is shortened properly
        EXPECTED: Long title is shortened with ... and fits the Title area
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           title=f'{self.surface_bet_title} {self.fake.name_female()*10}')
        import time
        time.sleep(60)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.tennis.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertEqual(1, len(surface_bets), msg=f'Only one Surface Bet should be shown not "{len(surface_bets)}"')
        surface_bet = next((sf_bet for sf_bet_name, sf_bet in surface_bets.items() if self.surface_bet_title in sf_bet_name), None)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')

        self.assertTrue(surface_bet.header.is_title_truncated(), msg=f'Title for "{self.surface_bet_title}" is not truncated')

    def test_006_verify_content_of_the_max_text_size_128_is_shown_properly(self):
        """
        DESCRIPTION: Verify content of the max text size (128) is shown properly
        EXPECTED: Content is properly wrapped within the Content area
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           title=f'{self.surface_bet_title}',
                                           content=f'{self.fake.paragraph(nb_sentences=10)}')
        import time
        time.sleep(60)  # there's delay between putting values on CMS and appearance on UI
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        surface_bets = self.site.tennis.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertEqual(1, len(surface_bets), msg=f'Only one Surface Bet should be shown not "{len(surface_bets)}"')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
        self.assertFalse(surface_bet.is_content_truncated(),
                         msg=f'Content for "{self.surface_bet_title}" is truncated')
