package com.ladbrokescoral.oxygen.seo.controller;

import com.ladbrokescoral.oxygen.seo.showdown.service.ShowdownReactiveService;
import com.ladbrokescoral.oxygen.seo.util.SeoConstants;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

@RestController
@Slf4j
public class SeoShowdownController {

  @Autowired private ShowdownReactiveService showdownReactiveService;

  @GetMapping("/5-a-side/leaderboard/{contestId}")
  public Mono<Boolean> getContestInfo(
      @PathVariable String contestId, @RequestHeader String userAgent) {
    log.info("In SeoShowdownController contestId {}", contestId);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? showdownReactiveService.getContestInfo(contestId).onErrorReturn(false)
        : Mono.just(false);
  }
}
