package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.RssRewardResponse;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.RssRewardPublicService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
public class RssRewardPublicApi implements Public {
  private final RssRewardPublicService rssRewardPublicService;

  public RssRewardPublicApi(RssRewardPublicService rssRewardPublicService) {
    this.rssRewardPublicService = rssRewardPublicService;
  }

  @GetMapping(value = "/bma/ce/rssrewards")
  public ResponseEntity<RssRewardResponse> getRssRewards() {
    log.info("RssRewardPublicApi Method starts");
    return rssRewardPublicService.getRssReward();
  }
}
