package com.coral.oxygen.middleware.featured.consumer;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.HighlightCarouselModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.InplayModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModule;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class ModuleEventIdParser {

  public static <T extends AbstractFeaturedModule> List<Long> getEventIds(T module) {
    return getEventIds(module, module.getModuleType());
  }

  private static <T extends AbstractFeaturedModule> List<Long> getEventIds(
      T module, ModuleType moduleType) {
    switch (moduleType) {
      case HIGHLIGHTS_CAROUSEL:
        return getHighlighCarouselEventIds((HighlightCarouselModule) module);
      case INPLAY:
        return getInplayEventIds((InplayModule) module);
      case FEATURED:
        return getFeaturedEventIds((EventsModule) module);
      case SURFACE_BET:
        return getSurfaceBetEventIds((SurfaceBetModule) module);
      case QUICK_LINK:
      case SUPPER_BUTTON:
      case RECENTLY_PLAYED_GAMES:
      case RACING_MODULE:
      default:
        return Collections.emptyList();
    }
  }

  private static List<Long> getFeaturedEventIds(EventsModule module) {
    return module.getData().stream().map(EventsModuleData::getId).collect(Collectors.toList());
  }

  private static List<Long> getHighlighCarouselEventIds(HighlightCarouselModule module) {
    return module.getEventIds();
  }

  private static List<Long> getInplayEventIds(InplayModule module) {
    return module.getData().stream()
        .flatMap(val -> val.getEventsIds().stream())
        .collect(Collectors.toList());
  }

  private static List<Long> getSurfaceBetEventIds(SurfaceBetModule module) {
    return module.getData().stream().map(EventsModuleData::getId).collect(Collectors.toList());
  }
}
