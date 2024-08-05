package com.egalacoral.spark.siteserver.api;

import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.SSResponse;
import com.egalacoral.spark.siteserver.model.Type;
import com.fatboyindustrial.gsonjodatime.Converters;
import com.google.common.collect.Lists;
import com.google.gson.GsonBuilder;
import java.net.SocketTimeoutException;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/** Created by oleg.perushko@symphony-solutions.eu on 8/3/16 */
public class SiteServerAPI {
  private static final transient Logger logger = LoggerFactory.getLogger(SiteServerAPI.class);
  private OkHttpClient httpClient;
  private HttpLoggingInterceptor loggingInterceptor =
      new HttpLoggingInterceptor(message -> logger.debug(message));
  private Retrofit retrofit;
  private SiteServerService service;

  private final String apiVersion;
  private final Integer maxNumberOfRetries;

  private SiteServerAPI(Builder builder) {

    loggingInterceptor.setLevel(builder.level);

    this.apiVersion = builder.apiVersion;
    this.maxNumberOfRetries = builder.maxNumberOfRetries;

    httpClient =
        new OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .readTimeout(builder.readTimeout, TimeUnit.SECONDS)
            .connectTimeout(builder.connectionTimeout, TimeUnit.SECONDS)
            .build();

    retrofit =
        new Retrofit.Builder()
            .baseUrl(builder.baseUrl)
            .addConverterFactory(
                GsonConverterFactory.create(
                    Converters.registerDateTime(new GsonBuilder()).create()))
            .client(httpClient)
            .build();

    service = retrofit.create(SiteServerService.class);
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
  public Optional<List<Type>> getClassToSubTypeForClass(String classId, SimpleFilter filter) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getClassToSubTypeForClass(
                this.apiVersion, classId, filter.getQueryMap(), "en", true));
    if (response.isPresent()) {
      return Optional.ofNullable(
          response.get().getChildren().stream()
              .map(s -> s.getCategory())
              .filter(Objects::nonNull)
              .flatMap(s -> s.getTypes().stream())
              .collect(Collectors.toList()));
    } else {
      return Optional.empty();
    }
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
  public Optional<List<Type>> getClassToSubTypeForClass(List<String> classId, SimpleFilter filter) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getClassToSubTypeForClass(
                this.apiVersion, toComaSeparatedString(classId), filter.getQueryMap(), "en", true));
    if (response.isPresent()) {
      return Optional.ofNullable(
          response.get().getChildren().stream()
              .map(s -> s.getCategory())
              .filter(Objects::nonNull)
              .flatMap(s -> s.getTypes().stream())
              .collect(Collectors.toList()));
    } else {
      return Optional.empty();
    }
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
  public Optional<List<Type>> getClassToSubType(SimpleFilter filter) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getClassToSubType(this.apiVersion, filter.getQueryMap(), "en", true));
    if (response.isPresent()) {
      return Optional.ofNullable(
          response.get().getChildren().stream()
              .map(s -> s.getCategory())
              .filter(Objects::nonNull)
              .flatMap(s -> s.getTypes().stream())
              .collect(Collectors.toList()));
    } else {
      return Optional.empty();
    }
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
  public Optional<List<Event>> getEventForType(String typeId, SimpleFilter filter) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventForType(this.apiVersion, typeId, filter.getQueryMap(), "en", true));
    if (response.isPresent()) {
      return Optional.ofNullable(
          response.get().getChildren().stream()
              .map(s -> s.getEvent())
              .filter(Objects::nonNull)
              .collect(Collectors.toList()));
    } else {
      return Optional.empty();
    }
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
  public Optional<List<Event>> getEventForType(List<String> typeId, SimpleFilter filter) {
    return pagedCalls(typeId, 100, input -> doGetEventForType(input, filter));
  }

  private Optional<List<Event>> doGetEventForType(List<String> typeId, SimpleFilter filter) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventForType(
                this.apiVersion, toComaSeparatedString(typeId), filter.getQueryMap(), "en", true));
    if (response.isPresent()) {
      return Optional.ofNullable(
          response.get().getChildren().stream()
              .map(s -> s.getEvent())
              .filter(Objects::nonNull)
              .collect(Collectors.toList()));
    } else {
      return Optional.empty();
    }
  }

  /**
   * @param typeId certain Type
   * @param filter SimpleFilters can be applied at the following levels: Type, Event.
   * @return List of events with drilldown to outcomes
   */
  public Optional<List<Event>> getEventToOutcomeForType(String typeId, SimpleFilter filter) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToOutcomeForType(
                this.apiVersion, typeId, filter.getQueryMap(), "en", true));
    if (response.isPresent()) {
      return Optional.ofNullable(
          response.get().getChildren().stream()
              .map(s -> s.getEvent())
              .filter(Objects::nonNull)
              .collect(Collectors.toList()));
    } else {
      return Optional.empty();
    }
  }

  /**
   * Call events by type ids.
   *
   * @param typeId list of certain Type
   * @param filter SimpleFilters can be applied at the following levels: Type, Event.
   * @return List of events with drilldown to outcomes
   */
  public Optional<List<Event>> getEventToOutcomeForType(List<String> typeId, SimpleFilter filter) {
    return pagedCalls(typeId, 100, input -> doGetEventToOutcomeForType(input, filter));
  }

  protected Optional<List<Event>> doGetEventToOutcomeForType(
      List<String> typeId, SimpleFilter filter) {
    Optional<SSResponse> response =
        this.invokeSyncRequest(
            service.getEventToOutcomeForType(
                this.apiVersion, toComaSeparatedString(typeId), filter.getQueryMap(), "en", true));
    if (response.isPresent()) {
      return Optional.ofNullable(
          response.get().getChildren().stream()
              .map(s -> s.getEvent())
              .filter(Objects::nonNull)
              .collect(Collectors.toList()));
    } else {
      return Optional.empty();
    }
  }

  private Optional<SSResponse> invokeSyncRequest(Call<SSResponse> call) {
    Response<SSResponse> response = null;
    int counter = 0;
    boolean retry;
    do {
      retry = false;
      try {
        Call<SSResponse> localCall = call.clone();
        response = localCall.execute();
        if (!response.isSuccessful()) {
          throw new SiteServerException("Error response");
        }
      } catch (Exception e) {
        if (e instanceof SiteServerException) {
          throw new SiteServerException(e);
        }
        if (e instanceof SocketTimeoutException) {
          logger.error(
              "Can't get data from SiteServer API: {}. Root cause: SocketTimeoutException",
              call.request().url());
        }
        if (counter < this.maxNumberOfRetries) {
          retry = true;
          counter++;
          logger.error(
              "Retry {} for getting data from SiteServer API: {}", counter, call.request().url());
        }
      }
    } while (retry);
    if (Objects.nonNull(response) && response.isSuccessful()) {
      return Optional.ofNullable(response.body());
    } else {
      return Optional.empty();
    }
  }

  protected static <T, H> Optional<List<T>> pagedCalls(
      List<H> data, int pageSize, SiteServeCall<T, H> call) {
    List<List<H>> lists = Lists.partition(data, pageSize);
    List<T> result =
        lists.stream().flatMap(m -> call.call(m).get().stream()).collect(Collectors.toList());
    return Optional.of(result);
  }

  private String toComaSeparatedString(List<String> list) {
    return StringUtils.join(list, ",");
  }

  public static class Builder {
    private String apiVersion = "2.19";
    private Integer maxNumberOfRetries = 2;
    private Integer readTimeout = 10;
    private Integer connectionTimeout = 10;
    private final String baseUrl;
    private HttpLoggingInterceptor.Level level = HttpLoggingInterceptor.Level.NONE;

    public Builder(String baseUrl) {
      this.baseUrl = baseUrl;
    }

    public Builder setVersion(String apiVersion) {
      this.apiVersion = apiVersion;
      return this;
    }

    public Builder setMaxNumberOfRetries(Integer maxNumberOfRetries) {
      this.maxNumberOfRetries = maxNumberOfRetries;
      return this;
    }

    public Builder setReadTimeout(Integer readTimeout) {
      this.readTimeout = readTimeout;
      return this;
    }

    public Builder setConnectionTimeout(Integer connectionTimeout) {
      this.connectionTimeout = connectionTimeout;
      return this;
    }

    public Builder setLoggingLevel(Level level) {
      switch (level) {
        case BASIC:
          this.level = HttpLoggingInterceptor.Level.BASIC;
          break;
        case HEADERS:
          this.level = HttpLoggingInterceptor.Level.HEADERS;
          break;
        case BODY:
          this.level = HttpLoggingInterceptor.Level.BODY;
          break;
        default:
          this.level = HttpLoggingInterceptor.Level.NONE;
          break;
      }
      return this;
    }

    public SiteServerAPI build() {
      final SiteServerAPI api = new SiteServerAPI(this);
      return api;
    }
  }

  public enum Level {
    BASIC,
    HEADERS,
    BODY,
    NONE
  }
}
