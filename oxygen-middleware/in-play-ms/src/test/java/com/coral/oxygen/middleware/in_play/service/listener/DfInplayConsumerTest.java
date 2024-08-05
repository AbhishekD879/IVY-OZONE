package com.coral.oxygen.middleware.in_play.service.listener;

import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.in_play.service.TestUtil;
import com.coral.oxygen.middleware.in_play.service.TopicContentConverter;
import com.coral.oxygen.middleware.in_play.service.model.safbaf.Meta;
import com.coral.oxygen.middleware.in_play.service.scoreboards.*;
import com.coral.oxygen.middleware.in_play.service.siteserver.InplaySiteServeService;
import com.egalacoral.spark.liveserver.utils.JsonMapper;
import com.egalacoral.spark.siteserver.model.Category;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.lib.leader.LeaderStatus;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.record.TimestampType;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;

@RunWith(MockitoJUnitRunner.class)
public class DfInplayConsumerTest {

  DfInplayConsumer dfInplayConsumer;

  private TopicContentConverter converter;
  @Mock InplaySiteServeService siteServeService;

  @Mock private CacheManager caffeineCacheManager;
  @Mock private Cache cache;

  @Mock private ScoreBoardProcessor scoreBoardProcessor;

  @Mock private ScoreboardCache scoreboardCache;

  @Mock private MessagePublisher messagePublisher;

  private LeaderStatus leaderStatus;

  private static final String VIRTUAL_SPORT_CACHE = "virtualSportsCache";

  public static final String EVENT_ID = "123123";

  @Before
  public void init() {
    converter = new TopicContentConverter();
    leaderStatus = new LeaderStatus();
    dfInplayConsumer =
        new DfInplayConsumer(
            converter,
            siteServeService,
            caffeineCacheManager,
            scoreBoardProcessor,
            leaderStatus,
            List.of("soccer"));
  }

  @Test
  public void consumeScoreboardTest() {
    leaderStatus.setLeaderNode(true);
    String eventData =
        "{\"event\":{\"eventKey\":3808750,\"isEventFinished\":true,\"meta\":{\"operation\":\"update\",\"parents\":\"c.39:cl.36020:t.115028\",\"messageID\":\"14211937691\",\"channel\":\"OXIRep\",\"source\":\"playtech_virtuals_test\",\"recordModifiedTime\":\"2023-05-31T07:48:16Z\",\"messageTimestamp\":\"1685519298173\"}}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(eventData);
    Mockito.when(siteServeService.getClassesforVirtualHub()).thenReturn(getCategoryList());
    Mockito.when(caffeineCacheManager.getCache(VIRTUAL_SPORT_CACHE)).thenReturn(cache);

    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    if (leaderStatus.isLeaderNode()) {
      dfInplayConsumer.processSafUpdates(consumerRecord);
    } else {
      dfInplayConsumer.slaveAction();
    }
    Assert.assertNotNull(eventData);
  }

  @Test
  public void consumeScoreboardTestCacheNull() {
    leaderStatus.setLeaderNode(true);
    String eventData =
        "{\"event\":{\"eventKey\":3808750,\"isEventFinished\":true,\"meta\":{\"operation\":\"update\",\"parents\":\"c.39:cl.36020:t.115028\",\"messageID\":\"14211937691\",\"channel\":\"OXIRep\",\"source\":\"playtech_virtuals_test\",\"recordModifiedTime\":\"2023-05-31T07:48:16Z\",\"messageTimestamp\":\"1685519298173\"}}}";

    ConsumerRecord<String, String> consumerRecord = getRecord(eventData);
    Mockito.when(caffeineCacheManager.getCache(VIRTUAL_SPORT_CACHE)).thenReturn(null);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);

    if (leaderStatus.isLeaderNode()) {
      dfInplayConsumer.processSafUpdates(consumerRecord);
    } else {
      dfInplayConsumer.slaveAction();
    }

    Assert.assertNotNull(eventData);
  }

  @Test
  public void consumeScoreboardTestwithMetaDataNull() {
    leaderStatus.setLeaderNode(true);
    String eventDataNull =
        "{\"event\":{\"eventKey\":3808750,\"isEventFinished\":true,\"meta\":null}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(eventDataNull);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    if (leaderStatus.isLeaderNode()) {
      dfInplayConsumer.processSafUpdates(consumerRecord);
    } else {
      dfInplayConsumer.slaveAction();
    }
    Assert.assertNotNull(eventDataNull);
  }

  @Test
  public void consumeScoreboardTestWithMetaDataParentsNull() {
    leaderStatus.setLeaderNode(true);
    String eventDataParentsNull =
        "{\"event\":{\"eventKey\":3808750,\"isEventFinished\":true,\"meta\":{\"operation\":\"update\",\"parents\":null,\"messageID\":\"14211937691\",\"channel\":\"OXIRep\",\"source\":\"playtech_virtuals_test\",\"recordModifiedTime\":\"2023-05-31T07:48:16Z\",\"messageTimestamp\":\"1685519298173\"}}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(eventDataParentsNull);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    if (leaderStatus.isLeaderNode()) {
      dfInplayConsumer.processSafUpdates(consumerRecord);
    } else {
      dfInplayConsumer.slaveAction();
    }
    Assert.assertNotNull(eventDataParentsNull);
  }

  @Test
  public void consumeScoreboardTestWithSlave() {
    leaderStatus.setLeaderNode(false);
    String eventDataParentsNull =
        "{\"event\":{\"eventKey\":3808750,\"isEventFinished\":true,\"meta\":{\"operation\":\"update\",\"parents\":null,\"messageID\":\"14211937691\",\"channel\":\"OXIRep\",\"source\":\"playtech_virtuals_test\",\"recordModifiedTime\":\"2023-05-31T07:48:16Z\",\"messageTimestamp\":\"1685519298173\"}}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(eventDataParentsNull);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    dfInplayConsumer.slaveAction();
    Assert.assertNotNull(eventDataParentsNull);
  }

  @Test
  public void consumeScoreboardTestEventsNull() {

    String eventsData =
        "{\"eventKey\":3810587,\"meta\":{\"operation\":\"update\",\"parents\":\"c.35:cl.36026:t.115055\",\"messageID\":\"14211950911\",\"channel\":\"OXIRep\",\"source\":\"Inspired_test\",\"recordModifiedTime\":\"2023-05-31T08:13:59Z\",\"messageTimestamp\":\"1685520840753\"}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(eventsData);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    leaderStatus.setLeaderNode(true);
    if (leaderStatus.isLeaderNode()) {
      dfInplayConsumer.processSafUpdates(consumerRecord);
    } else {
      dfInplayConsumer.slaveAction();
    }
    Assert.assertNotNull(eventsData);
  }

  @Test
  public void consumeScoreboardTestWithParentsDifferentCategoryId() {

    String eventDataDiffId =
        "{\"event\":{\"eventKey\":3808750,\"isEventFinished\":true,\"meta\":{\"operation\":\"update\",\"parents\":\"c.34:cl.36020:t.115028\",\"messageID\":\"14211937691\",\"channel\":\"OXIRep\",\"source\":\"playtech_virtuals_test\",\"recordModifiedTime\":\"2023-05-31T07:48:16Z\",\"messageTimestamp\":\"1685519298173\"}}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(eventDataDiffId);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);
    leaderStatus.setLeaderNode(true);
    if (leaderStatus.isLeaderNode()) {
      dfInplayConsumer.processSafUpdates(consumerRecord);
    } else {
      dfInplayConsumer.slaveAction();
    }
    ;
    Assert.assertNotNull(eventDataDiffId);
  }

  @Test
  public void consumeScoreboardFailWithException() {

    String eventDataDiffId =
        "{\"event\":{\"eventKey\":3808750,\"isEventFinished\":true,\"meta\":{\"operation\":\"update\",\"parents\":\"c.34:cl.36020:t.115028\",\"messageID\":\"14211937691\",\"channel\":\"OXIRep\",\"source\":\"playtech_virtuals_test\",\"recordModifiedTime\":\"2023-05-31T07:48:16Z\",\"messageTimestamp\":\"1685519298173\"}}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(eventDataDiffId);

    LeaderStatus ls = Mockito.mock(LeaderStatus.class);
    Mockito.doThrow(new RuntimeException()).when(ls).isLeaderNode();

    dfInplayConsumer =
        new DfInplayConsumer(
            converter,
            siteServeService,
            caffeineCacheManager,
            scoreBoardProcessor,
            ls,
            List.of("soccer"));
    dfInplayConsumer.consumeScoreboard(Optional.of(EVENT_ID), consumerRecord);

    leaderStatus.setLeaderNode(true);
    if (leaderStatus.isLeaderNode()) {
      dfInplayConsumer.processSafUpdates(consumerRecord);
    } else {
      dfInplayConsumer.slaveAction();
    }
    Assert.assertNotNull(eventDataDiffId);
  }

  @Test
  public void testDfConsumeScoreBoards() {
    String updateMessage = TestUtil.getResourceByPath("Df/footballScoreboard.json");
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>("test.scoreboards.1", 0, 0, "123", updateMessage);
    record.headers().add("cd-eventKey", "112233".getBytes());
    ScoreBoardProcessor scoreBoardProcessor =
        buildScoreBoardProcessor(
            Arrays.asList("pre", "et1h", "etht", "et2h", "eet", "pen"), List.of("opta"));
    Mockito.when(scoreboardCache.findById(Mockito.any())).thenReturn(Optional.empty());
    Mockito.when(scoreboardCache.save(Mockito.any()))
        .thenAnswer(AdditionalAnswers.returnsFirstArg());
    leaderStatus.setLeaderNode(true);
    dfInplayConsumer =
        new DfInplayConsumer(
            converter,
            siteServeService,
            caffeineCacheManager,
            scoreBoardProcessor,
            leaderStatus,
            List.of("soccer"));
    dfInplayConsumer.consumeDfScoreBoard(Optional.of("112233"), Optional.of("soccer"), record);
    Mockito.verify(scoreboardCache, Mockito.times(1)).save(Mockito.any());
  }

  @Test
  public void testDfConsumerScoreBoardsLeaderDisabled() {
    leaderStatus.setLeaderNode(false);
    dfInplayConsumer.consumeDfScoreBoard(
        Optional.empty(), Optional.empty(), new ConsumerRecord<>("topic", 0, 0, "", ""));
    Mockito.verify(scoreBoardProcessor, Mockito.times(0))
        .processScoreBoardData(Mockito.any(), Mockito.any());
    Mockito.verify(scoreboardCache, Mockito.times(0)).findById(Mockito.any());
  }

  @Test
  public void testDfConsumerBoardsWithoutSportInHeader() {
    leaderStatus.setLeaderNode(true);
    dfInplayConsumer.consumeDfScoreBoard(
        Optional.empty(), Optional.of("basketball"), new ConsumerRecord<>("topic", 0, 0, "", ""));
    Mockito.verify(scoreBoardProcessor, Mockito.times(0))
        .processScoreBoardData(Mockito.any(), Mockito.any());
    Mockito.verify(scoreboardCache, Mockito.times(0)).findById(Mockito.any());
  }

  @Test
  public void testDfConsumerOtherThanFootball() {
    String updateMessage = TestUtil.getResourceByPath("Df/basketballScoreboard.json");
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>("test.scoreboards.1", 0, 0, "123", updateMessage);
    record.headers().add("cd-eventKey", "112233".getBytes());
    leaderStatus.setLeaderNode(true);
    dfInplayConsumer =
        new DfInplayConsumer(
            converter,
            siteServeService,
            caffeineCacheManager,
            scoreBoardProcessor,
            leaderStatus,
            List.of("basketball"));
    dfInplayConsumer.consumeDfScoreBoard(Optional.of("2233"), Optional.of("basketball"), record);
    Mockito.verify(scoreboardCache, Mockito.times(0)).findById(Mockito.any());
    Mockito.verify(scoreboardCache, Mockito.times(0)).save(Mockito.any());
    Mockito.verify(messagePublisher, Mockito.times(0))
        .publish(Mockito.any(), Mockito.any(), Mockito.any());
  }

  @Test
  public void testExceptionDFScoreBoard() {
    String updateMessage = TestUtil.getResourceByPath("Df/footballScoreboardex.json");
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>("test.scoreboards.1", 0, 0, "123", updateMessage);
    record.headers().add("cd-eventKey", "112233".getBytes());
    ScoreBoardProcessor scoreBoardProcessor =
        buildScoreBoardProcessor(
            Arrays.asList("pre", "et1h", "etht", "et2h", "eet", "pen"), List.of("opta"));
    leaderStatus.setLeaderNode(true);
    dfInplayConsumer =
        new DfInplayConsumer(
            converter,
            siteServeService,
            caffeineCacheManager,
            scoreBoardProcessor,
            leaderStatus,
            List.of("soccer"));
    dfInplayConsumer.consumeDfScoreBoard(Optional.of("2233"), Optional.of("soccer"), record);
    Mockito.verify(scoreboardCache, Mockito.times(0)).findById(Mockito.any());
  }

  @Test
  public void testExceptionDFScoreBoardForBothBasketBallAndFootBall() {
    String updateMessage = TestUtil.getResourceByPath("Df/basketballScoreboard.json");
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>("test.scoreboards.1", 0, 0, "123", updateMessage);
    record.headers().add("cd-eventKey", "112233".getBytes());
    ScoreBoardProcessor scoreBoardProcessor =
        buildScoreBoardProcessor(
            Arrays.asList("pre", "et1h", "etht", "et2h", "eet", "pen"), List.of("opta"));
    leaderStatus.setLeaderNode(true);
    dfInplayConsumer =
        new DfInplayConsumer(
            converter,
            siteServeService,
            caffeineCacheManager,
            scoreBoardProcessor,
            leaderStatus,
            List.of("soccer", "basketball"));
    dfInplayConsumer.consumeDfScoreBoard(Optional.of("2233"), Optional.of("basketball"), record);
    Mockito.verify(scoreboardCache, Mockito.times(0)).findById(Mockito.any());
  }

  @Test
  public void testForInvalidPeriods() {
    String updateMessage = TestUtil.getResourceByPath("Df/footballScoreboard.json");
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>("test.scoreboards.1", 0, 0, "123", updateMessage);
    record.headers().add("cd-eventKey", "112233".getBytes());
    ScoreBoardProcessor scoreBoardProcessor =
        buildScoreBoardProcessor(
            Arrays.asList("pre", "et1h", "etht", "et2h", "eet", "pen", "1h"), List.of("opta"));
    leaderStatus.setLeaderNode(true);
    dfInplayConsumer =
        new DfInplayConsumer(
            converter,
            siteServeService,
            caffeineCacheManager,
            scoreBoardProcessor,
            leaderStatus,
            List.of("soccer"));
    dfInplayConsumer.consumeDfScoreBoard(Optional.of("2233"), Optional.of("soccer"), record);
    Mockito.verify(scoreboardCache, Mockito.times(0)).findById(Mockito.any());
    Mockito.verify(messagePublisher, Mockito.times(0))
        .publish(Mockito.any(), Mockito.any(), Mockito.any());
  }

  @Test
  public void testForUpdateWithoutPeriod() {
    String updateMessage = TestUtil.getResourceByPath("Df/footballUpdateWithoutPeriod.json");
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>("test.scoreboards.1", 0, 0, "123", updateMessage);
    record.headers().add("cd-eventKey", "112233".getBytes());
    ScoreBoardProcessor scoreBoardProcessor =
        buildScoreBoardProcessor(
            Arrays.asList("pre", "et1h", "etht", "et2h", "eet", "pen", "1h"), List.of("opta"));
    leaderStatus.setLeaderNode(true);
    dfInplayConsumer =
        new DfInplayConsumer(
            converter,
            siteServeService,
            caffeineCacheManager,
            scoreBoardProcessor,
            leaderStatus,
            List.of("soccer"));
    dfInplayConsumer.consumeDfScoreBoard(Optional.of("2233"), Optional.of("soccer"), record);
    Mockito.verify(scoreboardCache, Mockito.times(0)).findById(Mockito.any());
    Mockito.verify(messagePublisher, Mockito.times(0))
        .publish(Mockito.any(), Mockito.any(), Mockito.any());
  }

  @Test
  public void testForInvalidProvider() {
    String updateMessage = TestUtil.getResourceByPath("Df/footballScoreboard.json");
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>("test.scoreboards.1", 0, 0, "123", updateMessage);
    record.headers().add("cd-eventKey", "112233".getBytes());
    ScoreBoardProcessor scoreBoardProcessor =
        buildScoreBoardProcessor(
            Arrays.asList("pre", "et1h", "etht", "et2h", "eet", "pen"), List.of("bwin"));
    leaderStatus.setLeaderNode(true);
    dfInplayConsumer =
        new DfInplayConsumer(
            converter,
            siteServeService,
            caffeineCacheManager,
            scoreBoardProcessor,
            leaderStatus,
            List.of("soccer"));
    dfInplayConsumer.consumeDfScoreBoard(Optional.of("2233"), Optional.of("soccer"), record);
    Mockito.verify(scoreboardCache, Mockito.times(0)).findById(Mockito.any());
    Mockito.verify(messagePublisher, Mockito.times(0))
        .publish(Mockito.any(), Mockito.any(), Mockito.any());
  }

  @Test
  public void testForInvalidDfScoreboardUpdate() {
    String json = TestUtil.getResourceByPath("Df/footballScoreboard.json");
    ScoreboardEvent previousEvent = new ScoreboardEvent("112233", json);
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>("test.scoreboards.1", 0, 0, "123", json);
    record.headers().add("cd-eventKey", "112233".getBytes());
    ScoreBoardProcessor scoreBoardProcessor =
        buildScoreBoardProcessor(
            Arrays.asList("pre", "et1h", "etht", "et2h", "eet", "pen"), List.of("opta"));
    leaderStatus.setLeaderNode(true);
    dfInplayConsumer =
        new DfInplayConsumer(
            converter,
            siteServeService,
            caffeineCacheManager,
            scoreBoardProcessor,
            leaderStatus,
            List.of("soccer"));
    Mockito.when(scoreboardCache.findById(Mockito.any())).thenReturn(Optional.of(previousEvent));
    dfInplayConsumer.consumeDfScoreBoard(Optional.of("112233"), Optional.of("soccer"), record);
    Mockito.verify(scoreboardCache, Mockito.times(1)).findById(Mockito.any());
    Mockito.verify(messagePublisher, Mockito.times(0))
        .publish(Mockito.any(), Mockito.any(), Mockito.any());
    Mockito.verify(scoreboardCache, Mockito.times(0)).save(Mockito.any());
  }

  @Test
  public void testForValidScoreboardUpdateCompareToPrevious() {
    String json = TestUtil.getResourceByPath("Df/footballScoreboardUp.json");
    String previousRedis = TestUtil.getResourceByPath("Df/footballScoreboard.json");
    ScoreboardEvent previousEvent = new ScoreboardEvent("112233", previousRedis);
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>("test.scoreboards.1", 0, 0, "123", json);
    record.headers().add("cd-eventKey", "112233".getBytes());
    ScoreBoardProcessor scoreBoardProcessor =
        buildScoreBoardProcessor(
            Arrays.asList("pre", "et1h", "etht", "et2h", "eet", "pen"), List.of("opta"));
    leaderStatus.setLeaderNode(true);
    dfInplayConsumer =
        new DfInplayConsumer(
            converter,
            siteServeService,
            caffeineCacheManager,
            scoreBoardProcessor,
            leaderStatus,
            List.of("soccer"));
    Mockito.when(scoreboardCache.findById(Mockito.any())).thenReturn(Optional.of(previousEvent));
    Mockito.when(scoreboardCache.save(Mockito.any()))
        .thenAnswer(AdditionalAnswers.returnsFirstArg());
    dfInplayConsumer.consumeDfScoreBoard(Optional.of("112233"), Optional.of("soccer"), record);
    Mockito.verify(scoreboardCache, Mockito.times(1)).findById(Mockito.any());
    Mockito.verify(scoreboardCache, Mockito.times(1)).save(Mockito.any());
  }

  private ScoreBoardProcessor buildScoreBoardProcessor(
      List<String> unsupportedPeriods, List<String> supportedProviders) {
    FootballValidator footballValidator =
        new FootballValidator(unsupportedPeriods, supportedProviders);
    EventValidator eventValidator = new EventValidator(footballValidator);
    FootballMapper footballMapper = new FootballMapper();
    EventMapper eventMapper = new EventMapper(footballMapper);
    return new ScoreBoardProcessor(eventValidator, scoreboardCache, eventMapper);
  }

  public JsonMapper jsonMapper() {
    ObjectMapper mapper = new ObjectMapper();
    mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
    mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    mapper.setDateFormat(new SimpleDateFormat("MMM dd, YYYY h:MM:ss a"));
    return new JsonMapper(mapper);
  }

  private Meta getMeta() {

    Meta meta = new Meta();
    meta.setEventKey(3808750);
    meta.setParents("c.39:cl.36020:t.115028:e.3808750:m.51780056");
    return meta;
  }

  private ConsumerRecord<String, String> getRecord(String value) {
    return new ConsumerRecord<>(
        "test.scoreboards.1",
        0,
        0,
        123,
        TimestampType.NO_TIMESTAMP_TYPE,
        123,
        1,
        1,
        "dfsdgsdgfddsere::showdown::leaderboard",
        value);
  }

  private List<Category> getCategoryList() {
    List<Category> categories = new ArrayList<>();
    Category category = new Category();
    category.setCategoryId(16);
    category.setCategoryName("Football");
    category.setId(1);
    categories.add(category);
    return categories;
  }
}
