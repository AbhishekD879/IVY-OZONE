package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionSubTab;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionTab;
import com.ladbrokescoral.oxygen.cms.api.repository.CompetitionModuleRepository;
import java.util.Collections;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CompetitionModuleServiceTest extends BDDMockito {

  @Mock private CompetitionModuleRepository repository;
  @Mock private SiteServerApi siteServerApiMock;

  @InjectMocks private CompetitionModuleService competitionModuleService;

  private CompetitionModule module;

  @Before
  public void setUp() throws Exception {
    module = new CompetitionModule();
    module.setTypeId(442);
  }

  @Test
  public void testPrepareModelBeforeSaveWithEmptyTypeId() {
    module = new CompetitionModule();
    competitionModuleService.prepareModelBeforeSave(module);
    verifyNoMoreInteractions(siteServerApiMock);
  }

  @Test
  public void findByBrandTest() {
    String brand = "testBrand";
    doReturn(Collections.singletonList(module)).when(repository).findAll();
    competitionModuleService.findByBrand(brand);
    verify(repository, times(1)).findAll();
  }

  @Test
  public void populatePathAndSaveTest() {
    module.setPath(null);
    assertNull(module.getPath());
    competitionModuleService.populatePathAndSave(new CompetitionTab(), module);
    assertNotNull(module.getPath());
  }

  @Test
  public void populatePathSubTabAndSaveTest() {
    module.setPath(null);
    assertNull(module.getPath());
    competitionModuleService.populatePathAndSave(new CompetitionSubTab(), module);
    assertNotNull(module.getPath());
  }

  @Test
  public void testFindByModuleByType() {
    CompetitionModule competitionModule = new CompetitionModule();
    competitionModule.setId("11");
    competitionModule.setName("Highlights");
    competitionModule.setType(CompetitionModuleType.HIGHLIGHT_CAROUSEL);
    doReturn(Collections.singletonList(competitionModule)).when(repository).findByType(any());
    List<CompetitionModule> competitionModules =
        this.competitionModuleService.findCompetitionModulesByType(
            CompetitionModuleType.HIGHLIGHT_CAROUSEL);
    verify(repository, times(1)).findByType(any());
    Assert.assertEquals("Highlights", competitionModules.get(0).getName());
  }
}
