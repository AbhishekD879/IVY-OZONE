package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSeason;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneNewSeasonCreateException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewSeasonRepository;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class FanzonesNewSeasonServiceTest extends BDDMockito {

  @InjectMocks private FanzonesNewSeasonService fanzonesNewSeasonService;
  @Mock private FanzonesNewSeasonRepository fanzonesNewSeasonRepository;
  @Mock CrudService<User> userServiceObj;
  private FanzoneNewSeason fanzoneNewSeason = createFanzoneNewSeason();

  @Before
  public void init() {
    fanzonesNewSeasonService = new FanzonesNewSeasonService(fanzonesNewSeasonRepository);
  }

  @Test
  public void testFindAllByBrand() {
    when(fanzonesNewSeasonRepository.findAllByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneNewSeason));
    assertNotNull(fanzonesNewSeasonService.findAllByBrand(anyString()));
  }

  @Test
  public void testFindAllByBrandNotPresent() {
    when(fanzonesNewSeasonRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
    assertNotNull(fanzonesNewSeasonService.findAllByBrand(anyString()));
  }

  @Test
  public void testFindByBrandAndId() {
    when(fanzonesNewSeasonRepository.findAllByBrandAndId(anyString(), anyString()))
        .thenReturn(Optional.of(fanzoneNewSeason));
    assertNotNull(fanzonesNewSeasonService.findAllByBrandAndId(anyString(), anyString()));
  }

  @Test
  public void testFindByBrandAndIdNotPresent() {
    when(fanzonesNewSeasonRepository.findAllByBrandAndId(anyString(), anyString()))
        .thenReturn(Optional.empty());
    assertNotNull(fanzonesNewSeasonService.findAllByBrandAndId(anyString(), anyString()));
  }

  @Test
  public void testToCheckFanzoneNewSeason() throws Exception {
    when(fanzonesNewSeasonRepository.findAllByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneNewSeason));
    fanzonesNewSeasonService.checkFanzoneNewSeason(fanzoneNewSeason.getBrand());
    Boolean isFanzoneNewSeasonCreated = true;
    assertTrue(isFanzoneNewSeasonCreated);
  }

  @Test
  public void testToCheckFanzoneNewSeasonFalse() throws Exception {
    when(fanzonesNewSeasonRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
    fanzonesNewSeasonService.checkFanzoneNewSeason(fanzoneNewSeason.getBrand());
    Boolean isFanzoneNewSeasonCreated = false;
    assertFalse(isFanzoneNewSeasonCreated);
  }

  @Test
  public void testToGetFanzoneNewSeason() throws Exception {
    Boolean isFanzoneNewSeasonCreated = false;
    try {
      when(fanzonesNewSeasonRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
      fanzonesNewSeasonService.getFanzoneNewSeason(fanzoneNewSeason, fanzoneNewSeason.getBrand());
    } catch (FanzoneNewSeasonCreateException e) {
      isFanzoneNewSeasonCreated = true;
    }
    assertFalse(isFanzoneNewSeasonCreated);
  }

  @Test
  public void testToGetFanzoneNewSeasonException() throws Exception {
    Boolean isFanzoneNewSeasonCreated = false;
    try {
      when(fanzonesNewSeasonRepository.findAllByBrand(anyString()))
          .thenReturn(Optional.of(fanzoneNewSeason));
      fanzonesNewSeasonService.getFanzoneNewSeason(fanzoneNewSeason, fanzoneNewSeason.getBrand());
    } catch (FanzoneNewSeasonCreateException e) {
      isFanzoneNewSeasonCreated = true;
    }
    assertTrue(isFanzoneNewSeasonCreated);
  }

  @Test
  public void testToPopulateCreatorAndUpdater() throws Exception {
    Boolean isFanzoneNewSeasonCreated = false;
    try {
      fanzonesNewSeasonService.populateCreatorAndUpdater(userServiceObj, fanzoneNewSeason);
      isFanzoneNewSeasonCreated = true;
    } catch (FanzoneNewSeasonCreateException e) {
    }
    assertTrue(isFanzoneNewSeasonCreated);
  }

  @Test
  public void testDeleteAllByBrand() {
    when(fanzonesNewSeasonRepository.findAllByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneNewSeason));
    fanzonesNewSeasonService.deleteAllByBrand(anyString());
    assertNotNull(fanzonesNewSeasonService);
    verify(fanzonesNewSeasonRepository, atLeastOnce()).delete(fanzoneNewSeason);
  }

  @Test
  public void testDeleteAllByBrandException() throws Exception {
    boolean thrown = false;
    try {
      when(fanzonesNewSeasonRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
      fanzonesNewSeasonService.deleteAllByBrand(anyString());
    } catch (NotFoundException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  private static FanzoneNewSeason createFanzoneNewSeason() {
    FanzoneNewSeason entity = new FanzoneNewSeason();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setFzNewSeasonHeading("Fanzone New Season");
    entity.setFzNewSeasonTitle("Fanzone New Season Pop Up Title");
    entity.setFzNewSeasonDescription("Fanzone New Season Pop Up Descriptionn");
    entity.setFzNewSeasonBgImageDesktop("Fanzone_Syc2");
    entity.setFzNewSeasonBgImageMobile("Fanzone_Syc2");
    entity.setFzNewSeasonBadgeMobile("Fanzone_Syc2");
    entity.setFzNewSeasonBadgeDesktop("Fanzone_Syc2");
    entity.setFzNewSeasonLightningMobile("Fanzone_Syc2");
    entity.setFzNewSeasonLightningDesktop("Fanzone_Syc2");
    return entity;
  }
}
