package com.ladbrokescoral.oxygen.seo.cms.service;

import reactor.core.publisher.Mono;

public interface CmsReactiveService {

  Mono<Boolean> isVirtualSport(String brand, String title, String className, String eventId);

  Mono<Boolean> isFanzone(String brand, String teamName, String tabName);

  Mono<Boolean> isEventHubData(String brand, String deviceType, Integer hubIndex);

  Mono<Boolean> isPromotion(String brand, String promoKey);

  Mono<Boolean> isSportTab(
      String brand, String categoryName, String tabName, String subTabName, String deviceType);

  Mono<Boolean> isInplaySport(String brand, String categoryName);

  Mono<Boolean> isSportName(String brand, String sportName, String deviceType);

  Mono<Boolean> isCompetition(String brand, String competitionName, String uri);
}
