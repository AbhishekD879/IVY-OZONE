import pytest
from faker import Faker
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot modify cms / create modules on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.mobile_only
@vtest
class Test_C9607551_Verify_disabled_Surface_Bets_displaying(Common):
    """
    TR_ID: C9607551
    NAME: Verify disabled Surface Bets displaying
    DESCRIPTION: Test cases verifies that disabled Surface Bets are not shown
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Open this category page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)

    def surface_bets(self):
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.__class__.ui_surface_bet = surface_bets.get(self.surface_bet_title_2)

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: 1. There are a few valid Surface Bets added to the SLP/Homepage in the CMS
        PRECONDITIONS: 2. Open this category page in the application
        """
        category_id = self.ob_config.football_config.category_id
        cms_surface_bet = self.cms_config.get_sport_module(sport_id=category_id,
                                                           module_type='SURFACE_BET')[0]
        if cms_surface_bet['disabled']:
            self.cms_config.change_sport_module_state(sport_module=cms_surface_bet)

        event = self.ob_config.add_autotest_premier_league_football_event()
        selection_id = event.selection_ids[event.team1]
        selection_id_2 = event.selection_ids[event.team2]
        eventID = event.event_id

        self.cms_config.add_surface_bet(selection_id=selection_id,
                                                        categoryIDs=category_id,
                                                        content=self.content,
                                                        eventIDs=eventID,
                                                        edpOn=True,
                                                        priceNum=self.price_num,
                                                        priceDen=self.price_den
                                                        )

        surface_bet_2 = self.cms_config.add_surface_bet(selection_id=selection_id_2,
                                                        categoryIDs=category_id,
                                                        content=self.content,
                                                        eventIDs=eventID,
                                                        edpOn=True,
                                                        priceNum=self.price_num,
                                                        priceDen=self.price_den)
        self.__class__.surface_bet_title_2 = surface_bet_2.get('title').upper()
        self.__class__.surface_bet_id = surface_bet_2.get('id')

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football', timeout=60)

        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')

    def test_001_in_cms_disable_one_of_the_surface_bets_and_save_changes(self):
        """
        DESCRIPTION: In CMS disable one of the Surface Bets and save changes.
        EXPECTED:
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id, disabled=True)

    def test_002_in_application_refresh_the_pageverify_disabled_surface_bet_isnt_shown_within_the_carousel(self):
        """
        DESCRIPTION: In application refresh the page.
        DESCRIPTION: Verify disabled Surface Bet isn't shown within the carousel.
        EXPECTED: Disabled Surface bet isn't shown
        """
        # changes for surface bets is taking sometime to reflect
        sleep(30)
        self.device.refresh_page()
        self.surface_bets()
        self.assertFalse(self.ui_surface_bet,
                         msg=f'Disabled surface bet "{self.surface_bet_title_2}" is appearing on UI')

    def test_003_in_cms_enable_previously_disabled_surface_bets(self):
        """
        DESCRIPTION: In CMS enable previously disabled Surface Bets.
        EXPECTED:
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id, disabled=False)

    def test_004_in_application_refresh_the_pageverify_reenabled_surface_bet_is_shown_within_the_carousel(self):
        """
        DESCRIPTION: In application refresh the page.
        DESCRIPTION: Verify reenabled Surface Bet is shown within the carousel.
        EXPECTED: Surface bet is now shown
        """
        # changes for surface bets is taking sometime to reflect
        sleep(30)
        self.device.refresh_page()
        self.site.wait_splash_to_hide(timeout=30)
        self.surface_bets()
        self.assertTrue(self.ui_surface_bet, msg=f'Surface bet "{self.surface_bet_title_2}" is not displaying')
