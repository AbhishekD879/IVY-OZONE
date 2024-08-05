package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SegmentReference;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModuleDataItem;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportsQuickLink;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class QuickLinkModuleProcessor
    implements ModuleConsumer<QuickLinkModule>, SegmentOrderProcessor {

  @Override
  public QuickLinkModule processModule(
      SportPageModule cmsModule, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds)
      throws SportsModuleProcessException {
    QuickLinkModule qlModule = new QuickLinkModule(cmsModule.getSportModule());
    List<QuickLinkData> data =
        cmsModule.getPageData().stream()
            .map(this::createQuickLinkData)
            .collect(Collectors.toList());
    qlModule.setData(data);
    return qlModule;
  }

  private QuickLinkData createQuickLinkData(SportPageModuleDataItem data) {
    return new QuickLinkData((SportsQuickLink) data);
  }

  @Override
  public List<QuickLinkModule> processModules(
      SportPageModule moduleConfig, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds) {
    try {
      return Arrays.asList(processModule(moduleConfig, cmsSystemConfig, excludedEventIds));
    } catch (Exception e) {
      log.error("Quick link module processor exception {} ", moduleConfig, e);
      return Collections.emptyList();
    }
  }

  public void processSegmentwiseModules(
      QuickLinkModule module, Map<String, SegmentView> segmentWiseModules, String moduleType) {
    module
        .getData()
        .forEach(
            (QuickLinkData data) ->
                data.getSegments()
                    .forEach(
                        (String seg) -> {
                          SegmentView segmentView =
                              segmentWiseModules.containsKey(seg)
                                  ? segmentWiseModules.get(seg)
                                  : new SegmentView();
                          Optional<SegmentReference> segmentReference =
                              data.getSegmentReferences().stream()
                                  .filter(
                                      segRef ->
                                          segRef.getSegment().equals(seg)
                                              && segRef.getDisplayOrder() >= 0)
                                  .findFirst();
                          double sortOrder =
                              segmentReference.isPresent()
                                  ? segmentReference.get().getDisplayOrder()
                                  : getSortOrderFromSegmentView(segmentView, moduleType);

                          double segmentOrder =
                              (module.getDisplayOrder().doubleValue() * MODULE_DISPLAY_ORDER
                                      + sortOrder)
                                  / MODULE_DISPLAY_ORDER;

                          SegmentOrderdModuleData segmentOrderdModuleData =
                              new SegmentOrderdModuleData(segmentOrder, data);

                          Map<String, SegmentOrderdModuleData> quickLinkData =
                              segmentView.getQuickLinkData();
                          quickLinkData.put(data.getId(), segmentOrderdModuleData);
                          segmentWiseModules.put(seg, segmentView);
                          updateModuleSegmentView(seg, data, module, segmentOrderdModuleData);
                        }));
  }

  private void updateModuleSegmentView(
      String segment,
      QuickLinkData data,
      QuickLinkModule module,
      SegmentOrderdModuleData segmentOrderdModuleData) {
    Map<String, SegmentView> moduleSegmentView = module.getModuleSegmentView();
    SegmentView segmentView =
        moduleSegmentView.containsKey(segment) ? moduleSegmentView.get(segment) : new SegmentView();
    segmentView.getQuickLinkData().put(data.getId(), segmentOrderdModuleData);
    moduleSegmentView.put(segment, segmentView);
    module.setModuleSegmentView(moduleSegmentView);
  }
}
