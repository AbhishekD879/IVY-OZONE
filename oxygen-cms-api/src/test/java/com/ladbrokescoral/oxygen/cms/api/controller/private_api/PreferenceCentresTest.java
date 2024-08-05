package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.PreferenceCentresRepository;
import com.ladbrokescoral.oxygen.cms.api.service.PreferenceCentresService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.annotation.CreatedBy;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      PreferenceCentres.class,
      PreferenceCentresRepository.class,
      PreferenceCentresService.class,
      UserService.class,
      User.class,
      CreatedBy.class,
      Util.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class PreferenceCentresTest extends AbstractControllerTest {

  private PreferenceCentre preferenceCentre;

  @MockBean PreferenceCentresRepository preferenceCentresRepository;
  @Autowired PreferenceCentresService preferenceCentresService;

  @Before
  public void init() {
    preferenceCentre = createPreferenceCentre();

    given(preferenceCentresRepository.save(any(PreferenceCentre.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(preferenceCentresRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .willReturn(Optional.of(preferenceCentre));
    given(preferenceCentresRepository.findByBrand(anyString()))
        .willReturn(Arrays.asList(preferenceCentre));
  }

  @Test
  public void testToCreatePreferenceCentre() throws Exception {
    PreferenceCentre preferenceCentre = createPreferenceCentre();
    given(preferenceCentresRepository.findByBrand(anyString())).willReturn(Arrays.asList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-preference-center")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(preferenceCentre)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToCreatePreferenceCentreException() throws Exception {
    PreferenceCentre preferenceCentre = createPreferenceCentre();
    given(preferenceCentresRepository.findByBrand(anyString()))
        .willReturn(Arrays.asList(preferenceCentre));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-preference-center")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(preferenceCentre)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToDeleteAllPreferenceCentre() throws Exception {
    given(preferenceCentresRepository.findAllPreferencesByBrand(anyString()))
        .willReturn(Optional.of(preferenceCentre));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/ladbrokes/fanzone-preference-center")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadPreferenceCentre() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/fanzone-preference-center")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdatePreferenceCentreById() throws Exception {
    given(preferenceCentresRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .willReturn(Optional.of(preferenceCentre));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone-preference-center/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(preferenceCentre)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToUpdatePreferenceCentreById1() throws Exception {
    PreferenceCentre preferenceCentre = createPreferenceCentre();
    preferenceCentre.setId("123");
    given(preferenceCentresRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .willReturn(Optional.of(preferenceCentre));
    given(preferenceCentresService.findOne(anyString())).willReturn(Optional.of(preferenceCentre));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone-preference-center/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(preferenceCentre)))
        .andExpect(status().is2xxSuccessful());
  }

  private static PreferenceCentre createPreferenceCentre() {
    PreferenceCentre entity = new PreferenceCentre();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setPageName("fanzoneSyc");
    entity.setPcDescription("Labore et dolore magna aliqua. Ut enim ad minim veniam");
    entity.setCtaText("SUBMIT");
    entity.setSubscribeText("SUBSCRIBE");
    entity.setConfirmText("Do you confirm to save the preferences?");
    entity.setConfirmCTA("CONFIRM");
    entity.setExitCTA("EXIT");
    entity.setNotificationDescriptionDesktop(
        " Don’t miss a thing! Go to the Ladbrokes app and set your push notification preferences to receive team news, in-play match updates and more. These are for the app platform only; they are not sent on desktop or mobile web platforms.");
    entity.setUnsubscribeDescription(
        "Are you sure you want to unsubscribe? By pressing CONFIRM you will lose access to FANZONE. If you signed up less than 30 days ago you will need to wait until the 30 days expire to re-subscribe.");
    entity.setNotificationPopupTitle("TEAM ALERTS");
    entity.setUnsubscribeTitle("UNSUBSCRIBE FROM FANZONE");
    entity.setOptInCTA("'OPT IN'");
    entity.setNoThanksCTA("'NO THANKS'");
    entity.setActive(true);
    entity.setPushPreferenceCentreTitle("PUSH PREFERENCE CENTRE");
    entity.setGenericTeamNotificationTitle("Title");
    entity.setGenericTeamNotificationDescription("Description");
    List<Map<String, String>> pcKeysList = new ArrayList<Map<String, String>>();
    Map<String, String> pcKey1 = new HashMap<String, String>();
    pcKey1.put("name", "ALL");
    pcKey1.put("key", "ALL");
    Map<String, String> pcKey2 = new HashMap<String, String>();
    pcKey2.put("name", "Team News");
    pcKey2.put("key", "TEAM_NEWS");
    Map<String, String> pcKey3 = new HashMap<String, String>();
    pcKey3.put("name", "In-Play");
    pcKey3.put("key", "IN_PLAY");
    pcKeysList.add(pcKey1);
    pcKeysList.add(pcKey2);
    pcKeysList.add(pcKey3);
    entity.setPcKeys(pcKeysList);
    return entity;
  }
}
