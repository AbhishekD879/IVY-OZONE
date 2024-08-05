import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod # Cannot grant free ride in prod/beta env
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.races
@pytest.mark.free_ride
@vtest
class Test_C62933318_Verify_display_of_Race_card_page_EDP_on_clicking_on_CTA_to_Race_Card_button(Common):
    """
    TR_ID: C62933318
    NAME: Verify display of Race card page (EDP) on clicking on 'CTA to Race Card' button
    DESCRIPTION: This test case verifies display of Race card page on clicking on 'CTA to Race Card' button
    PRECONDITIONS: 1. Third question with Answers(option1,Option2 and Option3) are configured in CMS (Free Ride-&gt; campaign -&gt; Questions)
    PRECONDITIONS: 2. Login to Ladbrokes application with eligible customers for Free Ride
    PRECONDITIONS: 3. Click on 'Launch Banner' in Homepage
    PRECONDITIONS: 4. Click on CTA Button in Splash Page
    PRECONDITIONS: 5. User should select answers for First, Second and Third questions
    """
    keep_browser_open = True

    def selecting_options(self, question):
        self.assertTrue(question, msg='Question is not displayed yet')
        wait_for_result(lambda: self.site.free_ride_overlay.answers.items_as_ordered_dict is not None,
                        timeout=20, name='Waiting for options to be displayed')
        options = list(self.site.free_ride_overlay.answers.items_as_ordered_dict.values())
        options[0].click()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Third question with Answers(option1,Option2 and Option3) are configured in CMS (Free Ride-&gt; campaign -&gt; Questions)
        PRECONDITIONS: 2. Login to Ladbrokes application with eligible customers for Free Ride
        PRECONDITIONS: 3. Click on 'Launch Banner' in Homepage
        PRECONDITIONS: 4. Click on CTA Button in Splash Page
        PRECONDITIONS: 5. User should select answers for First, Second and Third questions
        """
        username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=username)
        self.update_spotlight_events_price(class_id=223)
        campaign_id = self.cms_config.check_update_and_create_freeride_campaign()
        self.__class__.response = self.cms_config.get_freeride_campaign_details(freeride_campaignid=campaign_id)
        self.site.login(username=username)
        self.site.home.free_ride_banner().click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE, timeout=10, verify_name=False)
        dialog.cta_button.click()
        first_question = wait_for_result(lambda: self.site.free_ride_overlay.first_question is not None,
                                         timeout=10, name='Waiting for First Question to be displayed')
        self.selecting_options(question=first_question)
        second_question = wait_for_result(lambda: self.site.free_ride_overlay.second_question is not None,
                                          timeout=10, name='Waiting for Second Question to be displayed')
        self.selecting_options(question=second_question)
        third_question = wait_for_result(lambda: self.site.free_ride_overlay.third_question is not None,
                                         timeout=10, name='Waiting for First Question to be displayed')
        self.selecting_options(question=third_question)

    def test_001_verify_display_of_automated_betslip(self):
        """
        DESCRIPTION: Verify display of automated betslip
        EXPECTED: Automated betslip should be successfully generated in Free Ride Overlay
        """
        automated_betslip = self.site.free_ride_overlay.results_container.split('\n')
        self.assertTrue(automated_betslip, msg="Automated betslip is not generated")
        self.assertTrue(automated_betslip[0], msg="Message is not shown on the automated betslip")
        self.assertTrue(automated_betslip[1], msg="Horse name is not shown on the automated betslip")
        self.assertTrue(automated_betslip[2], msg="Jockey name is not shown on the automated betslip")
        self.assertTrue(automated_betslip[3],
                        msg="Event time and Meeting place name is not shown on the automated betslip")
        jockey_logo = self.site.free_ride_overlay.jockey_logo
        self.assertTrue(jockey_logo.is_displayed(), msg="Jockey Logo is not displayed on automated betlsip")
        CTA_to_racecard = self.site.free_ride_overlay.CTA_button
        self.assertTrue(CTA_to_racecard.is_displayed(), msg="CTA TO RACECARD is not displayed")

    def test_002_verify_the_fields_inautomated_betslip(self):
        """
        DESCRIPTION: Verify the fields in automated betslip
        EXPECTED: Below information should be displayed:
        EXPECTED: * That’s it! We made something for you:
        EXPECTED: * Name of the Horse:
        EXPECTED: * Name of the Jockey
        EXPECTED: * Event Time, Meeting place name
        EXPECTED: * Jockey(kits and crests) logo below to summary details
        EXPECTED: * "CTA TO RACECARD" button should be displayed
        """
        # Covered in step test_002

    def test_003_click_on_cta_to_racecard_button(self):
        """
        DESCRIPTION: Click on 'CTA TO RACECARD' button
        EXPECTED: * User should be navigated to race card page of the allocated horse (EDP)
        EXPECTED: * User should be able to see the ongoing journey(s) in the race card page
        """
        cta_button = wait_for_result(lambda: self.site.free_ride_overlay.CTA_button, timeout=10,
                                     name='"Go Racing" button to be displayed')
        cta_button.click()
        self.site.wait_content_state(state_name='RacingEventDetails')
