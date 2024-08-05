package com.coral.oxygen.middleware.featured.consumer.sportpage.virtual;

import static org.apache.commons.lang.BooleanUtils.isTrue;

import com.coral.oxygen.middleware.featured.consumer.sportpage.ModuleConsumer;
import com.coral.oxygen.middleware.featured.consumer.sportpage.SportsModuleProcessException;
import com.coral.oxygen.middleware.featured.service.injector.VirtualEventDataInjector;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.VirtualEvent;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.VirtualEventModule;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
@RequiredArgsConstructor
public class VirtualEventsModuleProcessor implements ModuleConsumer<VirtualEventModule> {

  private final VirtualEventDataInjector virtualEventDataInjector;

  @Value("${app.virtualevent.limit:12}")
  private int virtualEventLimit;

  private static final String PRIMARY = "PrimaryMarket";
  public static final String TWO_UP_MARKET = "2UpMarket";

  @Override
  public VirtualEventModule processModule(
      SportPageModule moduleConfig, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds)
      throws SportsModuleProcessException {
    throw new UnsupportedOperationException(
        "VirtualEventModuleProcessor unsupported this operation.");
  }

  @Override
  public List<VirtualEventModule> processModules(
      SportPageModule sportPageModule,
      CmsSystemConfig cmsSystemConfig,
      Set<Long> excludedEventIds) {
    try {
      SportModule cmsSportModule = sportPageModule.getSportModule();
      return sportPageModule.getPageData().stream()
          .filter(VirtualEvent.class::isInstance)
          .map(VirtualEvent.class::cast)
          .map((VirtualEvent virtualEvent) -> toVirtualEventModule(virtualEvent, cmsSportModule))
          .map(this::filterEvents)
          .collect(Collectors.toCollection(ArrayList::new));

    } catch (Exception e) {
      log.error("VirtualEventsModuleProcessor -> ", e);
      return Collections.emptyList();
    }
  }

  private VirtualEventModule filterEvents(VirtualEventModule eventModule) {
    eventModule.getData().removeIf(this::shouldBeExcluded);
    eventModule.setEventIds(
        eventModule.getData().stream()
            .map(EventsModuleData::getId)
            .collect(Collectors.toCollection(ArrayList::new)));
    return eventModule;
  }

  private boolean shouldBeExcluded(EventsModuleData event) {
    return isTrue(event.getFinished()) || isTrue(event.getEventIsLive()) || !pricesPresent(event);
  }

  private boolean pricesPresent(EventsModuleData event) {
    return event.getMarkets().stream()
        .flatMap(m -> m.getOutcomes().stream())
        // ignoring SP prices as well
        .anyMatch(o -> !CollectionUtils.isEmpty(o.getPrices()));
  }

  public void applyLimits(List<AbstractFeaturedModule<?>> modules) {
    AtomicInteger totalLimit = new AtomicInteger(this.virtualEventLimit);
    Iterator<AbstractFeaturedModule<?>> iterator = modules.iterator();
    while (iterator.hasNext()) {
      AbstractFeaturedModule<?> module = iterator.next();

      if (module instanceof VirtualEventModule virtualEventModule) {
        if (totalLimit.get() > 0) {
          applyLimit(virtualEventModule, totalLimit);
        } else {
          iterator.remove();
        }
      }
    }
  }

  private void applyLimit(VirtualEventModule virtualEventModule, AtomicInteger totalLimit) {
    List<EventsModuleData> limitedData = null;
    int limit = Math.min(virtualEventModule.getData().size(), totalLimit.get());

    if (virtualEventModule.getLimit() == null || virtualEventModule.getLimit() < 0) {
      virtualEventModule.setLimit(totalLimit.get());
    }

    limit = Math.min(limit, virtualEventModule.getLimit());

    totalLimit.getAndAdd(-limit);

    limitedData =
        virtualEventModule.getData().stream()
            .limit(limit)
            .collect(Collectors.toCollection(ArrayList::new));

    virtualEventModule.setData(limitedData);
    virtualEventModule.setTotalEvents(limitedData.size());
    virtualEventModule.setEventIds(
        limitedData.stream()
            .map(EventsModuleData::getId)
            .collect(Collectors.toCollection(ArrayList::new)));
  }

  protected VirtualEventModule toVirtualEventModule(
      VirtualEvent virtualEvent, SportModule cmsSportModule) {
    VirtualEventModule virtualEventModule = new VirtualEventModule();
    commonToVirtualEventModule(virtualEventModule, virtualEvent, cmsSportModule);
    if (StringUtils.isNotBlank(virtualEvent.getTypeIds())) {

      virtualEventDataInjector.injectDataEvents(virtualEventModule);
    }
    return virtualEventModule;
  }

  /**
   * This method used to reduce duplicate code for Fanzone HighlightCarouselModule and Existing
   * HighlightCarouselModule process
   *
   * @param virtualEventModule it is HighlightCarouselModule mapped from CMS module
   * @param virtualEvent it is CMS module
   * @param cmsSportModule it is CMS sportmodule data
   */
  protected void commonToVirtualEventModule(
      VirtualEventModule virtualEventModule,
      VirtualEvent virtualEvent,
      SportModule cmsSportModule) {
    virtualEventModule.setId(virtualEvent.getId());

    virtualEventModule.setLimit(virtualEvent.getLimit());
    virtualEventModule.setSportId(virtualEvent.getSportId());
    virtualEventModule.setMobileImageId(virtualEvent.getMobileImageId());
    virtualEventModule.setDesktopImageId(virtualEvent.getDesktopImageId());
    virtualEventModule.setRedirectionUrl(virtualEvent.getRedirectionUrl());
    virtualEventModule.setButtonText(virtualEvent.getButtonText());
    virtualEventModule.setTitle(virtualEvent.getTitle());
    virtualEventModule.setDisabled(virtualEvent.isDisabled());
    virtualEventModule.setDisplayOrder(cmsSportModule.getSortOrderOrDefault(null));
    virtualEventModule.setSecondaryDisplayOrder(getDisplayOrder(virtualEvent));
    virtualEventModule.setPageType(virtualEvent.getPageType());
    virtualEventModule.setTypeIds(virtualEvent.getTypeIds());
    virtualEventModule.setSegments(virtualEvent.getSegments());
    virtualEventModule.setSegmentReferences(virtualEvent.getSegmentReferences());
    virtualEventModule.setDisplayMarketType(
        virtualEvent.getDisplayMarketType() == null
            ? PRIMARY
            : virtualEvent.getDisplayMarketType());
  }

  protected BigDecimal getDisplayOrder(VirtualEvent virtualEvent) {
    return virtualEvent.getDisplayOrder() == null
        ? BigDecimal.ZERO
        : BigDecimal.valueOf(virtualEvent.getDisplayOrder());
  }
}
