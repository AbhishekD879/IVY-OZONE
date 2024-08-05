package com.coral.oxygen.middleware.featured.service.impl;

import com.coral.oxygen.middleware.featured.exception.TrendingBetDataException;
import com.coral.oxygen.middleware.featured.service.PopularBetService;
import com.coral.oxygen.middleware.pojos.model.cms.featured.PopularAccaWidgetData;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.PopularAccaDto;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.PopularAccaResponse;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.PopularAccaType;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.TrendingBetsDto;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import retrofit2.Call;
import retrofit2.Response;

@Service
@Slf4j
public class PopularBetRestService implements PopularBetService {

  private final PopularBetApi popularBetApi;

  @Autowired
  public PopularBetRestService(PopularBetApi popularBetApi) {
    this.popularBetApi = popularBetApi;
  }

  @Override
  public TrendingBetsDto getTrendingBetByChannel(String chennelId) {
    return invokeSyncRequest(popularBetApi.getTrendingBetEvents(chennelId), TrendingBetsDto.class)
        .orElseThrow(() -> new TrendingBetDataException("Trending data version is empty"));
  }

  @Override
  public PopularAccaResponse getPopularAccaForData(PopularAccaWidgetData data) {
    PopularAccaDto popularAccaDto = populatePopularAccaRequest(data);
    return invokeSyncRequest(
            popularBetApi.getPopularAcca(popularAccaDto), PopularAccaResponse.class)
        .orElseThrow(() -> new TrendingBetDataException("Couldn't popular acca from trending ms"));
  }

  private PopularAccaDto populatePopularAccaRequest(PopularAccaWidgetData data) {
    return PopularAccaDto.builder()
        .key(PopularAccaType.getPopularAccaType(data.getAccaIdsType()))
        .values(data.getListOfIds())
        .minAccas(getValueOrDefault(data.getAccaRangeMin()))
        .maxAccas(getValueOrDefault(data.getAccaRangeMax()))
        .marketIdentifiers(stripValues(data.getMarketTemplateIds()))
        .build();
  }

  private List<String> stripValues(List<String> values) {
    if (!CollectionUtils.isEmpty(values)) {
      return values.stream().map(String::strip).toList();
    }
    return values;
  }

  private int getValueOrDefault(Integer value) {
    return value != null ? value : 0;
  }

  private <T> Optional<T> invokeSyncRequest(Call<T> call, Class<T> classOfT) {
    try {
      Response<T> response = call.execute();
      if (response.isSuccessful()) {
        // response is empty here only for `Call<String> getVersion()`
        // the others calls will produce EOFException
        return Optional.ofNullable(response.body());
      }
    } catch (Exception e) {
      log.error(
          "Can't get data trending bets MS. Error occurred for URL " + call.request().url(), e);
    }
    return Optional.empty();
  }
}
