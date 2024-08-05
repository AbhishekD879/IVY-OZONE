package com.egalacoral.spark.timeform.api.services;

import com.egalacoral.spark.timeform.api.services.endpoints.AuthEndpoint;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.egalacoral.spark.timeform.api.TimeFormContext;
import com.egalacoral.spark.timeform.model.internal.TokenData;

import retrofit2.Call;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/**
 * Created by oleg.perushko@symphony-solutions.eu on 8/2/16
 */
public class AuthenticationService extends AbstractTimeFormService {

  private static final String URL_SUFFIX = "token";

  private static final String VALUE_GRANT_TYPE_PASSWORD = "password";

  protected final Logger logger = LoggerFactory.getLogger(getClass());

  private final AuthEndpoint authEndpoint;

  public AuthenticationService(TimeFormContext context) {
    super(context);

    authEndpoint = new Retrofit.Builder() //
        .baseUrl(context.getLoginUrl()) //
        .addConverterFactory(GsonConverterFactory.create()) //
        .build() //
        .create(AuthEndpoint.class);
  }

  public Call<TokenData> getSessionToken(String user, String password) {
    return authEndpoint.login(VALUE_GRANT_TYPE_PASSWORD, user, password);
  }

}
