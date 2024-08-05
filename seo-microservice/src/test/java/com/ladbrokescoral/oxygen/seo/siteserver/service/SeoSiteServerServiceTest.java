package com.ladbrokescoral.oxygen.seo.siteserver.service;

import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SiteServerApiAsync;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Coupon;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Lottery;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Type;
import com.ladbrokescoral.oxygen.seo.util.QueryFilterBuilder;
import com.ladbrokescoral.oxygen.seo.util.SeoUtil;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.util.ReflectionTestUtils;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class SeoSiteServerServiceTest {

  @InjectMocks SeoSiteServerService seoSiteServerService;
  @Mock SiteServerApiAsync siteServerApiAsync;
  @MockBean Map<String, String> categoryIdConfigs = new HashMap<>();
  @MockBean @Spy SeoUtil seoUtil;

  @BeforeEach
  public void setUp() {
    categoryIdConfigs.put("football", "16");
    categoryIdConfigs.put("horse-racing", "21");
    categoryIdConfigs.put("greyhound-racing", "19");
    seoSiteServerService = new SeoSiteServerService(siteServerApiAsync, categoryIdConfigs, seoUtil);
  }

  public Optional<Event> getEventData() {
    Event event = new Event();
    event.setName("football");
    event.setId("132568");
    return Optional.of(event);
  }

  @Test
  void getEventEmptyTest() {
    when(siteServerApiAsync.getEventToOutcomeForEvent("132568"))
        .thenReturn(Mono.just(Optional.empty()));
    Mono<Boolean> getEventMono = seoSiteServerService.getEvent("132568");
    StepVerifier.create(getEventMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getEventTest() {
    Event event = new Event();
    event.setName("football");
    event.setId("132568");
    when(siteServerApiAsync.getEventToOutcomeForEvent("132568"))
        .thenReturn(Mono.just(Optional.of(event)));
    Mono<Boolean> getEventMono = seoSiteServerService.getEvent("132568");
    StepVerifier.create(getEventMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void get5ASideEmptyEventTest() {
    when(siteServerApiAsync.getEvent("238549826")).thenReturn(Mono.just(Optional.empty()));
    Mono<Boolean> FiveASideEventMono =
        seoSiteServerService.get5ASideEvent(
            "football", "football-england", "fa-cup", "leeds-vs-cardiff", "238549826");
    StepVerifier.create(FiveASideEventMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void get5ASideEventDataCheckTest() {
    Event event = new Event();
    event.setName("leeds-vs-cardif");
    event.setClassName("football-england");
    event.setCategoryName("football");
    event.setTypeName("fa-cup");
    event.setId("238549826");
    when(siteServerApiAsync.getEvent("238549826")).thenReturn(Mono.just(Optional.of(event)));
    Mono<Boolean> FiveASideEventMono =
        seoSiteServerService.get5ASideEvent(
            "football", "football-england", "fa-cup", "leeds-vs-cardiff", "238549826");
    StepVerifier.create(FiveASideEventMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void get5ASideEventTest() {
    Event event = new Event();
    event.setName("leeds-vs-cardiff");
    event.setClassName("football-england");
    event.setCategoryName("football");
    event.setTypeName("fa-cup");
    event.setId("238549826");
    when(siteServerApiAsync.getEvent("238549826")).thenReturn(Mono.just(Optional.of(event)));
    Mono<Boolean> FiveASideEventMono =
        seoSiteServerService.get5ASideEvent(
            "football", "football-england", "fa-cup", "leeds-vs-cardiff", "238549826");
    StepVerifier.create(FiveASideEventMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getEventToOutcomeForEventReactiveEmptyTest() {
    when(siteServerApiAsync.getEventToOutcomeForEvent("238549826"))
        .thenReturn(Mono.just(Optional.empty()));
    Mono<Boolean> EventToOutcomeForEventReactiveMono =
        seoSiteServerService.getEventToOutcomeForEventReactive(
            "football",
            "international",
            "international-friendlies",
            "panama-v-saudi-arabia",
            "238549826",
            "all-markets",
            "",
            "");
    StepVerifier.create(EventToOutcomeForEventReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getEventToOutcomeForEventReactiveTest() {
    when(siteServerApiAsync.getEventToOutcomeForEvent("238197021"))
        .thenReturn(Mono.just(Optional.of(getEventToOutcomeData())));
    Mono<Boolean> EventToOutcomeForEventReactiveMono =
        seoSiteServerService.getEventToOutcomeForEventReactive(
            "football",
            "international",
            "premier-league",
            "panama-v-saudi-arabia",
            "238197021",
            "all-markets",
            "",
            "");
    StepVerifier.create(EventToOutcomeForEventReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getEventToOutcomeCollectionNotMatchReactiveTest() {
    when(siteServerApiAsync.getEventToOutcomeForEvent("238197021"))
        .thenReturn(Mono.just(Optional.of(getEventCollectionNameData())));
    Mono<Boolean> EventToOutcomeForEventReactiveMono =
        seoSiteServerService.getEventToOutcomeForEventReactive(
            "football",
            "international",
            "premier-league",
            "panama-v-saudi-arabia",
            "238197021",
            "all",
            "",
            "");
    StepVerifier.create(EventToOutcomeForEventReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getEventToOutcomeForEventReactiveTotePoolTest() {
    when(siteServerApiAsync.getEventToOutcomeForEvent("238197021"))
        .thenReturn(Mono.just(Optional.of(getEventToOutcomeHrData())));
    Mono<Boolean> EventToOutcomeForEventReactiveMono =
        seoSiteServerService.getEventToOutcomeForEventReactive(
            "horse-racing",
            "international",
            "premier-league",
            "panama-v-saudi-arabia",
            "238197021",
            "totepool",
            "win",
            "");
    StepVerifier.create(EventToOutcomeForEventReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getEventToOutcomeForEventReactiveOriginTest() {
    when(siteServerApiAsync.getEventToOutcomeForEvent("238197021"))
        .thenReturn(Mono.just(Optional.of(getEventToOutcomeGhData())));
    Mono<Boolean> EventToOutcomeForEventReactiveMono =
        seoSiteServerService.getEventToOutcomeForEventReactive(
            "greyhound-racing",
            "international",
            "premier-league",
            "panama-v-saudi-arabia",
            "238197021",
            "forecast",
            "",
            "offers-and-features");
    StepVerifier.create(EventToOutcomeForEventReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  public Event getEventName() {
    Event event = new Event();
    event.setId("238197021");
    event.setName("panama-v-saudi-arabias");
    event.setClassName("international");
    event.setTypeName("premier-league");
    event.setCategoryName("football");
    Market market = new Market();
    market.setCollectionNames("Win-or-Each,tricast,all-markets");
    event.getMarkets().add(market);
    return event;
  }

  public Event getEventClassName() {
    Event event = new Event();
    event.setId("238197021");
    event.setName("panama-v-saudi-arabia");
    event.setClassName("internationals");
    event.setTypeName("premier-league");
    event.setCategoryName("football");
    Market market = new Market();
    market.setCollectionNames("Win-or-Each,tricast,all-markets");
    event.getMarkets().add(market);
    return event;
  }

  public Event getEventTypeName() {
    Event event = new Event();
    event.setId("238197021");
    event.setName("panama-v-saudi-arabia");
    event.setClassName("international");
    event.setTypeName("premier-leagues");
    event.setCategoryName("football");
    Market market = new Market();
    market.setCollectionNames("Win-or-Each,tricast,all-markets");
    event.getMarkets().add(market);
    return event;
  }

  public Event getCatgoryName() {
    Event event = new Event();
    event.setId("238197021");
    event.setName("panama-v-saudi-arabia");
    event.setClassName("international");
    event.setTypeName("premier-league");
    event.setCategoryName("footballTest");
    Market market = new Market();
    market.setCollectionNames("Win-or-Each,tricast,all-markets");
    event.getMarkets().add(market);
    return event;
  }

  @Test
  void getEventToOutcomeForCategoryNameNegativeTest() {
    when(siteServerApiAsync.getEventToOutcomeForEvent("238197021"))
        .thenReturn(Mono.just(Optional.of(getCatgoryName())));
    Mono<Boolean> EventToOutcomeForEventReactiveMono =
        seoSiteServerService.getEventToOutcomeForEventReactive(
            "football",
            "international",
            "premier-league",
            "panama-v-saudi-arabia",
            "238197021",
            "other-markets",
            "",
            "");
    StepVerifier.create(EventToOutcomeForEventReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getEventToOutcomeForEventNameNegativeTest() {
    when(siteServerApiAsync.getEventToOutcomeForEvent("238197021"))
        .thenReturn(Mono.just(Optional.of(getEventName())));
    Mono<Boolean> eventToOutcomeForEventReactiveMono =
        seoSiteServerService.getEventToOutcomeForEventReactive(
            "football",
            "international",
            "premier-league",
            "panama-v-saudi-arabia",
            "238197021",
            "other-markets",
            "",
            "");
    StepVerifier.create(eventToOutcomeForEventReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getEventToOutcomeForTypeNameNegativeTest() {
    when(siteServerApiAsync.getEventToOutcomeForEvent("238197021"))
        .thenReturn(Mono.just(Optional.of(getEventTypeName())));
    Mono<Boolean> EventToOutcomeForEventReactiveMono =
        seoSiteServerService.getEventToOutcomeForEventReactive(
            "football",
            "international",
            "premier-league",
            "panama-v-saudi-arabia",
            "238197021",
            "other-markets",
            "",
            "");
    StepVerifier.create(EventToOutcomeForEventReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getEventToOutcomeForClassNameNegativeTest() {
    when(siteServerApiAsync.getEventToOutcomeForEvent("238197021"))
        .thenReturn(Mono.just(Optional.of(getEventClassName())));
    Mono<Boolean> eventToOutcomeForEventReactiveMono =
        seoSiteServerService.getEventToOutcomeForEventReactive(
            "football",
            "international",
            "premier-league",
            "panama-v-saudi-arabia",
            "238197021",
            "other-markets",
            "",
            "");
    StepVerifier.create(eventToOutcomeForEventReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getCouponsTest() {
    Coupon coupon = new Coupon();
    coupon.setCategoryName("football");
    coupon.setName("weekend-matches");
    when(siteServerApiAsync.getCoupon("112")).thenReturn(Mono.just(Optional.of(coupon)));
    Mono<Boolean> CouponsMono =
        seoSiteServerService.getCoupons("football", "weekend-matches", "112");
    StepVerifier.create(CouponsMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getCouponsEmptyTest() {
    Coupon coupon = new Coupon();
    coupon.setCategoryName("football");
    coupon.setName("weekend-matches");
    when(siteServerApiAsync.getCoupon("112")).thenReturn(Mono.just(Optional.empty()));
    Mono<Boolean> CouponsMono =
        seoSiteServerService.getCoupons("football", "weekend-matches", "112");
    StepVerifier.create(CouponsMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getCouponNameNegativeTest() {
    Coupon coupon = new Coupon();
    coupon.setCategoryName("football");
    coupon.setName("weekend-test");
    when(siteServerApiAsync.getCoupon("112")).thenReturn(Mono.just(Optional.of(coupon)));
    Mono<Boolean> CouponsMono =
        seoSiteServerService.getCoupons("football", "weekend-matches", "112");
    StepVerifier.create(CouponsMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getCouponsNegativeTest() {
    Coupon coupon = new Coupon();
    coupon.setCategoryName("footballTest");
    coupon.setName("weekend-matches");
    when(siteServerApiAsync.getCoupon("112")).thenReturn(Mono.just(Optional.of(coupon)));
    Mono<Boolean> CouponsMono =
        seoSiteServerService.getCoupons("football", "weekend-matches", "112");
    StepVerifier.create(CouponsMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  public Event getEventCollectionNameData() {
    Event event = new Event();
    event.setId("238197021");
    event.setName("panama-v-saudi-arabia");
    event.setClassName("international");
    event.setTypeName("premier-league");
    event.setCategoryName("football");
    Market market = new Market();
    // market.setCollectionNames("Win-or-Each-Way,tricast,all-markets");
    event.getMarkets().add(market);
    return event;
  }

  public Event getEventToOutcomeData() {
    Event event = new Event();
    event.setId("238197021");
    event.setName("panama-v-saudi-arabia");
    event.setClassName("international");
    event.setTypeName("premier-league");
    event.setCategoryName("football");
    Market market = new Market();
    market.setCollectionNames("Win-or-Each-Way,tricast,all-markets");
    event.getMarkets().add(market);
    return event;
  }

  public Event getEventToOutcomeHrData() {
    Event event = new Event();
    event.setId("238197021");
    event.setName("panama-v-saudi-arabia");
    event.setClassName("international");
    event.setTypeName("premier-league");
    event.setCategoryName("horse-racing");
    Market market = new Market();
    market.setCollectionNames("Win-or-Each-Way,tricast,all-markets");
    event.getMarkets().add(market);
    return event;
  }

  public Event getEventToOutcomeGhData() {
    Event event = new Event();
    event.setId("238197021");
    event.setName("panama-v-saudi-arabia");
    event.setClassName("international");
    event.setTypeName("premier-league");
    event.setCategoryName("greyhound-racing");
    Market market = new Market();
    market.setCollectionNames("Win-or-Each-Way,tricast,all-markets");
    event.getMarkets().add(market);
    return event;
  }

  @Test
  void getCompetitionReactiveTest() {
    Type type = new Type();
    type.setId(72);
    type.setName("football-england");

    Category category = new Category();
    category.setId(72);
    category.setCategoryName("football");
    category.setName("international");

    when(siteServerApiAsync.getClasses(QueryFilterBuilder.getClassWithOpenEventsSimpleFilter("16")))
        .thenReturn(Flux.just(category));
    Integer classId =
        siteServerApiAsync
            .getClasses(QueryFilterBuilder.getClassWithOpenEventsSimpleFilter("16"))
            .filter(
                categ -> SeoUtil.formatEventData(categ.getName()).equalsIgnoreCase("international"))
            .map(Category::getId)
            .blockFirst();
    when(siteServerApiAsync.getClassToSubTypeForClass(
            QueryFilterBuilder.getClassToSubTypeSimpleFilter(), String.valueOf(classId)))
        .thenReturn(Flux.just(type));
    Mono<Boolean> CompetitionReactiveMono =
        seoSiteServerService.getCompetitionReactive(
            "football", "international", "football-england");
    StepVerifier.create(CompetitionReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getCompetitionEmptyCategoryReactiveTest() {
    Type type = new Type();
    type.setId(72);
    type.setName("football-england");

    Category category = new Category();
    category.setId(72);
    category.setCategoryName("football");
    category.setName("international");

    when(siteServerApiAsync.getClasses(QueryFilterBuilder.getClassWithOpenEventsSimpleFilter("16")))
        .thenReturn(Flux.just(category));
    Integer classId =
        siteServerApiAsync
            .getClasses(QueryFilterBuilder.getClassWithOpenEventsSimpleFilter("16"))
            .filter(
                categ -> SeoUtil.formatEventData(categ.getName()).equalsIgnoreCase("international"))
            .map(Category::getId)
            .blockFirst();
    when(siteServerApiAsync.getClassToSubTypeForClass(
            QueryFilterBuilder.getClassToSubTypeSimpleFilter(), String.valueOf(classId)))
        .thenReturn(Flux.just(type));
    Mono<Boolean> CompetitionReactiveMono =
        seoSiteServerService.getCompetitionReactive(
            "football", "internationalTest", "football-england");
    StepVerifier.create(CompetitionReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getCompetitionEmptyCategoryIdReactiveTest() {
    Type type = new Type();
    type.setId(72);
    type.setName("football-england");

    Category category = new Category();
    category.setId(72);
    category.setCategoryName("football");
    category.setName("international");

    when(siteServerApiAsync.getClasses(QueryFilterBuilder.getClassWithOpenEventsSimpleFilter("16")))
        .thenReturn(Flux.just(category));
    Integer classId =
        siteServerApiAsync
            .getClasses(QueryFilterBuilder.getClassWithOpenEventsSimpleFilter("16"))
            .filter(
                categ -> SeoUtil.formatEventData(categ.getName()).equalsIgnoreCase("international"))
            .map(Category::getId)
            .blockFirst();
    when(siteServerApiAsync.getClassToSubTypeForClass(
            QueryFilterBuilder.getClassToSubTypeSimpleFilter(), String.valueOf(classId)))
        .thenReturn(Flux.just(type));
    Mono<Boolean> CompetitionReactiveMono =
        seoSiteServerService.getCompetitionReactive(
            "footTest", "international", "football-england");
    StepVerifier.create(CompetitionReactiveMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getLottoTest() {
    ReflectionTestUtils.setField(seoUtil, "ballRegex", "\\d\\s*\\b(ball|Ball)\\b\\s*");
    ReflectionTestUtils.setField(seoUtil, "lottoRegex", "\\s*\\b(Lottery|Lotto)\\b\\s*");
    Lottery lottery = new Lottery();
    lottery.setDescription("Irish Lotto 7 ball");
    when(siteServerApiAsync.getLottery(QueryFilterBuilder.getLotteryToSimpleFilter()))
        .thenReturn(Flux.just(lottery));
    Mono<Boolean> lottoMono = seoSiteServerService.getLotto("daily-millions");
    StepVerifier.create(lottoMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getLotto49Test() {
    ReflectionTestUtils.setField(seoUtil, "ballRegex", "\\d\\s*\\b(ball|Ball)\\b\\s*");
    ReflectionTestUtils.setField(seoUtil, "lottoRegex", "\\s*\\b(Lottery|Lotto)\\b\\s*");
    Lottery lottery = new Lottery();
    lottery.setDescription("49's 6 Ball");
    when(siteServerApiAsync.getLottery(QueryFilterBuilder.getLotteryToSimpleFilter()))
        .thenReturn(Flux.just(lottery));
    Mono<Boolean> lottoMono = seoSiteServerService.getLotto("daily-millions");
    StepVerifier.create(lottoMono)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }
}
