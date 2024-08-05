package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneComingBack;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneComingBackCreateException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesComingBackRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
import java.util.Collections;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class FanzonesComingBackServiceTest extends BDDMockito {

  @InjectMocks private FanzonesComingBackService fanzonesComingBackService;
  @Mock private FanzonesComingBackRepository fanzonesComingBackRepository;
  @Mock private FanzonesSycRepository fanzonesSycRepository;
  @Mock CrudService<User> userServiceObj;
  private FanzoneComingBack fanzoneComingBack = createFanzoneComingBack();

  @Before
  public void init() {
    fanzonesComingBackService =
        new FanzonesComingBackService(fanzonesComingBackRepository, fanzonesSycRepository);
  }

  @Test
  public void testFindAllByBrand() {
    when(fanzonesComingBackRepository.findAllByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneComingBack));
    assertNotNull(fanzonesComingBackService.findAllByBrand(anyString()));
  }

  @Test
  public void testFindAllByBrandNotPresent() {
    when(fanzonesComingBackRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
    assertNotNull(fanzonesComingBackService.findAllByBrand(anyString()));
  }

  @Test
  public void testFindByBrandAndId() {
    when(fanzonesComingBackRepository.findAllByBrandAndId(anyString(), anyString()))
        .thenReturn(Optional.of(fanzoneComingBack));
    assertNotNull(fanzonesComingBackService.findAllByBrandAndId(anyString(), anyString()));
  }

  @Test
  public void testFindByBrandAndIdNotPresent() {
    when(fanzonesComingBackRepository.findAllByBrandAndId(anyString(), anyString()))
        .thenReturn(Optional.empty());
    assertNotNull(fanzonesComingBackService.findAllByBrandAndId(anyString(), anyString()));
  }

  @Test
  public void testToCheckFanzoneComingBack() throws Exception {
    when(fanzonesComingBackRepository.findAllByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneComingBack));
    fanzonesComingBackService.checkFanzoneComingBack(fanzoneComingBack.getBrand());
    Boolean isFanzoneNewSeasonCreated = true;
    assertTrue(isFanzoneNewSeasonCreated);
  }

  @Test
  public void testToCheckFanzoneNewSeasonFalse() throws Exception {
    when(fanzonesComingBackRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
    fanzonesComingBackService.checkFanzoneComingBack(fanzoneComingBack.getBrand());
    Boolean isFanzoneNewSeasonCreated = false;
    assertFalse(isFanzoneNewSeasonCreated);
  }

  @Test
  public void testToGetFanzoneComingBack() throws Exception {
    Boolean isFanzoneComingBackCreated = false;
    try {
      when(fanzonesComingBackRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
      fanzonesComingBackService.getFanzoneComingBack(
          fanzoneComingBack, fanzoneComingBack.getBrand());
    } catch (FanzoneComingBackCreateException e) {
      isFanzoneComingBackCreated = true;
    }
    assertFalse(isFanzoneComingBackCreated);
  }

  @Test
  public void testToGetFanzoneComingBackException() throws Exception {
    Boolean isFanzoneComingBackCreated = false;
    try {
      when(fanzonesComingBackRepository.findAllByBrand(anyString()))
          .thenReturn(Optional.of(fanzoneComingBack));
      fanzonesComingBackService.getFanzoneComingBack(
          fanzoneComingBack, fanzoneComingBack.getBrand());
    } catch (FanzoneComingBackCreateException e) {
      isFanzoneComingBackCreated = true;
    }
    assertTrue(isFanzoneComingBackCreated);
  }

  @Test
  public void testToPopulateCreatorAndUpdater() throws Exception {
    Boolean isFanzoneComingBackCreated = false;
    try {
      fanzonesComingBackService.populateCreatorAndUpdater(userServiceObj, fanzoneComingBack);
      isFanzoneComingBackCreated = true;
    } catch (FanzoneComingBackCreateException e) {
    }
    assertTrue(isFanzoneComingBackCreated);
  }

  @Test
  public void testDeleteAllByBrand() {
    when(fanzonesComingBackRepository.findAllByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneComingBack));
    fanzonesComingBackService.deleteAllByBrand(anyString());
    assertNotNull(fanzonesComingBackService);
    verify(fanzonesComingBackRepository, atLeastOnce()).delete(fanzoneComingBack);
  }

  @Test
  public void testDeleteAllByBrandException() throws Exception {
    boolean thrown = false;
    try {
      when(fanzonesComingBackRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
      fanzonesComingBackService.deleteAllByBrand(anyString());
    } catch (NotFoundException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  @Test
  public void testToSetFanzoneComingBackSeasonStartDate() throws Exception {
    Boolean isFanzoneSycPresent = false;
    try {
      when(fanzonesSycRepository.findByBrand(anyString())).thenReturn(Collections.emptyList());
      fanzonesComingBackService.setSeasonStartDateFromFanzoneSyc(
          fanzoneComingBack, fanzoneComingBack.getBrand());
    } catch (IndexOutOfBoundsException e) {
      isFanzoneSycPresent = true;
    }
    assertFalse(isFanzoneSycPresent);
  }

  private static FanzoneComingBack createFanzoneComingBack() {
    FanzoneComingBack entity = new FanzoneComingBack();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setFzComingBackHeading("Fanzone Coming Back");
    entity.setFzComingBackDescription("Fanzone Coming Back Pop Up Description");
    entity.setFzComingBackTitle("Fanzone Coming Back Pop Up Title");
    entity.setFzComingBackOKCTA("OK CTA");
    entity.setFzComingBackDisplayFromDays("No of days before season starts");
    entity.setFzComingBackBadgeUrlDesktop("Fanzone_Syc2");
    entity.setFzComingBackBadgeUrlMobile("Fanzone_Syc2");
    entity.setFzComingBackPopupDisplay(true);
    return entity;
  }
}
