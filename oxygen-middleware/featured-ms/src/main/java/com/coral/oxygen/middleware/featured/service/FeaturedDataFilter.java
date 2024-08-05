package com.coral.oxygen.middleware.featured.service;

import static com.coral.oxygen.middleware.pojos.model.cms.EventLoadingType.*;
import static java.util.stream.Collectors.toList;

import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.ModuleDataSelection;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModuleData;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Aggregation;
import com.newrelic.api.agent.NewRelic;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.time.DateUtils;
import org.joda.time.DateTime;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class FeaturedDataFilter extends ModuleAdapter {

  private int eventStartTimeInPastThresholdHours = 24;

  private SiteServerApi siteServerApi;

  @Value("${event.start.time.in.past.threshold.hours}")
  public void setEventStartTimeInPastThresholdHours(int eventStartTimeInPastThresholdHours) {
    this.eventStartTimeInPastThresholdHours = eventStartTimeInPastThresholdHours;
  }

  @Autowired
  public void setSiteServerApi(SiteServerApi siteServerApi) {
    this.siteServerApi = siteServerApi;
  }

  /**
   * Module with racing grid is populated on client side by separated widget
   *
   * <p>This is candidate for improvement
   */
  public boolean isRacingGridModule(ModuleDataSelection moduleDataSelection) {
    return moduleDataSelection != null
        && RACING_GRID.isTypeOf(moduleDataSelection.getSelectionType());
  }

  public boolean isCashOutAvailable(List<? extends EventsModuleData> eventsModuleData) {
    boolean cashOutAvailable;
    if (eventsModuleData.stream().anyMatch(event -> event.getOutcomeId() != null)) {
      cashOutAvailable =
          eventsModuleData.stream()
              .filter(event -> event.getMarkets() != null && !event.getMarkets().isEmpty())
              .map(event -> event.getMarkets().get(0))
              .anyMatch(
                  market ->
                      market.getCashoutAvail() != null
                          && !market.getCashoutAvail().isEmpty()
                          && market.getCashoutAvail().equals("Y"));
    } else {
      cashOutAvailable =
          eventsModuleData.stream()
              .anyMatch(
                  event ->
                      event.getCashoutAvail() != null
                          && !event.getCashoutAvail().isEmpty()
                          && event.getCashoutAvail().equals("Y"));
    }
    return cashOutAvailable;
  }

  public void removeEmptyNodes(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> eventsModules) {
    Map<Long, Integer> inPlayMarketsCount = requestInPlayEventFilteringData(eventsModules);

    removeOutcomesWithoutPrices(eventsModules);

    // removing events without outcomes and markets without outcomes
    eventsModules.stream()
        .filter(EventsModule.class::isInstance)
        .map(EventsModule.class::cast)
        .forEach(
            module ->
                module
                    .getData()
                    .removeIf(
                        event -> {
                          long outcomesCount =
                              event.getMarkets().stream()
                                  .mapToInt(market -> market.getOutcomes().size())
                                  .sum();
                          boolean shouldBeRemoved =
                              outcomesCount == 0
                                  && (ENHANCED_MULTIPLES
                                          .getValue()
                                          .equalsIgnoreCase(
                                              module.getDataSelection().getSelectionType())
                                      || (!"FOOTBALL"
                                              .equalsIgnoreCase(
                                                  event.getCategoryCode()) // BMA-29040, Scenario 4
                                          && !shouldBeDisplayedAsOutright(
                                              event, inPlayMarketsCount)));

                          event.getMarkets().removeIf(market -> market.getOutcomes().isEmpty());

                          return shouldBeRemoved;
                        }));

    removeModulesWithoutEvents(eventsModules);
  }

  private Map<Long, Integer> requestInPlayEventFilteringData(
      List<? extends AbstractFeaturedModule<?>> eventsModules) {

    List<EventsModuleData> model =
        eventsModules.stream()
            .map(AbstractFeaturedModule::getData)
            .flatMap(Collection::stream)
            .filter(EventsModuleData.class::isInstance)
            .map(EventsModuleData.class::cast)
            .collect(Collectors.toList());

    List<String> mtchEventIds =
        model.stream()
            .filter(this::isSortCodeMTCH)
            .map(EventsModuleData::getId)
            .map(String::valueOf)
            .collect(toList());

    SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M")
                .addBinaryOperation("market.siteChannels", BinaryOperation.contains, "M")
                .addBinaryOperation(
                    "event.drilldownTagNames", BinaryOperation.intersects, "EVFLAG_BL")
                .addField("market.isMarketBetInRun")
                .build();
    Optional<List<Aggregation>> marketsCountForEvent =
        siteServerApi.getMarketsCountForEvent(mtchEventIds, simpleFilter);
    if (marketsCountForEvent.isPresent()) {
      return marketsCountForEvent.get().stream()
          .collect(
              Collectors.toMap(Aggregation::getRefRecordId, Aggregation::getCount, (a, b) -> a));
    } else {
      return new HashMap<>();
    }
  }

  private boolean isSortCodeMTCH(EventsModuleData event) {
    String eventSortCode = event.getEventSortCode();
    return Objects.nonNull(eventSortCode) && eventSortCode.toUpperCase().contains("MTCH");
  }

  private void removeOutcomesWithoutPrices(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> model) {
    model.stream()
        .filter(outputModule -> !isRaceTypeEventModule(outputModule))
        .forEach(
            module ->
                Optional.ofNullable(module.getData())
                    .ifPresent(
                        moduleDataItems ->
                            moduleDataItems.forEach(
                                event ->
                                    event.getMarkets().stream()
                                        .filter(
                                            m ->
                                                m.getPriceTypeCodes().contains("LP")
                                                    && !m.getPriceTypeCodes().contains("SP"))
                                        .forEach(
                                            m ->
                                                m.getOutcomes()
                                                    .removeIf(
                                                        o ->
                                                            o.getPrices() == null
                                                                || o.getPrices().isEmpty())))));
  }

  public boolean isRaceTypeEventModule(AbstractFeaturedModule<? extends EventsModuleData> module) {
    return module instanceof EventsModule
        && ((EventsModule) module).getDataSelection() != null
        && RACE_TYPE_ID
            .getValue()
            .equals(((EventsModule) module).getDataSelection().getSelectionType());
  }

  /**
   * See PHX-385
   *
   * <p>The event should display on the Featured tab when a primary market (i.e. a HH or MR market)
   * is in the SS response as per existing behaviour. When a primary market is available the prices
   * of the selections should display as per existing behaviour. The event should display if it is
   * pre-match or if it is in-play as per existing behaviour.
   *
   * <p>The event should display on the Featured tab when a primary market (i.e. a HH or MR market)
   * is not in the SS response. In this scenario the event should display as an outright similar to
   * the existing behaviour that is on the in-play page. The event should display if it is
   * pre-match. The event should display if it is in-play only if there is another market that is
   * in-play.
   *
   * <p>The event should display on the Featured tab when a primary market (i.e. a HH or MR market)
   * has undisplayed selections or selections without prices. In this scenario the event should
   * display as an outright similar to the existing behaviour that is on the in-play page. The event
   * should not display if it is pre-match. The event should display if it is in-play only if there
   * is another market that is in-play.
   */
  private boolean shouldBeDisplayedAsOutright(
      EventsModuleData event, Map<Long, Integer> inPlayMarketsCount) {
    if (event.getOutcomeId() != null
        || event instanceof SurfaceBetModuleData
        || !isSortCodeMTCH(event)) {
      // boosted selection should have market or should be removed if no markets
      return false;
    }
    if (isInPlayEvent(event)) {
      int eventMarketsNumber = inPlayMarketsCount.getOrDefault(event.getId(), 0);
      return hasNonPrimaryInPlayMarkets(event, eventMarketsNumber);
    } else {
      return event.getMarkets().isEmpty();
    }
  }

  private boolean hasNonPrimaryInPlayMarkets(EventsModuleData event, int allMarketsNumber) {
    OutputMarket market = event.getMarkets().isEmpty() ? null : event.getMarkets().get(0);
    return (market == null && allMarketsNumber > 0)
        || (market != null
            && Boolean.TRUE.equals(market.getMarketBetInRun())
            && allMarketsNumber > 1)
        || (market != null
            && !Boolean.TRUE.equals(market.getMarketBetInRun())
            && allMarketsNumber > 0);
  }

  private boolean isInPlayEvent(EventsModuleData event) {
    String drilldownTagNames = event.getDrilldownTagNames();
    return Objects.nonNull(drilldownTagNames)
        && drilldownTagNames.toUpperCase().contains("EVFLAG_BL");
  }

  private void removeModulesWithoutEvents(List<? extends AbstractFeaturedModule> modules) {
    modules.removeIf(module -> module.getData().isEmpty() && !isRacingGridModule(module));
  }

  public void removeModulesWithError(List<EventsModule> modules) {
    modules.removeIf(module -> module.getErrorMessage() != null);
  }

  public void removeOlderEvents(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> models,
      CmsSystemConfig cmsSystemConfig) {
    models.forEach(
        module ->
            Optional.ofNullable(module.getData())
                .ifPresent(
                    date ->
                        date.removeIf(
                            eventData -> {
                              if (eventData.getStartTime() == null) {
                                return false;
                              }
                              Integer eventMaxLiveHours =
                                  getMaxCategoryStartTimeHoursThreshold(
                                      cmsSystemConfig, eventData.getCategoryId());
                              return isEventStartedBefore(eventData, eventMaxLiveHours);
                            })));
  }

  private Integer getMaxCategoryStartTimeHoursThreshold(
      CmsSystemConfig cmsSystemConfig, String categoryId) {
    return Optional.ofNullable(cmsSystemConfig)
        .map(
            c ->
                c.getCategoryIdEventsTimeoutMap()
                    .getOrDefault(categoryId, eventStartTimeInPastThresholdHours))
        .orElse(eventStartTimeInPastThresholdHours);
  }

  private boolean isEventStartedBefore(EventsModuleData eventData, Integer eventMaxLiveHours) {
    try {
      // to handle cases when date comes like: 2019-03-11T13:12:12Z, 2019-03-11T13:12:12.001Z,
      // 2019-03-11T13:12:12+0200, 2019-03-11T13:12:12.001+0200
      Date startTime =
          DateUtils.parseDate(
              eventData.getStartTime(),
              "yyyy-MM-dd'T'HH:mm:ssZ",
              "yyyy-MM-dd'T'HH:mm:ss.sssZ",
              "yyyy-MM-dd'T'HH:mm:ssX",
              "yyyy-MM-dd'T'HH:mm:ss.sssX");
      return new DateTime(startTime).isBefore(DateTime.now().minusHours(eventMaxLiveHours));
    } catch (Exception e1) {
      NewRelic.noticeError(e1);
      log.error("Error parsing event.startTime", e1);
      return false;
    }
  }

  public void removeNotLiveservedLiveEvents(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> eventsModules) {
    Map<Long, Integer> inPlayMarketsCount = requestInPlayEventFilteringData(eventsModules);

    eventsModules.forEach(
        module ->
            Optional.ofNullable(module.getData())
                .ifPresent(
                    moduleDataItems ->
                        moduleDataItems.removeIf(
                            event -> {
                              if (event.getMarkets().isEmpty()
                                  || Boolean.TRUE.equals(
                                      event.getMarkets().get(0).getMarketBetInRun())
                                  || !Boolean.TRUE.equals(event.getEventIsLive())) {
                                return false;
                              }
                              // live event with not bet in run market
                              if (inPlayMarketsCount.getOrDefault(event.getId(), 0).equals(0)
                                  || event instanceof SurfaceBetModuleData) {
                                // no bet in run markets. We should remove this one
                                return true;
                              } else {
                                // there are other bet in run markets. We should display as outright
                                event.getMarkets().clear();
                                return false;
                              }
                            })));
  }

  public boolean isRacingGridModule(AbstractFeaturedModule module) {
    return module instanceof EventsModule
        && isRacingGridModule(((EventsModule) module).getDataSelection());
  }
}
