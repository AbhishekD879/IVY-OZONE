package com.ladbrokescoral.oxygen.seo.showdown.service;

import reactor.core.publisher.Mono;

public interface ShowdownReactiveService {

  Mono<Boolean> getContestInfo(String contestId);
}
