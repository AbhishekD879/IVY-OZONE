package com.oxygen.publisher.inplay.service;

import com.oxygen.publisher.model.*;
import java.util.List;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

/** Description of InplayConsumer API for Retrofit client */
public interface InplayConsumerApi {

  @GET("/api/inplay/generation")
  Call<String> getVersion();

  @GET("/api/inplay/model/{version}")
  Call<InPlayData> getInPlayModel(@Path("version") String version);

  @GET("/api/inplay/sportsribbon/{version}")
  Call<SportsRibbon> getSportsRibbon(@Path("version") String version);

  @GET("/api/inplay/cache/{version}")
  Call<InPlayCache> getInPlayCache(@Path("version") String version);

  @GET("/api/inplay/sportsegment/{storageKey}")
  Call<SportSegment> getSportSegment(@Path("storageKey") String storageKey);

  @GET("/api/inplay/virtuals/{version}")
  Call<List<VirtualSportEvents>> getVirtualSports(@Path("version") String version);
}
