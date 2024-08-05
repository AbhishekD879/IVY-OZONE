package com.ladbrokescoral.oxygen.seo.showdown.service;

import com.ladbrokescoral.oxygen.seo.configuration.ShowdownReactiveClient;
import com.ladbrokescoral.oxygen.seo.dto.ContestRequest;
import com.ladbrokescoral.oxygen.seo.dto.ContestResponse;
import com.ladbrokescoral.oxygen.seo.util.SeoConstants;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.ClientResponse;
import reactor.core.publisher.Mono;

@Service
@Slf4j
public class ShowdownReactiveServiceImpl implements ShowdownReactiveService {

  private ShowdownReactiveClient showdownReactiveClient;

  @Autowired
  public ShowdownReactiveServiceImpl(ShowdownReactiveClient showdownReactiveClient) {
    this.showdownReactiveClient = showdownReactiveClient;
  }

  @Override
  public Mono<Boolean> getContestInfo(String contestId) {
    return getContest(contestId).hasElement().switchIfEmpty(Mono.just(false));
  }

  private Mono<ContestResponse> getContest(String contestId) {
    ContestRequest contestRequest = new ContestRequest();
    contestRequest.setContestId(contestId);
    contestRequest.setBrand(SeoConstants.LAD_BRAND);
    return showdownReactiveClient
        .getClient()
        .post()
        .uri(
            uriBuilder ->
                uriBuilder.path("{brand}/leaderboard/contest").build(SeoConstants.LAD_BRAND))
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(contestRequest)
        .exchangeToMono(
            (ClientResponse clientResponse) -> {
              if (clientResponse.statusCode().is4xxClientError()) {
                Mono.just(false);
                log.error("showdown service failed");
                return clientResponse.createException().flatMap(Mono::error);
              } else {
                return clientResponse.bodyToMono(ContestResponse.class);
              }
            });
  }
}
