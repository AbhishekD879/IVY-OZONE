package com.egalacoral.spark.siteserver.api;

import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.toList;

import com.egalacoral.spark.siteserver.model.Aggregation;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.CategoryEntity;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Coupon;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.HealthCheck;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.MediaProvider;
import com.egalacoral.spark.siteserver.model.Pool;
import com.egalacoral.spark.siteserver.model.RacingResult;
import com.egalacoral.spark.siteserver.model.SSResponse;
import com.egalacoral.spark.siteserver.model.Scorecast;
import com.egalacoral.spark.siteserver.model.Type;
import com.egalacoral.spark.siteserver.parameter.RacingForm;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.EnumSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import lombok.extern.slf4j.Slf4j;
import okhttp3.ConnectionPool;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import org.apache.commons.collections4.ListUtils;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.jackson.JacksonConverterFactory;

@Slf4j
public class SiteServerImpl implements SiteServerApi, SiteServerManage, SiteServerMapper {

  private final ConnectionPool connectionPool;
  private SiteServerService service;

  private static final int PAGE_SIZE = 100;

  private final String apiVersion;
  private final Integer maxNumberOfRetries;
  private final List<Integer> configuredNextNValues;

  public static final ExistsFilter EMPTY_EXISTS_FILTER =
      new ExistsFilter.ExistsFilterBuilder().build();

  public static final SimpleFilter EMPTY_SIMPLE_FILTER =
      (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build();

  protected SiteServerImpl(Builder builder)
      throws NoSuchAlgorithmException, KeyManagementException {

    HttpLoggingInterceptor loggingInterceptor = new HttpLoggingInterceptor(log::info);
    loggingInterceptor.setLevel(builder.getLevel());

    this.apiVersion = builder.getApiVersion();
    this.maxNumberOfRetries = builder.getMaxNumberOfRetries();
    this.configuredNextNValues = builder.getConfiguredNextNValues();
    this.connectionPool =
        new ConnectionPool(builder.getPoolSize(), builder.getKeepAliveSeconds(), TimeUnit.SECONDS);

    log.warn("**** Allow untrusted SSL connection ****");

    final TrustManager[] listOfTrustManagers =
        new TrustManager[] {
          new X509TrustManager() {
            @Override
            public X509Certificate[] getAcceptedIssuers() {
              X509Certificate[] certificates = new X509Certificate[0];
              return certificates;
            }

            @Override
            public void checkServerTrusted(final X509Certificate[] chain, final String authType)
                throws CertificateException {}

            @Override
            public void checkClientTrusted(final X509Certificate[] chain, final String authType)
                throws CertificateException {}
          }
        };

    SSLContext sslContext = SSLContext.getInstance("SSL");
    sslContext.init(null, listOfTrustManagers, new java.security.SecureRandom());

    OkHttpClient httpClient =
        new OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .readTimeout(builder.getReadTimeout(), TimeUnit.SECONDS)
            .connectTimeout(builder.getConnectionTimeout(), TimeUnit.SECONDS)
            .connectionPool(connectionPool)
            .sslSocketFactory(
                sslContext.getSocketFactory(), (X509TrustManager) listOfTrustManagers[0])
            .hostnameVerifier((hostname, session) -> true)
            .build();

    Retrofit retrofit =
        new Retrofit.Builder()
            .baseUrl(builder.getBaseUrl())
            .addConverterFactory(JacksonConverterFactory.create(this.getObjectMapper()))
            .client(httpClient)
            .build();

    service = retrofit.create(SiteServerService.class);
  }

  /**
   * Returns upcoming events for specified classIds, where N - number of events per class to be
   * returned
   *
   * <p>By default, SiteServer accepts 3, 5, 7 and 12 as N parameter. Library will trim to desired
   * number of events per class, if client passes N less then any of mentioned above parameters. For
   * example: If client passes N=2, request will be sent with N=3, but result will be trimed to 2
   * events.
   */
  @Override
  public Optional<List<Event>> getNextNEventsForClass(
      int N,
      List<String> classIds,
      SimpleFilter simpleFilter,
      ExistsFilter existsFilter,
      boolean includeUndisplayed) {
    if (configuredNextNValues.isEmpty()) {
      log.warn("configuredNextNValues not set. returning empty for getNextNEventsForClass");
      return Optional.empty();
    } else if (N <= 0 || N > Collections.max(configuredNextNValues)) {
      log.warn(
          "N={} in getNextNEventsForClass is not accepted. Min=1. Max={}",
          N,
          Collections.max(configuredNextNValues));
      return Optional.empty();
    } else if (Objects.isNull(classIds)) {
      log.warn("classIds is null");
      return Optional.empty();
    } else if (classIds.isEmpty()) {
      log.warn("classIds is empty, probably it isn't configured at CMS");
      return Optional.empty();
    }
    boolean isNConfigured = configuredNextNValues.contains(N);

    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getNextNEventsForClass(
                this.apiVersion,
                isNConfigured ? N : findConfiguredCeilingN(N),
                toComaSeparatedString(classIds),
                simpleFilter.getQueryMap(),
                existsFilter.getQueryMap(),
                "en",
                includeUndisplayed));

    return processGetClassToEventResponse(response)
        .map(
            events -> {
              if (!isNConfigured) {
                return trimToDesiredNextNEvents(events, N);
              }
              return events;
            });
  }

  @Override
  public Optional<List<Event>> getNextNEventsForClass(
      int no,
      List<String> classIds,
      SimpleFilter simpleFilter,
      ExistsFilter existsFilter,
      boolean includeUndisplayed,
      Boolean referenceEachWayTerms) {
    if (configuredNextNValues.isEmpty() || Objects.isNull(classIds) || classIds.isEmpty()) {
      log.warn(
          "configuredNextNValues not set returning empty for getNextNEventsForClass or classIds is null or classIds is empty, probably it isn't configured at CMS ");
      return Optional.empty();
    } else if (no <= 0 || no > Collections.max(configuredNextNValues)) {
      log.warn(
          "N={} defined in method getNextNEventsForClass isn't allowed, the allowed values are Min=1. Max={}",
          no,
          Collections.max(configuredNextNValues));
      return Optional.empty();
    }
    boolean isNConfigured = configuredNextNValues.contains(no);

    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getNextNEventsForClass(
                this.apiVersion,
                isNConfigured ? no : findConfiguredCeilingN(no),
                toComaSeparatedString(classIds),
                simpleFilter.getQueryMap(),
                existsFilter.getQueryMap(),
                "en",
                includeUndisplayed,
                referenceEachWayTerms));

    return processGetClassToEventResponse(response)
        .map(
            (List<Event> events) -> {
              if (!isNConfigured) {
                return trimToDesiredNextNEvents(events, no);
              }
              return events;
            });
  }

  private int findConfiguredCeilingN(int N) {
    for (Integer configuredNextNValue : configuredNextNValues) {
      if (N <= configuredNextNValue) {
        return configuredNextNValue;
      }
    }
    log.warn("Didn't find ceiling of N={} in configuredNextNValues={}", N, configuredNextNValues);
    return N;
  }

  private List<Event> trimToDesiredNextNEvents(List<Event> nextNEvents, int requestN) {
    Map<String, List<Event>> eventsGroupedByClassId =
        nextNEvents.stream().collect(groupingBy(Event::getClassId));

    List<Event> result = new ArrayList<>();
    for (Entry<String, List<Event>> eventsByClassIdEntry : eventsGroupedByClassId.entrySet()) {
      List<Event> eventsForClass = eventsByClassIdEntry.getValue();
      result.addAll(eventsForClass.stream().limit(requestN).collect(Collectors.toList()));
    }
    return result;
  }

  @Trace(dispatcher = true)
  public Optional<List<Category>> getClasses(SimpleFilter filter, ExistsFilter existsFilter) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/Class", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getClasses(
                this.apiVersion, filter.getQueryMap(), existsFilter.getQueryMap(), "en"));
    return processGetClassToCategoryResponse(response);
  }

  @Override
  public Optional<HealthCheck> getHealthCheck() {
    Optional<SSResponse> response = this.invokeSyncRequest(service.getHealth(this.apiVersion));
    return response.map(
        resp ->
            resp.getChildren().stream()
                .map(Children::getHealthCheck)
                .filter(Objects::nonNull)
                .findFirst()
                .orElse(null));
  }

  private Optional<List<Category>> processGetClassToCategoryResponse(
      Optional<SSResponse> response) {
    return response.map(
        resp ->
            resp.getChildren().stream()
                .map(Children::getCategory)
                .filter(Objects::nonNull)
                .collect(toList()));
  }

  private Optional<List<Type>> processGetClassToSubTypeResponse(Optional<SSResponse> response) {
    return response.map(
        resp ->
            resp.getChildren().stream()
                .map(Children::getCategory)
                .filter(Objects::nonNull)
                .flatMap(s -> s.getTypes().stream())
                .collect(toList()));
  }

  private Optional<List<Event>> processGetClassToEventResponse(Optional<SSResponse> response) {
    return response.map(
        resp ->
            resp.getChildren().stream()
                .map(Children::getEvent)
                .filter(Objects::nonNull)
                .collect(toList()));
  }

  /**
   * Get details of certain Classes, and of all their Types and Subtypes. The response will contain
   * a Class record for each Class indicated by the ClassIdSet, and each Class record will contain a
   * Type record for each Type belonging to that Class, and each Type record will contain a SubType
   * record for each SubType belonging to that Type. SimpleFilters can be applied at the following
   * levels: Class, Type, SubType. ExistsFilters can be applied to the following relationships:
   * Class-Type, Class-Event, Type-SubType, Type-Event, SubType-Event. LimitTo filters can be
   * applied to the following record-types: None. LimitRecords filters can be applied to the
   * following record-types: None. Pruning can be applied at the following levels: Class, Type.
   * Pruning is automatically applied at the following levels: None. Decorations can be applied at
   * the following levels: Class, Type. Aggregations cannot be requested for this resource.
   *
   * @param classId certain Class
   * @param filter SimpleFilters can be applied at the following levels: Class, Type, SubType
   * @return List of Types
   */
  @Trace(dispatcher = true)
  @Override
  public Optional<List<Type>> getClassToSubTypeForClass(String classId, SimpleFilter filter) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/ClassToSubTypeForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getClassToSubTypeForClass(
                this.apiVersion, classId, filter.getQueryMap(), "en", true));
    return processGetClassToSubTypeResponse(response);
  }

  /**
   * Get details of certain Classes, and of all their Types and Subtypes. The response will contain
   * a Class record for each Class indicated by the ClassIdSet, and each Class record will contain a
   * Type record for each Type belonging to that Class, and each Type record will contain a SubType
   * record for each SubType belonging to that Type. SimpleFilters can be applied at the following
   * levels: Class, Type, SubType. ExistsFilters can be applied to the following relationships:
   * Class-Type, Class-Event, Type-SubType, Type-Event, SubType-Event. LimitTo filters can be
   * applied to the following record-types: None. LimitRecords filters can be applied to the
   * following record-types: None. Pruning can be applied at the following levels: Class, Type.
   * Pruning is automatically applied at the following levels: None. Decorations can be applied at
   * the following levels: Class, Type. Aggregations cannot be requested for this resource.
   *
   * @param classId list of certain Class
   * @param filter SimpleFilters can be applied at the following levels: Class, Type, SubType
   * @return List of Types
   */
  @Trace(dispatcher = true)
  @Override
  public Optional<List<Type>> getClassToSubTypeForClass(List<String> classId, SimpleFilter filter) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/ClassToSubTypeForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getClassToSubTypeForClass(
                this.apiVersion, toComaSeparatedString(classId), filter.getQueryMap(), "en", true));
    return processGetClassToSubTypeResponse(response);
  }

  /**
   * Get details of all Classes, and of all their Types and Subtypes. The response will contain a
   * Class record for each Class known to SiteServer, and each Class record will contain a Type
   * record for each Type belonging to that Class, and each Type record will contain a SubType
   * record for each SubType belonging to that Type. SimpleFilters can be applied at the following
   * levels: Class, Type, SubType. ExistsFilters can be applied to the following relationships:
   * Class-Type, Type-SubType, Type-Event, SubType-Event. LimitTo lters can be applied to the
   * following record-types: None. LimitRecords lters can be applied to the following record-types:
   * None. Pruning can be applied at the following levels: Class, Type. Pruning is automatically
   * applied at the following levels: None. Decorations can be applied at the following levels:
   * Class, Type. Aggregations cannot be requested for this resource.
   *
   * @param filter SimpleFilters can be applied at the following levels: Class, Type, SubType
   * @return List of Types
   */
  @Trace(dispatcher = true)
  @Override
  public Optional<List<Type>> getClassToSubType(SimpleFilter filter) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/ClassToSubType", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getClassToSubType(this.apiVersion, filter.getQueryMap(), "en", true));
    return processGetClassToSubTypeResponse(response);
  }

  @Override
  public Optional<List<Category>> getClassToSubTypeForType(
      List<String> typeIds, BaseFilter filter) {
    if (typeIds == null || typeIds.isEmpty()) {
      throw new IllegalArgumentException("typeIds are null or empty");
    }
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/ClassToSubTypeForType", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    String commaSeparatedTypeIds =
        typeIds.size() > 1 ? typeIds.stream().collect(Collectors.joining(",")) : typeIds.get(0);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getClassToSubTypeForType(
                this.apiVersion, commaSeparatedTypeIds, filter.getQueryMap(), "en", true));

    return processGetClassToCategoryResponse(response);
  }

  @Override
  public Optional<List<Category>> getClassToSubTypeForType(String typeId, BaseFilter filter) {
    return getClassToSubTypeForType(Arrays.asList(typeId), filter);
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Market>> getEventToOutcomeForMarket(String id, Boolean includeUndisplayed) {
    return getEventToOutcomeForMarket(id, includeUndisplayed, false);
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Market>> getEventToOutcomeForMarket(
      String id, Boolean includeUndisplayed, Boolean includeRestricted) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForMarket", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToOutcomeForMarket(
                this.apiVersion, id, null, "en", includeUndisplayed, includeRestricted));
    return response.map(
        resp ->
            resp.getChildren().stream()
                .map(Children::getEvent)
                .filter(Objects::nonNull)
                .flatMap(s -> s.getMarkets().stream())
                .collect(toList()));
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getWholeEventToOutcomeForMarket(
      String id, Boolean includeUndisplayed) {
    return getEventToOutcomeForMarket(
        Collections.singletonList(id), includeUndisplayed, EMPTY_SIMPLE_FILTER);
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getWholeEventToOutcomeForMarket(
      List<String> marketIds, boolean includeUndisplayed) {
    return getEventToOutcomeForMarket(marketIds, includeUndisplayed, EMPTY_SIMPLE_FILTER);
  }

  @Override
  public Optional<List<Event>> getWholeEventToOutcomeForMarket(
      String id, Boolean includeUndisplayed, SimpleFilter simpleFilter) {
    return getEventToOutcomeForMarket(
        Collections.singletonList(id), includeUndisplayed, simpleFilter);
  }

  private Optional<List<Event>> getEventToOutcomeForMarket(
      List<String> marketIds, Boolean includeUndisplayed, SimpleFilter simpleFilter) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForMarket", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);

    return pagedCalls(
        marketIds, input -> doGetEventToOutcomeForMarket(input, includeUndisplayed, simpleFilter));
  }

  private Optional<List<Event>> doGetEventToOutcomeForMarket(
      List<String> marketIds, Boolean includeUndisplayed, SimpleFilter simpleFilter) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToOutcomeForMarket(
                this.apiVersion,
                marketIds.stream().collect(Collectors.joining(",")),
                simpleFilter.getQueryMap(),
                "en",
                includeUndisplayed,
                false));
    return processGetClassToEventResponse(response);
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEvents(SimpleFilter filter) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/Event", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEvents(this.apiVersion, filter.getQueryMap(), null, "en", true));
    return processGetClassToEventResponse(response);
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventForOBClass(String obClassId, SimpleFilter filter) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/EventForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventForClass(
                this.apiVersion, obClassId, filter.getQueryMap(), null, "en", true));
    return processGetClassToEventResponse(response);
  }

  @Override
  @Trace(dispatcher = true)
  public Optional<List<Event>> getEventByClass(
      List<String> classIds,
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/EventForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    String classIdString = classIds.stream().collect(Collectors.joining(","));

    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventForClass(
                this.apiVersion,
                classIdString,
                simpleFilter.map(SimpleFilter::getQueryMap).orElse(null),
                existsFilter.map(ExistsFilter::getQueryMap).orElse(null),
                "en",
                includeUndisplayed));
    return processGetClassToEventResponse(response);
  }

  @Override
  @Trace(dispatcher = true)
  public Optional<List<Event>> getEventToMarketForClass(
      List<String> classIds,
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToMarketForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    String classIdString = classIds.stream().collect(Collectors.joining(","));

    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToMarketForClass(
                this.apiVersion,
                classIdString,
                simpleFilter.map(SimpleFilter::getQueryMap).orElse(null),
                existsFilter.map(ExistsFilter::getQueryMap).orElse(null),
                "en",
                includeUndisplayed));
    return processGetClassToEventResponse(response);
  }

  @Override
  public Optional<List<Event>> getEventToMarketForEvent(
      List<String> eventIds,
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToMarketForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    String eventsIdString = eventIds.stream().collect(Collectors.joining(","));

    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToMarketForEvent(
                this.apiVersion,
                eventsIdString,
                simpleFilter.map(SimpleFilter::getQueryMap).orElse(null),
                existsFilter.map(ExistsFilter::getQueryMap).orElse(null),
                "en",
                includeUndisplayed));
    return processGetClassToEventResponse(response);
  }

  /**
   * Get details of the Events that belong to certain Types. The response will contain an Event
   * record for each Event belonging to the Type indicated by the TypeIdSet. SimpleFilters can be
   * applied at the following levels: Type, Event. ExistsFilters can be applied to the following
   * relationships: Event-Market. LimitTo lters can be applied to the following record-types: None.
   * LimitRecords lters can be applied to the following record-types: None. Pruning can be applied
   * at the following levels: None. Pruning is automatically applied at the following levels: None.
   * Decorations can be applied at the following levels: Event. Aggregations cannot be requested for
   * this resource.
   *
   * @param typeId certain Type
   * @param filter SimpleFilters can be applied at the following levels: Type, Event.
   * @return List of events
   */
  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventForType(String typeId, SimpleFilter filter) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/EventForType", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventForType(
                this.apiVersion, typeId, filter.getQueryMap(), null, "en", true));
    return processGetClassToEventResponse(response);
  }

  /**
   * Get details of the Events that belong to certain Types. The response will contain an Event
   * record for each Event belonging to the Type indicated by the TypeIdSet. SimpleFilters can be
   * applied at the following levels: Type, Event. ExistsFilters can be applied to the following
   * relationships: Event-Market. LimitTo lters can be applied to the following record-types: None.
   * LimitRecords lters can be applied to the following record-types: None. Pruning can be applied
   * at the following levels: None. Pruning is automatically applied at the following levels: None.
   * Decorations can be applied at the following levels: Event. Aggregations cannot be requested for
   * this resource.
   *
   * @param typeId list of certain types
   * @param filter SimpleFilters can be applied at the following levels: Type, Event.
   * @return List of events
   */
  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventForType(List<String> typeId, SimpleFilter filter) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/EventForType", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(typeId, input -> doGetEventForType(input, filter, EMPTY_EXISTS_FILTER, true));
  }

  @Override
  public Optional<List<Event>> getEventForType(
      List<String> typeId,
      Optional<SimpleFilter> filter,
      Optional<ExistsFilter> existsFilter,
      Boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/EventForType", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(
        typeId,
        input ->
            doGetEventForType(
                input,
                filter.orElse(EMPTY_SIMPLE_FILTER),
                existsFilter.orElse(EMPTY_EXISTS_FILTER),
                includeUndisplayed));
  }

  private Optional<List<Event>> doGetEventForType(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      Boolean includeUndisplayed) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventForType(
                this.apiVersion,
                toComaSeparatedString(typeId),
                filter.getQueryMap(),
                existsFilter.getQueryMap(),
                "en",
                includeUndisplayed));
    return processGetClassToEventResponse(response);
  }

  /**
   * @param typeId certain Type
   * @param filter SimpleFilters can be applied at the following levels: Type, Event.
   * @return List of events with drilldown to outcomes
   */
  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventToOutcomeForType(String typeId, SimpleFilter filter) {
    return getEventToOutcomeForType(Collections.singletonList(typeId), filter);
  }

  /**
   * Call events by type ids.
   *
   * @param typeId list of certain Type
   * @param filter SimpleFilters can be applied at the following levels: Type, Event.
   * @return List of events with drilldown to outcomes
   */
  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventToOutcomeForType(List<String> typeId, SimpleFilter filter) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForType", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(
        typeId,
        input -> doGetEventToOutcomeForType(input, filter, EMPTY_EXISTS_FILTER, null, true));
  }

  @Override
  @Trace(dispatcher = true)
  public Optional<List<Event>> getEventToOutcomeForType(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      List<String> prune,
      boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForType", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(
        typeId,
        input ->
            doGetEventToOutcomeForType(input, filter, existsFilter, prune, includeUndisplayed));
  }

  @Override
  @Trace(dispatcher = true)
  public Optional<List<Event>> getEventToOutcomeForType(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitsToFilter,
      List<String> prune,
      boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForType", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(
        typeId,
        input ->
            doGetEventToOutcomeForType(
                input, filter, existsFilter, limitsToFilter, prune, includeUndisplayed));
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventToOutcomeForType(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      List<String> prune,
      boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForType", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(
        typeId,
        input ->
            doGetEventToOutcomeForType(
                input,
                filter,
                existsFilter,
                limitsToFilter,
                limitRecordsFilter,
                prune,
                includeUndisplayed));
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Children>> getEventToOutcomeForEvent(
      List<String> eventId,
      SimpleFilter filter,
      EnumSet<RacingForm> racingForm,
      List<String> prune) {
    return getEventToOutcomeForEvent(eventId, filter, racingForm, prune, false);
  }

  @Override
  public Optional<List<Event>> getEventToOutcomeForEvent(
      List<String> eventId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      List<String> prune,
      boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForEvent", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<List<Children>> children =
        pagedCalls(
            eventId,
            input ->
                doGetEventToOutcomeForEvent(
                    input, filter, existsFilter, null, prune, includeUndisplayed, null));
    return children
        .map(List::stream)
        .map(stream -> stream.map(Children::getEvent).filter(Objects::nonNull).collect(toList()));
  }

  @Override
  public Optional<List<Event>> getEventToOutcomeForEvent(
      List<String> events,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitsToFilter,
      List<String> prune,
      boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForEvent", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<List<Children>> children =
        pagedCalls(
            events,
            input ->
                doGetEventToOutcomeForEvent(
                    input, filter, existsFilter, limitsToFilter, prune, includeUndisplayed));
    return children
        .map(List::stream)
        .map(stream -> stream.map(Children::getEvent).filter(Objects::nonNull).collect(toList()));
  }

  @Override
  public Optional<List<Event>> getEventToOutcomeForEvent(
      List<String> events,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      List<String> prune,
      boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForEvent", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<List<Children>> children =
        pagedCalls(
            events,
            input ->
                doGetEventToOutcomeForEvent(
                    input,
                    filter,
                    existsFilter,
                    limitsToFilter,
                    limitRecordsFilter,
                    prune,
                    includeUndisplayed));
    return children
        .map(List::stream)
        .map(stream -> stream.map(Children::getEvent).filter(Objects::nonNull).collect(toList()));
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Children>> getEventToOutcomeForEvent(
      List<String> eventId,
      SimpleFilter filter,
      EnumSet<RacingForm> racingForm,
      List<String> prune,
      boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForEvent", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(
        eventId,
        input ->
            doGetEventToOutcomeForEvent(
                input, filter, EMPTY_EXISTS_FILTER, racingForm, prune, includeUndisplayed, null));
  }

  @Override
  public Optional<List<Children>> getEventToOutcomeForEvent(
      List<String> eventId,
      SimpleFilter filter,
      EnumSet<RacingForm> racingForm,
      List<String> prune,
      boolean includeUndisplayed,
      int marketsLimit) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForEvent", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(
        eventId,
        input ->
            doGetEventToOutcomeForEvent(
                input,
                filter,
                EMPTY_EXISTS_FILTER,
                racingForm,
                prune,
                includeUndisplayed,
                marketsLimit));
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Aggregation>> getMarketsCountForEvent(
      List<String> eventId, SimpleFilter filter) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/MarketsCountForEvent", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(eventId, input -> doGetMarketsCountForEvent(input, filter));
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Aggregation>> getEventMarketsCountForClass(
      List<String> classIds, SimpleFilter filter) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/MarketsCountForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(classIds, input -> doGetEventMarketsCountForClass(input, filter));
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getCommentaryForEvent(List<String> eventId) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/CommentaryForEvent", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(eventId, this::doGetCommentaryForEvent);
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventToOutcomeForOutcome(
      List<String> eventId, SimpleFilter filter, List<String> prune) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForOutcome", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return getEventToOutcomeForOutcome(eventId, filter, prune, false);
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventToOutcomeForOutcome(
      List<String> eventId, SimpleFilter filter, List<String> prune, boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForOutcome", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return pagedCalls(
        eventId, input -> doGetEventToOutcomeForOutcome(input, filter, prune, includeUndisplayed));
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      ExistsFilter existsFilter) {
    return pagedCalls(
        classId,
        input ->
            doGetEventToOutcomeForClass(
                input,
                simpleFilter,
                limitsToFilter,
                new LimitRecordsFilter.LimitRecordsFilterBuilder().build(),
                existsFilter));
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      ExistsFilter existsFilter,
      Boolean referenceEachWayTerms) {
    return pagedCalls(
        classId,
        input ->
            doGetEventToOutcomeForClass(
                input,
                simpleFilter,
                limitsToFilter,
                new LimitRecordsFilter.LimitRecordsFilterBuilder().build(),
                existsFilter,
                referenceEachWayTerms));
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter) {
    return pagedCalls(
        classId,
        input ->
            doGetEventToOutcomeForClass(
                input, simpleFilter, limitsToFilter, limitRecordsFilter, existsFilter));
  }

  private Optional<List<Event>> doGetEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);

    return pagedCalls(
        classId,
        input -> {
          Optional<SSResponse> response =
              this.invokeSyncRequest(
                  service.getEventToOutcomeForClass(
                      this.apiVersion,
                      toComaSeparatedString(input),
                      simpleFilter.getQueryMap(),
                      limitsToFilter.getQueryMap(),
                      existsFilter.getQueryMap(),
                      "en",
                      limitRecordsFilter.getQueryMap()));

          return processGetClassToEventResponse(response);
        });
  }

  private Optional<List<Event>> doGetEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter,
      Boolean referenceEachWayTerms) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);

    return pagedCalls(
        classId,
        input -> {
          Optional<SSResponse> response =
              this.invokeSyncRequest(
                  service.getEventToOutcomeForClass(
                      this.apiVersion,
                      toComaSeparatedString(input),
                      simpleFilter.getQueryMap(),
                      limitsToFilter.getQueryMap(),
                      existsFilter.getQueryMap(),
                      "en",
                      limitRecordsFilter.getQueryMap(),
                      referenceEachWayTerms));

          return processGetClassToEventResponse(response);
        });
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      ExistsFilter existsFilter,
      List<String> prune) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);

    return pagedCalls(
        classId,
        input -> {
          Optional<SSResponse> response =
              this.invokeSyncRequest(
                  service.getEventToOutcomeForClass(
                      this.apiVersion,
                      toComaSeparatedString(input),
                      simpleFilter.getQueryMap(),
                      limitsToFilter.getQueryMap(),
                      existsFilter.getQueryMap(),
                      prune,
                      "en"));
          return processGetClassToEventResponse(response);
        });
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter,
      List<String> prune) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);

    return pagedCalls(
        classId,
        input -> {
          Optional<SSResponse> response =
              this.invokeSyncRequest(
                  service.getEventToOutcomeForClass(
                      this.apiVersion,
                      toComaSeparatedString(input),
                      simpleFilter.getQueryMap(),
                      limitsToFilter.getQueryMap(),
                      existsFilter.getQueryMap(),
                      prune,
                      "en",
                      limitRecordsFilter.getQueryMap()));
          return processGetClassToEventResponse(response);
        });
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter,
      List<String> prune,
      Boolean referenceEachWayTerms) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);

    return pagedCalls(
        classId,
        input -> {
          Optional<SSResponse> response =
              this.invokeSyncRequest(
                  service.getEventToOutcomeForClass(
                      this.apiVersion,
                      toComaSeparatedString(input),
                      simpleFilter.getQueryMap(),
                      limitsToFilter.getQueryMap(),
                      existsFilter.getQueryMap(),
                      prune,
                      "en",
                      limitRecordsFilter.getQueryMap(),
                      referenceEachWayTerms));
          return processGetClassToEventResponse(response);
        });
  }

  @Override
  public Optional<List<Children>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter,
      List<String> prune,
      String externalKeys) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);

    return pagedCalls(
        classId,
        input -> {
          Optional<SSResponse> response =
              this.invokeSyncRequest(
                  service.getEventToOutcomeForClass(
                      this.apiVersion,
                      toComaSeparatedString(input),
                      simpleFilter.getQueryMap(),
                      limitsToFilter.getQueryMap(),
                      existsFilter.getQueryMap(),
                      prune,
                      "en",
                      externalKeys,
                      limitRecordsFilter.getQueryMap()));
          return response.map(SSResponse::getChildren);
        });
  }

  @Override
  public Optional<List<Children>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter,
      List<String> prune,
      String externalKeys,
      Boolean referenceEachWayTerms) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToOutcomeForClass", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);

    return pagedCalls(
        classId,
        input -> {
          Optional<SSResponse> response =
              this.invokeSyncRequest(
                  service.getEventToOutcomeForClass(
                      this.apiVersion,
                      toComaSeparatedString(input),
                      simpleFilter.getQueryMap(),
                      limitsToFilter.getQueryMap(),
                      existsFilter.getQueryMap(),
                      prune,
                      "en",
                      externalKeys,
                      limitRecordsFilter.getQueryMap(),
                      referenceEachWayTerms));
          return response.map(SSResponse::getChildren);
        });
  }

  @Override
  @Trace(dispatcher = true)
  public Optional<Event> getEvent(String eventId, Optional<SimpleFilter> filter) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/Event", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return doGetEvent(Collections.singletonList(eventId), filter, Optional.empty(), false)
        .flatMap(list -> list.stream().findFirst());
  }

  @Override
  @Trace(dispatcher = true)
  public Optional<List<Event>> getEvent(
      List<String> eventIds,
      Optional<SimpleFilter> maybeSimplefilter,
      Optional<ExistsFilter> maybeExistsFilter) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/Event", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return doGetEvent(eventIds, maybeSimplefilter, maybeExistsFilter, false);
  }

  @Override
  @Trace(dispatcher = true)
  public Optional<Event> getEvent(String eventId, Boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Drilldown/{0}/Event", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return doGetEvent(
            Collections.singletonList(eventId),
            Optional.empty(),
            Optional.empty(),
            includeUndisplayed)
        .flatMap(list -> list.stream().findFirst());
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<Scorecast> getScorecast(String marketId, String scorerOutcomeId) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/Scorecasts/{1}/{2}",
            this.apiVersion, marketId, scorerOutcomeId);
    NewRelic.setTransactionName(null, transactionName);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getScorecast(this.apiVersion, marketId, scorerOutcomeId, "en"));
    if (response.isPresent()) {
      List<Scorecast> scorecasts =
          response.get().getChildren().stream()
              .map(Children::getScorecast)
              .filter(Objects::nonNull)
              .collect(toList());
      if (scorecasts.isEmpty()) {
        return Optional.ofNullable(null);
      } else {
        return Optional.of(scorecasts.get(0));
      }
    } else {
      return Optional.empty();
    }
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<List<MediaProvider>> getMedia(String eventId) {
    final String transactionName =
        MessageFormat.format("openbet-ssviewer/Media/{0}/MediaForEvent", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    Optional<SSResponse> response =
        this.invokeSyncRequest(service.getMedia(this.apiVersion, eventId, "en"));
    return response.map(
        resp ->
            resp.getChildren().stream()
                .map(Children::getMediaProvider)
                .filter(Objects::nonNull)
                .collect(toList()));
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<Market> getEventToMarketForMarket(String marketId) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToMarketForMarket/{1}", this.apiVersion, marketId);
    NewRelic.setTransactionName(null, transactionName);
    Optional<SSResponse> response =
        this.invokeSyncRequest(service.getEventToMarketForMarket(this.apiVersion, marketId));
    return response
        .map(SSResponse::getChildren)
        .flatMap(children -> children.stream().findFirst())
        .map(Children::getEvent)
        .map(Event::getChildren)
        .flatMap(children -> children.stream().findFirst())
        .map(Children::getMarket);
  }

  /**
   * @return {@link Event} for a given {@code marketId} containing the single {@link Market} that
   *     corresponds to that id.
   */
  @Trace(dispatcher = true)
  @Override
  public Optional<Event> getEventForMarket(String marketId) {
    String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/EventToMarketForMarket/{1}", this.apiVersion, marketId);

    NewRelic.setTransactionName(null, transactionName);

    return invokeSyncRequest(service.getEventToMarketForMarket(this.apiVersion, marketId))
        .map(SSResponse::getChildren)
        .flatMap(children -> children.stream().findFirst())
        .map(Children::getEvent);
  }

  @Override
  public Optional<CategoryEntity> getCategory(
      String categoryId,
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed) {
    NewRelic.setTransactionName(
        null,
        MessageFormat.format(
            "openbet-ssviewer/Drilldown/{0}/Category/{1}", this.apiVersion, categoryId));
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getCategory(
                this.apiVersion,
                categoryId,
                simpleFilter.orElse(EMPTY_SIMPLE_FILTER).getQueryMap(),
                existsFilter.orElse(EMPTY_EXISTS_FILTER).getQueryMap(),
                includeUndisplayed));
    return response
        .map(SSResponse::getChildren)
        .map(List::stream)
        .flatMap(
            stream -> stream.map(Children::getCategoryEntity).filter(Objects::nonNull).findFirst());
  }

  @Override
  public Optional<Event> getResultedEvent(
      String eventId,
      Optional<SimpleFilter> filter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/HistoricDrilldown/{0}/ResultedEvent", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return doGetResultedEvent(eventId, filter, existsFilter, includeUndisplayed);
  }

  @Override
  public Optional<RacingResult> getRacingResultsForEvent(String eventId) {
    final String transactionName =
        MessageFormat.format(
            "openbet-ssviewer/HistoricDrilldown/{0}/RacingResultsForEvent", this.apiVersion);
    NewRelic.setTransactionName(null, transactionName);
    return doGetRacingResultsForEvent(eventId);
  }

  private Optional<RacingResult> doGetRacingResultsForEvent(String eventId) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(service.getRacingResultsForEvent(this.apiVersion, eventId));
    return response
        .map(SSResponse::getChildren)
        .map(List::stream)
        .flatMap(
            stream -> stream.map(Children::getRacingResult).filter(Objects::nonNull).findFirst());
  }

  private Optional<Event> doGetResultedEvent(
      String eventId,
      Optional<SimpleFilter> maybeSimpleFilter,
      Optional<ExistsFilter> maybeExistsFilter,
      boolean includeUndisplayed) {
    SimpleFilter simpleFilter = maybeSimpleFilter.orElse(EMPTY_SIMPLE_FILTER);
    ExistsFilter existsFilter = maybeExistsFilter.orElse(EMPTY_EXISTS_FILTER);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getResultedEvent(
                this.apiVersion,
                eventId,
                simpleFilter.getQueryMap(),
                existsFilter.getQueryMap(),
                includeUndisplayed));
    return response
        .map(SSResponse::getChildren)
        .map(List::stream)
        .flatMap(
            stream -> stream.map(Children::getResultedEvent).filter(Objects::nonNull).findFirst());
  }

  @Override
  public Optional<List<CategoryEntity>> getCategories(
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed) {
    NewRelic.setTransactionName(
        null, MessageFormat.format("openbet-ssviewer/Drilldown/{0}/Category", this.apiVersion));
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getCategories(
                this.apiVersion,
                simpleFilter.orElse(EMPTY_SIMPLE_FILTER).getQueryMap(),
                existsFilter.orElse(EMPTY_EXISTS_FILTER).getQueryMap(),
                includeUndisplayed));
    return response
        .map(SSResponse::getChildren)
        .map(List::stream)
        .map(
            stream ->
                stream.map(Children::getCategoryEntity).filter(Objects::nonNull).collect(toList()));
  }

  @Override
  public Optional<Coupon> getCoupon(
      String couponId,
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed) {
    return this.invokeSyncRequest(
            service.getCoupon(
                this.apiVersion,
                couponId,
                simpleFilter.orElse(EMPTY_SIMPLE_FILTER).getQueryMap(),
                existsFilter.orElse(EMPTY_EXISTS_FILTER).getQueryMap(),
                "en",
                includeUndisplayed))
        .map(SSResponse::getChildren)
        .map(List::stream)
        .flatMap(stream -> stream.map(Children::getCoupon).filter(Objects::nonNull).findFirst());
  }

  @Override
  public Optional<List<Coupon>> getCoupons(
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed) {
    return this.invokeSyncRequest(
            service.getCoupons(
                this.apiVersion,
                simpleFilter.orElse(EMPTY_SIMPLE_FILTER).getQueryMap(),
                existsFilter.orElse(EMPTY_EXISTS_FILTER).getQueryMap(),
                "en",
                includeUndisplayed))
        .map(SSResponse::getChildren)
        .map(List::stream)
        .map(stream -> stream.map(Children::getCoupon).filter(Objects::nonNull).collect(toList()));
  }

  @Override
  public Optional<List<Pool>> getPools(SimpleFilter simpleFilter) {
    return this.invokeSyncRequest(
            service.getPools(this.apiVersion, simpleFilter.getQueryMap(), "en"))
        .map(SSResponse::getChildren)
        .map(List::stream)
        .map(stream -> stream.map(Children::getPool).filter(Objects::nonNull).collect(toList()));
  }

  @Override
  public Optional<List<Pool>> getPoolForEvent(String eventId, SimpleFilter simpleFilter) {
    return this.invokeSyncRequest(
            service.getPoolForEvent(this.apiVersion, eventId, simpleFilter.getQueryMap(), "en"))
        .map(SSResponse::getChildren)
        .map(List::stream)
        .map(stream -> stream.map(Children::getPool).filter(Objects::nonNull).collect(toList()));
  }

  private Optional<List<Event>> doGetEvent(
      List<String> eventIds,
      Optional<SimpleFilter> maybeSimpleFilter,
      Optional<ExistsFilter> maybeExistsFilter,
      Boolean includeUndisplayed) {
    SimpleFilter simpleFilter = maybeSimpleFilter.orElse(EMPTY_SIMPLE_FILTER);
    ExistsFilter existsFilter = maybeExistsFilter.orElse(EMPTY_EXISTS_FILTER);
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEvent(
                this.apiVersion,
                toComaSeparatedString(eventIds),
                simpleFilter.getQueryMap(),
                existsFilter.getQueryMap(),
                includeUndisplayed));
    return response
        .map(SSResponse::getChildren)
        .map(List::stream)
        .map(stream -> stream.map(Children::getEvent).filter(Objects::nonNull).collect(toList()));
  }

  private Optional<List<Event>> doGetEventToOutcomeForType(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      List<String> prune,
      boolean includeUndisplayed) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToOutcomeForType(
                this.apiVersion,
                toComaSeparatedString(typeId),
                filter.getQueryMap(),
                existsFilter.getQueryMap(),
                prune,
                "en",
                includeUndisplayed));
    return processGetClassToEventResponse(response);
  }

  private Optional<List<Event>> doGetEventToOutcomeForType(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitToFilter,
      List<String> prune,
      boolean includeUndisplayed) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToOutcomeForType(
                this.apiVersion,
                toComaSeparatedString(typeId),
                filter.getQueryMap(),
                existsFilter.getQueryMap(),
                limitToFilter.getQueryMap(),
                prune,
                "en",
                includeUndisplayed));
    return processGetClassToEventResponse(response);
  }

  private Optional<List<Event>> doGetEventToOutcomeForType(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitToFilter,
      LimitRecordsFilter limitRecordsFilter,
      List<String> prune,
      boolean includeUndisplayed) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToOutcomeForType(
                this.apiVersion,
                toComaSeparatedString(typeId),
                filter.getQueryMap(),
                existsFilter.getQueryMap(),
                limitToFilter.getQueryMap(),
                prune,
                "en",
                includeUndisplayed,
                limitRecordsFilter.getQueryMap()));
    return processGetClassToEventResponse(response);
  }

  private Optional<List<Event>> doGetEventToOutcomeForOutcome(
      List<String> eventId, SimpleFilter filter, List<String> prune, boolean includeUndisplayed) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToOutcomeForOutcome(
                this.apiVersion,
                toComaSeparatedString(eventId),
                filter.getQueryMap(),
                true,
                prune,
                "en",
                includeUndisplayed));
    return processGetClassToEventResponse(response);
  }

  private Optional<List<Aggregation>> doGetEventMarketsCountForClass(
      List<String> classIds, SimpleFilter filter) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getCountEventToMarketForClass(
                this.apiVersion,
                toComaSeparatedString(classIds),
                "event:market",
                filter.getQueryMap(),
                "en"));
    return response.map(
        resp ->
            resp.getChildren().stream()
                .map(Children::getAggregation)
                .filter(Objects::nonNull)
                .collect(toList()));
  }

  private Optional<List<Children>> doGetEventToOutcomeForEvent(
      List<String> eventId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      EnumSet<RacingForm> racingForm,
      List<String> prune,
      boolean includeUndisplayed,
      Integer marketsLimit) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToOutcomeForEvent(
                this.apiVersion,
                toComaSeparatedString(eventId),
                filter.getQueryMap(),
                existsFilter.getQueryMap(),
                racingForm,
                prune,
                "en",
                includeUndisplayed,
                Objects.isNull(marketsLimit) ? null : "market:" + marketsLimit));
    return response.map(SSResponse::getChildren);
  }

  private Optional<List<Children>> doGetEventToOutcomeForEvent(
      List<String> eventId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitToFilter,
      List<String> prune,
      boolean includeUndisplayed) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToOutcomeForEvent(
                this.apiVersion,
                toComaSeparatedString(eventId),
                filter.getQueryMap(),
                existsFilter.getQueryMap(),
                limitToFilter.getQueryMap(),
                prune,
                "en",
                includeUndisplayed));
    return response.map(SSResponse::getChildren);
  }

  private Optional<List<Children>> doGetEventToOutcomeForEvent(
      List<String> eventId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitToFilter,
      LimitRecordsFilter limitRecordsFilter,
      List<String> prune,
      boolean includeUndisplayed) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToOutcomeForEvent(
                this.apiVersion,
                toComaSeparatedString(eventId),
                filter.getQueryMap(),
                existsFilter.getQueryMap(),
                limitToFilter.getQueryMap(),
                prune,
                "en",
                includeUndisplayed,
                limitRecordsFilter.getQueryMap()));
    return response.map(SSResponse::getChildren);
  }

  private Optional<List<Aggregation>> doGetMarketsCountForEvent(
      List<String> eventId, SimpleFilter filter) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getCountEventToMarketForEvent(
                this.apiVersion,
                toComaSeparatedString(eventId),
                "event:market",
                filter.getQueryMap(),
                "en"));
    return response.map(
        resp ->
            resp.getChildren().stream()
                .map(Children::getAggregation)
                .filter(Objects::nonNull)
                .collect(toList()));
  }

  private Optional<List<Event>> doGetCommentaryForEvent(List<String> eventId) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getCommentaryForEvent(this.apiVersion, toComaSeparatedString(eventId), true));
    return processGetClassToEventResponse(response);
  }

  private Optional<SSResponse> invokeSyncRequest(Call<SSResponse> call) {
    Response<SSResponse> response = null;
    int counter = 0;
    boolean retry;
    do {
      retry = false;
      HttpUrl requestUrl = call.request().url();
      try {
        Call<SSResponse> localCall = call.clone();
        response = localCall.execute();
        if (!response.isSuccessful()) {
          throw new SiteServerException(requestUrl.toString(), response);
        }
      } catch (SiteServerException se) {
        NewRelic.noticeError(se);
        log.error(se.toString(), se);
        throw se;
      } catch (Exception e) {
        NewRelic.noticeError(e);
        log.error("Can't get data from SiteServer SiteServerApi: for URL {}", requestUrl, e);
        if (counter < this.maxNumberOfRetries) {
          retry = true;
          counter++;
          log.error(
              "Retry {} for getting data from SiteServer SiteServerApi: {}", counter, requestUrl);
        }
      }
    } while (retry);
    if (Objects.nonNull(response) && response.isSuccessful()) {
      return Optional.ofNullable(response.body());
    } else {
      return Optional.empty();
    }
  }

  private static <T, H> Optional<List<T>> pagedCalls(List<H> data, SiteServeCall<T, H> call) {
    List<List<H>> lists = ListUtils.partition(data, SiteServerImpl.PAGE_SIZE);
    List<Optional<List<T>>> collect =
        lists.stream()
            .map(
                m -> {
                  Optional<List<T>> listOptional = call.call(m);
                  return listOptional;
                })
            .collect(toList());
    if (collect.stream().anyMatch(o -> !o.isPresent())) {
      return Optional.empty();
    } else {
      List<T> result =
          collect.stream().flatMap(listOptional -> listOptional.get().stream()).collect(toList());
      return Optional.of(result);
    }
  }

  private String toComaSeparatedString(List<String> list) {
    return String.join(",", list);
  }

  @Override
  public void evictConnections() {
    this.connectionPool.evictAll();
  }
}
