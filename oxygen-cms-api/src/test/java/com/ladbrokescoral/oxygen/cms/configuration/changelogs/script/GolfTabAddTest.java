package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import static org.mockito.Mockito.any;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.Tier2SportTabsTemplate;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.DatabaseChangeLog2022;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class GolfTabAddTest {

  @Mock private MongockTemplate mongockTemplate;

  @InjectMocks private DatabaseChangeLog2022 databaseChangeLog;

  @Mock private Tier2SportTabsTemplate template;

  @Test
  public void testGolfTabAdd() {
    databaseChangeLog.addTabForGolf(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(2)).save(any(), any());
  }
}
