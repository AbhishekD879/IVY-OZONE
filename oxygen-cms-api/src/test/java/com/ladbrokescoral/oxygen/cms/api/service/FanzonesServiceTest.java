package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.*;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.InvalidPageNameException;
import com.ladbrokescoral.oxygen.cms.api.exception.InvalidTeamIdException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesRepository;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class FanzonesServiceTest extends BDDMockito {

  @InjectMocks private FanzonesService fanzonesService;
  @Mock private FanzonesRepository fanzonesRepository;
  @Mock CrudService<User> userServiceObj;
  private Fanzone fanzone = createFanzone();

  @Before
  public void init() {
    fanzonesService = new FanzonesService(fanzonesRepository);
  }

  @Test
  public void testFindAllByBrandAndPageName() {
    when(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .thenReturn(Optional.of(Arrays.asList(fanzone)));
    assertNotNull(fanzonesRepository.findAllFanzonesByBrand(anyString()));
  }

  @Test
  public void testFindByBrandAndColumn() {
    when(fanzonesRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .thenReturn(Optional.of(fanzone));
    assertNotNull(fanzonesService.findByBrandAndColumn(anyString(), anyString(), anyString()));
  }

  @Test
  public void testFindByBrandAndColumnNotPresent() {
    when(fanzonesRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .thenReturn(Optional.empty());
    assertNotNull(fanzonesService.findByBrandAndColumn(anyString(), anyString(), anyString()));
  }

  @Test
  public void testDeleteByBrandAndColumn() throws Exception {
    Fanzone entity = new Fanzone();
    entity.setPageName("fanzone");
    entity.setId("616e7a3c54409d7519879827");
    entity.setBrand("ladbrokes");
    when(fanzonesRepository.findByBrandAndColumn("ladbrokes", "id", "616e7a3c54409d7519879827"))
        .thenReturn(Optional.of(entity));
    fanzonesService.deleteByBrandAndColumn("ladbrokes", "id", "616e7a3c54409d7519879827");
    assertNotNull(fanzonesService);
    verify(fanzonesRepository, atLeastOnce()).delete(entity);
  }

  @Test
  public void testDeleteAllByBrandPageName() {
    when(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .thenReturn(Optional.of(Arrays.asList(fanzone)));
    fanzonesService.deleteAllByBrand(anyString());
    assertNotNull(fanzonesService);
    verify(fanzonesRepository, atLeastOnce()).delete(fanzone);
  }

  @Test
  public void testDeleteAllByBrandPageNameElse() throws Exception {
    boolean thrown = false;
    try {
      when(fanzonesService.findAllFanzonesByBrand(anyString())).thenReturn(Optional.empty());
      fanzonesService.deleteAllByBrand(anyString());
    } catch (NotFoundException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  // new processFanzone
  @Test
  public void testToProcessFanzone() throws Exception {
    when(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .thenReturn(Optional.of(Arrays.asList(fanzone)));
    Fanzone fanzone1 = new Fanzone();
    fanzone1.setName("");
    fanzone1.setTeamId("");
    Fanzone fanzoneEntity = fanzonesService.processFanzone(fanzone1, "");
    assertNotNull(fanzoneEntity);
  }

  @Test
  public void testToProcessFanzone1() throws Exception {
    when(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .thenReturn(Optional.of(Arrays.asList(fanzone)));
    Fanzone fanzone1 = new Fanzone();
    fanzone1.setName("Manchester");
    fanzone1.setTeamId("12");
    Fanzone fanzoneEntity = fanzonesService.processFanzone(fanzone1, "");
    assertNotNull(fanzoneEntity);
  }

  @Test
  public void testToProcessFanzoneElse() throws Exception {
    boolean thrown = false;
    try {
      when(fanzonesRepository.findAllFanzonesByBrand(anyString())).thenReturn(Optional.empty());
      fanzonesService.processFanzone(fanzone, "");
    } catch (NotFoundException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  @Test
  public void testToCheckFanzoneElse() throws Exception {
    boolean thrown = false;
    Optional<List<Fanzone>> fanzoneList = Optional.empty();
    try {
      fanzonesService.checkFanzone(fanzoneList, fanzone);
    } catch (NotFoundException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  @Test
  public void testToPopulateCreatorAndUpdater() throws Exception {
    Boolean isFanzonePresent = false;
    try {
      fanzonesService.populateCreatorAndUpdater(userServiceObj, fanzone);
      isFanzonePresent = true;
    } catch (InvalidPageNameException e) {
    }
    assertTrue(isFanzonePresent);
  }

  @Test
  public void testToTeamNameException() throws Exception {
    boolean thrown = false;
    Fanzone fanzone1 = new Fanzone();
    fanzone1.setTeamId("2");
    fanzone1.setName("Everton");
    try {
      when(fanzonesRepository.findAllFanzonesByBrand(anyString()))
          .thenReturn(Optional.of(Arrays.asList(fanzone)));
      fanzonesService.processFanzone(fanzone1, "");
    } catch (InvalidPageNameException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  @Test
  public void testToTeamIdException() throws Exception {
    boolean thrown = false;
    Fanzone fanzone1 = new Fanzone();
    fanzone1.setTeamId("1");
    try {
      when(fanzonesRepository.findAllFanzonesByBrand(anyString()))
          .thenReturn(Optional.of(Arrays.asList(fanzone)));
      fanzonesService.processFanzone(fanzone, "");
    } catch (InvalidTeamIdException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  @Test
  public void testProcessFanzoneForUpdate() throws Exception {
    Fanzone fanzone1 = createFanzone();
    Fanzone fanzone2 = createFanzone();
    fanzone1.setName("Arsenall");
    fanzone2.setName("Liverpool");
    fanzone1.setId("1234");
    fanzone2.setId("789");
    fanzone1.setTeamId("4");
    fanzone2.setTeamId("6");
    when(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .thenReturn(Optional.of(createFanzoneList()));
    Fanzone fanzoneEntity = fanzonesService.processFanzoneForUpdate(fanzone1, "", fanzone);
    assertNotNull(fanzoneEntity);
  }

  @Test
  public void testProcessFanzoneForUpdate2() throws Exception {
    Fanzone fanzone1 = createFanzone();
    Fanzone fanzone2 = createFanzone();
    fanzone1.setName("Arsenall");
    fanzone2.setName("Liverpool");
    fanzone1.setId("1234");
    fanzone2.setId("789");
    fanzone1.setTeamId("2");
    fanzone2.setTeamId("3");
    when(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .thenReturn(Optional.of(createFanzoneList()));
    try {
      Fanzone fanzoneEntity = fanzonesService.processFanzoneForUpdate(fanzone1, "", fanzone);
    } catch (InvalidTeamIdException e) {
      assertNotNull(e);
    }
  }

  @Test
  public void testProcessFanzoneForUpdate3() throws Exception {
    Fanzone fanzone1 = createFanzone();
    Fanzone fanzone2 = createFanzone();
    fanzone1.setName("Arsenal");
    fanzone2.setName("Liverpool");
    fanzone1.setId("1234");
    fanzone2.setId("789");
    fanzone1.setTeamId("6");
    fanzone2.setTeamId("9");
    when(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .thenReturn(Optional.of(createFanzoneList()));
    try {
      Fanzone fanzoneEntity = fanzonesService.processFanzoneForUpdate(fanzone1, "", fanzone);
    } catch (InvalidPageNameException e) {
      assertNotNull(e);
    }
  }

  @Test
  public void testToCheckFanzoneForUpdateElse() throws Exception {
    boolean thrown = false;
    Optional<List<Fanzone>> fanzoneList = Optional.empty();
    try {
      fanzonesService.checkFanzoneForUpdate(fanzoneList, fanzone);
    } catch (NotFoundException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  @Test
  public void testToProcessFanzoneUpdateElse() throws Exception {
    boolean thrown = false;
    Fanzone fanzone1 = new Fanzone();
    fanzone1.setId("66666");
    fanzone1.setName("ght");

    try {
      when(fanzonesRepository.findAllFanzonesByBrand(anyString())).thenReturn(Optional.empty());
      fanzonesService.processFanzoneForUpdate(fanzone, "", fanzone1);
    } catch (NotFoundException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  private List<Fanzone> createFanzoneList() {
    List<Fanzone> flist = new ArrayList<>();
    Fanzone fanzone1 = createFanzone();
    Fanzone fanzone2 = createFanzone();
    fanzone1.setName("Arsenal");
    fanzone2.setName("Liverpool");
    fanzone1.setId("1234");
    fanzone2.setId("789");
    fanzone1.setTeamId("2");
    fanzone2.setTeamId("3");
    flist.add(createFanzone());
    flist.add(fanzone1);
    flist.add(fanzone2);
    return flist;
  }

  private static Fanzone createFanzone() {
    Fanzone entity = new Fanzone();
    entity.setId("616e7a3c54409d7519879827");
    entity.setBrand("ladbrokes");
    entity.setLaunchBannerUrl("www.url.com");
    entity.setName("Everton");
    entity.setTeamId("1");
    entity.setOpenBetID("OB567800");
    entity.setAssetManagementLink("www.assetManagementLink.com");
    entity.setPrimaryCompetitionId("990,991,992");
    entity.setSecondaryCompetitionId("1,2,3");
    entity.setClubIds("990,991,992");
    entity.setLocation("stadium3,Nagpur,ADDA205");
    entity.setOutRightsLbl("obl");
    entity.setPremierLeagueLbl("abc");
    entity.setActive(false);
    entity.setNextGamesLbl("leicester");
    FanzoneConfiguration fanzoneConfiguration = new FanzoneConfiguration();
    fanzoneConfiguration.setShowCompetitionTable(true);
    fanzoneConfiguration.setShowNowNext(true);
    fanzoneConfiguration.setShowStats(false);
    fanzoneConfiguration.setShowClubs(false);
    fanzoneConfiguration.setSportsRibbon(true);
    fanzoneConfiguration.setAtozMenu(false);
    fanzoneConfiguration.setHomePage(true);
    fanzoneConfiguration.setFootballHome(false);
    fanzoneConfiguration.setLaunchBannerUrlDesktop("www.url.com");
    fanzoneConfiguration.setFanzoneBannerDesktop("www.url.com");
    fanzoneConfiguration.setShowGames(true);
    return entity;
  }
}
