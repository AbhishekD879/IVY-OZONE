package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.spotlight.SpotlightItems;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Headers;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface SpotlightEndPoint {

  @GET("v4/sportsbook-api/categories/{categoryId}/events/{eventId}/content")
  @Headers("Accept: application/json")
  Call<SpotlightItems> getSpotlightItems(
      @Path("categoryId") int categoryId,
      @Path("eventId") String eventId,
      @Query("api-key") String apiKey,
      @Query("locale") String locale);
}
