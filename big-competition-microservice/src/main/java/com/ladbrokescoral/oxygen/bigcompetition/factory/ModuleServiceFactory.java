package com.ladbrokescoral.oxygen.bigcompetition.factory;

import com.ladbrokescoral.oxygen.bigcompetition.service.*;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModuleType;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class ModuleServiceFactory {

  private final AemModuleService aemModuleService;
  private final GroupModuleService groupModuleService;
  private final KnockoutModuleService knockoutModuleService;
  private final NextEventsModuleService nextEventsModuleService;
  private final NextEventsIndividualModuleService nextEventsIndividualModuleService;
  private final OutrightsModuleService outrightsModuleService;
  private final PromotionModuleService promotionModuleService;
  private final ResultModuleService resultModuleService;
  private final SpecialModuleService specialModuleService;
  private final SurfaceBetsModuleService surfaceBetsModuleService;
  private final HighlightCarouselService highlightCarouselService;
  private final BybWidgetModuleService bybWidgetModuleService;

  public ModuleService getModuleService(CompetitionModuleType moduleType) {
    switch (moduleType) {
      case AEM:
        return aemModuleService;
      case NEXT_EVENTS:
        return nextEventsModuleService;
      case NEXT_EVENTS_INDIVIDUAL:
        return nextEventsIndividualModuleService;
      case PROMOTIONS:
        return promotionModuleService;
      case OUTRIGHTS:
        return outrightsModuleService;
      case SPECIALS:
      case SPECIALS_OVERVIEW:
        return specialModuleService;
      case GROUP_WIDGET:
      case GROUP_ALL:
      case GROUP_INDIVIDUAL:
        return groupModuleService;
      case RESULTS:
        return resultModuleService;
      case KNOCKOUTS:
        return knockoutModuleService;
      case SURFACEBET:
        return surfaceBetsModuleService;
      case HIGHLIGHT_CAROUSEL:
        return highlightCarouselService;
      case BYB_WIDGET:
        return bybWidgetModuleService;
      default:
        throw new UnsupportedOperationException("Module service not found for type " + moduleType);
    }
  }
}
