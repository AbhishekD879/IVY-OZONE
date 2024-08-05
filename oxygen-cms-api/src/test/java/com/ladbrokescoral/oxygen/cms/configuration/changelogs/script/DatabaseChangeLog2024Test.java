package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.DatabaseChangeLog2024;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class DatabaseChangeLog2024Test {
  @Mock private MongockTemplate mongockTemplate;

  @InjectMocks private DatabaseChangeLog2024 databaseChangeLog;

  @Test
  public void testAddPopularAccaWidgetModule() {
    databaseChangeLog.addPopularAccaModule(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.atLeastOnce())
        .insert(Mockito.any(SportModule.class), Mockito.anyString());
  }
}
