package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import static com.ladbrokescoral.oxygen.cms.util.BuilderFilterUtil.*;
import static com.ladbrokescoral.oxygen.cms.util.Util.listDiff;

import com.egalacoral.spark.siteserver.api.BaseFilter;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.ExistsFilter.ExistsFilterBuilder;
import com.egalacoral.spark.siteserver.api.LimitRecordsFilter;
import com.egalacoral.spark.siteserver.api.LimitToFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter.SimpleFilterBuilder;
import com.egalacoral.spark.siteserver.api.UnaryOperation;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.CategoryEntity;
import com.egalacoral.spark.siteserver.model.Coupon;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Pool;
import com.google.common.collect.Lists;
import com.ladbrokescoral.oxygen.cms.api.dto.*;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.exception.TypeIdIncorrectException;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeEventDtoMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeKnockoutEventDtoMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeMarketDtoMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeOutcomeDtoMapper;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import javax.validation.constraints.NotBlank;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

@Slf4j
@Service
@RequiredArgsConstructor
public class SiteServeServiceImpl implements SiteServeService {

  private static final String EVENT_CATEGORY_ID = "event.categoryId";
  private static final String EVENT_SITE_CHANNELS = "event.siteChannels";
  private static final String EVENT_SUSPEND_AT_TIME = "event.suspendAtTime";
  private static final String EVENT_IS_STARTED = "event.isStarted";
  private static final String EVENT_DRILLDOWN_TAG_NAMES = "event.drilldownTagNames";
  private static final String EVENT_IS_ACTIVE = "event.isActive";
  private static final String EVENT_START_TIME = "event.startTime";
  private static final String EVENT_IS_LIVE_NOW = "event.isLiveNowEvent";
  private static final String EVENT_IS_OPEN = "event.isOpenEvent";
  private static final String EVENT_SORT_CODE = "event.eventSortCode";
  private static final String EVENT_MARKET_IS_DISPLAYED = "event:simpleFilter:market.isDisplayed";
  private static final String EVENT_MARKET_IS_RESULTED = "event:simpleFilter:market.isResulted";
  private static final String CLASS_CATEGORY_ID = "class.categoryId";
  private static final String CLASS_SITE_CHANNELS = "class.siteChannels";
  private static final String CLASS_IS_ACTIVE = "class.isActive";
  private static final String EVENT_IS_FINISHED = "event.isFinished";
  private static final String EVENT_IS_RESULTED = "event.isResulted";
  private static final List<String> PRUNE_EVENT_N_MARKET = Arrays.asList("event", "market");

  private static final String TEMPLATE_MARKET_NAME = "market.templateMarketName";

  private static final String OUTRIGHT_SORT_CODES =
      "TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20";

  private final SiteServeApiProvider siteServeApiProvider;

  private static final int DURATION_24_HOURS = 24;
  private static final String BET_INPLAY_DRILLDOWN_TAG = "EVFLAG_BL";

  private static final String MARKET_BET_IN_RUN = "event:simpleFilter:market.isMarketBetInRun";

  @Value("${siteserver.priceboost.simplefilter.key}")
  private String priceBoostSimpleFilterKey;

  @Value("${siteserver.priceboost.simplefilter.value}")
  private String priceBoostSimpleFilterValue;

  @Value("${siteserver.priceboost.enabled:false}")
  private boolean isPriceBoostEnabled;

  @Override
  public Optional<SiteServeMarketDto> getMarketById(String brand, String marketId) {
    return siteServeApiProvider
        .api(brand)
        .getEventToMarketForMarket(marketId)
        .map(SiteServeMarketDtoMapper.INSTANCE::toDto);
  }

  @Override
  public Optional<List<Category>> getClassToSubTypeForType(String brand, String typeId) {
    return siteServeApiProvider
        .api(brand)
        .getClassToSubTypeForType(typeId, new SimpleFilter.SimpleFilterBuilder().build());
  }

  @Override
  public SiteServeEventValidationResultDto validateAndGetEventsById(
      String brand, List<String> ids, boolean onlySpecials) {
    ExistsFilter existsFilter = buildExistsFilter(onlySpecials);
    List<SiteServeMinimalEventDto> events =
        siteServeApiProvider.api(brand).getEvent(ids, Optional.empty(), Optional.of(existsFilter))
            .orElseGet(ArrayList::new).stream()
            .map(SiteServeEventDtoMapper.INSTANCE::toMinimalDto)
            .collect(Collectors.toList());

    List<String> resultEventIds =
        events.stream().map(SiteServeMinimalEventDto::getId).collect(Collectors.toList());
    List<String> invalidIds = listDiff(ids, resultEventIds);
    return new SiteServeEventValidationResultDto(events, invalidIds);
  }

  @Override
  public SiteServeEventValidationResultDto validateEventsByTypeId(
      String brand, List<String> ids, boolean onlySpecials) {
    ExistsFilter existsFilter = buildExistsFilter(onlySpecials);
    List<SiteServeMinimalEventDto> events =
        siteServeApiProvider
            .api(brand)
            .getEventForType(ids, Optional.empty(), Optional.of(existsFilter), false)
            .map(
                list ->
                    list.stream()
                        .map(SiteServeEventDtoMapper.INSTANCE::toMinimalDto)
                        .collect(Collectors.toList()))
            .orElseGet(ArrayList::new);
    List<String> invalidIds =
        ids.stream().filter(id -> !isTypeIdValid(brand, id)).collect(Collectors.toList());
    return new SiteServeEventValidationResultDto(events, invalidIds);
  }

  @Override
  public SiteServeEventValidationResultDto validateEventsByOutcomeId(
      String brand, List<String> ids) {
    SimpleFilter simpleFilter = (SimpleFilter) new SimpleFilterBuilder().build();
    List<SiteServeCompleteOutcomeDto> outcomes =
        siteServeApiProvider
            .api(brand)
            .getEventToOutcomeForOutcome(ids, simpleFilter, PRUNE_EVENT_N_MARKET, true)
            .map(
                list ->
                    list.stream()
                        .flatMap(event -> event.getMarkets().stream())
                        .flatMap(market -> market.getOutcomes().stream())
                        .map(
                            SiteServeOutcomeDtoMapper.SiteServeOutcomeDtoMapperInstance.INSTANCE
                                ::toDtoWithoutPrices)
                        .collect(Collectors.toList()))
            .orElseGet(ArrayList::new);
    List<String> resultOutcomeIds =
        outcomes.stream().map(SiteServeCompleteOutcomeDto::getId).collect(Collectors.toList());
    List<String> invalidIds = listDiff(ids, resultOutcomeIds);
    return new SiteServeEventValidationResultDto(Collections.emptyList(), invalidIds);
  }

  private ExistsFilter buildExistsFilter(boolean onlySpecials) {
    ExistsFilter.ExistsFilterBuilder existsFilterBuilder = new ExistsFilter.ExistsFilterBuilder();
    if (onlySpecials) {
      existsFilterBuilder.addBinaryOperation(
          "event:simpleFilter:market.drilldownTagNames", BinaryOperation.intersects, "MKTFLAG_SP");
    }
    return existsFilterBuilder.build();
  }

  @Override
  public boolean isTypeIdValid(String brand, String typeId) {
    return siteServeApiProvider
        .api(brand)
        .getClassToSubTypeForType(typeId, Collections::emptyList)
        .map(list -> !list.isEmpty())
        .orElse(false);
  }

  @Override
  public void isTypeIdValid(String brand, Integer typeId) {
    if (!isTypeIdValid(brand, typeId.toString())) {
      throw new TypeIdIncorrectException();
    }
  }

  @Override
  public Optional<SiteServeKnockoutEventDto> getKnockoutEvent(String brand, String eventId) {
    return siteServeApiProvider
        .api(brand)
        .getEvent(eventId, true)
        .map(SiteServeKnockoutEventDtoMapper.INSTANCE::toDto);
  }

  @Override
  public boolean isCategoryNotValidOrHasEvents(String brand, Integer categoryId) {
    return siteServeApiProvider
        .api(brand)
        .getCategory(categoryId.toString(), Optional.empty(), Optional.empty(), true)
        .map(CategoryEntity::getId)
        .map(id -> hasSiteServeCategoryEvents(brand, id))
        .orElse(true);
  }

  @Override
  public boolean anyLiveOrUpcomingEventsExists(SportCategory sport) {
    List<String> classes = getActiveClasses(sport.getBrand(), sport.getCategoryId());
    if (classes.isEmpty()) {
      return false;
    }
    return anyLiveEventExists(sport, classes) || anyUpcomingEventExistsForNext48H(sport, classes);
  }

  private boolean anyUpcomingEventExistsForNext48H(SportCategory sport, List<String> classes) {
    Instant now = nowUtcWithoutMillis();
    Instant in48Hours = nowUtcWithoutMillis().plus(Duration.ofHours(48));
    SimpleFilterBuilder upcomingEventsFilterBuilder =
        new SimpleFilterBuilder()
            .addField(EVENT_IS_ACTIVE)
            .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, sport.getCategoryId())
            .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
            .addBinaryOperation(EVENT_SORT_CODE, BinaryOperation.equals, "MTCH")
            .addUnaryOperation(EVENT_IS_STARTED, UnaryOperation.isFalse)
            .addBinaryOperation(EVENT_START_TIME, BinaryOperation.greaterThan, now)
            .addBinaryOperation(EVENT_START_TIME, BinaryOperation.lessThan, in48Hours)
            .addBinaryOperation(EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, now);
    defineMarketAndSortNames(upcomingEventsFilterBuilder, sport);
    ExistsFilter eventMarketIsAvailableFilter = getExistsFilter();
    return anyEventExists(
        sport.getBrand(),
        classes,
        (SimpleFilter) upcomingEventsFilterBuilder.build(),
        eventMarketIsAvailableFilter);
  }

  private boolean anyLiveEventExists(SportCategory sport, List<String> classes) {
    SimpleFilterBuilder liveEventsFilterBuilder = getLiveEventsFilterBuilder(sport);

    liveEventsFilterBuilder.addPriceStream(
        priceBoostSimpleFilterKey, priceBoostSimpleFilterValue, isPriceBoostEnabled);

    defineMarketAndSortNames(liveEventsFilterBuilder, sport);
    ExistsFilter eventMarketIsAvailableFilter = getEventMarketIsAvailableFilter();
    return anyEventExists(
        sport.getBrand(),
        classes,
        (SimpleFilter) liveEventsFilterBuilder.build(),
        eventMarketIsAvailableFilter);
  }

  private Boolean anyEventExists(
      @NotBlank String brand,
      List<String> classes,
      SimpleFilter simpleFilter,
      ExistsFilter existsFilter) {
    return getEventToOutcomeForClass(brand, classes, simpleFilter, existsFilter)
        .map(list -> !list.isEmpty())
        .orElse(false);
  }

  public boolean anyUpcomingEventsExistsForGolf(SportCategory sport) {
    List<String> classes = getActiveClasses(sport.getBrand(), sport.getCategoryId());
    if (classes.isEmpty()) {
      return false;
    }
    return anyUpcomingEvents(sport, classes);
  }

  public boolean anyUpcomingEventsExistsForMatchesTabGolf(SportCategory sport) {
    List<String> classes = getActiveClasses(sport.getBrand(), sport.getCategoryId());
    if (classes.isEmpty()) {
      return false;
    }

    return anyUpcomingEventsForMatchesTab(sport, classes);
  }

  private boolean anyUpcomingEventsForMatchesTab(SportCategory sport, List<String> classes) {
    SimpleFilterBuilder upcomingEventsFilterBuilder =
        getUpcomingEventExistsforMatchesTabBuilder(sport);
    ExistsFilter eventMarketIsAvailableFilter = getExistsFilter();
    return siteServeApiProvider
        .api(sport.getBrand())
        .getEventToOutcomeForClass(
            classes,
            (SimpleFilter) upcomingEventsFilterBuilder.build(),
            limitToFilter(),
            eventMarketIsAvailableFilter,
            PRUNE_EVENT_N_MARKET)
        .map(list -> !list.isEmpty())
        .orElse(false);
  }

  public boolean anyLiveOrUpcomingTodaysEventsExistsForGolf(SportCategory sport) {
    List<String> classes = getActiveClasses(sport.getBrand(), sport.getCategoryId());
    if (classes.isEmpty()) {
      return false;
    }
    return anyLiveEventExistsForGolf(sport, classes)
        || anyUpcomingEventExistsForNext24H(sport, classes);
  }

  public boolean anyUpcomingEventExistsForNext24H(SportCategory sport, List<String> classes) {
    SimpleFilterBuilder upcomingEventsFilterBuilder =
        getUpcomingEventExistsForNext24HBuilder(sport);
    ExistsFilter eventMarketIsAvailableFilter = getExistsFilter();
    return siteServeApiProvider
        .api(sport.getBrand())
        .getEventToOutcomeForClass(
            classes,
            (SimpleFilter) upcomingEventsFilterBuilder.build(),
            limitToFilter(),
            eventMarketIsAvailableFilter,
            PRUNE_EVENT_N_MARKET)
        .map(list -> !list.isEmpty())
        .orElse(false);
  }

  private boolean anyLiveEventExistsForGolf(SportCategory sport, List<String> classes) {
    SimpleFilterBuilder liveEventsFilterBuilder = getLiveEventsFilterBuilder(sport);
    ExistsFilter eventMarketIsAvailableFilter = getEventMarketIsAvailableFilter();
    return siteServeApiProvider
        .api(sport.getBrand())
        .getEventToOutcomeForClass(
            classes,
            (SimpleFilter) liveEventsFilterBuilder.build(),
            limitToFilter(),
            eventMarketIsAvailableFilter,
            PRUNE_EVENT_N_MARKET)
        .map(list -> !list.isEmpty())
        .orElse(false);
  }

  private boolean anyUpcomingEvents(SportCategory sport, List<String> classes) {
    SimpleFilterBuilder upcomingEventsFilterBuilder = getUpcomingEventBuilder(sport);
    ExistsFilter eventMarketIsAvailableFilter = getExistsFilter();
    return siteServeApiProvider
        .api(sport.getBrand())
        .getEventToOutcomeForClass(
            classes,
            (SimpleFilter) upcomingEventsFilterBuilder.build(),
            limitToFilter(),
            eventMarketIsAvailableFilter,
            PRUNE_EVENT_N_MARKET)
        .map(list -> !list.isEmpty())
        .orElse(false);
  }

  private Optional<List<Event>> getEventToOutcomeForClass(
      String brand, List<String> classes, SimpleFilter simpleFilter, ExistsFilter existsFilter) {
    return siteServeApiProvider
        .api(brand)
        .getEventToOutcomeForClass(
            classes,
            simpleFilter,
            limitToFilter(),
            limitMarketAndOutcomeRecords(),
            existsFilter,
            PRUNE_EVENT_N_MARKET);
  }

  private List<String> getActiveClasses(String brand, Integer categoryId) {
    SimpleFilter activeClassesFilter =
        (SimpleFilter)
            new SimpleFilterBuilder()
                .addBinaryOperation(CLASS_CATEGORY_ID, BinaryOperation.equals, categoryId)
                .addBinaryOperation(CLASS_SITE_CHANNELS, BinaryOperation.contains, "M")
                .addField(CLASS_IS_ACTIVE)
                .build();
    return siteServeApiProvider.api(brand).getClasses(activeClassesFilter, existsFilter())
        .orElse(Collections.emptyList()).stream()
        .map(Category::getId)
        .map(String::valueOf)
        .collect(Collectors.toList());
  }

  private List<String> getActiveClasses(String brand, Collection<Integer> categoryIds) {
    if (categoryIds.isEmpty()) {
      return Collections.emptyList();
    }
    String categoryIdsCsv = Util.join(",", categoryIds);
    SimpleFilter activeClassesFilter =
        (SimpleFilter)
            new SimpleFilterBuilder()
                .addBinaryOperation(CLASS_CATEGORY_ID, BinaryOperation.intersects, categoryIdsCsv)
                .addBinaryOperation(CLASS_SITE_CHANNELS, BinaryOperation.contains, "M")
                .addField(CLASS_IS_ACTIVE)
                .build();
    return siteServeApiProvider.api(brand).getClasses(activeClassesFilter, existsFilter())
        .orElse(Collections.emptyList()).stream()
        .map(Category::getId)
        .map(String::valueOf)
        .collect(Collectors.toList());
  }

  @Override
  public Boolean hasSiteServeCategoryEvents(String brand, Integer categoryId) {
    if (categoryId == null) {
      return false;
    }
    return findEventsByCategoryId(brand, categoryId).map(list -> !list.isEmpty()).orElse(false);
  }

  @Override
  public boolean hasSiteServeJackpotEvents(String brand) {
    return getPoolMarketIds(brand)
        .flatMap(ids -> getNotStartedEventsByMarkets(brand, ids))
        .map(events -> !events.isEmpty())
        .orElse(false);
  }

  /**
   * @param brand - brand
   * @return comma separated list of market ids
   */
  private Optional<String> getPoolMarketIds(String brand) {
    BaseFilter poolSimpleFilter =
        new SimpleFilter.SimpleFilterBuilder()
            .addField("pool.isActive")
            .addBinaryOperation("pool.type", BinaryOperation.equals, "V15")
            .build();

    return siteServeApiProvider
        .api(brand)
        .getPools((SimpleFilter) poolSimpleFilter)
        .flatMap(list -> list.stream().findFirst())
        .map(Pool::getMarketIds);
  }

  private Optional<List<Event>> getNotStartedEventsByMarkets(String brand, String marketIds) {
    BaseFilter simpleFilter =
        new SimpleFilter.SimpleFilterBuilder()
            .addUnaryOperation(EVENT_IS_STARTED, UnaryOperation.isFalse)
            .addPriceStream(
                priceBoostSimpleFilterKey, priceBoostSimpleFilterValue, isPriceBoostEnabled)
            .build();
    return siteServeApiProvider
        .api(brand)
        .getWholeEventToOutcomeForMarket(marketIds, false, (SimpleFilter) simpleFilter);
  }

  @Override
  public Set<Integer> filterByCompetitionEvents(String brand, List<SportCategory> categories) {
    Map<Integer, SportCategory> categoriesById =
        categories.stream()
            .collect(Collectors.toMap(SportCategory::getCategoryId, Function.identity()));
    Set<Integer> categoriesToCheck = categoriesById.keySet();
    Set<Integer> categoriesWithCompetitions = filterByOutrightEvents(brand, categoriesToCheck);
    categoriesToCheck.removeAll(categoriesWithCompetitions);

    log.info("Found Outrights for: {}", categoriesWithCompetitions.toString());

    for (Integer categoryId : categoriesToCheck) {
      if (this.hasAnyMatchesEvents(brand, categoriesById.get(categoryId))) {
        categoriesWithCompetitions.add(categoryId);
      }
    }
    return categoriesWithCompetitions;
  }

  private boolean hasAnyMatchesEvents(String brand, SportCategory sport) {
    List<String> activeClasses =
        getActiveClasses(brand, Collections.singleton(sport.getCategoryId()));
    SimpleFilterBuilder simpleFilterBuilder =
        new SimpleFilterBuilder()
            .addField(EVENT_IS_OPEN)
            .addField(EVENT_IS_ACTIVE)
            .addBinaryOperation(EVENT_SORT_CODE, BinaryOperation.notIn, OUTRIGHT_SORT_CODES)
            .addBinaryOperation(
                EVENT_DRILLDOWN_TAG_NAMES, BinaryOperation.notIntersects, "EVFLAG_SP")
            .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, sport.getCategoryId())
            .addBinaryOperation(
                EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, nowUtcWithoutMillis());
    defineMarketAndSortNames(simpleFilterBuilder, sport);
    return anyEventExists(
        brand, activeClasses, (SimpleFilter) simpleFilterBuilder.build(), existsFilter());
  }

  private void defineMarketAndSortNames(
      SimpleFilterBuilder simpleFilterBuilder, SportCategory sport) {
    if (!StringUtils.isEmpty(sport.getDispSortNames())) {
      simpleFilterBuilder.addBinaryOperation(
          Market.DISP_SORT_NAME, BinaryOperation.intersects, sport.getDispSortNames());
    }
    if (!StringUtils.isEmpty(sport.getPrimaryMarkets())) {
      simpleFilterBuilder.addBinaryOperation(
          Market.TEMPLATE_MARKET_NAME, BinaryOperation.intersects, sport.getPrimaryMarkets());
    }
  }

  @Override
  public Set<Integer> filterByOutrightEvents(String brand, Set<Integer> categoryIds) {
    String categoryIdsCsv = Util.join(",", categoryIds);
    List<String> activeClasses = getActiveClasses(brand, categoryIds);
    if (activeClasses.isEmpty()) {
      return Collections.emptySet();
    }
    SimpleFilter outrightEventsFilter =
        (SimpleFilter)
            new SimpleFilterBuilder()
                .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.in, categoryIdsCsv)
                .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
                .addBinaryOperation(
                    EVENT_SORT_CODE, BinaryOperation.intersects, OUTRIGHT_SORT_CODES)
                .addBinaryOperation(
                    EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, nowUtcWithoutMillis())
                .build();

    return extractCategoryIds(
        getEventToOutcomeForClass(brand, activeClasses, outrightEventsFilter, existsFilter())
            .orElse(Collections.emptyList()));
  }

  private Set<Integer> extractCategoryIds(Collection<Event> events) {
    return events.stream()
        .map(Event::getCategoryId)
        .map(Integer::valueOf)
        .collect(Collectors.toSet());
  }

  @Override
  public List<Coupon> getCouponsForTodaysAndUpcomingIn24hEvents(String brand) {
    SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilterBuilder()
                .addBinaryOperation("coupon.siteChannels", BinaryOperation.contains, "M")
                .build();
    ExistsFilter existsFilter =
        (ExistsFilter)
            new ExistsFilterBuilder()
                .addBinaryOperation(
                    "coupon:simpleFilter:event.startTime",
                    BinaryOperation.greaterThanOrEqual,
                    nowUtcWithoutMillis().truncatedTo(ChronoUnit.DAYS))
                .addBinaryOperation(
                    "coupon:simpleFilter:event.suspendAtTime",
                    BinaryOperation.greaterThan,
                    nowUtcWithoutMillis().plus(Duration.ofDays(1)))
                .addUnaryOperation("coupon:simpleFilter:event.isStarted", UnaryOperation.isFalse)
                .build();
    Optional<List<Coupon>> coupons =
        siteServeApiProvider
            .api(brand)
            .getCoupons(Optional.of(simpleFilter), Optional.of(existsFilter), false);
    return coupons.orElseGet(Collections::emptyList);
  }

  @Override
  public List<Event> getSportSpecials(String brand, int categoryId) {
    List<Category> classes = getActiveClassesForCategoryId(brand, categoryId);

    if (classes.isEmpty()) {
      return Collections.emptyList();
    } else {
      List<String> classIds =
          classes.stream().map(Category::getId).map(String::valueOf).collect(Collectors.toList());

      SimpleFilter eventsSimpleFilter =
          (SimpleFilter)
              new SimpleFilterBuilder()
                  .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.intersects, categoryId)
                  .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
                  .addBinaryOperation(
                      EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, nowUtcWithoutMillis())
                  .addPriceStream(
                      priceBoostSimpleFilterKey, priceBoostSimpleFilterValue, isPriceBoostEnabled)
                  .build();

      return siteServeApiProvider
          .api(brand)
          .getEventToOutcomeForClass(
              classIds,
              eventsSimpleFilter,
              limitToFilter(),
              buildExistsFilter(true),
              PRUNE_EVENT_N_MARKET)
          .orElseGet(Collections::emptyList);
    }
  }

  @Override
  public List<Event> getNextEvents(NextEventsParameters params) {
    List<Category> classes =
        getActiveClassesForCategoryId(params.getBrand(), params.getCategoryId());
    if (classes.isEmpty()) {
      return Collections.emptyList();
    } else {
      return doGetNextRacesEvents(params, classes);
    }
  }

  private List<Event> doGetNextRacesEvents(NextEventsParameters params, List<Category> classes) {
    List<String> classIds =
        classes.stream().map(Category::getId).map(String::valueOf).collect(Collectors.toList());

    SimpleFilter eventsSimpleFilter = buildNextRacesSimpleFilter(params);
    ExistsFilter existsFilter = buildNextRacesExistFilter();

    List<Event> events =
        siteServeApiProvider
            .api(params.getBrand())
            .getEventToOutcomeForClass(classIds, eventsSimpleFilter, limitToFilter(), existsFilter)
            .orElseGet(Collections::emptyList);

    Collections.sort(events, params.getComparator());
    return events;
  }

  private ExistsFilter buildNextRacesExistFilter() {
    ExistsFilterBuilder existsFilterBuilder = new ExistsFilterBuilder();
    existsFilterBuilder.addBinaryOperation(
        "event:simpleFilter:market.marketStatusCode", BinaryOperation.equals, "A");
    existsFilterBuilder.addBinaryOperation(
        "event:simpleFilter:market.name", BinaryOperation.equals, Market.WIN_OR_EACH_WAY);
    return existsFilterBuilder.build();
  }

  private SimpleFilter buildNextRacesSimpleFilter(NextEventsParameters params) {
    Instant now = Instant.now();
    Instant futureDateTime = now.plus(Duration.ofMinutes(params.getTimePeriodMinutes()));
    return (SimpleFilter)
        new SimpleFilterBuilder()
            .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
            .addBinaryOperation(
                "event.typeFlagCodes",
                BinaryOperation.intersects,
                params.getTypeFlagCodes().toString())
            .addBinaryOperation("market.name", BinaryOperation.equals, Market.WIN_OR_EACH_WAY)
            .addBinaryOperation("market.marketStatusCode", BinaryOperation.equals, "A")
            .addBinaryOperation("event.eventStatusCode", BinaryOperation.equals, "A")
            .addBinaryOperation("event.rawIsOffCode", BinaryOperation.notEquals, "Y")
            .addBinaryOperation(EVENT_START_TIME, BinaryOperation.greaterThanOrEqual, now)
            .addBinaryOperation(EVENT_START_TIME, BinaryOperation.lessThan, futureDateTime)
            .addPriceStream(
                priceBoostSimpleFilterKey, priceBoostSimpleFilterValue, isPriceBoostEnabled)
            .build();
  }

  @Override
  public List<CategoryEntity> getCategories(String brand) {
    return siteServeApiProvider
        .api(brand)
        .getCategories(Optional.empty(), Optional.empty(), true)
        .orElse(Collections.emptyList());
  }

  private List<Category> getActiveClassesForCategoryId(String brand, int categoryId) {
    SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilterBuilder()
                .addBinaryOperation(CLASS_CATEGORY_ID, BinaryOperation.equals, categoryId)
                .addBinaryOperation(CLASS_SITE_CHANNELS, BinaryOperation.contains, "M")
                .addField(CLASS_IS_ACTIVE)
                .build();
    return siteServeApiProvider
        .api(brand)
        .getClasses(simpleFilter, existsFilter())
        .orElseGet(Collections::emptyList);
  }

  @Override
  public List<Event> getCommentsByEventId(String brand, List<String> eventIds) {
    return siteServeApiProvider
        .api(brand)
        .getCommentaryForEvent(eventIds)
        .orElse(Collections.emptyList());
  }

  private Optional<List<Event>> findEventsByCategoryId(String brand, Integer categoryId) {
    SimpleFilter.SimpleFilterBuilder filterBuilder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, categoryId.toString())
            .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
            .addBinaryOperation(
                EVENT_SUSPEND_AT_TIME,
                BinaryOperation.greaterThanOrEqual,
                Instant.now().truncatedTo(ChronoUnit.MINUTES));

    return siteServeApiProvider
        .api(brand)
        .getEvent(
            Collections.emptyList(),
            Optional.of((SimpleFilter) filterBuilder.build()),
            Optional.empty());
  }

  public Optional<List<Event>> findNextEventsByCategoryId(String brand, Integer categoryId) {
    Instant now = nowUtcWithoutMillis().minus(Duration.ofMinutes(5));
    Instant next5Days = nowUtcWithoutMillis().plus(Duration.ofHours(120));
    SimpleFilter.SimpleFilterBuilder filterBuilder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, categoryId.toString())
            .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
            .addBinaryOperation(EVENT_START_TIME, BinaryOperation.greaterThanOrEqual, now)
            .addBinaryOperation(EVENT_START_TIME, BinaryOperation.lessThan, next5Days);

    return siteServeApiProvider
        .api(brand)
        .getEvent(
            Collections.emptyList(),
            Optional.of((SimpleFilter) filterBuilder.build()),
            Optional.empty());
  }

  public Optional<List<Event>> findPreviousEventsByCategoryId(String brand, Integer categoryId) {
    Instant now = nowUtcWithoutMillis();
    Instant past24Hours = nowUtcWithoutMillis().minus(Duration.ofHours(DURATION_24_HOURS));
    SimpleFilter.SimpleFilterBuilder filterBuilder =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, categoryId.toString())
            .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
            .addBinaryOperation(EVENT_START_TIME, BinaryOperation.greaterThanOrEqual, past24Hours)
            .addBinaryOperation(EVENT_START_TIME, BinaryOperation.lessThanOrEqual, now);

    return siteServeApiProvider
        .api(brand)
        .getEvent(
            Collections.emptyList(),
            Optional.of((SimpleFilter) filterBuilder.build()),
            Optional.empty());
  }

  private LimitRecordsFilter limitMarketAndOutcomeRecords() {
    return new LimitRecordsFilter.LimitRecordsFilterBuilder()
        .addField("market", 1)
        .addField("outcome", 1)
        .build();
  }

  private LimitToFilter limitToFilter() {
    return new LimitToFilter.LimitToFilterBuilder().build();
  }

  private ExistsFilter existsFilter() {
    return new ExistsFilterBuilder().build();
  }

  private static Instant nowUtcWithoutMillis() {
    return Instant.now().truncatedTo(ChronoUnit.SECONDS);
  }

  private static class Market {

    static final String TEMPLATE_MARKET_NAME = "market.templateMarketName";
    static final String DISP_SORT_NAME = "market.dispSortName";
    public static final String WIN_OR_EACH_WAY = "|Win or Each Way|";
  }

  @Override
  public List<Event> getNextFiveMinsAndLiveEvents(
      String brand, int categoryId, List<String> eventIds) {
    List<Event> events = new ArrayList<>();

    if (eventIds.isEmpty()) {
      return Collections.emptyList();
    } else {
      List<List<String>> eventIdSubSets = Lists.partition(eventIds, 100);
      eventIdSubSets.forEach(
          eventIdSet -> {
            events.addAll(getNext5MinsEvents(brand, eventIdSet, categoryId));
            events.addAll(getLiveEvents(brand, eventIdSet, categoryId));
          });
    }
    return events;
  }

  public List<Event> getNext5MinsEvents(String brand, List<String> eventIds, int categoryId) {
    Instant now = nowUtcWithoutMillis();
    Instant in5Minutes = nowUtcWithoutMillis().plus(Duration.ofMinutes(5));
    SimpleFilter upcomingEventsFilterBuilder =
        (SimpleFilter)
            new SimpleFilterBuilder()
                .addField(EVENT_IS_ACTIVE)
                .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, categoryId)
                .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
                .addBinaryOperation(EVENT_SORT_CODE, BinaryOperation.equals, "MTCH")
                .addUnaryOperation(EVENT_IS_STARTED, UnaryOperation.isFalse)
                .addBinaryOperation(EVENT_START_TIME, BinaryOperation.greaterThan, now)
                .addBinaryOperation(EVENT_START_TIME, BinaryOperation.lessThan, in5Minutes)
                .addUnaryOperation(EVENT_IS_RESULTED, UnaryOperation.isFalse)
                .build();

    return siteServeApiProvider
        .api(brand)
        .getEvent(eventIds, Optional.of(upcomingEventsFilterBuilder), Optional.of(existsFilter()))
        .orElseGet(Collections::emptyList);
  }

  private List<Event> getLiveEvents(String brand, List<String> eventIds, int categoryId) {
    SimpleFilter liveEventsFilterBuilder =
        (SimpleFilter)
            new SimpleFilterBuilder()
                .addBinaryOperation(EVENT_CATEGORY_ID, BinaryOperation.equals, categoryId)
                .addBinaryOperation(EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
                .addBinaryOperation(EVENT_SORT_CODE, BinaryOperation.equals, "MTCH")
                .addBinaryOperation(
                    EVENT_DRILLDOWN_TAG_NAMES, BinaryOperation.intersects, BET_INPLAY_DRILLDOWN_TAG)
                .addField(EVENT_IS_STARTED)
                .addUnaryOperation(EVENT_IS_RESULTED, UnaryOperation.isFalse)
                .build();
    return siteServeApiProvider
        .api(brand)
        .getEvent(eventIds, Optional.of(liveEventsFilterBuilder), Optional.of(existsFilter()))
        .orElseGet(Collections::emptyList);
  }
}
