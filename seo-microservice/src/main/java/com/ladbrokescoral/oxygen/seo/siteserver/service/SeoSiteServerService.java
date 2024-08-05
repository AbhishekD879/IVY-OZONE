package com.ladbrokescoral.oxygen.seo.siteserver.service;

import com.egalacoral.spark.siteserver.api.SiteServerApiAsync;
import com.egalacoral.spark.siteserver.model.*;
import com.ladbrokescoral.oxygen.seo.util.QueryFilterBuilder;
import com.ladbrokescoral.oxygen.seo.util.SeoConstants;
import com.ladbrokescoral.oxygen.seo.util.SeoUtil;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
@Slf4j
public class SeoSiteServerService {

  private SiteServerApiAsync siteServerApiAsync;
  private Map<String, String> categoryIdConfigs;
  SeoUtil seoUtil;

  @Autowired
  public SeoSiteServerService(
      SiteServerApiAsync siteServerApiAsync,
      Map<String, String> categoryIdConfigs,
      SeoUtil seoUtil) {
    this.siteServerApiAsync = siteServerApiAsync;
    this.categoryIdConfigs = categoryIdConfigs;
    this.seoUtil = seoUtil;
  }

  public Mono<Boolean> getEvent(String eventId) {
    return siteServerApiAsync
        .getEventToOutcomeForEvent(eventId)
        .flatMap(
            (Optional<Event> event) -> {
              Boolean flag = false;
              if (event.isPresent()) {
                flag = true;
              }
              return Mono.just(flag);
            });
  }

  public Mono<Boolean> get5ASideEvent(
      String reqCategoryName,
      String reqClassName,
      String reqTypeName,
      String reqEventName,
      String reqEventId) {
    return siteServerApiAsync
        .getEvent(reqEventId)
        .flatMap(
            (Optional<Event> eventOptional) -> {
              Boolean flag = false;
              if (eventOptional.isPresent()) {
                Event event = eventOptional.get();
                if (validateEventData(
                    event, reqCategoryName, reqClassName, reqTypeName, reqEventName)) {
                  flag = true;
                }
              } else {
                flag = false;
              }
              return Mono.just(flag);
            });
  }

  public Mono<Boolean> getEventToOutcomeForEventReactive(
      String reqCategoryName,
      String reqClassName,
      String reqTypeName,
      String reqEventName,
      String reqEventId,
      String reqMarketName,
      String reqTotepoolName,
      String reqOrigin) {
    return siteServerApiAsync
        .getEventToOutcomeForEvent(reqEventId)
        .flatMap(
            (Optional<Event> event) -> {
              Boolean flag = false;
              if (event.isPresent()) {
                Event eventData = event.get();
                Set<String> collectionNames =
                    eventData.getMarkets().stream()
                        .map(Market::getCollectionNames)
                        .filter(Objects::nonNull)
                        .flatMap(str -> Arrays.stream(str.split(",")))
                        .map(SeoUtil::formatEventData)
                        .collect(Collectors.toSet());
                collectionNames = collectionNameUpdate(collectionNames, reqCategoryName);

                Set<String> queryNames =
                    new HashSet<>(Arrays.asList("offers-and-features", "next-races"));

                Set<String> toteNames =
                    new HashSet<>(
                        Arrays.asList("win", "place", "exacta", "trifecta", "quadpot", "placepot"));

                if (validateEventData(
                        eventData, reqCategoryName, reqClassName, reqTypeName, reqEventName)
                    && collectionNames.stream()
                        .anyMatch(
                            collectionName -> collectionName.equalsIgnoreCase(reqMarketName))) {
                  if (StringUtils.isNoneBlank(reqOrigin)) {
                    flag = queryNames.stream().anyMatch(s -> s.equalsIgnoreCase(reqOrigin));
                  } else if (StringUtils.isNoneBlank(reqTotepoolName)) {
                    flag = toteNames.stream().anyMatch(s -> s.equalsIgnoreCase(reqTotepoolName));
                  } else {
                    flag = true;
                  }
                }
              }
              return Mono.just(flag);
            });
  }

  private Set<String> collectionNameUpdate(Set<String> collectionNames, String reqCategoryName) {
    if (SeoConstants.HR_CATEGORY_NAME.equalsIgnoreCase(reqCategoryName)
        || SeoConstants.GH_CATEGORY_NAME.equalsIgnoreCase(reqCategoryName)) {
      collectionNames.add("Win-or-Each-Way");
      collectionNames.add("forecast");
      collectionNames.add("tricast");
      collectionNames.add("trap-market");
      collectionNames.add("totepool");
      collectionNames.add("trap-winner");
      collectionNames.add("win-only");
      collectionNames.add("to-finish");
      collectionNames.add("top-finish");
      collectionNames.add("insurance");
      collectionNames.add("ante-post");
      collectionNames.add("Each-Way-Additional-Places");
      collectionNames.add("Place-Only");
      collectionNames.add("Betting-Without");
      collectionNames.add("Outright");
      collectionNames.add("Standard");
      collectionNames.add("To-Win-By-1-Lengths");
      collectionNames.add("To-Win-By-3-Lengths");
      collectionNames.add("insurance-place-1");
      collectionNames.add("insurance-place-2");
      collectionNames.add("insurance-place-3");
      collectionNames.add("insurance-place-4");
      collectionNames.add("Faller-Insurance");
      collectionNames.add("To-Win");
      collectionNames.add("To-Not-Win");
      collectionNames.add("To-Not-Place");
      collectionNames.add("Best-Rest");
      collectionNames.add("Place-Insurance-2");
      collectionNames.add("Place-Insurance-3");
      collectionNames.add("Place-Insurance-4");
      collectionNames.add("Other-Markets");
      collectionNames.add("Winning-Distance-Specials");
      collectionNames.add("Best-Price-Guaranteed");
      collectionNames.add("Various-Specials");
    } else {
      collectionNames.add("all-markets");
      collectionNames.add("other-markets");
      collectionNames.add("bet-builder"); // lads
      collectionNames.add("main-markets");
      collectionNames.add("build-your-bet"); // coral
      collectionNames.add("5-a-side");
      collectionNames.add("2upwin--early-payout");
    }
    return collectionNames;
  }

  public Mono<Boolean> getCompetitionReactive(
      String categoryName, String className, String typeName) {
    String categoryId = categoryIdConfigs.get(categoryName);
    if (StringUtils.isEmpty(categoryId)) return Mono.just(false);
    Integer classId =
        siteServerApiAsync
            .getClasses(QueryFilterBuilder.getClassWithOpenEventsSimpleFilter(categoryId))
            .filter(
                category -> SeoUtil.formatEventData(category.getName()).equalsIgnoreCase(className))
            .map(Category::getId)
            .blockFirst();
    log.info("CompetitionReactive classId {}", classId);
    if (classId == null) return Mono.just(false);
    return siteServerApiAsync
        .getClassToSubTypeForClass(
            QueryFilterBuilder.getClassToSubTypeSimpleFilter(), String.valueOf(classId))
        .collectList()
        .flatMapMany(Flux::just)
        .any(
            types ->
                types.stream()
                    .anyMatch(
                        type ->
                            SeoUtil.formatEventData(type.getName()).equalsIgnoreCase(typeName)));
  }

  public Mono<Boolean> getCoupons(String categoryName, String couponName, String couponId) {
    return siteServerApiAsync
        .getCoupon(couponId)
        .flatMap(
            (Optional<Coupon> coupon) -> {
              Boolean flag = false;
              if (coupon.isPresent()) {
                log.info(
                    "couponName {} category Name {}",
                    SeoUtil.formatEventData(coupon.get().getName()),
                    SeoUtil.formatEventData(coupon.get().getCategoryName()));
                flag =
                    SeoUtil.formatEventData(coupon.get().getName()).equalsIgnoreCase(couponName)
                        && SeoUtil.formatEventData(coupon.get().getCategoryName())
                            .equalsIgnoreCase(categoryName);
                log.info("coupon flag {} ", flag);
              }
              return Mono.just(flag);
            });
  }

  public Mono<Boolean> getLotto(String lottoName) {
    return siteServerApiAsync
        .getLottery(QueryFilterBuilder.getLotteryToSimpleFilter())
        .collectList()
        .flatMapMany(Flux::just)
        .any(
            lotteries ->
                lotteries.stream()
                    .anyMatch(
                        lottery ->
                            seoUtil
                                .filterLottoDesc(lottery.getDescription())
                                .equalsIgnoreCase(lottoName)));
  }

  private boolean validateEventData(
      Event eventData,
      String reqCategoryName,
      String reqClassName,
      String reqTypeName,
      String reqEventName) {
    log.info(
        "ssRespClassName {} className {}",
        eventData.getClassName(),
        SeoUtil.formatEventData(eventData.getClassName()));
    log.info(
        "ssRespTypeName {} typeName {}",
        eventData.getTypeName(),
        SeoUtil.formatEventData(eventData.getTypeName()));
    log.info(
        "ssRespEventName {} eventName {}",
        eventData.getName(),
        SeoUtil.formatEventData(eventData.getName()));
    boolean flag = false;
    if (reqCategoryName.equalsIgnoreCase(SeoUtil.formatEventData(eventData.getCategoryName()))
        && reqClassName.equalsIgnoreCase(SeoUtil.formatEventData(eventData.getClassName()))
        && reqTypeName.equalsIgnoreCase(SeoUtil.formatEventData(eventData.getTypeName()))
        && reqEventName.equalsIgnoreCase(SeoUtil.formatEventData(eventData.getName()))) {
      flag = true;
    }
    return flag;
  }
}
