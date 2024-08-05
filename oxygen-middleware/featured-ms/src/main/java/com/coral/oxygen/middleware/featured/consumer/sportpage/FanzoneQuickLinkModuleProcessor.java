package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.pojos.model.output.featured.FanzoneSegmentView;
import com.coral.oxygen.middleware.pojos.model.output.featured.QuickLinkData;
import com.coral.oxygen.middleware.pojos.model.output.featured.QuickLinkModule;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@SuppressWarnings("java:S4605")
@Service
public class FanzoneQuickLinkModuleProcessor extends QuickLinkModuleProcessor {

  /**
   * processFanzoneSegmentwiseModules for each Segment
   *
   * @param module is QuickLinkModule Module to be processed
   * @param fanzoneSegmentWiseModules it will be used to prepare Fanzone structure for QL
   */
  public void processFanzoneSegmentwiseModules(
      QuickLinkModule module, Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules) {
    log.info("Started processFanzoneSegmentwiseModules for quicklink");
    module
        .getData()
        .forEach(
            (QuickLinkData data) ->
                data.getFanzoneSegments()
                    .forEach(
                        (String teamId) -> {
                          FanzoneSegmentView fanzoneSegmentView =
                              fanzoneSegmentWiseModules.containsKey(teamId)
                                  ? fanzoneSegmentWiseModules.get(teamId)
                                  : new FanzoneSegmentView();
                          Map<String, QuickLinkData> quickLinkModule =
                              fanzoneSegmentView.getQuickLinkModuleData();
                          quickLinkModule.put(data.getId(), data);
                          fanzoneSegmentWiseModules.put(teamId, fanzoneSegmentView);
                          updateFanzoneModuleSegmentView(teamId, data, module);
                        }));

    log.info("End processFanzoneSegmentwiseModules for quicklink");
  }
  /**
   * creating fanzoneModuleSegmentView for each module to get MODULE_CONTENT_CHANGE
   *
   * @param teamId is the unique opta id of each team
   * @param module is QuickLinkModule Module to be processed
   */
  private void updateFanzoneModuleSegmentView(
      String teamId, QuickLinkData data, QuickLinkModule module) {
    Map<String, FanzoneSegmentView> fanzoneModuleSegmentView = module.getFanzoneModuleSegmentView();
    FanzoneSegmentView fanzoneSegmentView =
        fanzoneModuleSegmentView.containsKey(teamId)
            ? fanzoneModuleSegmentView.get(teamId)
            : new FanzoneSegmentView();
    fanzoneSegmentView.getQuickLinkModuleData().put(data.getId(), data);
    fanzoneModuleSegmentView.put(teamId, fanzoneSegmentView);
    module.setFanzoneModuleSegmentView(fanzoneModuleSegmentView);
  }
}
