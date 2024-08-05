package com.ladbrokescoral.oxygen.seo.controller;

import com.ladbrokescoral.oxygen.seo.cms.service.CmsReactiveService;
import com.ladbrokescoral.oxygen.seo.util.SeoConstants;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

@RestController
@Slf4j
public class SeoCmsController {

  private CmsReactiveService cmsReactiveService;

  public SeoCmsController(CmsReactiveService cmsReactiveService) {
    this.cmsReactiveService = cmsReactiveService;
  }

  // /fanzone/sport-football/AstonVilla/now-next
  @GetMapping(value = "/fanzone/sport-football/{teamName}/{tabName}")
  public Mono<Boolean> getFanzones(
      @PathVariable String teamName,
      @PathVariable String tabName,
      @RequestHeader String userAgent,
      @RequestHeader String brand) {
    log.info("In SeoCmsController getFanzones {}", teamName);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? cmsReactiveService.isFanzone(brand, teamName, tabName)
        : Mono.just(false);
  }

  // in-play/football & /in-play/horse-racing
  @GetMapping(value = "/in-play/{categoryName}")
  public Mono<Boolean> getInplaySport(
      @PathVariable String categoryName,
      @RequestHeader String userAgent,
      @RequestHeader String brand) {
    log.info("In SeoCmsController getInplaySport {}", categoryName);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? cmsReactiveService.isInplaySport(brand, categoryName)
        : Mono.just(false);
  }

  /*
   * /sport/football/matches/today , /sport/football/matches/tomorrow
   * /sport/football/matches/future , /sport/football/specials
   */
  @GetMapping(
      value = {"/sport/{categoryName}/{tabName}", "/sport/{categoryName}/{tabName}/{subTabName}"})
  public Mono<Boolean> getSportTab(
      @RequestHeader @PathVariable String categoryName,
      @PathVariable String tabName,
      @PathVariable(required = false) String subTabName,
      @RequestHeader String userAgent,
      @RequestHeader String brand,
      @RequestHeader String deviceType) {
    log.info("In SeoCmsController getSportTab {}", tabName);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? cmsReactiveService.isSportTab(brand, categoryName, tabName, subTabName, deviceType)
        : Mono.just(false);
  }

  /*
   * virtual-sports/football/euro-cup && virtual-sports/us-horse-racing/neightherly-hills
   * virtual-sports/horse-racing/horse-racing-flat/237945501
   */
  @GetMapping(
      value = {
        "/virtual-sports/{sportTitle}/{trackTitle}",
        "/virtual-sports/{sportTitle}/{trackTitle}/{eventId}"
      })
  public Mono<Boolean> getVirtualSports(
      @PathVariable String sportTitle,
      @PathVariable String trackTitle,
      @PathVariable(required = false) String eventId,
      @RequestHeader String userAgent,
      @RequestHeader String brand) {
    log.info("In SeoCmsController getVirtualSports {}", trackTitle);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? cmsReactiveService.isVirtualSport(brand, sportTitle, trackTitle, eventId)
        : Mono.just(false);
  }

  // /promotions/details/1-2-FREE & /promotions/details/27
  @GetMapping(value = "/promotions/details/{promoKey}")
  public Mono<Boolean> getPromotions(
      @PathVariable String promoKey, @RequestHeader String userAgent, @RequestHeader String brand) {
    log.info("In SeoCmsController getPromotions {}", promoKey);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? cmsReactiveService.isPromotion(brand, promoKey)
        : Mono.just(false);
  }

  // /home/eventhub/4 & /home/eventhub/1
  @GetMapping("/home/eventhub/{hubIndex}")
  public Mono<Boolean> getHomePageEventhubData(
      @PathVariable Integer hubIndex,
      @RequestHeader String userAgent,
      @RequestHeader String brand,
      @RequestHeader String deviceType) {
    log.info("In SeoCmsController getHomePageEventhubData {}", hubIndex);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? cmsReactiveService.isEventHubData(brand, deviceType, hubIndex)
        : Mono.just(false);
  }

  // sport/football & sport/tv-specials
  @GetMapping(value = "/sport/{sportName}")
  public Mono<Boolean> getSportName(
      @PathVariable String sportName,
      @RequestHeader String userAgent,
      @RequestHeader String brand,
      @RequestHeader String deviceType) {
    log.info("In SeoCmsController getSportName {}", sportName);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? cmsReactiveService.isSportName(brand, sportName, deviceType)
        : Mono.just(false);
  }

  @GetMapping(value = "/big-competition/{competitionName}/{uri}")
  public Mono<Boolean> getCompetitionByBrandAndUri(
      @PathVariable String competitionName,
      @PathVariable String uri,
      @RequestHeader String brand,
      @RequestHeader String userAgent) {
    // This one has to handle subtab /big-competition/world-cup/matches/match-list
    log.info("In SeoBigCompetitionController {}", competitionName);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? cmsReactiveService.isCompetition(brand, competitionName, uri)
        // .onErrorReturn(false)
        : Mono.just(false); // Here /world-cup-2022 page was 404 due to that returning false
  }
}
