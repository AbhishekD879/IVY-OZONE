package com.egalacoral.spark.siteserver.api;

import com.egalacoral.spark.siteserver.model.SSResponse;
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

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventForType/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventForType(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForType/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForType(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> options,
      @Query("translationLang") String lang,
      @Query("includeUndisplayed") Boolean includeUndisplayed);
}
