package com.ladbrokescoral.oxygen.notification.client.optin;

import com.fatboyindustrial.gsonjodatime.Converters;
import com.fortify.annotations.FortifyCheckReturnValue;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.oxygen.notification.client.optin.model.IGMEvent;
import com.newrelic.api.agent.NewRelic;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.X509Certificate;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import lombok.extern.slf4j.Slf4j;
import okhttp3.ConnectionPool;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

@Slf4j
public class IGameMediaApiImpl implements IGameMediaApi {

  private final OxygenSettingsApiService service;
  private final int maxNumberOfRetries;

  public IGameMediaApiImpl(Builder builder)
      throws NoSuchAlgorithmException, KeyManagementException {

    maxNumberOfRetries = builder.getMaxNumberOfRetries();
    HttpLoggingInterceptor loggingInterceptor = new HttpLoggingInterceptor(logger::info);
    loggingInterceptor.setLevel(builder.getLevel());

    ConnectionPool connectionPool =
        new ConnectionPool(builder.getPoolSize(), builder.getKeepAliveSeconds(), TimeUnit.SECONDS);

    logger.warn("**** Allow untrusted SSL connection ****");

    final TrustManager[] listOfTrustManagers =
        new TrustManager[] {
          new X509TrustManager() {
            @Override
            public X509Certificate[] getAcceptedIssuers() {
              return new X509Certificate[0];
            }

            @Override
            public void checkServerTrusted(final X509Certificate[] chain, final String authType) {}

            @Override
            public void checkClientTrusted(final X509Certificate[] chain, final String authType) {}
          }
        };

    SSLContext sslContext = getSslContext(listOfTrustManagers);

    OkHttpClient httpClient =
        new OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .readTimeout(builder.getReadTimeout(), TimeUnit.SECONDS)
            .connectTimeout(builder.getConnectionTimeout(), TimeUnit.SECONDS)
            .connectionPool(connectionPool)
            .sslSocketFactory(
                sslContext.getSocketFactory(), (X509TrustManager) listOfTrustManagers[0])
            .hostnameVerifier((hostname, session) -> (hostname != null && session != null))
            .build();

    Retrofit retrofit =
        new Retrofit.Builder()
            .baseUrl(builder.getBaseUrl())
            .addConverterFactory(
                GsonConverterFactory.create(
                    Converters.registerDateTime(new GsonBuilder()).create()))
            .client(httpClient)
            .build();

    service = retrofit.create(OxygenSettingsApiService.class);
  }

  @FortifyCheckReturnValue
  private SSLContext getSslContext(TrustManager[] listOfTrustManagers)
      throws NoSuchAlgorithmException, KeyManagementException {
    SSLContext sslContext = SSLContext.getInstance("TLSv1.2");
    sslContext.init(null, listOfTrustManagers, new java.security.SecureRandom());
    return sslContext;
  }

  @Override
  public List<IGMEvent> getOpenedStreamEvents() {
    return invokeSyncRequest(service.getOpenedStreamEvents()).orElse(Collections.emptyList());
  }

  private Optional<List<IGMEvent>> invokeSyncRequest(Call<List<IGMEvent>> call) {
    Optional<Response<List<IGMEvent>>> response = Optional.empty();
    int counter = 0;
    boolean retry;
    do {
      retry = false;
      HttpUrl requestUrl = call.request().url();
      try {
        Call<List<IGMEvent>> localCall = call.clone();
        response = Optional.ofNullable(localCall.execute());
        if (response.isPresent() && !response.get().isSuccessful()) {
          throw new OxygenSettingsException(requestUrl.toString(), response.get());
        }
      } catch (OxygenSettingsException se) {
        NewRelic.noticeError(se);
        logger.error(se.toString(), se);
        throw se;
      } catch (Exception e) {
        NewRelic.noticeError(e);
        logger.error("Can't get data from OxygenSettingsAPI: for URL {}", requestUrl, e);
        if (counter < this.maxNumberOfRetries) {
          retry = true;
          counter++;
          logger.error("Retry {} for getting data from OxygenSettingsAPI: {}", counter, requestUrl);
        }
      }
    } while (retry);

    return response.filter(Response::isSuccessful).map(Response::body);
  }
}
