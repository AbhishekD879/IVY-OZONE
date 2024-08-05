package com.coral.siteserver.api;

import com.coral.siteserver.model.SSResponse;
import java.util.List;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Headers;
import retrofit2.http.Path;
import retrofit2.http.Query;

/** Created by ogavur on 5/10/17. */
public interface CallsAPI {

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToMarketForMarket/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToMarketForMarket(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("includeRestricted") boolean includeRestricted,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/EventToOutcomeForOutcome/{id}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEventToOutcomeForOutcome(
      @Path("apiVersion") String apiVersion,
      @Path("id") String id,
      @Query("simpleFilter") List<String> simpleFilter,
      @Query("includeRestricted") boolean includeRestricted,
      @Query("includeUndisplayed") Boolean includeUndisplayed);

  @GET("openbet-ssviewer/Drilldown/{apiVersion}/Event/{ids}")
  @Headers("Accept: application/json")
  Call<SSResponse> getEvents(
      @Path("apiVersion") String apiVersion,
      @Path("ids") String ids,
      @Query("includeUndisplayed") Boolean includeUndisplayed);
}
