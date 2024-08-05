package com.ladbrokescoral.oxygen.cms.api.service;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.DatabaseChangeLog;
import java.util.Collections;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.mongodb.core.query.Query;

@ExtendWith(MockitoExtension.class)
public class RgyModuleStructureUpdateTest {

  @Mock private MongockTemplate mongockTemplate;

  private DatabaseChangeLog databaseChangeLog = new DatabaseChangeLog();

  @Test
  public void testRgyModuleUpdate() {
    RGYModuleEntity rgyModule = createEntity("Testing");
    rgyModule.setAliasModules(Collections.singletonList(createDto()));
    Mockito.when(
            this.mongockTemplate.find(Mockito.any(Query.class), Mockito.eq(RGYModuleEntity.class)))
        .thenReturn(Collections.singletonList(createEntity("Testing")));
    ;
    Mockito.when(this.mongockTemplate.save(Mockito.any(RGYModuleEntity.class), Mockito.anyString()))
        .thenReturn(rgyModule);
    Assertions.assertDoesNotThrow(
        () -> databaseChangeLog.updateRgyEntityStructure(mongockTemplate));
    Mockito.verify(mongockTemplate, Mockito.times(2))
        .save(Mockito.any(RGYModuleEntity.class), Mockito.eq("rgy-modules"));
  }

  @Test
  public void testRgyModulesWithNoUpdate() {
    Mockito.when(
            this.mongockTemplate.find(Mockito.any(Query.class), Mockito.eq(RGYModuleEntity.class)))
        .thenReturn(Collections.singletonList(createEntity(null)));
    Assertions.assertDoesNotThrow(
        () -> databaseChangeLog.updateRgyEntityStructure(mongockTemplate));
    Mockito.verify(mongockTemplate, Mockito.times(0))
        .save(Mockito.any(RGYModuleEntity.class), Mockito.eq("rgy-modules"));
  }

  private RGYModuleEntity createEntity(String aliasModulesNames) {
    RGYModuleEntity rgyModule = new RGYModuleEntity();
    rgyModule.setId("22");
    rgyModule.setAliasModuleNames(aliasModulesNames);
    return rgyModule;
  }

  private AliasModuleNamesDto createDto() {
    AliasModuleNamesDto aliasModuleNamesDto = new AliasModuleNamesDto();
    aliasModuleNamesDto.setTitle("Testing");
    aliasModuleNamesDto.setAddTag(Boolean.TRUE);
    return aliasModuleNamesDto;
  }
}
