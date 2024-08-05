package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.Application;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.spotlight.SpotlightEventInfo;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.spotlight.SpotlightItems;
import com.ladbrokescoral.oxygen.cms.api.service.showdown.ShowdownService;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import javax.annotation.PostConstruct;
import lombok.Data;
import okhttp3.OkHttpClient;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.DependsOn;
import org.springframework.stereotype.Service;
import retrofit2.Retrofit;
import retrofit2.converter.jackson.JacksonConverterFactory;

@Service
@DependsOn(Application.MONGOCK)
public class SpotlightApiClient {
  public static final int RACING_CATEGORY_ID = 21;

  @Value("${nextRaces.categoryId}")
  private int categoryId = RACING_CATEGORY_ID;

  public static final String SPOTLIGHT_QUERY_STRING =
      "%sv4/sportsbook-api/categories/%s/events/%s/content?locale=en-GB&api-key=%s";
  private final BrandService brandService;

  private OkHttpClient okHttpClient;

  private ShowdownService showdownService;

  private static final Map<String, SpotlightApiConfig> SPOTLIGHT_APIS_BY_BRAND = new HashMap<>();

  public SpotlightApiClient(
      BrandService brandService, ShowdownService showdownService, OkHttpClient okHttpClient) {
    this.brandService = brandService;
    this.showdownService = showdownService;
    this.okHttpClient = okHttpClient;
  }

  // FIXME: nothing will happen on add/delete Brand
  @PostConstruct
  private void initApis() {
    this.brandService
        .findAll()
        .forEach(
            (Brand brand) -> {
              if (StringUtils.isNotBlank(brand.getSpotlightEndpoint())
                  && StringUtils.isNotBlank(brand.getSpotlightApiKey())) {
                SpotlightApiConfig spotlightApiConfig = new SpotlightApiConfig();
                spotlightApiConfig.url = brand.getSpotlightEndpoint();
                spotlightApiConfig.apiKey = brand.getSpotlightApiKey();
                SPOTLIGHT_APIS_BY_BRAND.put(brand.getBrandCode(), spotlightApiConfig);
              }
            });
  }

  public SpotlightEventInfo fetchSpotlightByEventId(String brand, String eventId) {
    SpotlightApiConfig config = SPOTLIGHT_APIS_BY_BRAND.get(brand);
    SpotlightEventInfo spotlightEventInfo;

    if (config != null) {
      spotlightEventInfo = requestFromSpotlightApi(eventId, config);
    } else {
      spotlightEventInfo = new SpotlightEventInfo();
      spotlightEventInfo.setError(true);
    }
    return spotlightEventInfo;
  }

  private SpotlightEventInfo requestFromSpotlightApi(String eventId, SpotlightApiConfig config) {
    SpotlightEventInfo spotlightEventInfo = new SpotlightEventInfo();
    SpotlightItems spotlightItems;
    Optional<SpotlightItems> resposne = getSpotlightInfo(eventId, config);
    if (resposne.isPresent()) {
      spotlightItems = resposne.get();
    } else {
      spotlightEventInfo.setError(true);
      return spotlightEventInfo;
    }
    Optional.ofNullable(spotlightItems.getSpotlightPostsByEventId().get(eventId))
        .ifPresent(
            (SpotlightEventInfo item) -> {
              spotlightEventInfo.setHorses(item.getHorses());
              spotlightEventInfo.setVerdict(item.getVerdict());
              spotlightEventInfo.setRaceName(item.getRaceName());
            });
    spotlightEventInfo.setError(spotlightItems.getError());
    return spotlightEventInfo;
  }

  private Optional<SpotlightItems> getSpotlightInfo(String eventId, SpotlightApiConfig config) {
    SpotlightEndPoint spotlightEndPoint =
        new Retrofit.Builder()
            .baseUrl(config.url)
            .client(okHttpClient)
            .addConverterFactory(JacksonConverterFactory.create())
            .build()
            .create(SpotlightEndPoint.class);

    return showdownService.invokeSyncRequest(
        spotlightEndPoint.getSpotlightItems(categoryId, eventId, config.apiKey, "en-GB"));
  }

  @Data
  private static class SpotlightApiConfig {
    private String url;
    private String apiKey;
  }
}
