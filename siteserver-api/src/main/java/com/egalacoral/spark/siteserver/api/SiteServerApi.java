package com.egalacoral.spark.siteserver.api;

import com.egalacoral.spark.siteserver.model.Aggregation;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.CategoryEntity;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Coupon;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.MediaProvider;
import com.egalacoral.spark.siteserver.model.Pool;
import com.egalacoral.spark.siteserver.model.RacingResult;
import com.egalacoral.spark.siteserver.model.Scorecast;
import com.egalacoral.spark.siteserver.model.Type;
import com.egalacoral.spark.siteserver.parameter.RacingForm;
import com.newrelic.api.agent.Trace;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.EnumSet;
import java.util.List;
import java.util.Optional;
import okhttp3.logging.HttpLoggingInterceptor;

public interface SiteServerApi {

  enum Level {
    NONE,
    BASIC,
    HEADERS,
    BODY
  }

  String COMPETITION_OUTCOME_NAME_DELIMITERS = " [Vv@/] | vs | Vs | VS |/";

  Optional<List<Event>> getNextNEventsForClass(
      int N,
      List<String> classIds,
      SimpleFilter simpleFilter,
      ExistsFilter existsFilter,
      boolean includeUndisplayed);

  Optional<List<Event>> getNextNEventsForClass(
      int no,
      List<String> classIds,
      SimpleFilter simpleFilter,
      ExistsFilter existsFilter,
      boolean includeUndisplayed,
      Boolean referenceEachWayTerms);

  Optional<List<Category>> getClasses(SimpleFilter filter, ExistsFilter existsFilter);

  Optional<List<Type>> getClassToSubTypeForClass(String classId, SimpleFilter filter);

  Optional<List<Type>> getClassToSubTypeForClass(List<String> classId, SimpleFilter filter);

  Optional<List<Type>> getClassToSubType(SimpleFilter filter);

  Optional<List<Category>> getClassToSubTypeForType(String typeId, BaseFilter filter);

  Optional<List<Category>> getClassToSubTypeForType(List<String> typeIds, BaseFilter filter);

  Optional<List<Market>> getEventToOutcomeForMarket(String id, Boolean includeUndisplayed);

  Optional<List<Market>> getEventToOutcomeForMarket(
      String id, Boolean includeUndisplayed, Boolean includeRestricted);

  Optional<List<Event>> getWholeEventToOutcomeForMarket(String id, Boolean includeUndisplayed);

  @Trace(dispatcher = true)
  Optional<List<Event>> getWholeEventToOutcomeForMarket(
      List<String> marketIds, boolean includeUndisplayed);

  Optional<List<Event>> getWholeEventToOutcomeForMarket(
      String id, Boolean includeUndisplayed, SimpleFilter simpleFilter);

  Optional<List<Event>> getEvents(SimpleFilter filter);

  Optional<List<Event>> getEventForOBClass(String obClassId, SimpleFilter filter);

  Optional<List<Event>> getEventByClass(
      List<String> classIds,
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed);

  Optional<List<Event>> getEventToMarketForClass(
      List<String> classIds,
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed);

  Optional<List<Event>> getEventToMarketForEvent(
      List<String> eventIds,
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed);

  Optional<List<Event>> getEventForType(String typeId, SimpleFilter filter);

  Optional<List<Event>> getEventForType(List<String> typeId, SimpleFilter filter);

  Optional<List<Event>> getEventForType(
      List<String> typeId,
      Optional<SimpleFilter> filter,
      Optional<ExistsFilter> existsFilter,
      Boolean includeUndisplayed);

  Optional<List<Event>> getEventToOutcomeForType(String typeId, SimpleFilter filter);

  Optional<List<Event>> getEventToOutcomeForType(List<String> typeId, SimpleFilter filter);

  Optional<List<Event>> getEventToOutcomeForType(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      List<String> prune,
      boolean includeUndisplayed);

  Optional<List<Event>> getEventToOutcomeForType(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitsToFilter,
      List<String> prune,
      boolean includeUndisplayed);

  Optional<List<Event>> getEventToOutcomeForType(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      List<String> prune,
      boolean includeUndisplayed);

  Optional<List<Children>> getEventToOutcomeForEvent(
      List<String> eventId,
      SimpleFilter filter,
      EnumSet<RacingForm> racingForm,
      List<String> prune);

  Optional<List<Event>> getEventToOutcomeForEvent(
      List<String> eventId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      List<String> prune,
      boolean includeUndisplayed);

  Optional<List<Event>> getEventToOutcomeForEvent(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitsToFilter,
      List<String> prune,
      boolean includeUndisplayed);

  Optional<List<Event>> getEventToOutcomeForEvent(
      List<String> typeId,
      SimpleFilter filter,
      ExistsFilter existsFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      List<String> prune,
      boolean includeUndisplayed);

  Optional<List<Children>> getEventToOutcomeForEvent(
      List<String> eventId,
      SimpleFilter filter,
      EnumSet<RacingForm> racingForm,
      List<String> prune,
      boolean includeUndisplayed);

  Optional<List<Children>> getEventToOutcomeForEvent(
      List<String> eventId,
      SimpleFilter filter,
      EnumSet<RacingForm> racingForm,
      List<String> prune,
      boolean includeUndisplayed,
      int marketsLimit);

  Optional<List<Aggregation>> getMarketsCountForEvent(List<String> eventId, SimpleFilter filter);

  Optional<List<Aggregation>> getEventMarketsCountForClass(
      List<String> classIds, SimpleFilter filter);

  Optional<List<Event>> getCommentaryForEvent(List<String> eventId);

  Optional<List<Event>> getEventToOutcomeForOutcome(
      List<String> eventId, SimpleFilter filter, List<String> prune);

  Optional<List<Event>> getEventToOutcomeForOutcome(
      List<String> eventId, SimpleFilter filter, List<String> prune, boolean includeUndisplayed);

  Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      ExistsFilter existsFilter);

  Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      ExistsFilter existsFilter,
      Boolean referenceEachWayTerms);

  Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter);

  Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      ExistsFilter existsFilter,
      List<String> prune);

  Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter,
      List<String> prune);

  Optional<List<Event>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter,
      List<String> prune,
      Boolean referenceEachWayTerms);

  Optional<List<Children>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter,
      List<String> prune,
      String externalKeys);

  Optional<List<Children>> getEventToOutcomeForClass(
      List<String> classId,
      SimpleFilter simpleFilter,
      LimitToFilter limitsToFilter,
      LimitRecordsFilter limitRecordsFilter,
      ExistsFilter existsFilter,
      List<String> prune,
      String externalKeys,
      Boolean referenceEachWayTerms);

  Optional<Event> getEvent(String eventId, Optional<SimpleFilter> simpleFilter);

  Optional<List<Event>> getEvent(
      List<String> eventIds,
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter);

  Optional<Event> getEvent(String eventId, Boolean includeUndisplayed);

  Optional<Scorecast> getScorecast(String marketId, String scorerOutcomeId);

  Optional<List<MediaProvider>> getMedia(String eventId);

  Optional<Market> getEventToMarketForMarket(String marketId);

  Optional<Event> getEventForMarket(String marketId);

  Optional<CategoryEntity> getCategory(
      String categoryId,
      Optional<SimpleFilter> filter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed);

  Optional<List<CategoryEntity>> getCategories(
      Optional<SimpleFilter> filter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed);

  Optional<Event> getResultedEvent(
      String eventId,
      Optional<SimpleFilter> filter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed);

  Optional<RacingResult> getRacingResultsForEvent(String eventId);

  Optional<Coupon> getCoupon(
      String couponId,
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed);

  Optional<List<Coupon>> getCoupons(
      Optional<SimpleFilter> simpleFilter,
      Optional<ExistsFilter> existsFilter,
      boolean includeUndisplayed);

  Optional<List<Pool>> getPools(SimpleFilter simpleFilter);

  Optional<List<Pool>> getPoolForEvent(String eventId, SimpleFilter simpleFilter);

  public static class Builder {
    private String apiVersion = "2.54";
    private Integer maxNumberOfRetries = 2;
    private Integer readTimeout = 10;
    private Integer connectionTimeout = 10;
    private String baseUrl = "https://127.0.0.1";
    private int poolSize = 5;
    private long keepAliveSeconds = 5 * 60;
    private HttpLoggingInterceptor.Level level = HttpLoggingInterceptor.Level.BODY;
    /**
     * Configured at OpenBet side. These are values that can be passed as N to such requests as
     * NextNEventForClass/{N}/{classIds} by default OB will return empty result for any other values
     * without re-configuration
     */
    private List<Integer> configuredNextNValues = Arrays.asList(3, 5, 7, 12);

    public Builder setUrl(String baseUrl) {
      this.baseUrl = baseUrl;
      return this;
    }

    public Builder setVersion(String apiVersion) {
      this.apiVersion = apiVersion;
      return this;
    }

    public Builder setMaxNumberOfRetries(Integer maxNumberOfRetries) {
      this.maxNumberOfRetries = maxNumberOfRetries;
      return this;
    }

    public Builder setConfiguredNextNValues(List<Integer> configuredNextNValues) {
      this.configuredNextNValues = configuredNextNValues;
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

    public Builder setLoggingLevel(SiteServerImpl.Level level) {
      switch (level) {
        case NONE:
          this.level = HttpLoggingInterceptor.Level.NONE;
          break;
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

    public Builder setConnectionPoolSettings(int poolSize, long keepAliveSeconds) {
      this.poolSize = poolSize;
      this.keepAliveSeconds = keepAliveSeconds;
      return this;
    }

    protected String getApiVersion() {
      return apiVersion;
    }

    protected Integer getMaxNumberOfRetries() {
      return maxNumberOfRetries;
    }

    protected Integer getReadTimeout() {
      return readTimeout;
    }

    protected Integer getConnectionTimeout() {
      return connectionTimeout;
    }

    protected String getBaseUrl() {
      return baseUrl;
    }

    protected int getPoolSize() {
      return poolSize;
    }

    protected long getKeepAliveSeconds() {
      return keepAliveSeconds;
    }

    protected HttpLoggingInterceptor.Level getLevel() {
      return level;
    }

    public SiteServerApi build() throws KeyManagementException, NoSuchAlgorithmException {
      return new SiteServerImpl(this);
    }

    public SiteServerManage manage(SiteServerApi siteServerApi) {
      if (siteServerApi instanceof SiteServerManage) {
        return (SiteServerManage) siteServerApi;
      }
      return null;
    }

    public List<Integer> getConfiguredNextNValues() {
      return this.configuredNextNValues;
    }
  }
}
