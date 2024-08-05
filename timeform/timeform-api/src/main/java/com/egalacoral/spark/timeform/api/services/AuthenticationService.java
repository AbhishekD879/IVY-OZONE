package com.egalacoral.spark.timeform.api.services;

import com.egalacoral.spark.timeform.api.TimeFormContext;
import com.egalacoral.spark.timeform.api.services.endpoints.AuthEndpoint;
import com.egalacoral.spark.timeform.model.internal.TokenData;
import com.fortify.annotations.FortifyNotPassword;
import okhttp3.OkHttpClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import retrofit2.Call;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class AuthenticationService extends AbstractTimeFormService {

  // resolved in 19.2 version but could see in lower version
  @FortifyNotPassword private static final String VALUE_GRANT_TYPE_PASSWORD = "password";

  protected final Logger logger = LoggerFactory.getLogger(getClass());

  private final AuthEndpoint authEndpoint;

  public AuthenticationService(TimeFormContext context) {
    super(context);

    OkHttpClient.Builder httpClient = new OkHttpClient.Builder();

    if (context.getInterceptor() != null) {
      httpClient.addInterceptor(context.getInterceptor());
    }

    authEndpoint =
        new Retrofit.Builder() //
            .baseUrl(context.getLoginUrl()) //
            .addConverterFactory(GsonConverterFactory.create()) //
            .client(httpClient.build()) //
            .build() //
            .create(AuthEndpoint.class);
  }

  public Call<TokenData> getSessionToken(String user, String password) {
    return authEndpoint.login(VALUE_GRANT_TYPE_PASSWORD, user, password);
  }
}
