import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C57732108_Verify_game_transition_from_Current_to_Previous(Common):
    """
    TR_ID: C57732108
    NAME: Verify game transition from Current to Previous
    DESCRIPTION: This test case verifies data retrieving from CMS to 'Current Tab'
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: for Qubit version (deprecated) https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: for Oxygen version: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. User expands '1-2-Free' section in the left menu
    PRECONDITIONS: 3. User opens 'Game view'
    PRECONDITIONS: 4. User open Detail View for existing game
    """
    keep_browser_open = True

    def test_001_configure_current_game_with__future_events_start_time_eg_today_1400_pm__display_to_date_eg_today_1600_pmsave_changes(self):
        """
        DESCRIPTION: Configure Current game with:
        DESCRIPTION: - future events start time (eg. Today, 14:00 PM)
        DESCRIPTION: - Display To Date (eg. Today, 16:00 PM)
        DESCRIPTION: Save changes
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_002_open_1_2_free_ui_and_make_predictions(self):
        """
        DESCRIPTION: Open 1-2-Free UI and make predictions
        EXPECTED: - All data retrieved from CMS and Current game displayed
        EXPECTED: - Predictions made
        """
        pass

    def test_003_wait_until_current_game_endsopen_1_2_free_ui_again(self):
        """
        DESCRIPTION: Wait until current game ends
        DESCRIPTION: Open 1-2-Free UI again
        EXPECTED: - All data retrieved from CMS and Previous game displayed
        """
        pass
