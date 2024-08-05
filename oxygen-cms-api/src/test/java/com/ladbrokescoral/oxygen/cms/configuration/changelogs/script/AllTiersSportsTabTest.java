package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import static org.mockito.ArgumentMatchers.any;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.DatabaseChangeLog2022;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class AllTiersSportsTabTest {
  @Mock private MongockTemplate mongockTemplate;

  @InjectMocks private DatabaseChangeLog2022 databaseChangeLog;

  @Test
  public void testaddTabsForUntiedSportForGreyhoundsToday() {
    databaseChangeLog.addTabsForUntiedSportForGreyhoundsToday(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(2)).save(any(), any());
  }

  @Test
  public void testaddTabsForUntiedSportForGreyhoundsTomorrow() {
    databaseChangeLog.addTabsForUntiedSportForGreyhoundsTomorrow(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(2)).save(any(), any());
  }

  @Test
  public void testaddTabsForUntiedSportForHorseRacing() {
    databaseChangeLog.addTabsForUntiedSportForHorseRacing(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(2)).save(any(), any());
  }

  @Test
  public void testAddTabsForUntiedSportForPopularBets() {
    databaseChangeLog.addTabsForTier1SportForPopularBets(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(2)).save(any(), any());
  }

  @Test
  public void testCreateBetsBasedOnYourTeamForFanzone() {
    databaseChangeLog.createBetsBasedOnYourTeamForFanzone(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(1)).insert(any(SportModule.class), any());
  }

  @Test
  public void testCreateBetsBasedOnOtherFansForFanzone() {
    databaseChangeLog.createBetsBasedOnOtherFansForFanzone(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(1)).insert(any(SportModule.class), any());
  }
}
