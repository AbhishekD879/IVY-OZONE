package com.egalacoral.spark.timeform.api.services.endpoints;

import com.egalacoral.spark.timeform.model.internal.TokenData;

import retrofit2.Call;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.POST;

public interface AuthEndpoint {

  @FormUrlEncoded
  @POST("token")
  Call<TokenData> login( //
      @Field("grant_type") String grantType, //
      @Field("username") String user, //
      @Field("password") String password);

}
