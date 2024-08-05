package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.FanBets;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModuleDataItem;
import com.coral.oxygen.middleware.pojos.model.output.featured.FanBetsConfig;
import com.coral.oxygen.middleware.pojos.model.output.featured.FanBetsModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.FanzoneSegmentView;
import com.newrelic.api.agent.NewRelic;
import java.util.*;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Service;

@Service
public class FanBetsFZModuleProcessor implements ModuleConsumer<FanBetsModule> {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private static final String FANZONEPAGEID = "160";

  @Override
  public FanBetsModule processModule(
      SportPageModule sportPageModule,
      CmsSystemConfig cmsSystemConfig,
      Set<Long> excludedEventIds) {
    try {
      if (!FANZONEPAGEID.equals(sportPageModule.getSportModule().getPageId())) {
        throw new IllegalArgumentException(
            "Bets based on other fans module can only be created for the fanzone category (page ID 160)");
      }
      FanBetsModule module = new FanBetsModule(sportPageModule.getSportModule());
      List<FanBetsConfig> data =
          sportPageModule.getPageData().stream()
              .map(FanBets.class::cast)
              .map(
                  (FanBets fanBets) -> {
                    FanBetsConfig fanBetsConfig = new FanBetsConfig();
                    fanBetsConfig.setFanzoneSegments(fanBets.getFanzoneSegments());
                    fanBetsConfig.setId(UUID.randomUUID().toString());
                    fanBetsConfig.setNoOfMaxSelections(fanBets.getNoOfMaxSelections());
                    fanBetsConfig.setEnableBackedTimes(fanBets.isEnableBackedTimes());
                    fanBetsConfig.setPageType(fanBets.getPageType());
                    return fanBetsConfig;
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
      FanBetsModule module = new FanBetsModule();
      module.setErrorMessage(e.getMessage());
      NewRelic.noticeError(e);
      ASYNC_LOGGER.warn(
          "Bets based on other fans module for sportId 160 was defected by reason [Error Message ]: >> {} ",
          e.getMessage());
      return module;
    }
  }

  public void processFanzoneSegmentwiseModules(
      FanBetsModule module, Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules) {
    ASYNC_LOGGER.info(
        "Started executing processFanzoneSegmentwiseModules for fanzone Bets based on other fans ");
    module
        .getData()
        .forEach(
            (FanBetsConfig data) ->
                data.getFanzoneSegments()
                    .forEach(
                        (String teamId) -> {
                          FanzoneSegmentView fanzoneSegmentView =
                              fanzoneSegmentWiseModules.containsKey(teamId)
                                  ? fanzoneSegmentWiseModules.get(teamId)
                                  : new FanzoneSegmentView();

                          Map<String, FanBetsConfig> fanBetsModuleData =
                              fanzoneSegmentView.getFanBetsModuleData();

                          data.setSegments(null);
                          fanBetsModuleData.put(data.getId(), data);
                          fanzoneSegmentWiseModules.put(teamId, fanzoneSegmentView);
                          updateFanzoneModuleSegmentView(teamId, data, module);
                        }));
    ASYNC_LOGGER.info(
        "Ended executing processFanzoneSegmentwiseModules for fanzone Bets based on your team ");
  }

  private void updateFanzoneModuleSegmentView(
      String teamId, FanBetsConfig data, FanBetsModule module) {
    Map<String, FanzoneSegmentView> fanzoneModuleSegmentView = module.getFanzoneModuleSegmentView();
    FanzoneSegmentView fanzoneSegmentView =
        fanzoneModuleSegmentView.containsKey(teamId)
            ? fanzoneModuleSegmentView.get(teamId)
            : new FanzoneSegmentView();
    fanzoneSegmentView.getFanBetsModuleData().put(data.getId(), data);
    fanzoneModuleSegmentView.put(teamId, fanzoneSegmentView);
    module.setFanzoneModuleSegmentView(fanzoneModuleSegmentView);
  }
}
