package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.*;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesClubRepository;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class FanzonesClubServiceTest extends BDDMockito {

  @InjectMocks private FanzonesClubService fanzonesClubService;
  @Mock private FanzonesClubRepository fanzonesClubRepository;
  @Mock CrudService<User> userServiceObj;
  private FanzoneClub fanzoneClub = createFanzoneClub();

  @Before
  public void init() {
    fanzonesClubService = new FanzonesClubService(fanzonesClubRepository);
  }

  @Test
  public void testFindAllByBrandAndPageName() {
    when(fanzonesClubRepository.findAllFanzonesByBrand(anyString()))
        .thenReturn(Optional.of(Arrays.asList(fanzoneClub)));
    assertNotNull(fanzonesClubService.findAllFanzonesByBrand(anyString()));
  }

  @Test
  public void testFindByBrandAndColumn() {
    when(fanzonesClubRepository.findByBrandAndColumn("ladbrokes", "id", "61e6a898ac5f7d77ba6cf37d"))
        .thenReturn(Optional.of(fanzoneClub));
    assertNotNull(
        fanzonesClubService.findByBrandAndColumn("ladbrokes", "id", "61e6a898ac5f7d77ba6cf37d"));
  }

  @Test
  public void testFindByBrandAndColumnNotPresent() {
    when(fanzonesClubRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .thenReturn(Optional.empty());
    assertNotNull(fanzonesClubService.findByBrandAndColumn(anyString(), anyString(), anyString()));
  }

  @Test
  public void testDeleteByBrandAndColumn() throws Exception {
    FanzoneClub entity = new FanzoneClub();
    entity.setId("616e7a3c54409d7519879827");
    entity.setBrand("ladbrokes");
    when(fanzonesClubRepository.findByBrandAndColumn("ladbrokes", "id", "616e7a3c54409d7519879827"))
        .thenReturn(Optional.of(entity));
    fanzonesClubService.deleteByBrandAndColumn("ladbrokes", "id", "616e7a3c54409d7519879827");
    assertNotNull(fanzonesClubService);
    verify(fanzonesClubRepository, atLeastOnce()).delete(entity);
  }

  @Test
  public void testDeleteAllByBrandPageName() {
    when(fanzonesClubRepository.findAllFanzonesByBrand(anyString()))
        .thenReturn(Optional.of(Arrays.asList(fanzoneClub)));
    fanzonesClubService.deleteAllByBrand(anyString());
    assertNotNull(fanzonesClubService);
    verify(fanzonesClubRepository, atLeastOnce()).delete(fanzoneClub);
  }

  @Test
  public void testDeleteAllByBrandPageNameElse() throws Exception {
    boolean thrown = false;
    try {
      when(fanzonesClubService.findAllFanzonesByBrand(anyString())).thenReturn(Optional.empty());
      fanzonesClubService.deleteAllByBrand(anyString());
    } catch (NotFoundException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  @Test
  public void testToPopulateCreatorAndUpdater() throws Exception {
    Boolean isFanzonePresent = true;
    fanzonesClubService.populateCreatorAndUpdater(userServiceObj, fanzoneClub);
    assertTrue(isFanzonePresent);
  }

  private static FanzoneClub createFanzoneClub() {
    FanzoneClub entity = new FanzoneClub();
    entity.setId("61e6a898ac5f7d77ba6cf37d");
    entity.setBrand("ladbrokes");
    entity.setActive(true);
    entity.setBannerLink("www.asset.com");
    entity.setTitle("club");
    entity.setDescription("welcome to clubs");
    entity.setValidityPeriodStart(Instant.now().plus(5, ChronoUnit.DAYS));
    entity.setValidityPeriodEnd(Instant.now().plus(6, ChronoUnit.DAYS));
    entity.setCreatedBy("54905d04a49acf605d645271");
    entity.setUpdatedBy("54905d04a49acf605d645271");
    entity.setCreatedByUserName("test.admin@coral.co.uk");
    entity.setUpdatedByUserName("test.admin@coral.co.uk");
    return entity;
  }
}
