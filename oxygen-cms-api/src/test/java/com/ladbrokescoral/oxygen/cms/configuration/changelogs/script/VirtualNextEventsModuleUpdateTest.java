package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.DatabaseChangeLog;
import java.util.Arrays;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.mongodb.core.query.Query;

@ExtendWith(MockitoExtension.class)
class VirtualNextEventsModuleUpdateTest {

  @Mock private MongockTemplate mongockTemplate;

  private final DatabaseChangeLog databaseChangeLog = new DatabaseChangeLog();

  @Test
  void testForVirtualNextEventsModuleUpdate() {

    Mockito.when(this.mongockTemplate.find(Mockito.any(Query.class), Mockito.eq(SportModule.class)))
        .thenReturn(
            Arrays.asList(
                createSportModule("HC", SportModuleType.HIGHLIGHTS_CAROUSEL),
                createSportModule("SB", SportModuleType.SURFACE_BET)));
    Mockito.when(this.mongockTemplate.insert(Mockito.any(SportModule.class), Mockito.anyString()))
        .thenReturn(createSportModule("VNE", SportModuleType.VIRTUAL_NEXT_EVENTS));

    Assertions.assertDoesNotThrow(
        () -> this.databaseChangeLog.addVirtualNextEventsModuleToVirtuals(mongockTemplate));
  }

  @Test
  void testForVirtualNextEventsModuleNotCreated() {

    Mockito.when(this.mongockTemplate.find(Mockito.any(Query.class), Mockito.eq(SportModule.class)))
        .thenReturn(
            Arrays.asList(
                createSportModule("HC", SportModuleType.HIGHLIGHTS_CAROUSEL),
                createSportModule("VNE", SportModuleType.VIRTUAL_NEXT_EVENTS)));

    Assertions.assertDoesNotThrow(
        () -> this.databaseChangeLog.addVirtualNextEventsModuleToVirtuals(mongockTemplate));
  }

  private SportModule createSportModule(String title, SportModuleType moduleType) {
    SportModule sportModule = new SportModule();
    sportModule.setTitle(title);
    sportModule.setModuleType(moduleType);
    return sportModule;
  }
}
