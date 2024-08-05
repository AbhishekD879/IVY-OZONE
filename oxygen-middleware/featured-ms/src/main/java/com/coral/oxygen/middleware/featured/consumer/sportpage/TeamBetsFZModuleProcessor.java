package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModuleDataItem;
import com.coral.oxygen.middleware.pojos.model.cms.featured.TeamBets;
import com.coral.oxygen.middleware.pojos.model.output.featured.FanzoneSegmentView;
import com.coral.oxygen.middleware.pojos.model.output.featured.TeamBetsConfig;
import com.coral.oxygen.middleware.pojos.model.output.featured.TeamBetsModule;
import com.newrelic.api.agent.NewRelic;
import java.util.*;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Service;

@Service
public class TeamBetsFZModuleProcessor implements ModuleConsumer<TeamBetsModule> {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private static final String FANZONEPAGEID = "160";

  @Override
  public TeamBetsModule processModule(
      SportPageModule sportPageModule,
      CmsSystemConfig cmsSystemConfig,
      Set<Long> excludedEventIds) {
    try {

      if (!FANZONEPAGEID.equals(sportPageModule.getSportModule().getPageId())) {
        throw new IllegalArgumentException(
            "Bets based on your team module can only be created for the fanzone category (page ID 160)");
      }
      TeamBetsModule module = new TeamBetsModule(sportPageModule.getSportModule());
      List<TeamBetsConfig> data =
          sportPageModule.getPageData().stream()
              .map(TeamBets.class::cast)
              .map(
                  (TeamBets teamBets) -> {
                    TeamBetsConfig teamBetsConfig = new TeamBetsConfig();
                    teamBetsConfig.setFanzoneSegments(teamBets.getFanzoneSegments());
                    teamBetsConfig.setId(UUID.randomUUID().toString());
                    teamBetsConfig.setNoOfMaxSelections(teamBets.getNoOfMaxSelections());
                    teamBetsConfig.setEnableBackedTimes(teamBets.isEnableBackedTimes());
                    teamBetsConfig.setPageType(teamBets.getPageType());
                    return teamBetsConfig;
                  })
              .collect(Collectors.toCollection(ArrayList::new));
      module.setData(data);
      module.setFanzoneSegments(
          sportPageModule.getPageData().stream()
              .map(SportPageModuleDataItem::getFanzoneSegments)
              .flatMap(List::stream)
              .toList());
      return module;
    } catch (Exception e) {
      TeamBetsModule module = new TeamBetsModule();
      module.setErrorMessage(e.getMessage());
      NewRelic.noticeError(e);
      ASYNC_LOGGER.warn(
          "Bets based on your team module for sportId 160 was defected by reason [Error Message ]: >> {} ",
          e.getMessage());
      return module;
    }
  }

  public void processFanzoneSegmentwiseModules(
      TeamBetsModule module, Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules) {
    ASYNC_LOGGER.info(
        "Started executing processFanzoneSegmentwiseModules for fanzone Bets based on your team ");
    module
        .getData()
        .forEach(
            (TeamBetsConfig data) ->
                data.getFanzoneSegments()
                    .forEach(
                        (String teamId) -> {
                          FanzoneSegmentView fanzoneSegmentView =
                              fanzoneSegmentWiseModules.containsKey(teamId)
                                  ? fanzoneSegmentWiseModules.get(teamId)
                                  : new FanzoneSegmentView();

                          Map<String, TeamBetsConfig> teamBetsModuleData =
                              fanzoneSegmentView.getTeamBetsModuleData();

                          data.setSegments(null);
                          teamBetsModuleData.put(data.getId(), data);
                          fanzoneSegmentWiseModules.put(teamId, fanzoneSegmentView);
                          updateFanzoneModuleSegmentView(teamId, data, module);
                        }));
    ASYNC_LOGGER.info(
        "Ended executing processFanzoneSegmentwiseModules for fanzone Bets based on your team ");
  }

  private void updateFanzoneModuleSegmentView(
      String teamId, TeamBetsConfig data, TeamBetsModule module) {
    Map<String, FanzoneSegmentView> fanzoneModuleSegmentView = module.getFanzoneModuleSegmentView();
    FanzoneSegmentView fanzoneSegmentView =
        fanzoneModuleSegmentView.containsKey(teamId)
            ? fanzoneModuleSegmentView.get(teamId)
            : new FanzoneSegmentView();
    fanzoneSegmentView.getTeamBetsModuleData().put(data.getId(), data);
    fanzoneModuleSegmentView.put(teamId, fanzoneSegmentView);
    module.setFanzoneModuleSegmentView(fanzoneModuleSegmentView);
  }
}
