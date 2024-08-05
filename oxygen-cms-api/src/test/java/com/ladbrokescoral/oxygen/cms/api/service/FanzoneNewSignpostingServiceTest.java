package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSignposting;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneNewSignpostingCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewSignpostingRepository;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class FanzoneNewSignpostingServiceTest extends BDDMockito {

  @InjectMocks private FanzonesNewSignpostingService fanzonesNewSignpostingService;
  @Mock private FanzonesNewSignpostingRepository fanzonesNewSignpostingRepository;

  @Mock CrudService<User> userServiceObj;
  private FanzoneNewSignposting fanzoneNewSignposting = createFanzoneNewSignposting();

  @Before
  public void init() {
    fanzonesNewSignpostingService =
        new FanzonesNewSignpostingService(fanzonesNewSignpostingRepository);
  }

  @Test
  public void testFindAllByBrand() {
    when(fanzonesNewSignpostingRepository.findAllByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneNewSignposting));
    assertNotNull(fanzonesNewSignpostingService.findAllByBrand(anyString()));
  }

  @Test
  public void testFindAllByBrandNotPresent() {
    when(fanzonesNewSignpostingRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
    assertNotNull(fanzonesNewSignpostingService.findAllByBrand(anyString()));
  }

  @Test
  public void testFindByBrandAndId() {
    when(fanzonesNewSignpostingRepository.findAllByBrandAndId(anyString(), anyString()))
        .thenReturn(Optional.of(fanzoneNewSignposting));
    assertNotNull(fanzonesNewSignpostingService.findAllByBrandAndId(anyString(), anyString()));
  }

  @Test
  public void testFindByBrandAndIdNotPresent() {
    when(fanzonesNewSignpostingRepository.findAllByBrandAndId(anyString(), anyString()))
        .thenReturn(Optional.empty());
    assertNotNull(fanzonesNewSignpostingService.findAllByBrandAndId(anyString(), anyString()));
  }

  @Test
  public void testToCheckFanzoneNewSeason() throws Exception {
    when(fanzonesNewSignpostingRepository.findAllByBrand(anyString()))
        .thenReturn(Optional.of(fanzoneNewSignposting));
    fanzonesNewSignpostingService.checkFanzoneNewSignposting(fanzoneNewSignposting.getBrand());
    Boolean isFanzoneNewSignpostingCreated = true;
    assertTrue(isFanzoneNewSignpostingCreated);
  }

  @Test
  public void testToCheckFanzoneNewSeasonFalse() throws Exception {
    when(fanzonesNewSignpostingRepository.findAllByBrand(anyString())).thenReturn(Optional.empty());
    fanzonesNewSignpostingService.checkFanzoneNewSignposting(fanzoneNewSignposting.getBrand());
    Boolean isFanzoneNewSignpostingCreated = false;
    assertFalse(isFanzoneNewSignpostingCreated);
  }

  @Test
  public void testToGetFanzoneNewSeason() throws Exception {
    Boolean isFanzoneNewSignpostingCreated = false;
    try {
      when(fanzonesNewSignpostingRepository.findAllByBrand(anyString()))
          .thenReturn(Optional.empty());
      fanzonesNewSignpostingService.getFanzoneNewSignposting(
          fanzoneNewSignposting, fanzoneNewSignposting.getBrand());
    } catch (FanzoneNewSignpostingCreateException e) {
      isFanzoneNewSignpostingCreated = true;
    }
    assertFalse(isFanzoneNewSignpostingCreated);
  }

  @Test
  public void testToGetFanzoneNewSeasonException() throws Exception {
    Boolean isFanzoneNewSignpostingCreated = false;
    try {
      when(fanzonesNewSignpostingRepository.findAllByBrand(anyString()))
          .thenReturn(Optional.of(fanzoneNewSignposting));
      fanzonesNewSignpostingService.getFanzoneNewSignposting(
          fanzoneNewSignposting, fanzoneNewSignposting.getBrand());
    } catch (FanzoneNewSignpostingCreateException e) {
      isFanzoneNewSignpostingCreated = true;
    }
    assertTrue(isFanzoneNewSignpostingCreated);
  }

  @Test
  public void testToPopulateCreatorAndUpdater() throws Exception {
    Boolean isFanzoneNewSeasonCreated = false;
    try {
      fanzonesNewSignpostingService.populateCreatorAndUpdater(
          userServiceObj, fanzoneNewSignposting);
      isFanzoneNewSeasonCreated = true;
    } catch (FanzoneNewSignpostingCreateException e) {
    }
    assertTrue(isFanzoneNewSeasonCreated);
  }

  private static FanzoneNewSignposting createFanzoneNewSignposting() {
    FanzoneNewSignposting entity = new FanzoneNewSignposting();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setActive(true);
    entity.setNewSignPostingIcon("new");
    entity.setStartDate(Instant.now().plus(5, ChronoUnit.DAYS));
    entity.setEndDate(Instant.now().plus(6, ChronoUnit.DAYS));
    return entity;
  }
}
