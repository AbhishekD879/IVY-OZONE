package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.common.service.featured.OddsCardHeader;
import com.coral.oxygen.middleware.featured.service.FeaturedDataFilter;
import com.coral.oxygen.middleware.featured.service.injector.SingleOutcomeEventsModuleInjector;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentOrderdModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentView;
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModuleData;
import java.util.*;
import java.util.stream.Collectors;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Data
@Service
public class SurfaceBetModuleProcessor
    implements ModuleConsumer<SurfaceBetModule>, SegmentOrderProcessor {
  private final SingleOutcomeEventsModuleInjector singleOutcomeDataInjector;
  private final OddsCardHeader oddsCardHeader;
  private final FeaturedDataFilter featuredDataFilter;

  @Value("${cms.fanzone.pageid}")
  private String fanzonePageId;

  @Override
  public SurfaceBetModule processModule(
      SportPageModule sportPageModule,
      CmsSystemConfig cmsSystemConfig,
      Set<Long> excludedEventIds) {
    SportModule surfaceBetModule = sportPageModule.getSportModule();
    SurfaceBetModule module = new SurfaceBetModule();
    module.setId(surfaceBetModule.getId());
    module.setTitle(surfaceBetModule.getTitle());
    module.setSportId(surfaceBetModule.getSportId());
    module.setDisplayOrder(surfaceBetModule.getSortOrderOrDefault(null));
    module.setData(toSurfaceBetData(sportPageModule.getPageData()));
    module.setPageType(surfaceBetModule.getPageType());
    IdsCollector idsCollector = new IdsCollector(Collections.emptyList());
    idsCollector.setOutcomesIds(
        sportPageModule.getPageData().stream()
            .filter(SurfaceBet.class::isInstance)
            .map(SurfaceBet.class::cast)
            .map(SurfaceBet::getSelectionId)
            .collect(Collectors.toSet()));
    if (StringUtils.isNotBlank(fanzonePageId)
        && fanzonePageId.equals(sportPageModule.getSportModule().getPageId())) {
      singleOutcomeDataInjector.injectData(module.getData(), idsCollector, true);
    }
    singleOutcomeDataInjector.injectData(module.getData(), idsCollector);
    return retainValidEvents(module);
  }

  private SurfaceBetModule retainValidEvents(SurfaceBetModule module) {
    module.getData().removeIf(d -> d.getMarkets().stream().noneMatch(this::isMarketWithPrice));
    return module;
  }

  private boolean isMarketWithPrice(OutputMarket market) {
    return (Objects.nonNull(market.getPriceTypeCodes())
            && !market.getPriceTypeCodes().contains("LP"))
        || market.getOutcomes().stream()
            .flatMap(o -> o.getPrices().stream())
            .filter(Objects::nonNull)
            .anyMatch(p -> Objects.nonNull(p.getId()));
  }

  private List<SurfaceBetModuleData> toSurfaceBetData(List<SportPageModuleDataItem> pageData) {
    return pageData.stream()
        .filter(SurfaceBet.class::isInstance)
        .map(SurfaceBet.class::cast)
        .map(this::createEventData)
        .collect(Collectors.toList());
  }

  protected SurfaceBetModuleData createEventData(SurfaceBet surfaceBet) {
    SurfaceBetModuleData data = new SurfaceBetModuleData();
    commonToSurfaceBetModule(data, surfaceBet);
    return data;
  }

  /**
   * This method is implemented to avoid code duplication for fanzone flow and csp flow
   *
   * @param data this is SurfaceBetModuleData used for mapping
   * @param surfaceBet this is cms surfacebet data
   */
  protected void commonToSurfaceBetModule(SurfaceBetModuleData data, SurfaceBet surfaceBet) {
    data.setTitle(surfaceBet.getTitle());
    data.setSvgId(surfaceBet.getSvgId());
    data.setSvgBgImgPath(surfaceBet.getSvgBgImgPath());
    data.setContent(surfaceBet.getContent());
    data.setContentHeader(surfaceBet.getContentHeader());
    data.setSvgBgId(surfaceBet.getSvgBgId());
    data.setSelectionId(surfaceBet.getSelectionId());
    data.setDisplayOrder(surfaceBet.getDisplayOrder());
    data.setOldPrice(surfaceBet.getPrice());
    data.setOutcomeId(surfaceBet.getSelectionId());
    data.setSegments(surfaceBet.getSegments());
    data.setSegmentReferences(surfaceBet.getSegmentReferences());
    data.setObjId(surfaceBet.getId());
    data.setDisplayOnDesktop(surfaceBet.getDisplayOnDesktop());
  }

  public SurfaceBetModule postProcessModule(SurfaceBetModule surfaceBetModule) {
    if (CollectionUtils.isEmpty(surfaceBetModule.getData())) {
      surfaceBetModule.setHasNoLiveEvents(true);
      return surfaceBetModule;
    }
    surfaceBetModule.setOutcomeColumnsTitles(
        oddsCardHeader.calculateHeadTitles(surfaceBetModule.getData()));
    surfaceBetModule.setHasNoLiveEvents(
        surfaceBetModule.getData().stream()
            .noneMatch(event -> Boolean.TRUE.equals(event.getEventIsLive())));
    surfaceBetModule.setCashoutAvail(
        featuredDataFilter.isCashOutAvailable(surfaceBetModule.getData()));
    return surfaceBetModule;
  }

  @Override
  public List<SurfaceBetModule> processModules(
      SportPageModule cmsModule, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds) {
    try {
      return Arrays.asList(processModule(cmsModule, cmsSystemConfig, excludedEventIds));
    } catch (Exception e) {
      log.error("Quick link module processor exception {} ", cmsModule, e);
      return Collections.emptyList();
    }
  }

  public void processSegmentwiseModules(
      SurfaceBetModule module, Map<String, SegmentView> segmentWiseModules, String moduleType) {
    module
        .getData()
        .forEach(
            (SurfaceBetModuleData data) ->
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
                                          segRef.getSegment().equalsIgnoreCase(seg)
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

                          Map<String, SegmentOrderdModuleData> surfaceBetModuleData =
                              segmentView.getSurfaceBetModuleData();
                          surfaceBetModuleData.put(data.getObjId(), segmentOrderdModuleData);
                          segmentWiseModules.put(seg, segmentView);
                          updateModuleSegmentView(seg, data, module, segmentOrderdModuleData);
                        }));
  }

  private void updateModuleSegmentView(
      String segment,
      SurfaceBetModuleData data,
      SurfaceBetModule module,
      SegmentOrderdModuleData segmentOrderdModuleData) {
    Map<String, SegmentView> moduleSegmentView = module.getModuleSegmentView();
    SegmentView segmentView =
        moduleSegmentView.containsKey(segment) ? moduleSegmentView.get(segment) : new SegmentView();
    segmentView.getSurfaceBetModuleData().put(data.getObjId(), segmentOrderdModuleData);
    moduleSegmentView.put(segment, segmentView);
    module.setModuleSegmentView(moduleSegmentView);
  }
}
