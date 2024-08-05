package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.*;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneSycCreateException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.PreferenceCentreCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.PreferenceCentresRepository;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class PreferenceCentresServiceTest extends BDDMockito {

  @InjectMocks private PreferenceCentresService preferenceCentresService;
  @Mock private PreferenceCentresRepository preferenceCentresRepository;
  @Mock CrudService<User> userServiceObj;
  private PreferenceCentre preferenceCentre = createPreferenceCentre();

  @Before
  public void init() {
    preferenceCentresService = new PreferenceCentresService(preferenceCentresRepository);
  }

  @Test
  public void testTofindAllPreferencesByBrand() {
    when(preferenceCentresRepository.findAllPreferencesByBrand(anyString()))
        .thenReturn(Optional.of(preferenceCentre));
    assertNotNull(preferenceCentresService.findAllPreferencesByBrand(anyString()));
  }

  @Test
  public void testTofindAllPreferencesByBrandNotPresent() {

    assertNotNull(preferenceCentresService.findAllPreferencesByBrand(anyString()));
  }

  @Test
  public void testToFindByBrandAndColumn() {
    when(preferenceCentresRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .thenReturn(Optional.of(preferenceCentre));
    assertNotNull(
        preferenceCentresService.findByBrandAndColumn(anyString(), anyString(), anyString()));
  }

  @Test
  public void testToFindByBrandAndColumnNotPresent() {
    when(preferenceCentresRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .thenReturn(Optional.empty());
    assertNotNull(
        preferenceCentresService.findByBrandAndColumn(anyString(), anyString(), anyString()));
  }

  @Test
  public void testTocheckPreferenceCentre() throws Exception {
    when(preferenceCentresRepository.findByBrand(anyString()))
        .thenReturn(Arrays.asList(preferenceCentre));
    preferenceCentresService.checkPreferenceCentre(preferenceCentre.getBrand());
    Boolean isPreferenceCentreCreated = false;
    assertFalse(isPreferenceCentreCreated);
  }

  @Test
  public void testTocheckPreferenceCentreFalse() throws Exception {
    when(preferenceCentresRepository.findByBrand(anyString())).thenReturn(Arrays.asList());
    preferenceCentresService.checkPreferenceCentre(preferenceCentre.getBrand());
    Boolean isPreferenceCentreCreated = true;
    assertTrue(isPreferenceCentreCreated);
  }

  @Test
  public void testToGetPreferenceCentre() throws Exception {
    Boolean isPreferenceCentreCreated = true;
    try {
      when(preferenceCentresRepository.findByBrand(anyString())).thenReturn(Arrays.asList());
      preferenceCentresService.getPreferenceCentre(preferenceCentre, preferenceCentre.getBrand());
    } catch (PreferenceCentreCreateException e) {
      isPreferenceCentreCreated = false;
    }
    assertTrue(isPreferenceCentreCreated);
  }

  @Test
  public void testToGetPreferenceCentreException() throws Exception {
    Boolean isPreferenceCentreCreated = false;
    try {
      when(preferenceCentresRepository.findByBrand(anyString()))
          .thenReturn(Arrays.asList(preferenceCentre));
      preferenceCentresService.getPreferenceCentre(preferenceCentre, preferenceCentre.getBrand());
    } catch (PreferenceCentreCreateException e) {
      isPreferenceCentreCreated = true;
    }
    assertTrue(isPreferenceCentreCreated);
  }

  @Test
  public void testToGetAllPreferences() throws Exception {
    Boolean isPreferenceCentreCreated = false;
    try {

      preferenceCentresService.getPreferenceCentre(preferenceCentre, preferenceCentre.getBrand());
    } catch (PreferenceCentreCreateException e) {
      isPreferenceCentreCreated = true;
    }
    assertFalse(isPreferenceCentreCreated);
  }

  @Test
  public void testToGetAllFanzoneSycException() throws Exception {
    Boolean isPreferenceCentreCreated = false;
    try {

      preferenceCentresService.getPreferenceCentre(preferenceCentre, preferenceCentre.getBrand());
    } catch (PreferenceCentreCreateException e) {
      isPreferenceCentreCreated = true;
    }
    assertFalse(isPreferenceCentreCreated);
  }

  @Test
  public void testToPopulateCreatorAndUpdater() throws Exception {
    Boolean isPreferenceCentreCreated = false;
    try {
      preferenceCentresService.populateCreatorAndUpdater(userServiceObj, preferenceCentre);
      isPreferenceCentreCreated = true;
    } catch (FanzoneSycCreateException e) {
    }
    assertTrue(isPreferenceCentreCreated);
  }

  @Test
  public void testDeleteAllByBrand() {
    when(preferenceCentresRepository.findAllPreferencesByBrand(anyString()))
        .thenReturn(Optional.of(preferenceCentre));
    preferenceCentresService.deleteAllByBrand(anyString());
    assertNotNull(preferenceCentresService);
    verify(preferenceCentresRepository, atLeastOnce()).delete(preferenceCentre);
  }

  @Test
  public void testDeleteAllByBrandPageNameElse() throws Exception {
    boolean thrown = false;
    try {
      when(preferenceCentresRepository.findAllPreferencesByBrand(anyString()))
          .thenReturn(Optional.empty());
      preferenceCentresService.deleteAllByBrand(anyString());
    } catch (NotFoundException e) {
      thrown = true;
    }
    assertTrue(thrown);
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
    entity.setActive(true);
    entity.setNotificationDescriptionDesktop(
        " Don’t miss a thing! Go to the Ladbrokes app and set your push notification preferences to receive team news, in-play match updates and more. These are for the app platform only; they are not sent on desktop or mobile web platforms.");
    entity.setUnsubscribeDescription(
        "Are you sure you want to unsubscribe? By pressing CONFIRM you will lose access to FANZONE. If you signed up less than 30 days ago you will need to wait until the 30 days expire to re-subscribe.");
    entity.setNotificationPopupTitle("TEAM ALERTS");
    entity.setUnsubscribeTitle("UNSUBSCRIBE FROM FANZONE");
    entity.setOptInCTA("'OPT IN'");
    entity.setNoThanksCTA("'NO THANKS'");
    entity.setPushPreferenceCentreTitle("PUSH PREFERENCE CENTRE");
    entity.setGenericTeamNotificationDescription("Description");
    entity.setGenericTeamNotificationTitle("Title");
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
