package com.coral.oxygen.middleware.featured.aem;

import com.coral.oxygen.middleware.JsonFacade;
import com.coral.oxygen.middleware.featured.aem.model.AemPublicEndpoints;
import com.coral.oxygen.middleware.featured.aem.model.OfferObject;
import com.fatboyindustrial.gsonjodatime.Converters;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

@Slf4j
public class AemMetaConsumer {

  private String brandName;

  private final AemPublicEndpoints aemPublicEndpoints;

  public AemMetaConsumer(String baseUrl, String brandName, OkHttpClient okHttpClient) {
    this.brandName = brandName;
    aemPublicEndpoints =
        new Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(okHttpClient)
            .addConverterFactory(
                GsonConverterFactory.create(
                    Converters.registerDateTime(JsonFacade.GSON_BUILDER).create()))
            .build()
            .create(AemPublicEndpoints.class);
  }

  public List<OfferObject> getBanners() {
    return executeRequest(aemPublicEndpoints.getCarouselsBanners(brandName))
        .map(
            x -> {
              int count = 0;
              for (OfferObject offer : x.getOffers()) {
                offer.setDisplayOrder(count++);
              }
              return x.getOffers();
            })
        .orElse(Collections.emptyList());
  }

  private <T> Optional<T> executeRequest(Call<T> call) {
    try {
      Response<T> response = call.execute();
      if (!response.isSuccessful()) {
        String errorBody = response.errorBody() != null ? response.errorBody().string() : null;
        log.warn("[AemMetaConsumer] Response code: {}, errorBody: {}.", response.code(), errorBody);
        return Optional.empty();
      }
      return Optional.ofNullable(response.body());
    } catch (Exception e) {
      log.error("[AemMetaConsumer] Response code: NaN ", e);
      return Optional.empty();
    }
  }
}
