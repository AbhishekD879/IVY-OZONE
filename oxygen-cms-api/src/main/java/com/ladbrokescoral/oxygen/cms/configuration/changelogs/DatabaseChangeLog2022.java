package com.ladbrokescoral.oxygen.cms.configuration.changelogs;

import com.github.cloudyrock.mongock.ChangeLog;
import com.github.cloudyrock.mongock.ChangeSet;
import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTabMetaData;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.MainTier1Sports;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.Tier1SportTabsTemplate;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.UntiedSportTabsTemplate;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.UntiedSports;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.script.*;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.script.ConfigsBrandMenuUpdate;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.script.SportTabsMarketNamesMigrator;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.script.SportTabsMigrator;
import java.util.Arrays;

@ChangeLog(order = "002")
public class DatabaseChangeLog2022 {

  private static final String CORAL = "bma";
  private static final String LADBROKES = "ladbrokes";

  /**
   * As author, developer name to be specified Note, method rename as well as order, id change leads
   * to the changeset being run again
   */
  @ChangeSet(order = "01", id = "updateSegmentMenu", author = "system")
  public void updateSegmentMenu(MongockTemplate mongockTemplate) {
    new ConfigsBrandMenuUpdate().updateSegmentMenu(mongockTemplate, CORAL);
    new ConfigsBrandMenuUpdate().updateSegmentMenu(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "02", id = "updateOnBoardingMenu", author = "system")
  public void updateOnBoardingMenu(MongockTemplate mongockTemplate) {
    new ConfigsBrandMenuUpdate().updateOnBoardingMenu(mongockTemplate, CORAL);
    new ConfigsBrandMenuUpdate().updateOnBoardingMenu(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "02", id = "saveSportTabsMarketNames", author = "system")
  public void saveSportTabsMarketNames(MongockTemplate mongockTemplate) {
    SportTabsMarketNamesMigrator migrator = new SportTabsMarketNamesMigrator(mongockTemplate);
    migrator.saveSportsTabMarketNames(CORAL);
    migrator.saveSportsTabMarketNames(LADBROKES);
  }

  @ChangeSet(order = "03", id = "addTabForGolf", author = "system")
  public void addTabForGolf(MongockTemplate mongockTemplate) {
    SportTabsMigrator stm = new SportTabsMigrator(mongockTemplate);
    stm.addTabsForGolf(mongockTemplate, CORAL);
    stm.addTabsForGolf(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "04", id = "addTabForInplayGolf", author = "system")
  public void addTabForInPlayGolf(MongockTemplate mongockTemplate) {
    SportTabsMigrator stm = new SportTabsMigrator(mongockTemplate);
    stm.addTabsForInplayGolf(mongockTemplate, CORAL);
    stm.addTabsForInplayGolf(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "05", id = "addTabsForUntiedSportForGreyHoundsToday", author = "system")
  public void addTabsForUntiedSportForGreyhoundsToday(MongockTemplate mongockTemplate) {
    SportTabsMigrator stm = new SportTabsMigrator(mongockTemplate);
    SportTabMetaData sportTabMetaDataCORALToday =
        new SportTabMetaData(
            mongockTemplate,
            CORAL,
            UntiedSports.GREYHOUNDS,
            new UntiedSportTabsTemplate(),
            String.valueOf(SportTabNames.TODAY));
    stm.addTabsForAnySportTier(sportTabMetaDataCORALToday);
    SportTabMetaData sportTabMetaDataLADSToday =
        new SportTabMetaData(
            mongockTemplate,
            LADBROKES,
            UntiedSports.GREYHOUNDS,
            new UntiedSportTabsTemplate(),
            String.valueOf(SportTabNames.TODAY));
    stm.addTabsForAnySportTier(sportTabMetaDataLADSToday);
  }

  @ChangeSet(order = "06", id = "addTabsForUntiedSportForGreyHoundsTomorrow", author = "system")
  public void addTabsForUntiedSportForGreyhoundsTomorrow(MongockTemplate mongockTemplate) {
    SportTabsMigrator stm = new SportTabsMigrator(mongockTemplate);
    SportTabMetaData sportTabMetaDataCORALTomorrow =
        new SportTabMetaData(
            mongockTemplate,
            CORAL,
            UntiedSports.GREYHOUNDS,
            new UntiedSportTabsTemplate(),
            String.valueOf(SportTabNames.TOMORROW));
    stm.addTabsForAnySportTier(sportTabMetaDataCORALTomorrow);
    SportTabMetaData sportTabMetaDataLADSTomorrow =
        new SportTabMetaData(
            mongockTemplate,
            LADBROKES,
            UntiedSports.GREYHOUNDS,
            new UntiedSportTabsTemplate(),
            String.valueOf(SportTabNames.TOMORROW));
    stm.addTabsForAnySportTier(sportTabMetaDataLADSTomorrow);
  }

  @ChangeSet(order = "07", id = "addTabsForUntiedSportForHorseRacing", author = "system")
  public void addTabsForUntiedSportForHorseRacing(MongockTemplate mongockTemplate) {
    SportTabsMigrator stm = new SportTabsMigrator(mongockTemplate);
    SportTabMetaData sportTabMetaDataCORALMeetings =
        new SportTabMetaData(
            mongockTemplate,
            CORAL,
            UntiedSports.HORSERACING,
            new UntiedSportTabsTemplate(),
            String.valueOf(SportTabNames.MEETINGS));
    SportTabMetaData sportTabMetaDataLADSMeetings =
        new SportTabMetaData(
            mongockTemplate,
            LADBROKES,
            UntiedSports.HORSERACING,
            new UntiedSportTabsTemplate(),
            String.valueOf(SportTabNames.MEETINGS));

    stm.addTabsForAnySportTier(sportTabMetaDataCORALMeetings);
    stm.addTabsForAnySportTier(sportTabMetaDataLADSMeetings);
  }

  @ChangeSet(order = "08", id = "addTabsForTier1SportForPopularBets", author = "system")
  public void addTabsForTier1SportForPopularBets(MongockTemplate mongockTemplate) {
    SportTabsMigrator stm = new SportTabsMigrator(mongockTemplate);
    SportTabMetaData sportTabMetaDataCORALMeetings =
        new SportTabMetaData(
            mongockTemplate,
            CORAL,
            MainTier1Sports.FOOTBALL,
            new Tier1SportTabsTemplate(),
            String.valueOf(SportTabNames.POPULARBETS));
    SportTabMetaData sportTabMetaDataLADSMeetings =
        new SportTabMetaData(
            mongockTemplate,
            LADBROKES,
            MainTier1Sports.FOOTBALL,
            new Tier1SportTabsTemplate(),
            String.valueOf(SportTabNames.POPULARBETS));

    stm.addTabsForAnySportTier(sportTabMetaDataCORALMeetings);
    stm.addTabsForAnySportTier(sportTabMetaDataLADSMeetings);
  }

  @ChangeSet(order = "09", id = "addBetsBasedOnYourTeamModuleForFanzone", author = "system")
  public void createBetsBasedOnYourTeamForFanzone(MongockTemplate mongockTemplate) {
    new TeamAndFansBetsModuleUpdate()
        .createBetsModulesForFanzone(mongockTemplate, SportModuleType.BETS_BASED_ON_YOUR_TEAM);
  }

  @ChangeSet(order = "10", id = "addBetsBasedOnOtherFansModuleForFanzone", author = "system")
  public void createBetsBasedOnOtherFansForFanzone(MongockTemplate mongockTemplate) {
    new TeamAndFansBetsModuleUpdate()
        .createBetsModulesForFanzone(mongockTemplate, SportModuleType.BETS_BASED_ON_OTHER_FANS);
  }

  @ChangeSet(order = "11", id = "addForYouTabsForPopularBets", author = "system")
  public void addForYouTabsForPopularBets(MongockTemplate mongockTemplate) {
    SportTabsMigrator stm = new SportTabsMigrator(mongockTemplate);
    stm.addOrUpdateTrendingTabsForSportTab(
        LADBROKES,
        MainTier1Sports.FOOTBALL.getCategoryId(),
        SportTabNames.POPULARBETS.nameLowerCase(),
        "insights-forYou",
        "for-you",
        Arrays.asList("for-you-personalized-bets"));
    stm.addOrUpdateTrendingTabsForSportTab(
        CORAL,
        MainTier1Sports.FOOTBALL.getCategoryId(),
        SportTabNames.POPULARBETS.nameLowerCase(),
        "insights-forYou",
        "for-you",
        Arrays.asList("for-you-personalized-bets"));
  }

  @ChangeSet(order = "12", id = "addBybWidgetModule", author = "system")
  public void addBybWidgetModule(MongockTemplate mongockTemplate) {
    new SportModulesUpdate().addBybWidgetModule(mongockTemplate, CORAL);
    new SportModulesUpdate().addBybWidgetModule(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "13", id = "initHomePageLuckyDipSportModule", author = "Rakesh.Bonu")
  public void initLuckyDipSportsModule(MongockTemplate mongockTemplate) {
    new SportModulesUpdate().addLuckyDipSportModule(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "15", id = "addSuperButtonModule", author = "system")
  public void addSuperButtonModule(MongockTemplate mongockTemplate) {
    new SportModulesUpdate().addSuperButtonModule(mongockTemplate, LADBROKES);
    new SportModulesUpdate().addSuperButtonModule(mongockTemplate, CORAL);
  }
}
