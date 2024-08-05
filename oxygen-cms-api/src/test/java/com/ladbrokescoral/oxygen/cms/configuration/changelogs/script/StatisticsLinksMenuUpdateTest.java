package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.DatabaseChangeLog;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.Silent.class)
public class StatisticsLinksMenuUpdateTest {
  @Mock private MongockTemplate mongockTemplate;
  private final DatabaseChangeLog databaseChangeLog = new DatabaseChangeLog();
  @InjectMocks private StatisticsLinksMenuUpdate statisticsLinksMenuUpdate;

  @Test
  public void testAddStatisticsLinksMenu() {
    Assert.assertNotNull(databaseChangeLog);
    databaseChangeLog.addStatisticsLinksMenu(mongockTemplate);
  }
}
