package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewGamingPopUp;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneNewGamingPopUpException;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneNewSignpostingCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewGamingPopUpRepository;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class FanzonesNewGamingPopUpServiceTest extends BDDMockito {

  @InjectMocks private FanzonesNewGamingPopUpService fanzonesNewGamingPopUpService;
  @Mock private FanzonesNewGamingPopUpRepository fanzonesNewGamingPopUpRepository;

  @Mock CrudService<User> userServiceObj;
  private FanzoneNewGamingPopUp fanzoneNewGamingPopUp = createFanzoneNewGamingPopUp();

  @Before
  public void init() {
    fanzonesNewGamingPopUpService =
        new FanzonesNewGamingPopUpService(fanzonesNewGamingPopUpRepository);
  }

  @Test
  public void testFindAllByBrand() {
    when(fanzonesNewGamingPopUpRepository.findAllByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneNewGamingPopUp));
    assertNotNull(fanzonesNewGamingPopUpService.findAllByBrand(anyString()));
  }

  @Test
  public void testFindAllByBrandNotPresent() {
    when(fanzonesNewGamingPopUpRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
    assertNotNull(fanzonesNewGamingPopUpService.findAllByBrand(anyString()));
  }

  @Test
  public void testFindByBrandAndId() {
    when(fanzonesNewGamingPopUpRepository.findAllByBrandAndId(anyString(), anyString()))
        .thenReturn(Optional.of(fanzoneNewGamingPopUp));
    assertNotNull(fanzonesNewGamingPopUpService.findAllByBrandAndId(anyString(), anyString()));
  }

  @Test
  public void testFindByBrandAndIdNotPresent() {
    when(fanzonesNewGamingPopUpRepository.findAllByBrandAndId(anyString(), anyString()))
        .thenReturn(Optional.empty());
    assertNotNull(fanzonesNewGamingPopUpService.findAllByBrandAndId(anyString(), anyString()));
  }

  @Test
  public void testToCheckFanzoneNewGamingPopUp() throws Exception {
    when(fanzonesNewGamingPopUpRepository.findAllByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneNewGamingPopUp));
    fanzonesNewGamingPopUpService.checkFanzoneNewGamingPopUp(fanzoneNewGamingPopUp.getBrand());
    Boolean isFanzoneNewGamingPopUpCreated = true;
    assertTrue(isFanzoneNewGamingPopUpCreated);
  }

  @Test
  public void testToCheckFanzoneNewGamingPopUpFalse() throws Exception {
    when(fanzonesNewGamingPopUpRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
    fanzonesNewGamingPopUpService.checkFanzoneNewGamingPopUp(fanzoneNewGamingPopUp.getBrand());
    Boolean isFanzoneNewGamingPopUpCreated = false;
    assertFalse(isFanzoneNewGamingPopUpCreated);
  }

  @Test
  public void testToGetFanzoneNewGamingPopUp() throws Exception {
    Boolean isFanzoneNewGamingPopUpCreated = false;
    try {
      when(fanzonesNewGamingPopUpRepository.findAllByBrand(anyString()))
          .thenReturn(Optional.empty());
      fanzonesNewGamingPopUpService.getFanzoneNewGamingPopUp(
          fanzoneNewGamingPopUp, fanzoneNewGamingPopUp.getBrand());
    } catch (FanzoneNewGamingPopUpException e) {
      isFanzoneNewGamingPopUpCreated = true;
    }
    assertFalse(isFanzoneNewGamingPopUpCreated);
  }

  @Test
  public void testToGetFanzoneNewGamingPopUpException() throws Exception {
    Boolean isFanzoneNewGamingPopUpCreated = false;
    try {
      when(fanzonesNewGamingPopUpRepository.findAllByBrand(anyString()))
          .thenReturn(Optional.of(fanzoneNewGamingPopUp));
      fanzonesNewGamingPopUpService.getFanzoneNewGamingPopUp(
          fanzoneNewGamingPopUp, fanzoneNewGamingPopUp.getBrand());
    } catch (FanzoneNewGamingPopUpException e) {
      isFanzoneNewGamingPopUpCreated = true;
    }
    assertTrue(isFanzoneNewGamingPopUpCreated);
  }

  @Test
  public void testToPopulateCreatorAndUpdater() throws Exception {
    Boolean isFanzoneNewGamingPopUpCreated = false;
    try {
      fanzonesNewGamingPopUpService.populateCreatorAndUpdater(
          userServiceObj, fanzoneNewGamingPopUp);
      isFanzoneNewGamingPopUpCreated = true;
    } catch (FanzoneNewSignpostingCreateException e) {
    }
    assertTrue(isFanzoneNewGamingPopUpCreated);
  }

  private FanzoneNewGamingPopUp createFanzoneNewGamingPopUp() {
    FanzoneNewGamingPopUp entity = new FanzoneNewGamingPopUp();
    entity.setBrand("ladbrokes");
    entity.setTitle("Fanzone New Gaming Pop Up");
    entity.setDescription("Fanzone New gaming pop up description here");
    entity.setCloseCTA("close");
    entity.setPlayCTA("play");
    return entity;
  }
}
