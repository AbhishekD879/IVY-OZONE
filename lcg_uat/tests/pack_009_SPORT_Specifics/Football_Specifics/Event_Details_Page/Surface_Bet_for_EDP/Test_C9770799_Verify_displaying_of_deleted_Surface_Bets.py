from time import sleep
import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from faker import Faker


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events cannot be created/suspend on prod & beta
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.homepage_featured
@vtest
class Test_C9770799_Verify_displaying_of_deleted_Surface_Bets(BaseFeaturedTest, BaseBetSlipTest):
    """
    TR_ID: C9770799
    NAME: Verify displaying of deleted Surface Bets
    DESCRIPTION: Test case verifies that deleted Surface Bet isn't shown
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
    PRECONDITIONS: 2. Open this EDP
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)

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
        self.__class__.marketID = event.default_market_id

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
        self.navigate_to_edp(self.eventID, timeout=15)
        self.assertTrue(self.site.sport_event_details.tab_content.has_surface_bets(),
                        msg=f'Surface Bet module is not shown on the EDP with event_id: "{self.eventID}"')

    def test_001_delete_the_surface_bet_from_the_cms(self):
        """
        DESCRIPTION: Delete the Surface Bet from the CMS
        """
        self.cms_config.delete_surface_bet(surface_bet_id=self.surface_bet_id)
        # Updating the surface bet list, since one bet-id is removed above
        self.cms_config._created_surface_bets.remove(self.surface_bet_id)

        # Post delete of surface bet, taking sometime for reflection on UI, hence sleep is used.
        sleep(30)
        self.device.refresh_page()
        self.navigate_to_edp(self.eventID, timeout=40)
        self.site.wait_splash_to_hide(5)
        self.site.wait_content_state(state_name='EventDetails', timeout=60)
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        ui_surface_bet = surface_bets.get(self.surface_bet_title_2)
        self.assertFalse(ui_surface_bet,
                         msg=f'Disabled surface bet "{self.surface_bet_title_2}" is appearing on UI')

    def test_002_in_the_application_refresh_the_edpverify_the_surface_bet_is_deleted(self):
        """
        DESCRIPTION: In the application refresh the EDP
        DESCRIPTION: Verify the Surface bet is deleted
        EXPECTED: Deleted Surface Bet isn't shown on the page
        """
        # Covered in step-1
