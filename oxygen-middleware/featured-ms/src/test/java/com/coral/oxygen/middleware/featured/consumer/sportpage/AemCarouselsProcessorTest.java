package com.coral.oxygen.middleware.featured.consumer.sportpage;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.common.configuration.GsonConfiguration;
import com.coral.oxygen.middleware.common.configuration.OkHttpClientCreator;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.common.service.SportsConfig;
import com.coral.oxygen.middleware.common.utils.OrdinalToNumberConverter;
import com.coral.oxygen.middleware.featured.aem.AemMetaConsumer;
import com.coral.oxygen.middleware.featured.aem.model.AemBannersRawKey;
import com.coral.oxygen.middleware.featured.aem.model.OfferObject;
import com.coral.oxygen.middleware.featured.configuration.AemMetaConsumerConfig;
import com.coral.oxygen.middleware.featured.configuration.AemMetaConsumerConfigTest.Oxygen;
import com.coral.oxygen.middleware.pojos.model.output.featured.AemBannersImg;
import com.coral.oxygen.middleware.pojos.model.output.featured.AemBannersModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@EnableConfigurationProperties
@Import(AemMetaConsumerConfig.class)
@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(
    classes = {
      SportsConfig.class,
      GsonConfiguration.class,
      OrdinalToNumberConverter.class,
      OkHttpClientCreator.class,
      Oxygen.class
    })
public class AemCarouselsProcessorTest {

  @Autowired AemCarouselsProcessor processor;

  @MockBean AemMetaConsumer aemMetaConsumer;

  @Test
  public void multiplyCollections() {
    OfferObject offer =
        OfferObject.builder()
            .offerName("carousel-test")
            .pages(Arrays.asList("coral:allowed-pages/football", "coral:allowed-pages/volleyball"))
            .carousels(Arrays.asList("coral:carousels/carousel2", "coral:carousels/carousel1"))
            .build();
    Map<AemBannersRawKey, OfferObject> node = processor.multiplyCollections(offer);
    assertTrue(node.size() == 4);
  }

  @Test
  public void testIdResolver_OK() {
    AemBannersRawKey expectedKey =
        AemBannersRawKey.builder()
            .type(PageType.sport)
            .pageId("21")
            .carouselId("carousel4")
            .build();
    assertEquals(
        expectedKey,
        processor.idResolver("coral:allowed-pages/horse-racing", "coral:carousels/carousel4"));
  }

  @Test
  public void testIdResolver_NPE_Cases_OK() {
    assertTrue(
        AemBannersRawKey.UNKNOWN_PAGE_KEY.equals(
            processor.idResolver("coral:allowed-pages/bla-bla", "coral:carousels/carousel4")));
    assertTrue(
        AemBannersRawKey.UNKNOWN_PAGE_KEY.hashCode()
            == processor
                .idResolver("coral:allowed-pages/bla-bla", "coral:carousels/carousel4")
                .hashCode());
    assertEquals(
        AemBannersRawKey.UNKNOWN_PAGE_KEY,
        processor.idResolver("coral:allowed-pages/bla-bla", "coral:carousels/carousel4"));
    assertEquals(AemBannersRawKey.UNKNOWN_PAGE_KEY, processor.idResolver(null, null));
  }

  @Test
  public void multiplyCollections_AllPages_Ok() {
    List<String> allPages =
        Arrays.asList(
            "coral:allowed-pages/rowing",
            "coral:allowed-pages/enhanced-multiples",
            "coral:allowed-pages/gaa",
            "coral:allowed-pages/powerboat",
            "coral:allowed-pages/ufc",
            "coral:allowed-pages/triathlon",
            "coral:allowed-pages/chess",
            "coral:allowed-pages/weightlifting",
            "coral:allowed-pages/sailing",
            "coral:allowed-pages/golf",
            "coral:allowed-pages/cricket",
            "coral:allowed-pages/synchronised-swimming",
            "coral:allowed-pages/motor-bikes",
            "coral:allowed-pages/volleyball",
            "coral:allowed-pages/virtual",
            "coral:allowed-pages/homepage-native",
            "coral:allowed-pages/skiing",
            "coral:allowed-pages/intl-tote",
            "coral:allowed-pages/movies",
            "coral:allowed-pages/politics",
            "coral:allowed-pages/tennis",
            "coral:allowed-pages/ski-jumping",
            "coral:allowed-pages/ice-hockey",
            "coral:allowed-pages/equestrian",
            "coral:allowed-pages/gymnastics",
            "coral:allowed-pages/lotto",
            "coral:allowed-pages/tv-specials",
            "coral:allowed-pages/taekwondo",
            "coral:allowed-pages/american-football",
            "coral:allowed-pages/motor-cars",
            "coral:allowed-pages/olympics",
            "coral:allowed-pages/wrestling",
            "coral:allowed-pages/baseball",
            "coral:allowed-pages/canoeing",
            "coral:allowed-pages/snooker",
            "coral:allowed-pages/motor-sports",
            "coral:allowed-pages/christmas-specials",
            "coral:allowed-pages/greyhounds",
            "coral:allowed-pages/shooting",
            "coral:allowed-pages/boxing",
            "coral:allowed-pages/floorball",
            "coral:allowed-pages/esports",
            "coral:allowed-pages/table-tennis",
            "coral:allowed-pages/athletics",
            "coral:allowed-pages/modern-pantathlon",
            "coral:allowed-pages/sports-homepage",
            "coral:allowed-pages/archery",
            "coral:allowed-pages/specials",
            "coral:allowed-pages/current-affairs",
            "coral:allowed-pages/darts",
            "coral:allowed-pages/hurling",
            "coral:allowed-pages/squash",
            "coral:allowed-pages/futsal",
            "coral:allowed-pages/winter-olympics",
            "coral:allowed-pages/motor-speedway",
            "coral:allowed-pages/football",
            "coral:allowed-pages/wolrd-cup",
            "coral:allowed-pages/new-year-specials",
            "coral:allowed-pages/weather",
            "coral:allowed-pages/sport-multiples",
            "coral:allowed-pages/gaelic-football",
            "coral:allowed-pages/water-polo",
            "coral:allowed-pages/curling",
            "coral:allowed-pages/beach-soccer",
            "coral:allowed-pages/judo",
            "coral:allowed-pages/winter-sports",
            "coral:allowed-pages/beach-volleyball",
            "coral:allowed-pages/rugby-league",
            "coral:allowed-pages/homepage",
            "coral:allowed-pages/lacrosse",
            "coral:allowed-pages/pool",
            "coral:allowed-pages/handball",
            "coral:allowed-pages/cycling",
            "coral:allowed-pages/australian-rules",
            "coral:allowed-pages/bandy",
            "coral:allowed-pages/celebrities",
            "coral:allowed-pages/pelota",
            "coral:allowed-pages/seasonal",
            "coral:allowed-pages/world-cup",
            "coral:allowed-pages/commonwealth-games",
            "coral:allowed-pages/fishing",
            "coral:allowed-pages/badminton",
            "coral:allowed-pages/swimming",
            "coral:allowed-pages/yachting",
            "coral:allowed-pages/worldcup-group1",
            "coral:allowed-pages/pesapolla",
            "coral:allowed-pages/shinty",
            "coral:allowed-pages/worldcup-featured",
            "coral:allowed-pages/netball",
            "coral:allowed-pages/royal-specials",
            "coral:allowed-pages/speed-skating",
            "coral:allowed-pages/hockey",
            "coral:allowed-pages/bowls",
            "coral:allowed-pages/biathlon",
            "coral:allowed-pages/multiples",
            "coral:allowed-pages/horse-racing",
            "coral:allowed-pages/fencing",
            "coral:allowed-pages/nordic-combined",
            "coral:allowed-pages/rugby-union",
            "coral:allowed-pages/basketball",
            "coral:allowed-pages/poker",
            "coral:allowed-pages/diving",
            "coral:allowed-pages/music");
    OfferObject offer =
        OfferObject.builder()
            .offerName("carousel-test")
            .pages(allPages)
            .carousels(Arrays.asList("coral:carousels/carousel1"))
            .build();
    Map<AemBannersRawKey, OfferObject> node = processor.multiplyCollections(offer);
    assertEquals(36, node.size());
  }

  @Test
  public void multiplyCollections_AllCarousels_Ok() {
    OfferObject offer =
        OfferObject.builder()
            .offerName("carousel-test")
            .pages(Arrays.asList("coral:allowed-pages/golf"))
            .carousels(
                Arrays.asList(
                    "coral:carousels/carousel1",
                    "coral:carousels/carousel2",
                    "coral:carousels/carousel3",
                    "coral:carousels/carousel4"))
            .build();
    Map<AemBannersRawKey, OfferObject> node = processor.multiplyCollections(offer);
    assertTrue(node.size() == 4);
  }

  @Test
  public void bucketStateChangeFromFullToEmpty() {
    populateBannersBucket_Ok();
    populateBannersBucketNoConnectionWithAEM();
  }

  @Test
  public void populateBannersBucketNoConnectionWithAEM() {
    when(aemMetaConsumer.getBanners()).thenReturn(Collections.emptyList());
    assertFalse(processor.populateBannersBucket());
    assertEquals(
        0,
        processor
            .getBannersForModule(
                AemBannersRawKey.builder()
                    .carouselId("carousel1")
                    .pageId("18")
                    .type(PageType.sport)
                    .build())
            .size());
  }

  @Test
  public void populateBannersBucketInvalidBanner() {
    when(aemMetaConsumer.getBanners()).thenReturn(Collections.emptyList());
    assertFalse(processor.populateBannersBucket());
    assertEquals(
        Collections.emptyList(),
        processor.getBannersForModule(
            AemBannersRawKey.builder().type(PageType.sport).pageId("0").carouselId("#1").build()));
  }

  @Test
  public void populateBannersBucket_Ok() {
    OfferObject offer =
        OfferObject.builder()
            .offerName("carousel-test")
            .pages(Arrays.asList("coral:allowed-pages/golf"))
            .carousels(
                Arrays.asList(
                    "coral:carousels/carousel1",
                    "coral:carousels/carousel2",
                    "coral:carousels/carousel3",
                    "coral:carousels/carousel4"))
            .build();
    when(aemMetaConsumer.getBanners()).thenReturn(Arrays.asList(offer));

    assertTrue(processor.populateBannersBucket());
    assertEquals(
        1,
        processor
            .getBannersForModule(
                AemBannersRawKey.builder()
                    .carouselId("carousel1")
                    .pageId("18")
                    .type(PageType.sport)
                    .build())
            .size());
    assertEquals(
        1,
        processor
            .getBannersForModule(
                AemBannersRawKey.builder()
                    .carouselId("carousel2")
                    .pageId("18")
                    .type(PageType.sport)
                    .build())
            .size());
    assertEquals(
        1,
        processor
            .getBannersForModule(
                AemBannersRawKey.builder()
                    .carouselId("carousel3")
                    .pageId("18")
                    .type(PageType.sport)
                    .build())
            .size());
    assertEquals(
        offer,
        processor
            .getBannersForModule(
                AemBannersRawKey.builder()
                    .carouselId("carousel1")
                    .pageId("18")
                    .type(PageType.sport)
                    .build())
            .get(0));
    assertEquals(
        offer,
        processor
            .getBannersForModule(
                AemBannersRawKey.builder()
                    .carouselId("carousel2")
                    .pageId("18")
                    .type(PageType.sport)
                    .build())
            .get(0));
    assertEquals(
        offer,
        processor
            .getBannersForModule(
                AemBannersRawKey.builder()
                    .carouselId("carousel3")
                    .pageId("18")
                    .type(PageType.sport)
                    .build())
            .get(0));
    assertEquals(
        offer,
        processor
            .getBannersForModule(
                AemBannersRawKey.builder()
                    .carouselId("carousel4")
                    .pageId("18")
                    .type(PageType.sport)
                    .build())
            .get(0));
    assertTrue(processor.getBannersForModule(AemBannersRawKey.UNKNOWN_PAGE_KEY).isEmpty());
  }

  @Test
  public void populateBannersBucket_eventhub_Ok() {
    OfferObject offer =
        OfferObject.builder()
            .offerName("new-standard-banner")
            .pages(
                Arrays.asList(
                    "coral:allowed-pages/football",
                    "coral:allowed-pages/h4",
                    "coral:allowed-pages/h1",
                    "coral:allowed-pages/homepage",
                    "coral:allowed-pages/h2"))
            .carousels(Arrays.asList("coral:carousels/carousel2", "coral:carousels/carousel1"))
            .build();
    when(aemMetaConsumer.getBanners()).thenReturn(Arrays.asList(offer));

    assertTrue(processor.populateBannersBucket());

    AemBannersRawKey key =
        AemBannersRawKey.builder()
            .carouselId("carousel1")
            .pageId("h2")
            .type(PageType.eventhub)
            .build();
    assertEquals(offer, processor.getBannersForModule(key).get(0));
  }

  @Test
  public void serializeTest() {
    AemBannersModule testModel =
        AemBannersModule.builder()
            .id("id")
            .pageType(PageType.sport)
            .sportId(0)
            .publishedDevices(Collections.emptyList())
            .showExpanded(true)
            .data(Arrays.asList(AemBannersImg.builder().altText("alt").imgUrl("url").build()))
            .build();

    String output = ModuleAdapter.FEATURED_GSON.toJson(testModel);
    AemBannersModule outputModel =
        ModuleAdapter.FEATURED_GSON.fromJson(output, AemBannersModule.class);
    assertEquals(testModel, outputModel);
  }
}
