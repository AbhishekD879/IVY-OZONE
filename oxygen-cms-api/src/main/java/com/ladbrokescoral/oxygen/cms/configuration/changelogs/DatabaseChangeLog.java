package com.ladbrokescoral.oxygen.cms.configuration.changelogs;

import com.github.cloudyrock.mongock.ChangeLog;
import com.github.cloudyrock.mongock.ChangeSet;
import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.script.*;
import com.mongodb.client.model.IndexOptions;
import org.bson.Document;
import org.springframework.context.annotation.Profile;
import org.springframework.core.env.Environment;

@ChangeLog(order = "001")
public class DatabaseChangeLog {

  private static final String CORAL = "bma";
  private static final String LADBROKES = "ladbrokes";

  // NeedCodeChange: remove all "vanilla" clues
  private static final String LADBROKES_VANILLA = "vanilla";

  /**
   * As author, developer name to be specified Note, method rename as well as order, id change leads
   * to the changeset being run again
   */
  @ChangeSet(order = "001", id = "initialSsrConfigSetupV1", author = "ikovalovska")
  public void basicSsrConfigSetup(MongockTemplate mongockTemplate) {
    new ConfigsBrandMenuUpdate().updateSsrConfig(mongockTemplate, CORAL);
  }

  @ChangeSet(order = "002", id = "initialSsrConfigSetupLadbrokesV1", author = "mzobro")
  public void basicSsrConfigSetupLadbrokes(MongockTemplate mongockTemplate) {
    new ConfigsBrandMenuUpdate().updateSsrConfig(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "001", id = "initialSportsPagesSetupV1", author = "ikovalovska")
  public void basicSportsPagesSetup(MongockTemplate mongockTemplate) {
    new SportPagesMenuUpdate().initSportPagesMenu(mongockTemplate, CORAL);
  }

  @ChangeSet(order = "003", id = "initialSportsPagesSetupLadbrokesV1", author = "mzobro")
  public void basicSportsPagesSetupLadbrokes(MongockTemplate mongockTemplate) {
    new SportPagesMenuUpdate().initSportPagesMenu(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "004", id = "addSportsPagesSubMenuItems", author = "mzobro")
  public void addSportsPagesSubMenuItems(MongockTemplate mongockTemplate) {
    new SportPagesMenuUpdate().addSportPagesSubMenus(mongockTemplate, CORAL);
    new SportPagesMenuUpdate().addSportPagesSubMenus(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "005", id = "updateInitialSsrConfigStructure", author = "mzobro")
  public void updateSsrConfigSetupDefaultValues(MongockTemplate mongockTemplate) {
    new ConfigsBrandMenuUpdate().updateSSRConfigDefaultValue(mongockTemplate, CORAL);
    new ConfigsBrandMenuUpdate().updateSSRConfigDefaultValue(mongockTemplate, LADBROKES);
  }

  /**
   * it might be useful to run the ChangeSet on each deployment to create required modules for all
   * sport categories. However, this will consume startup time by adding extra checks
   */
  @ChangeSet(order = "006", id = "initSportModulesV1", author = "mzobro")
  public void initSportsModules(MongockTemplate mongockTemplate) {
    new SportModulesUpdate().initSportModules(mongockTemplate, CORAL);
    new SportModulesUpdate().initSportModules(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "007", id = "initQuestionEngineMenu", author = "ikovalovska")
  public void initQuestionEngineMenu(MongockTemplate mongockTemplate) {
    new QuestionEngineMenuUpdate().initQuestionEngineMenu(mongockTemplate, CORAL);
    new QuestionEngineMenuUpdate().initQuestionEngineMenu(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "009", id = "updateBipScoreEventsConfig", author = "abanul")
  public void updateBipScoreEventsConfig(MongockTemplate mongockTemplate) {
    new BipScoreEventsUpdate().updateBipScoreEventsValue(mongockTemplate, CORAL);
    new BipScoreEventsUpdate().updateBipScoreEventsValue(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "011", id = "updateTier1SportTabs", author = "mzobro")
  public void updateTier1SportTabs(MongockTemplate mongockTemplate) {
    SportTabsMigrator migrator = new SportTabsMigrator(mongockTemplate);
    migrator.updateCheckEventsForTier1SportsTab(CORAL);
    migrator.updateCheckEventsForTier1SportsTab(LADBROKES);
  }

  @ChangeSet(order = "012", id = "createAEMBannersModules", author = "aliaksei.yarotski")
  public void createAemBanners(MongockTemplate mongockTemplate) {
    new SportModulesUpdate().createAemBanners(mongockTemplate, CORAL);
    new SportModulesUpdate().createAemBanners(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "014", id = "initial5ASideConfigSetupV1", author = "akurtiak")
  public void basic5ASideConfigSetup(MongockTemplate mongockTemplate) {
    new ConfigsBrandMenuUpdate().update5ASideConfig(mongockTemplate, CORAL);
  }

  @ChangeSet(order = "015", id = "initial5ASideConfigSetupLadbrokesV1", author = "akurtiak")
  public void basic5ASideConfigSetupLadbrokes(MongockTemplate mongockTemplate) {
    new ConfigsBrandMenuUpdate().update5ASideConfig(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "016", id = "updateBybMenuV1", author = "akurtiak")
  public void updateBybMenuV1(MongockTemplate mongockTemplate) {
    new BybMenuUpdate().updateBybMenu(mongockTemplate, CORAL);
  }

  @ChangeSet(order = "017", id = "updateBybMenuLadbrokesV1", author = "akurtiak")
  public void updateBybMenuLadbrokes(MongockTemplate mongockTemplate) {
    new BybMenuUpdate().updateBybMenu(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "019", id = "moveTier3ToTier2-Ladbrokes", author = "andrii.kravchuk")
  public void moveTier3ToTier2ForLadbrokes(MongockTemplate mongockTemplate) {
    SportCategoriesMigrator categoriesMigrator = new SportCategoriesMigrator(mongockTemplate);
    categoriesMigrator.updateSportsTier(LADBROKES);

    SportTabsMigrator sportTabsMigrator = new SportTabsMigrator(mongockTemplate);
    sportTabsMigrator.updateSportsTabsAccordingToTemplates(LADBROKES);
  }

  @ChangeSet(order = "020", id = "updateSportSettings-Ladbrokes", author = "andrii.kravchuk")
  public void updateSportSettingsForLadbrkoes(MongockTemplate mongockTemplate) {
    new SportCategoriesMigrator(mongockTemplate).updateSportSettings(LADBROKES);
  }

  @ChangeSet(order = "021", id = "addAssetManagement", author = "akurtiak")
  public void addAssetManagement(MongockTemplate mongockTemplate) {
    new BybMenuUpdate().addAssetManagementMenu(mongockTemplate, CORAL);
  }

  @ChangeSet(order = "022", id = "addAssetManagementLadbrokes", author = "akurtiak")
  public void addAssetManagementLadbrokes(MongockTemplate mongockTemplate) {
    new BybMenuUpdate().addAssetManagementMenu(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "024", id = "moveTier3ToTier2-Coral", author = "andrii.kravchuk")
  public void moveTier3ToTier2ForCoral(MongockTemplate mongockTemplate) {
    SportCategoriesMigrator categoriesMigrator = new SportCategoriesMigrator(mongockTemplate);
    categoriesMigrator.updateSportsTier(CORAL);

    SportTabsMigrator sportTabsMigrator = new SportTabsMigrator(mongockTemplate);
    sportTabsMigrator.updateSportsTabsAccordingToTemplates(CORAL);
  }

  @ChangeSet(order = "025", id = "updateSportSettings-Coral", author = "andrii.kravchuk")
  public void updateSportSettingsForCoral(MongockTemplate mongockTemplate) {
    new SportCategoriesMigrator(mongockTemplate).updateSportSettings(CORAL);
  }

  @ChangeSet(order = "027", id = "moveTier3ToTier2-VanillaLB", author = "andrii.kravchuk")
  public void moveTier3ToTier2ForVanillaLB(MongockTemplate mongockTemplate) {
    SportCategoriesMigrator categoriesMigrator = new SportCategoriesMigrator(mongockTemplate);
    categoriesMigrator.updateSportsTier(LADBROKES_VANILLA);

    SportTabsMigrator sportTabsMigrator = new SportTabsMigrator(mongockTemplate);
    sportTabsMigrator.updateSportsTabsAccordingToTemplates(LADBROKES_VANILLA);
  }

  @ChangeSet(order = "028", id = "updateSportSettings-VanillaLB", author = "andrii.kravchuk")
  public void updateSportSettingsForVanillaLB(MongockTemplate mongockTemplate) {
    new SportCategoriesMigrator(mongockTemplate).updateSportSettings(LADBROKES_VANILLA);
  }

  @ChangeSet(order = "029", id = "insertRacingModules", author = "bohdan.laba")
  public void addRacingModules(MongockTemplate mongockTemplate) {
    new RacingModuleUpdate(mongockTemplate).addRacingModules(CORAL);
    new RacingModuleUpdate(mongockTemplate).addRacingModules(LADBROKES);
  }

  /**
   * @deprecated As of v108. remove this and #SportTabsMigrator
   * @param mongockTemplate
   */
  @Deprecated
  @ChangeSet(order = "030", id = "removeDuplicateTabs", author = "marta.zobro")
  public void removeDuplicateTabs(MongockTemplate mongockTemplate) {

    SportTabsMigrator sportTabsMigrator = new SportTabsMigrator(mongockTemplate);
    sportTabsMigrator.removeDuplicateTabs(CORAL);
    sportTabsMigrator.removeDuplicateTabs(LADBROKES);
    sportTabsMigrator.removeDuplicateTabs(LADBROKES_VANILLA);

    // @deprecated As of v108. make sure to uncomment index here: #SportTab
    mongockTemplate
        .getCollection("sporttabs")
        .createIndex(
            new Document().append("brand", 1).append("sportId", 1).append("name", 1),
            new IndexOptions().name("brand_sport_name_unique").unique(true));
  }

  @ChangeSet(order = "031", id = "migrateSystemConfigurations", author = "marta.zobro")
  public void migrateSystemConfigurations(MongockTemplate mongockTemplate) {
    new SystemConfigurationsUpdate(mongockTemplate).migrateAllConfigs();
  }

  @ChangeSet(order = "031", id = "insertRacingModules-Ladbrokes", author = "bohdan.laba")
  public void addRacingModulesLadbrokes(MongockTemplate mongockTemplate) {
    new RacingModuleUpdate(mongockTemplate).addRacingModules(LADBROKES);
  }

  @ChangeSet(order = "032", id = "insertRacingModules-Coral", author = "bohdan.laba")
  public void addRacingModulesCoral(MongockTemplate mongockTemplate) {
    new RacingModuleUpdate(mongockTemplate).addRacingModules(CORAL);
  }

  @ChangeSet(order = "033", id = "initOptInSecrets", author = "marta.zobro")
  public void initOptInSecrets(MongockTemplate mongockTemplate) {
    new SecretUpdate(mongockTemplate).initOptInSecrets(CORAL);
    new SecretUpdate(mongockTemplate).initOptInSecrets(LADBROKES);
    new SecretUpdate(mongockTemplate).initOptInSecrets(LADBROKES_VANILLA);
  }

  @ChangeSet(order = "034", id = "updateNativeConfig", author = "kwandzel")
  public void updateNativeConfig(MongockTemplate mongockTemplate) {
    new ConfigsBrandMenuUpdate().updateNativeConfig(mongockTemplate, CORAL);
    new ConfigsBrandMenuUpdate().updateNativeConfig(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "035", id = "addUngroupedFeaturedModule", author = "kwandzel")
  public void updateUngroupedFeatured(MongockTemplate mongockTemplate) {
    new SportModulesUpdate().addUngroupedFeaturedSportsModuleForHomepage(mongockTemplate, CORAL);
    new SportModulesUpdate()
        .addUngroupedFeaturedSportsModuleForHomepage(mongockTemplate, LADBROKES);
  }

  @ChangeSet(
      order = "037",
      id = "updateUkIrishRacingAndModulesDefaultConfigs",
      author = "marta.zobro")
  public void updateUkIrishRacingAndModulesDefaultConfigs(MongockTemplate mongockTemplate) {
    new RacingModuleUpdate(mongockTemplate).updateUkIrishRacingAndModulesDefaultConfigs(CORAL);
    new RacingModuleUpdate(mongockTemplate).updateUkIrishRacingAndModulesDefaultConfigs(LADBROKES);
  }

  @ChangeSet(
      order = "038",
      id = "updateVirtualRacingModuleDefaultConfigsProd",
      author = "volodymyr.kulpa")
  public void updateVirtualRacingModuleDefaultConfigsOnProd(
      MongockTemplate mongockTemplate, Environment environment) {
    new RacingModuleUpdate(mongockTemplate, environment)
        .updateVirtualRacingModuleDefaultConfigs("PRD", CORAL);
    new RacingModuleUpdate(mongockTemplate, environment)
        .updateVirtualRacingModuleDefaultConfigs("PRD", LADBROKES);
  }

  @ChangeSet(
      order = "038",
      id = "updateVirtualRacingModuleDefaultConfigsDev",
      author = "volodymyr.kulpa")
  @Profile({"LOCAL", "DEV0", "DEV1", "DEV2", "DEV3", "TST0", "TST1"})
  public void updateVirtualRacingModuleDefaultConfigsOnDev(
      MongockTemplate mongockTemplate, Environment environment) {
    new RacingModuleUpdate(mongockTemplate, environment)
        .updateVirtualRacingModuleDefaultConfigs("TST", CORAL);
    new RacingModuleUpdate(mongockTemplate, environment)
        .updateVirtualRacingModuleDefaultConfigs("TST", LADBROKES);
  }

  @ChangeSet(
      order = "038",
      id = "updateVirtualRacingModuleDefaultConfigsStg",
      author = "volodymyr.kulpa")
  @Profile({"STG0"})
  public void updateVirtualRacingModuleDefaultConfigsOnStg(
      MongockTemplate mongockTemplate, Environment environment) {
    new RacingModuleUpdate(mongockTemplate, environment)
        .updateVirtualRacingModuleDefaultConfigs("STG", CORAL);
    new RacingModuleUpdate(mongockTemplate, environment)
        .updateVirtualRacingModuleDefaultConfigs("STG", LADBROKES);
  }

  @ChangeSet(order = "039", id = "updateRacingEventsModuleDefaultConfigs", author = "marta.zobro")
  public void updateRacingEventsModuleDefaultConfigs(MongockTemplate mongockTemplate) {
    RacingModuleUpdate racingModuleUpdate = new RacingModuleUpdate(mongockTemplate);
    racingModuleUpdate.updateRacingEventsModulesConfigs(CORAL);
    racingModuleUpdate.updateRacingEventsModulesConfigs(LADBROKES);
  }

  @ChangeSet(order = "040", id = "updateInternationalToteModuleConfig", author = "volodymyr.kulpa")
  public void updateInternationalToteModuleConfig(
      MongockTemplate mongockTemplate, Environment environment) {
    new RacingModuleUpdate(mongockTemplate, environment).updateInternationalToteModuleConfig(CORAL);
    new RacingModuleUpdate(mongockTemplate, environment)
        .updateInternationalToteModuleConfig(LADBROKES);
  }

  @ChangeSet(order = "039", id = "deactivateGreyhoundsRacingModules", author = "marta.zobro")
  public void deactivateGreyhoundsRacingModules(MongockTemplate mongockTemplate) {
    new RacingModuleUpdate(mongockTemplate).deactivateGreyhoundsRacingModules(CORAL);
    new RacingModuleUpdate(mongockTemplate).deactivateGreyhoundsRacingModules(LADBROKES);
  }

  @ChangeSet(order = "041", id = "addSegmentedModule", author = "system")
  public void addSegmentedModule(MongockTemplate mongockTemplate) {
    new SegmentedModuleCreate().addSegmentedModule(mongockTemplate);
  }

  @ChangeSet(order = "042", id = "addSegment", author = "system")
  public void addSegment(MongockTemplate mongockTemplate) {
    new SegmentCreate().addSegment(mongockTemplate);
  }

  @ChangeSet(order = "043", id = "deleteUnBrandRecords", author = "system")
  public void deleteUnBrandRecords(MongockTemplate mongockTemplate) {
    new DeleteUnBrandRecords().deleteUnBrandRecords(mongockTemplate);
  }

  @ChangeSet(order = "044", id = "addSeMgmentedModulesByBrand", author = "system")
  public void addSegmentedModuleByBrand(MongockTemplate mongockTemplate) {
    new SegmentedModuleCreate().addSegmentedModule(mongockTemplate, CORAL);
    new SegmentedModuleCreate().addSegmentedModule(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "045", id = "addSegmentsByBrand", author = "system")
  public void addSegmentByBrand(MongockTemplate mongockTemplate) {
    new SegmentCreate().addSegment(mongockTemplate, LADBROKES);
    new SegmentCreate().addSegment(mongockTemplate, CORAL);
  }

  @ChangeSet(order = "046", id = "addIndexOnSegments", author = "system")
  public void addIndexOnSegments(MongockTemplate mongockTemplate) {
    new SegmentIndexCreate().createIndex(mongockTemplate);
  }

  @ChangeSet(order = "047", id = "UpdateHomeModuleSortOrder", author = "system")
  public void updateSortOrderForHomeModules(MongockTemplate mongockTemplate) {
    new UpdateHomeModuleSortOrder().updateSortOrder(mongockTemplate);
  }

  @ChangeSet(order = "048", id = "addStatisticsLinksMenu", author = "system")
  public void addStatisticsLinksMenu(MongockTemplate mongockTemplate) {
    new StatisticsLinksMenuUpdate().init(mongockTemplate, CORAL);
    new StatisticsLinksMenuUpdate().init(mongockTemplate, LADBROKES);
  }

  @ChangeSet(order = "049", id = "addVirtualNextEventsModule", author = "vamsi.putta")
  public void addVirtualNextEventsModuleToVirtuals(MongockTemplate mongockTemplate) {
    new VirtualNextEventsModuleUpdate(mongockTemplate).addVirtualNextEventsModule(CORAL);
    new VirtualNextEventsModuleUpdate(mongockTemplate).addVirtualNextEventsModule(LADBROKES);
  }

  @ChangeSet(order = "050", id = "updateRgyEntityStructure", author = "system")
  public void updateRgyEntityStructure(MongockTemplate mongockTemplate) {
    new RgyModuleStructureUpdate(mongockTemplate).updateStructureInRgyModules(CORAL);
    new RgyModuleStructureUpdate(mongockTemplate).updateStructureInRgyModules(LADBROKES);
  }

  @ChangeSet(order = "051", id = "addPopularBetModuleToHomePageSports", author = "system")
  public void addPopularBetModuleToHomePageSports(MongockTemplate mongockTemplate) {
    // don't have for coral enable once coral popular bets added
    new PopularBetModuleUpdate(mongockTemplate).addPopularBetModule(LADBROKES);
  }

  @ChangeSet(order = "053", id = "inplayStatsSorting", author = "system")
  public void addTheInplayStatsSorting(MongockTemplate mongockTemplate) {
    new InplayStatsSortingUpdate(mongockTemplate).insertStats(CORAL);
    new InplayStatsSortingUpdate(mongockTemplate).insertStats(LADBROKES);
  }
}
