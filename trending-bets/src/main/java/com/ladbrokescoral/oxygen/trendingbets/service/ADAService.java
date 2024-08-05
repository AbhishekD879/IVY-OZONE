package com.ladbrokescoral.oxygen.trendingbets.service;

import com.ladbrokescoral.oxygen.trendingbets.dto.PersonalizedBets;
import com.ladbrokescoral.oxygen.trendingbets.model.ADARequestModel;
import com.ladbrokescoral.oxygen.trendingbets.webclient.ADARequestClient;
import java.util.Arrays;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
@Slf4j
public class ADAService {

  private final ADARequestClient adaRequestClient;
  private static final int MAX_LEG = 5;

  @Value("${fy.maxPlayerRecs:20}")
  private int playersMaxRec;

  public Mono<PersonalizedBets> getForYouTrendingBets(String userName) {
    ADARequestModel adaRequest = prepareADARequest(userName, true, false, null);
    return adaRequestClient.executePersonalizedRequest(adaRequest);
  }

  public Mono<PersonalizedBets> getFanzoneTrendingBets(String teamId) {
    ADARequestModel adaRequest = prepareADARequest(null, false, true, teamId);
    return adaRequestClient.executePersonalizedRequest(adaRequest);
  }

  private ADARequestModel prepareADARequest(
      String userName, boolean personalizedBets, boolean fzBets, String fzTeamId) {
    return ADARequestModel.builder()
        .players(userName != null ? Arrays.asList(userName) : null)
        .maxLegsToRec(MAX_LEG)
        .playerMaxRecCount(playersMaxRec)
        .handleMissingPlayers(true)
        .recommendModelBet(true)
        .personalizedRecs(personalizedBets)
        .fanzoneWidgetRecs(fzBets)
        .fanzoneTeamId(fzTeamId)
        .build();
  }
}
