import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C17796016_To_Edit__add_Ladbrokes_prod_URLs_Verify_IGM_streaming_URL_on_Virtuals(Common):
    """
    TR_ID: C17796016
    NAME: [To Edit - add Ladbrokes prod URLs] Verify IGM streaming URL on Virtuals
    DESCRIPTION: This test case verifies IGM streaming URL on Virtuals
    PRECONDITIONS: Virtual events for all sports are available:
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: 'virtual-horse-racing':'horsesflat',
    PRECONDITIONS: 'virtual-football':'football',
    PRECONDITIONS: 'virtual-greyhounds':'dogs',
    PRECONDITIONS: 'virtual-boxing':'boxing',
    PRECONDITIONS: 'virtual-darts':'darts',
    PRECONDITIONS: 'virtual-tennis':'tennis',
    PRECONDITIONS: 'virtual-cycling':'cycling',
    PRECONDITIONS: 'virtual-speedway':'speedway',
    PRECONDITIONS: 'virtual-motorsports':'cars',
    PRECONDITIONS: 'virtual-grand-national':'grandnational'
    PRECONDITIONS: "virtual-basketball":"basketball",
    PRECONDITIONS: "virtual-jumps-horse-racing":"horsesjumps"
    PRECONDITIONS: Coral:
    PRECONDITIONS: "virtual-horse-racing":"horses",
    PRECONDITIONS: "virtual-football":"test1",
    PRECONDITIONS: "virtual-greyhounds":"dogs",
    PRECONDITIONS: "virtual-boxing":"boxing",
    PRECONDITIONS: "virtual-darts":"darts",
    PRECONDITIONS: "virtual-tennis":"tennis",
    PRECONDITIONS: "virtual-cycling":"cycling",
    PRECONDITIONS: "virtual-speedway":"speedway",
    PRECONDITIONS: "virtual-motorsports":"cars",
    PRECONDITIONS: "virtual-grand-national":"grandnational",
    PRECONDITIONS: "virtual-basketball":"basketball",
    PRECONDITIONS: "virtual-jumps-horse-racing":"horsesjumps"
    PRECONDITIONS: For check URL see screen:
    PRECONDITIONS: ![](index.php?/attachments/get/35740)
    """
    keep_browser_open = True

    def test_001_load_appnavigate_to_virtuals_page(self):
        """
        DESCRIPTION: Load app
        DESCRIPTION: Navigate to Virtuals page
        EXPECTED: 
        """
        pass

    def test_002_select_virtual_horse_racinginspect_media_player_in_devtoolselementsverify_iframe_url_for_player(self):
        """
        DESCRIPTION: Select 'Virtual Horse Racing'
        DESCRIPTION: Inspect media player in DevTools>Elements
        DESCRIPTION: Verify iframe URL for player
        EXPECTED: **Coral:**
        EXPECTED: <iframe allowfullscreen="" class="vs-video-stream" src="https://player.igamemedia.com/vplayer?c=83127&s=horses&q=mobhi"
        EXPECTED: Note:
        EXPECTED: 'q=web' for Desktop
        EXPECTED: 'q=mobhi' for Tablet
        EXPECTED: 'q=moblo' for Mobile
        EXPECTED: **Ladbrokes:**
        EXPECTED: <iframe allowfullscreen="" class="vs-video-stream" src="https://player-test.igamemedia.com/vplayer?c=30473&s=horsesflat&q=adpt"
        EXPECTED: Note:
        EXPECTED: 'q=adpt' for all: Mobile, Tablet, Desktop
        """
        pass

    def test_003_select_virtual_footballinspect_media_player_in_devtoolselementsverify_iframe_url_for_player(self):
        """
        DESCRIPTION: Select ''virtual-football'
        DESCRIPTION: Inspect media player in DevTools>Elements
        DESCRIPTION: Verify iframe URL for player
        EXPECTED: **Coral:**
        EXPECTED: <iframe allowfullscreen="" class="vs-video-stream" src="https://player.igamemedia.com/vplayer?c=83127&s=test1&q=mobhi"
        EXPECTED: Note:
        EXPECTED: 'q=web' for Desktop
        EXPECTED: 'q=mobhi' for Tablet
        EXPECTED: **Ladbrokes:**
        EXPECTED: <iframe allowfullscreen="" class="vs-video-stream" src="https://player-test.igamemedia.com/vplayer?c=30473&s=football&q=adpt"
        EXPECTED: Note:
        EXPECTED: 'q=adpt' for all: Mobile, Tablet, Desktop
        """
        pass

    def test_004_select_virtual_greyhoundsinspect_media_player_in_devtoolselementsverify_iframe_url_for_player(self):
        """
        DESCRIPTION: Select 'virtual-greyhounds'
        DESCRIPTION: Inspect media player in DevTools>Elements
        DESCRIPTION: Verify iframe URL for player
        EXPECTED: **Coral:**
        EXPECTED: <iframe allowfullscreen="" class="vs-video-stream" src="https://player.igamemedia.com/vplayer?c=83127&s=dogs&q=mobhi"
        EXPECTED: Note:
        EXPECTED: 'q=web' for Desktop
        EXPECTED: 'q=mobhi' for Tablet
        EXPECTED: 'q=moblo' for Mobile
        EXPECTED: **Ladbrokes:**
        EXPECTED: <iframe allowfullscreen="" class="vs-video-stream" src="https://player-test.igamemedia.com/vplayer?c=30473&s=dogs&q=adpt"
        EXPECTED: Note:
        EXPECTED: 'q=adpt' for all: Mobile, Tablet, Desktop
        """
        pass

    def test_005_check_other_virtual_sportsverify_that_sappropriate_sportvirtual_boxingboxingvirtual_dartsdartsvirtual_tennistennisvirtual_cyclingcyclingvirtual_speedwayspeedwayvirtual_motorsportscarsvirtual_grand_nationalgrandnationalvirtual_basketballbasketballvirtual_jumps_horse_racinghorsesjumps(self):
        """
        DESCRIPTION: Check other virtual sports:
        DESCRIPTION: Verify that s=appropriate sport:
        DESCRIPTION: "virtual-boxing":"boxing"
        DESCRIPTION: 'virtual-darts':'darts',
        DESCRIPTION: 'virtual-tennis':'tennis',
        DESCRIPTION: 'virtual-cycling':'cycling',
        DESCRIPTION: 'virtual-speedway':'speedway',
        DESCRIPTION: 'virtual-motorsports':'cars',
        DESCRIPTION: 'virtual-grand-national':'grandnational'
        DESCRIPTION: "virtual-basketball":"basketball",
        DESCRIPTION: "virtual-jumps-horse-racing":"horsesjumps"
        EXPECTED: Results are the same and appropriate sport is shown.
        EXPECTED: **Coral:**
        EXPECTED: <iframe allowfullscreen="" class="vs-video-stream" src="https://player.igamemedia.com/vplayer?c=83127&s=**sport**&q=mobhi"
        EXPECTED: Note:
        EXPECTED: 'q=web' for Desktop
        EXPECTED: 'q=mobhi' for Tablet
        EXPECTED: 'q=moblo' for Mobile
        EXPECTED: **Ladbrokes:**
        EXPECTED: <iframe allowfullscreen="" class="vs-video-stream" src="https://player-test.igamemedia.com/vplayer?c=30473&s=**sport**&q=adpt"
        EXPECTED: Note:
        EXPECTED: 'q=adpt' for all: Mobile, Tablet, Desktop
        """
        pass
