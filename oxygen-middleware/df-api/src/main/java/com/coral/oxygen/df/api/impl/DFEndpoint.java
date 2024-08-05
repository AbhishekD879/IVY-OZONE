package com.coral.oxygen.df.api.impl;

import com.coral.oxygen.middleware.pojos.model.df.RaceEvents;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface DFEndpoint {

  @GET("/{version}/sportsbook-api/categories/{category}/events/{eventIds}/content")
  Call<RaceEvents> getRaceEvent(
      @Path("version") String version,
      @Path("category") Integer category,
      @Path("eventIds") String eventIds,
      @Query("locale") String locale,
      @Query("api-key") String apiKey);
}
