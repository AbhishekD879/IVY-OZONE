import pytest
from time import sleep
from faker import Faker
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot modify cms / create modules on prod
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.desktop
@vtest
class Test_C9700971_Verify_Surface_Bet_module_enabling_disabling_for_the_Sport_category(BaseFeaturedTest):
    """
    TR_ID: C9700971
    NAME: Verify Surface Bet module enabling/disabling for the Sport category
    DESCRIPTION: Test case verifies possibility to enable or disable the Surface Bet module on the home page or sport category page
    PRECONDITIONS: 1. There is at least one Surface Bet added to the SLP/Homepage in CMS.
    PRECONDITIONS: 2. Open this SLP/Homepage in Oxygen application.
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)

    def surface_bets(self):
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.__class__.ui_surface_bet = surface_bets.get(self.surface_bet_title_2)

    def test_000_preconditions(self):
        """
        DESCRIPTION: There are a few valid Surface Bets added to the Greyhound and Horse racing categories in the CMS
        """
        self.__class__.category_id = self.ob_config.football_config.category_id
        cms_surface_bet = self.cms_config.get_sport_module(sport_id=self.category_id,
                                                           module_type='SURFACE_BET')[0]
        if cms_surface_bet['disabled']:
            self.cms_config.change_sport_module_state(sport_module=cms_surface_bet)

        event = self.ob_config.add_autotest_premier_league_football_event()
        selection_id = event.selection_ids[event.team1]
        self.__class__.selection_id_2 = event.selection_ids[event.team2]
        self.__class__.eventID = event.event_id

        surface_bet_1 = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                        categoryIDs=self.category_id,
                                                        content=self.content,
                                                        eventIDs=self.eventID,
                                                        edpOn=True,
                                                        priceNum=self.price_num,
                                                        priceDen=self.price_den
                                                        )
        self.__class__.surface_bet_title_1 = surface_bet_1.get('title').upper()

        surface_bet_2 = self.cms_config.add_surface_bet(selection_id=self.selection_id_2,
                                                        categoryIDs=self.category_id,
                                                        content=self.content,
                                                        eventIDs=self.eventID,
                                                        edpOn=True,
                                                        priceNum=self.price_num,
                                                        priceDen=self.price_den)
        self.__class__.surface_bet_title_2 = surface_bet_2.get('title').upper()
        self.__class__.surface_bet_id = surface_bet_2.get('id')

        self.navigate_to_edp(self.eventID, timeout=30)
        self.assertTrue(self.site.sport_event_details.tab_content.has_surface_bets(),
                        msg=f'Surface Bet module is not shown on the EDP with event_id: "{self.eventID}"')

    def test_001_in_the_cms_make_a_module_for_the_homepageslp_not_activein_the_application_refresh_the_homepageslp_verify_the_surface_bet_module_isnt_displayed(self):
        """
        DESCRIPTION: In the CMS make a module for the homepage/SLP not active
        DESCRIPTION: In the application refresh the homepage/SLP. Verify the Surface Bet module isn't displayed
        EXPECTED: Surface Bet module isn't shown
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id, disabled=True)
        # changes for surface bets is taking sometime to reflect
        sleep(30)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.navigate_to_edp(self.eventID, timeout=30)
        self.site.wait_splash_to_hide()
        self.surface_bets()
        self.assertFalse(self.ui_surface_bet,
                         msg=f'Disabled surface bet "{self.surface_bet_title_2}" is appearing on UI')

    def test_002_in_the_cms_make_a_module_for_the_homepageslp_activein_the_application_refresh_the_homepageslp_verify_the_surface_bet_module_is_displayed(self):
        """
        DESCRIPTION: In the CMS make a module for the homepage/SLP active
        DESCRIPTION: In the application refresh the homepage/SLP. Verify the Surface Bet module is displayed
        EXPECTED: Surface Bet module is shown
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id, disabled=False)
        # changes for surface bets is taking sometime to reflect
        sleep(30)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.navigate_to_edp(self.eventID, timeout=30)
        self.site.wait_splash_to_hide()
        self.surface_bets()
        self.assertTrue(self.ui_surface_bet, msg=f'Surface bet "{self.surface_bet_title_2}" is not displaying')
