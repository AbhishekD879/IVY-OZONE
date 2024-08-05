import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C59489930_Verify_Generic_silk_display_in_absence_of_bespoke(Common):
    """
    TR_ID: C59489930
    NAME: Verify Generic silk display in absence of bespoke
    DESCRIPTION: This test case verifies display of Generic silk in horse racing EDP for all horses of all races(UK& IRE and International) when bespoke silk is not provided
    PRECONDITIONS: 1.Bespoke silk should not be present for any one of horse in HR EDP
    """
    keep_browser_open = True

    def test_001_login_to_the_application_and_navigate_to_horse_racing_from_header_sub_menuin_mobile_from_sports_ribbonor_in_play___horse_racing(self):
        """
        DESCRIPTION: Login to the application and navigate to horse racing from header sub menu(In mobile from sports ribbon)
        DESCRIPTION: or In play - Horse racing
        EXPECTED: Horse racing landing page - meetings tab should display
        EXPECTED: if user is navigate from in play tab in play horse racing events should display
        """
        pass

    def test_002_click_on_any_event_from_uk_and_ire_for_which_bespoke_silk_is_not_provided_at_least_for_one_horse(self):
        """
        DESCRIPTION: Click on any event from UK and IRE for which bespoke silk is not provided at least for one horse
        EXPECTED: All the horse in EDP should have bespoke silk
        EXPECTED: for the horse which don't have bespoke silk should display generic silk
        """
        pass

    def test_003_to_confirm_above_step_right_click_on_any_bespoke_silk_and_inspect_and_change_image_id_with_dummy_id_and_see_in_febackground_image_urlhttpsaggregationladbrokescomsilksracingpostxxxx(self):
        """
        DESCRIPTION: To confirm above step right click on any bespoke silk and inspect and change image id with dummy id and see in FE
        DESCRIPTION: background-image: url("https://aggregation.ladbrokes.com/silks/racingpost/xxxx
        EXPECTED: In FE generic silk should be displayed
        """
        pass

    def test_004_repeat_above_step_from_below_racesmeeting_tab___race_from_usameeting_tab___race_from_francemeeting_tab___race_from_australiameeting_tab___race_from_international_racesmeeting_tab___race_from_international_tote_carasoulmeeting_tab___race_from_virtual_race_carasoulmeeting_tab___race_from_extra_place_offersmeeting_tab___race_from_ladbrokes_legendsfuture_tab___race_from_flat_tabfuture_tab___race_from_international_tabfuture_tab___race_from_national_hunts_tabany_race_from_next_races_tabany_race_from_special_races_tabinplay_races(self):
        """
        DESCRIPTION: Repeat above step from below races
        DESCRIPTION: Meeting tab - race from USA
        DESCRIPTION: Meeting tab - race from FRANCE
        DESCRIPTION: Meeting tab - race from AUSTRALIA
        DESCRIPTION: Meeting tab - race from International races
        DESCRIPTION: Meeting tab - race from international tote carasoul
        DESCRIPTION: Meeting tab - race from Virtual race carasoul
        DESCRIPTION: Meeting tab - race from extra place offers
        DESCRIPTION: Meeting tab - race from Ladbrokes legends
        DESCRIPTION: Future tab - race from flat tab
        DESCRIPTION: Future tab - race from International tab
        DESCRIPTION: Future tab - race from National hunts tab
        DESCRIPTION: Any race from next races tab
        DESCRIPTION: Any race from Special races tab
        DESCRIPTION: Inplay races
        EXPECTED: 
        """
        pass

    def test_005_verify_generic_silk_in_differnt_markets(self):
        """
        DESCRIPTION: Verify Generic silk in differnt markets
        EXPECTED: All applicable markets should display generic silk
        """
        pass
