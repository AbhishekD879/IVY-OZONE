package com.ladbrokescoral.oxygen.seo.controller;

import com.ladbrokescoral.oxygen.seo.siteserver.service.SeoSiteServerService;
import com.ladbrokescoral.oxygen.seo.util.SeoConstants;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

@RestController
@Slf4j
public class SeoSiteServerController {

  private final SeoSiteServerService seoSiteServerService;

  @Autowired
  public SeoSiteServerController(SeoSiteServerService seoSiteServerService) {
    this.seoSiteServerService = seoSiteServerService;
  }

  /*
   * /event/football/international/international-friendlies/panama-v-saudi-arabia/237766317/all-markets
   */
  @GetMapping(
      value = "/event/{categoryName}/{className}/{typeName}/{eventName}/{eventId}/{marketName}")
  public Mono<Boolean> getTierEdpEvent(
      @PathVariable String categoryName,
      @PathVariable String className,
      @PathVariable String typeName,
      @PathVariable String eventName,
      @PathVariable String eventId,
      @PathVariable String marketName,
      @RequestHeader String userAgent) {
    log.info(
        "In SeoSiteServerController getTierEdpEvent className {} typeName {} eventName {}",
        className,
        typeName,
        eventName);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? seoSiteServerService
            .getEventToOutcomeForEventReactive(
                categoryName, className, typeName, eventName, eventId, marketName, null, null)
            .onErrorReturn(false)
        : Mono.just(false);
  }

  /**
   * horse-racing & greyhound-racing EDP url handling
   *
   * <p>"greyhound-racing/greyhounds-live/doncaster/18-28-doncaster-dg/237851304/win-or-each-way"
   * "horse-racing/horse-racing-live/kempton/16-20-kempton/237837292/win-or-each-way"
   * "horse-racing/horse-racing-live/cagnes-sur/4-places/238170846/forecast?origin=offers-and-features"
   */
  @GetMapping(
      value = {
        "/{categoryName}/{className}/{typeName}/{eventName}/{eventId}/{marketName}",
        "/{categoryName}/{className}/{typeName}/{eventName}/{eventId}/{marketName}/{totepoolName}"
      })
  public Mono<Boolean> getHRAndGHEdpEvents(
      @PathVariable String categoryName,
      @PathVariable String className,
      @PathVariable String typeName,
      @PathVariable String eventName,
      @PathVariable String eventId,
      @PathVariable String marketName,
      @PathVariable(required = false) String totepoolName,
      @RequestParam(value = "origin", required = false) String origin,
      @RequestHeader String userAgent) {
    log.info(
        "In SeoSiteServerController getHRAndGHEdpEvents className {} typeName {} eventName {}",
        className,
        typeName,
        eventName);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? seoSiteServerService.getEventToOutcomeForEventReactive(
            categoryName, className, typeName, eventName, eventId, marketName, totepoolName, origin)
        : Mono.just(false);
  }

  /*
   * /event/football/football-england/fa-cup/leeds-vs-cardiff/238549826/5-a-side/pitch
   */
  @GetMapping(
      value = "/event/{categoryName}/{className}/{typeName}/{eventName}/{eventId}/5-a-side/pitch")
  public Mono<Boolean> get5AsideEvent(
      @PathVariable String categoryName,
      @PathVariable String className,
      @PathVariable String typeName,
      @PathVariable String eventName,
      @PathVariable String eventId,
      @RequestHeader String userAgent) {
    log.info(
        "In SeoSiteServerController get5AsideEvent className {} typeName {} eventName {}",
        className,
        typeName,
        eventName);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? seoSiteServerService.get5ASideEvent(categoryName, className, typeName, eventName, eventId)
        : Mono.just(false);
  }

  // competitions/football/english/fa-cup && competitions/football/international/world-cup-2022
  @GetMapping(value = "/competitions/{categoryName}/{className}/{typeName}")
  public Mono<Boolean> getCompetitions(
      @PathVariable String categoryName,
      @PathVariable String className,
      @PathVariable String typeName,
      @RequestHeader String userAgent) {
    log.info(
        "In SeoSiteServerController getCompetitions className {} typeName {} ",
        className,
        typeName);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? seoSiteServerService.getCompetitionReactive(categoryName, className, typeName)
        : Mono.just(false);
  }

  // /lotto/lotto-49s & /lotto/daily-millions
  @GetMapping(value = "/lotto/{lottoName}")
  public Mono<Boolean> getLotto(@PathVariable String lottoName, @RequestHeader String userAgent) {
    log.info("In SeoSiteServerController getLotto lottoName {} ", lottoName);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? seoSiteServerService.getLotto(lottoName)
        : Mono.just(false);
  }

  // coupons/football/weekend-matches/112 && /coupons/football/bankers-coupon/44
  @GetMapping(value = "/coupons/{categoryName}/{couponName}/{couponId}")
  public Mono<Boolean> getCoupons(
      @PathVariable String categoryName,
      @PathVariable String couponName,
      @PathVariable String couponId,
      @RequestHeader String userAgent) {
    log.info("In SeoSiteServerController getCoupons couponName {} ", couponName);
    return SeoConstants.USER_AGENT.equalsIgnoreCase(userAgent)
        ? seoSiteServerService.getCoupons(categoryName, couponName, couponId)
        : Mono.just(false);
  }
}
