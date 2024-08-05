package com.coral.oxygen.middleware.featured.aem.model;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

public interface AemPublicEndpoints {

  @GET(
      "/bin/lc/{brandName}/offers.json/locale/en-gb/channels/any/pages/any/userType/any/carousels/any/imsLevel/any/response.json")
  Call<AemBannersResponse> getCarouselsBanners(@Path("brandName") String brandName);
}
