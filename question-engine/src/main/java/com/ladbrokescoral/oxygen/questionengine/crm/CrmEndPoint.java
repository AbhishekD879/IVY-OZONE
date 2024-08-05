package com.ladbrokescoral.oxygen.questionengine.crm;

import com.ladbrokescoral.oxygen.questionengine.dto.crm.CoinRequest;
import com.ladbrokescoral.oxygen.questionengine.dto.crm.CoinResponse;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Headers;
import retrofit2.http.POST;

public interface CrmEndPoint {

    @POST("/api/rest/v1/reward/awardAPI")
    @Headers("Content-Type: application/json")
    Call<CoinResponse> getRewardData(@Body CoinRequest coinRequest);
}
