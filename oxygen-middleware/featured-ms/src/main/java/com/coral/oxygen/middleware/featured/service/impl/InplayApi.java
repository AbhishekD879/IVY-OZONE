package com.coral.oxygen.middleware.featured.service.impl;

import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbon;
import java.util.List;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

public interface InplayApi {

  @GET("/api/inplay/model/{version}")
  Call<InPlayData> getInPlayModel(@Path("version") String version);

  @GET("/api/inplay/generation")
  Call<String> getVersion();

  @GET("/api/inplay/sportsribbon/{version}")
  Call<SportsRibbon> getSportsRibbon(@Path("version") String version);

  @GET("/api/inplay/sportsegment/{storageKey}")
  Call<SportSegment> getSportSegment(@Path("storageKey") String storageKey);

  @GET("/api/inplay/virtuals/{storageKey}")
  Call<List<VirtualSportEvents>> getVirtualSportsData(@Path("storageKey") String storageKey);
}
