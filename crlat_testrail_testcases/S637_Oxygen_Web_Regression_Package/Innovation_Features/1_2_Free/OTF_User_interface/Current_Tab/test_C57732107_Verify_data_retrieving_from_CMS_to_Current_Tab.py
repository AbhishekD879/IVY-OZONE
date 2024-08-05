import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732107_Verify_data_retrieving_from_CMS_to_Current_Tab(Common):
    """
    TR_ID: C57732107
    NAME: Verify data retrieving from CMS to 'Current Tab'
    DESCRIPTION: This test case verifies data retrieving from CMS to 'Current Tab'
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. User expands '1-2-Free' section in the left menu
    PRECONDITIONS: 3. User opens 'Game view'
    PRECONDITIONS: 4. User open Detail View for existing game
    """
    keep_browser_open = True

    def test_001_populate_all_existing_fields_with_valid_data_and_save_it_in_game_detail_view_and__in_cms(self):
        """
        DESCRIPTION: Populate all existing fields with valid data and save it in Game Detail View and  in CMS
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_002_open_current_tab_on_1_2_free_uisee_howplustoplusrunplusunpublishedplusqubitplusvariationplusonplusladbrokes_documentation_in_preconditions(self):
        """
        DESCRIPTION: Open 'Current Tab' on 1-2-Free UI
        DESCRIPTION: (see How+to+run+unpublished+Qubit+variation+on+Ladbrokes documentation in preconditions)
        EXPECTED: All data retrieved from CMS and displayed
        EXPECTED: - Close button
        EXPECTED: - Expanded/Collapsed text from CMS (Static text-&gt; Current page-&gt; pageText1)
        EXPECTED: - 'Deadline missed' messages (Static text-&gt; Current page-&gt; pageText3)
        EXPECTED: - 'Already Played' messages (Static text-&gt; Current page-&gt; pageText4)
        EXPECTED: - Submit (Static text-&gt; Current page-&gt; ctaText1)
        EXPECTED: - Events(CMS-&gt;Active game):
        EXPECTED: - Event number: *e.g. Match 1*
        EXPECTED: - Date of event: *e.g. 15:00 MON*
        EXPECTED: - Team name *Liverpool*
        EXPECTED: - Team kits
        EXPECTED: - Event TV icon *BBC*
        EXPECTED: All data successfully styled
        """
        pass
