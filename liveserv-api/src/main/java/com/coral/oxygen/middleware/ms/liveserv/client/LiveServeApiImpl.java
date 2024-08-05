package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.client.model.SubscriptionRequest;
import com.coral.oxygen.middleware.ms.liveserv.client.model.SubscriptionResponse;
import okhttp3.OkHttpClient;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.jackson.JacksonConverterFactory;

public class LiveServeApiImpl implements LiveServeApi, LiveServerMapper {

  private LiveServeService liveServeService;

  public LiveServeApiImpl(String liveServeBaseUrl) {
    Retrofit retrofit =
        new Retrofit.Builder()
            .baseUrl(liveServeBaseUrl)
            .addConverterFactory(JacksonConverterFactory.create(this.getObjectMapper()))
            .client(new OkHttpClient.Builder().build())
            .build();

    liveServeService = retrofit.create(LiveServeService.class);
  }

  @Override
  public SubscriptionResponse subscribe(SubscriptionRequest subscriptionRequest) {
    try {
      Response<SubscriptionResponse> liveServeResponse =
          liveServeService.subscribe(subscriptionRequest).execute();
      if (!liveServeResponse.isSuccessful()) {
        return SubscriptionResponse.failed(liveServeResponse.errorBody().string());
      }
      return liveServeResponse.body();
    } catch (Exception e) {
      return SubscriptionResponse.failed(e.getMessage());
    }
  }
}
