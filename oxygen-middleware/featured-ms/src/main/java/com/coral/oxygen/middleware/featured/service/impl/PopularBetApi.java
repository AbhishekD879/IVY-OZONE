package com.coral.oxygen.middleware.featured.service.impl;

import com.coral.oxygen.middleware.pojos.model.output.popular_bet.PopularAccaDto;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.PopularAccaResponse;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.TrendingBetsDto;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;

public interface PopularBetApi {

  @GET("/api/trendingbets/betslip/{channelId}")
  Call<TrendingBetsDto> getTrendingBetEvents(@Path("channelId") String channelId);

  @POST("/api/popular-acca")
  Call<PopularAccaResponse> getPopularAcca(@Body PopularAccaDto popularAccaDto);
}
