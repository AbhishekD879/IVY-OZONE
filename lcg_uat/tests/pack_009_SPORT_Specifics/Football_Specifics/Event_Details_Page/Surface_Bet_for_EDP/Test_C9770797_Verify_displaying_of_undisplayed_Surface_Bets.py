import pytest
from time import sleep
from faker import Faker
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events cannot be created on prod & beta
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.homepage_featured
@vtest
class Test_C9770797_Verify_displaying_of_undisplayed_Surface_Bets(BaseFeaturedTest, BaseBetSlipTest):
    """
    TR_ID: C9770797
    NAME: Verify displaying of "undisplayed" Surface Bets
    DESCRIPTION: Test case verifies that undisplayed Surface Bet isn't shown
    DESCRIPTION: This test case needs to be reviewed. It can be a duplicate of https://ladbrokescoral.testrail.com/index.php?/cases/view/9770795
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
    PRECONDITIONS: 2. Open this EDP
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)

    def surface_bets(self):
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.__class__.ui_surface_bet = surface_bets.get(self.surface_bet_title_2)

    def test_000_pre_conditions(self):
        """
           PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
           PRECONDITIONS: 2. Open this EDP
           PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
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

    def test_001_in_cms_disable_one_of_the_surface_bets_and_save_changes(self):
        """
        DESCRIPTION: In CMS disable one of the Surface Bets and save changes.
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id, disabled=True)
        # changes for surface bets is taking sometime to reflect
        sleep(30)
        self.device.refresh_page()
        self.navigate_to_edp(self.eventID, timeout=30)
        self.surface_bets()
        self.assertFalse(self.ui_surface_bet,
                         msg=f'Disabled surface bet "{self.surface_bet_title_2}" is appearing on UI')

    def test_002_in_application_refresh_the_pageverify_disabled_surface_bet_isnt_shown_within_the_carousel(self):
        """
        DESCRIPTION: In application refresh the page.
        DESCRIPTION: Verify disabled Surface Bet isn't shown within the carousel.
        EXPECTED: Disabled Surface bet isn't shown
        """
        # Covered in step-1

    def test_003_in_cms_enable_previously_disabled_surface_bets(self):
        """
        DESCRIPTION: In CMS enable previously disabled Surface Bets.
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id, disabled=False)
        # changes for surface bets is taking sometime to reflect
        sleep(30)
        self.device.refresh_page()
        self.navigate_to_edp(self.eventID, timeout=30)
        self.surface_bets()
        self.assertTrue(self.ui_surface_bet, msg=f'Surface bet "{self.surface_bet_title_2}" is not displaying')

    def test_004_in_application_refresh_the_pageverify_reenabled_surface_bet_is_shown_within_the_carousel(self):
        """
        DESCRIPTION: In application refresh the page.
        DESCRIPTION: Verify reenabled Surface Bet is shown within the carousel.
        EXPECTED: Surface bet is now shown
        """
        # Covered in step-3
