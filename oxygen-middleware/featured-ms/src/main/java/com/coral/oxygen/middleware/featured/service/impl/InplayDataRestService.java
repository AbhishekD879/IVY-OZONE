package com.coral.oxygen.middleware.featured.service.impl;

import com.coral.oxygen.middleware.featured.exception.InplayDataException;
import com.coral.oxygen.middleware.featured.service.InplayDataService;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import java.io.EOFException;
import java.io.IOException;
import java.text.MessageFormat;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import retrofit2.Call;
import retrofit2.Response;

@Service
@Slf4j
@AllArgsConstructor
public class InplayDataRestService implements InplayDataService {

  private static final String SPORT_SEGMENT_KEY =
      "{0}::{1}::LIVE_EVENT"; // version::sportId::LIVE_EVENT

  private final InplayApi inplayApi;

  @Override
  public String getInplayDataVersion() {
    return invokeSyncRequest(inplayApi.getVersion(), String.class)
        .orElseThrow(() -> new InplayDataException("Inplay data version is empty"));
  }

  @Override
  public InPlayData getInplayData(String version) {
    return invokeSyncRequest(inplayApi.getInPlayModel(version), InPlayData.class)
        .orElseThrow(
            () ->
                new InplayDataException(
                    MessageFormat.format("Inplay data is empty for version {0}", version)));
  }

  @Override
  public SportSegment getSportSegment(String version, Integer sportId) {
    String query = buildSportSegmentQuery(version, sportId);
    return invokeSyncRequest(inplayApi.getSportSegment(query), SportSegment.class)
        .orElseThrow(
            () ->
                new InplayDataException(
                    MessageFormat.format(
                        "Sport is empty for version {0} and sportId {1}", version, sportId)));
  }

  @Override
  public List<VirtualSportEvents> getVirtualSportData(String storageKey) {
    try {
      return inplayApi.getVirtualSportsData(storageKey).execute().body();
    } catch (Exception e) {
      log.info(e.getMessage());
      return Collections.emptyList();
    }
  }

  private String buildSportSegmentQuery(String verion, Integer sportId) {
    return MessageFormat.format(SPORT_SEGMENT_KEY, verion, sportId);
  }

  private <T> Optional<T> invokeSyncRequest(Call<T> call, Class<T> classOfT) {
    try {
      Response<T> response = call.execute();
      if (Objects.nonNull(response) && response.isSuccessful()) {
        // response is empty here only for `Call<String> getVersion()`
        // the others calls will produce EOFException
        return Optional.ofNullable(response.body());
      }
    } catch (EOFException e) {
      // on empty response log it
      log.info(
          "InPlay (Generic of {}) data empty response for URL {}", classOfT, call.request().url());
      // and create empty classOfT
      try {
        return Optional.of(classOfT.newInstance());
      } catch (Exception exception) {
        return Optional.empty();
      }
    } catch (IOException e) {
      log.error(
          "Can't get data inplay middleware. Error occurred for URL " + call.request().url(), e);
    }
    return Optional.empty();
  }
}
