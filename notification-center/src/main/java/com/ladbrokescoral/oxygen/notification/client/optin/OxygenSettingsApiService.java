package com.ladbrokescoral.oxygen.notification.client.optin;

import com.ladbrokescoral.oxygen.notification.client.optin.model.IGMEvent;
import java.util.List;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Headers;

public interface OxygenSettingsApiService {

  @GET("opened")
  @Headers("Accept: application/json")
  Call<List<IGMEvent>> getOpenedStreamEvents();
}
