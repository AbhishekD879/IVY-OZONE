package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.DatabaseChangeLog2022;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import org.assertj.core.api.Assertions;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class DatabaseChangeLog2022Test {
  @Mock private MongockTemplate mongockTemplate;

  @InjectMocks private DatabaseChangeLog2022 databaseChangeLog;

  @Test
  public void testSaveSportTabsMarketNames() {
    Mockito.when(mongockTemplate.find(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(getSportTabs());
    databaseChangeLog.saveSportTabsMarketNames(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.atLeastOnce()).save(Mockito.any());
  }

  private List<Object> getSportTabs() {
    return Arrays.asList(
        SportTab.builder()
            .name("matches")
            .displayName("Matches")
            .sortOrder(1.0)
            .enabled(true)
            .brand("bma")
            .sportId(16)
            .build(),
        SportTab.builder()
            .name("live")
            .displayName("In-Play")
            .sortOrder(2.0)
            .enabled(true)
            .brand("bma")
            .sportId(16)
            .build(),
        SportTab.builder()
            .name("competitions")
            .displayName("Competitions")
            .sortOrder(3.0)
            .enabled(true)
            .brand("bma")
            .sportId(16)
            .build(),
        SportTab.builder()
            .name("coupons")
            .displayName("Coupons")
            .sortOrder(4.0)
            .enabled(true)
            .checkEvents(true)
            .brand("bma")
            .sportId(16)
            .build(),
        SportTab.builder()
            .name("outrights")
            .displayName("Outrights")
            .sortOrder(5.0)
            .enabled(true)
            .brand("bma")
            .sportId(16)
            .build(),
        SportTab.builder()
            .name("specials")
            .displayName("Specials")
            .sortOrder(7.0)
            .enabled(true)
            .checkEvents(true)
            .brand("bma")
            .sportId(16)
            .build(),
        SportTab.builder()
            .name("jackpot")
            .displayName("Jackpot")
            .sortOrder(6.0)
            .enabled(true)
            .checkEvents(true)
            .brand("bma")
            .sportId(16)
            .build());
  }

  @Test
  public void testAddOrUpdateTrendingTabsTest() {
    SportTab sportTab =
        SportTab.builder()
            .name("popularbets")
            .displayName("popularbets")
            .sortOrder(3.0)
            .enabled(true)
            .brand("bma")
            .sportId(16)
            .trendingTabs(new ArrayList<>())
            .build();
    Mockito.when(mongockTemplate.findOne(Mockito.any(), Mockito.any())).thenReturn(sportTab);
    databaseChangeLog.addForYouTabsForPopularBets(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.atLeastOnce()).save(Mockito.any());
  }

  @Test
  public void testAddOrUpdateTrendingTabsNullTest() {
    SportTab sportTab =
        SportTab.builder()
            .name("popularbets")
            .displayName("popularbets")
            .sortOrder(3.0)
            .enabled(true)
            .brand("bma")
            .sportId(16)
            .trendingTabs(null)
            .build();
    Mockito.when(mongockTemplate.findOne(Mockito.any(), Mockito.any())).thenReturn(sportTab);
    databaseChangeLog.addForYouTabsForPopularBets(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.atLeastOnce()).save(Mockito.any());
  }

  @Test
  public void testAddBybWidgetModule() {
    databaseChangeLog.addBybWidgetModule(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.atLeastOnce())
        .insert(Mockito.any(SportModule.class), Mockito.anyString());
  }

  @Test
  public void testAddSuperButtonModule() {
    databaseChangeLog.addSuperButtonModule(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.atLeastOnce())
        .insert(Mockito.any(SportModule.class), Mockito.anyString());
  }

  @Test
  public void initLuckyDipSportsModuleTest() {
    SportModule sportModule = createSportModule(0);
    sportModule.setModuleType(SportModuleType.RACING_MODULE);
    Mockito.when(mongockTemplate.find(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(Arrays.asList(sportModule));
    databaseChangeLog.initLuckyDipSportsModule(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.atLeastOnce())
        .insert(Mockito.any(SportModule.class), Mockito.anyString());
  }

  @Test
  public void initLuckyDipSportsModuleTestWhenDataEmpty() {
    Mockito.when(mongockTemplate.find(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(new ArrayList<>());
    databaseChangeLog.initLuckyDipSportsModule(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(0))
        .insert(Mockito.any(SportModule.class), Mockito.anyString());
  }

  @Test
  public void initLuckyDipSportsModuleTestWithException() {
    Mockito.when(mongockTemplate.find(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(null);
    Assertions.assertThatExceptionOfType(NullPointerException.class)
        .isThrownBy(() -> databaseChangeLog.initLuckyDipSportsModule(mongockTemplate));
  }

  @Test
  public void initLuckyDipSportsModuleWhenLDipModuleAlreadyExistTest() {
    SportModule sportModule = createSportModule(0);
    sportModule.setModuleType(SportModuleType.LUCKY_DIP);
    Mockito.when(mongockTemplate.find(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(Arrays.asList(sportModule));
    databaseChangeLog.initLuckyDipSportsModule(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(0))
        .insert(Mockito.any(SportModule.class), Mockito.anyString());
  }

  private SportModule createSportModule(Integer sportId) {
    SportModule module = new SportModule();
    module.setSportId(sportId);
    module.setPageId(String.valueOf(sportId));
    module.setId(String.valueOf(sportId) + new Random().nextInt());
    module.setPageType(PageType.sport);
    return module;
  }
}
