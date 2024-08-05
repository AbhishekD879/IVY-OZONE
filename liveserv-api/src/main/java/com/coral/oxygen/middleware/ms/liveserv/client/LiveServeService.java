package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.client.model.SubscriptionRequest;
import com.coral.oxygen.middleware.ms.liveserv.client.model.SubscriptionResponse;
import retrofit2.Call;
import retrofit2.http.*;

public interface LiveServeService {
  @POST("subscription")
  @Headers("Accept: application/json")
  Call<SubscriptionResponse> subscribe(@Body SubscriptionRequest subscription);
}
