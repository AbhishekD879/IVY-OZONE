package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.DatabaseChangeLog2022;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class OnboardingMenuAddTest {

  @Mock private MongockTemplate mongockTemplate;

  @InjectMocks private DatabaseChangeLog2022 databaseChangeLog;

  @Test
  public void testupdateSegmentMenue() {
    databaseChangeLog.updateOnBoardingMenu(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(2))
        .find(Mockito.any(), Mockito.any(), Mockito.any());
  }
}
