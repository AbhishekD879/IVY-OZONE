package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.middleware.common.service.featured.OddsCardHeader;
import com.coral.oxygen.middleware.featured.service.FeaturedDataFilter;
import com.coral.oxygen.middleware.featured.service.injector.SingleOutcomeEventsModuleInjector;
import com.coral.oxygen.middleware.pojos.model.cms.Fanzone;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SurfaceBet;
import com.coral.oxygen.middleware.pojos.model.output.featured.FanzoneSegmentView;
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModuleData;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * This class is used for prepare Surfacebets for Fanzone Page by interacting with Site Serve and
 * CMS
 */
@SuppressWarnings("java:S4605")
@Service
@Slf4j
public class FanzoneSurfaceBetModuleProcessor extends SurfaceBetModuleProcessor {
  private final CmsService cmsService;

  public FanzoneSurfaceBetModuleProcessor(
      SingleOutcomeEventsModuleInjector singleOutcomeDataInjector,
      OddsCardHeader oddsCardHeader,
      FeaturedDataFilter featuredDataFilter,
      CmsService cmsService) {
    super(singleOutcomeDataInjector, oddsCardHeader, featuredDataFilter);
    this.cmsService = cmsService;
  }

  /**
   * This Method will Map CMS Surfacebet data to SurfacebetModule Data
   *
   * @param surfaceBet Cms Module contains surfacebet inforamtion
   * @return returns SurfaceBetModuleData
   */
  @Override
  protected SurfaceBetModuleData createEventData(SurfaceBet surfaceBet) {
    log.info("Started executing createEventData for fanzone sb");
    SurfaceBetModuleData data = new SurfaceBetModuleData();
    commonToSurfaceBetModule(data, surfaceBet);
    validateFanZoneForSurfaceBet(surfaceBet);
    data.setFanzoneSegments(surfaceBet.getFanzoneSegments());
    log.info("Ended executing createEventData for fanzone sb");
    return data;
  }

  /**
   * Fanzone BMA-62181: validateFanZoneForSurfaceBet and FanzoneSegments
   *
   * @param module it is SurfaceBetModule used for Validation
   */
  private void validateFanZoneForSurfaceBet(SurfaceBet module) {
    log.info("Started executing validateFanZoneForSurfaceBet");
    List<Fanzone> fanZones = new ArrayList<>(cmsService.getFanzones());
    List<String> configuredFzSegments = new ArrayList<>();
    List<String> fanzoneSegments = module.getFanzoneSegments();
    fanZones.forEach((Fanzone fanZone) -> configuredFzSegments.add(fanZone.getTeamId()));
    if (fanzoneSegments.retainAll(configuredFzSegments)) module.setFanzoneSegments(fanzoneSegments);
    log.info("Ended executing validateFanZoneForSurfaceBet");
  }

  /**
   * Fanzone BMA-62181: processFanzoneSegmentwiseModules for each Segment to prepare the SurfaceBet
   * Module.
   *
   * @param module this module used to prepare Fanzone segment structure
   * @param fanzoneSegmentWiseModules it is used to create Fanzone Data structure
   */
  public void processFanzoneSegmentwiseModules(
      SurfaceBetModule module, Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules) {
    log.info("Started executing processFanzoneSegmentwiseModules for fanzone sb ");
    module
        .getData()
        .forEach(
            (SurfaceBetModuleData data) ->
                data.getFanzoneSegments()
                    .forEach(
                        (String teamId) -> {
                          FanzoneSegmentView fanzoneSegmentView =
                              fanzoneSegmentWiseModules.containsKey(teamId)
                                  ? fanzoneSegmentWiseModules.get(teamId)
                                  : new FanzoneSegmentView();

                          Map<String, SurfaceBetModuleData> surfaceBetModuleData =
                              fanzoneSegmentView.getSurfaceBetModuleData();
                          // setting segments and fanzone segments null to avoid display of unused
                          // data
                          data.setSegments(null);
                          surfaceBetModuleData.put(data.getObjId(), data);
                          fanzoneSegmentWiseModules.put(teamId, fanzoneSegmentView);
                          updateFanzoneModuleSegmentView(teamId, data, module);
                        }));
    log.info("Ended executing processFanzoneSegmentwiseModules for fanzone sb ");
  }

  /**
   * creating fanzoneModuleSegmentView for each module to get MODULE_CONTENT_CHANGE
   *
   * @param teamId is the unique opta Id of each team
   * @param data is the individual surfacebet data
   * @param module is SurfaceBetModule to be processed
   */
  private void updateFanzoneModuleSegmentView(
      String teamId, SurfaceBetModuleData data, SurfaceBetModule module) {
    Map<String, FanzoneSegmentView> fanzoneModuleSegmentView = module.getFanzoneModuleSegmentView();
    FanzoneSegmentView fanzoneSegmentView =
        fanzoneModuleSegmentView.containsKey(teamId)
            ? fanzoneModuleSegmentView.get(teamId)
            : new FanzoneSegmentView();
    fanzoneSegmentView.getSurfaceBetModuleData().put(data.getObjId(), data);
    fanzoneModuleSegmentView.put(teamId, fanzoneSegmentView);
    module.setFanzoneModuleSegmentView(fanzoneModuleSegmentView);
  }
}
