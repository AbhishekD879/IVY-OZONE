package com.egalacoral.spark.siteserver.api;

import com.egalacoral.spark.siteserver.model.SSResponse;
import com.egalacoral.spark.siteserver.parameter.RacingForm;
import java.util.EnumSet;
import java.util.List;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Headers;
import retrofit2.http.Path;
import retrofit2.http.Query;

/** Created by oleg.perushko@symphony-solutions.eu on 8/3/16 */
public interface SiteServerService {

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/ClassToSubTypeForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getClassToSubTypeForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/ClassToSubType")
  @Headers("Accept: application/json")
  Call<SSResponse> getClassToSubType(
      @Path("apiVersion") String apiVersion,
      @Query("simpleFilter") List<String> options,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/ClassToSubTypeForType/{typeIds}")
  @Headers("Accept: application/json")
  Call<SSResponse> getClassToSubTypeForType(
      @Path("apiVersion") String apiVersion,
      @Path("typeIds") String typeIds,
      @Query("simpleFilter") List<String> options,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/Event")
  @Headers("Accept: application/json")
  Call<SSResponse> getEvents(
      @Path("apiVersion") String apiVersion,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/NextNEventForClass/{N}/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getNextNEventsForClass(
      @Path("apiVersion") String apiVersion,
      @Path("N") int N,
      @Path("id") String classIds,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/NextNEventForClass/{N}/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getNextNEventsForClass(
      @Path("apiVersion") String apiVersion,
      @Path("N") int N,
      @Path("id") String classIds,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed,
      @Query("referenceEachWayTerms") Boolean referenceEachWayTerms);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToMarketForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToMarketForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventForType/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventForType(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForType/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForType(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> simpleFilterOptions,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForType/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForType(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> simpleFilterOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForType/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForType(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> simpleFilterOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed,
      @Query("limitRecords") List<String> limitRecords);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/Class")
  @Headers("Accept: application/json")
  Call<SSResponse> getClasses(
      @Path("apiVersion") String apiVersion,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang,
      @Query("limitRecords") List<String> limitRecords);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang,
      @Query("limitRecords") List<String> limitRecords,
      @Query("referenceEachWayTerms") Boolean referenceEachWayTerms);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("existsFilter") List<String> existsOptions,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("existsFilter") List<String> existsOptions,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang,
      @Query("limitRecords") List<String> limitRecords);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("existsFilter") List<String> existsOptions,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang,
      @Query("limitRecords") List<String> limitRecords,
      @Query("referenceEachWayTerms") Boolean referenceEachWayTerms);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("existsFilter") List<String> existsOptions,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang,
      @Query("externalKeys") String externalKeys,
      @Query("limitRecords") List<String> limitRecords);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("existsFilter") List<String> existsOptions,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang,
      @Query("externalKeys") String externalKeys,
      @Query("limitRecords") List<String> limitRecords,
      @Query("referenceEachWayTerms") Boolean referenceEachWayTerms);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForEvent/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForEvent(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("existsFilter") List<String> existsOptions,
      @Query("racingForm") EnumSet<RacingForm> racingForm,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed,
      @Query("limitRecords") String limitRecords);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForEvent/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForEvent(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> simpleFilterOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForEvent/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForEvent(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> simpleFilterOptions,
      @Query("limitTo") List<String> limitTo,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed,
      @Query("limitRecords") List<String> limitRecords);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToMarketForEvent/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getCountEventToMarketForEvent(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("count") String countedEntity,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("translationLang") String lang);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToMarketForClass/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getCountEventToMarketForClass(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("count") String countedEntity,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("translationLang") String lang);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForOutcome/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForOutcome(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("includeRestricted") boolean includeRestricted,
      @Query("prune") List<String> prune,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Commentary/{apiVersion}/CommentaryForEvent/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getCommentaryForEvent(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForMarket/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForMarket(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed,
      @Query("includeRestricted") Boolean includeRestricted);

  @GET("openbet-ssviewer/Common/{apiVersion}/HealthCheck")
  @Headers("Accept: application/json")
  Call<SSResponse> getHealth(@Path("apiVersion") String apiVersion);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/Scorecasts/{marketId}/{scorerOutcomeId}")
  @Headers("Accept: application/json")
  Call<SSResponse> getScorecast(
      @Path("apiVersion") String apiVersion,
      @Path("marketId") String marketId,
      @Path("scorerOutcomeId") String scorerOutcomeId,
      @Query("translationLang") String lang);

  @GET("openbet-ssviewer/Media/{apiVersion}/MediaForEvent/{eventId}")
  @Headers("Accept: application/json")
  Call<SSResponse> getMedia(
      @Path("apiVersion") String apiVersion,
      @Path("eventId") String eventId,
      @Query("translationLang") String lang);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToMarketForMarket/{marketId}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToMarketForMarket(
      @Path("apiVersion") String apiVersion, @Path("marketId") String marketId);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/Event/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEvent(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("existsFilter") List<String> existsOptions,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/Category/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getCategory(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("existsFilter") List<String> existsOptions,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/Category")
  @Headers("Accept: application/json")
  Call<SSResponse> getCategories(
      @Path("apiVersion") String apiVersion,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("existsFilter") List<String> existsOptions,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/Coupon/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getCoupon(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/Coupon")
  @Headers("Accept: application/json")
  Call<SSResponse> getCoupons(
      @Path("apiVersion") String apiVersion,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/Pool")
  @Headers("Accept: application/json")
  Call<SSResponse> getPools(
      @Path("apiVersion") String apiVersion,
      @Query("simpleFilter") List<String> simpleFilter,
      @Query("translationLang") String lang);

  @GET("openbet-ssviewer/HistoricDrilldown/{apiVersion}/ResultedEvent/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getResultedEvent(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleOptions,
      @Query("existsFilter") List<String> existsOptions,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/HistoricDrilldown/{apiVersion}/RacingResultsForEvent/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getRacingResultsForEvent(
      @Path("apiVersion") String apiVersion, @Path("id") String id);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToMarketForEvent/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToMarketForEvent(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("existsFilter") List<String> existsOptions,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/PoolForEvent/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getPoolForEvent(
      @Path("apiVersion") String apiVersion,
      @Path("id") String eventId,
      @Query("simpleFilter") List<String> queryMap,
      @Query("translationLang") String en);
}
