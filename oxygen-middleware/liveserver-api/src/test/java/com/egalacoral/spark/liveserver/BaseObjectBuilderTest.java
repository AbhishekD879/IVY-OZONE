package com.egalacoral.spark.liveserver;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.common.service.DefaultCommentaryValuesType;
import com.egalacoral.spark.liveserver.BaseObject.Event;
import com.egalacoral.spark.liveserver.BaseObject.Market;
import com.egalacoral.spark.liveserver.BaseObject.Outcome;
import com.egalacoral.spark.liveserver.BaseObject.Price;
import com.egalacoral.spark.liveserver.configuration.LiveServeUtilsConfig;
import com.egalacoral.spark.liveserver.meta.EventMetaInfo;
import com.egalacoral.spark.liveserver.meta.EventMetaInfoRepository;
import com.egalacoral.spark.liveserver.utils.JsonMapper;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.mockito.Mockito;
import org.skyscreamer.jsonassert.JSONAssert;

/** Created by Aliaksei Yarotski on 9/19/17. */
public class BaseObjectBuilderTest extends AbstractBuilderTest {

  public final String meaasgeHeaderMask = "Ms%s%s!!!!!&36[RGs%s%s%06X%06X";
  private static JsonMapper jsonMapper;
  private final EventMetaInfoRepository eventMetaInfoRepository =
      Mockito.mock(EventMetaInfoRepository.class);

  @BeforeClass
  public static void setUpClass() throws Exception {
    LiveServeUtilsConfig utilsConfig = new LiveServeUtilsConfig();
    jsonMapper = utilsConfig.jsonMapper();
  }

  @Before
  public void setUp() throws Exception {
    Optional<EventMetaInfo> eventResolved =
        Optional.of(EventMetaInfo.builder().eventId(BigInteger.valueOf(8317199)).build());
    when(eventMetaInfoRepository.getBySelectionId(Mockito.any())).thenReturn(eventResolved);
    when(eventMetaInfoRepository.getByMarketId(Mockito.any())).thenReturn(eventResolved);
    when(eventMetaInfoRepository.getByEventId(Mockito.any()))
        .thenAnswer(
            invocation -> {
              String eventId = invocation.getArgument(0) + "";
              return Optional.of(
                  EventMetaInfo.builder().eventId(new BigInteger(eventId)).categoryId(16).build());
            });
  }

  @Test
  public void testPRICE_Structure_OK() throws Exception {
    // prepare date
    Message priceMessage =
        createMessage(
            TYPE_DEF.PRICE,
            (baseObject) -> {
              String eventId = String.format("%010d", baseObject.getEvent().getEventId());
              String outcomeId =
                  String.format(
                      "%010d", baseObject.getEvent().getMarket().getOutcome().getOutcomeId());
              int length = thisType.getSource().length();

              return String.format(
                  meaasgeHeaderMask,
                  thisType.name(),
                  eventId,
                  thisType.name(),
                  outcomeId,
                  length,
                  length);
            });

    priceMessage.setJsonData(
        write(compoundBaseObject.getEvent().getMarket().getOutcome().getPrice()));

    BaseObjectBuilder builder =
        BaseObjectBuilder.create(priceMessage, jsonMapper)
            .eventMetaInfoRepository(eventMetaInfoRepository);

    BaseObject baseObject = builder.build();

    JSONAssert.assertEquals(TYPE_DEF.PRICE.getSource(), write(baseObject), false);
  }

  @Test
  public void testEVMKT_Structure_OK() throws Exception {
    // prepare date
    Message priceMessage =
        createMessage(
            TYPE_DEF.EVMKT,
            (baseObject) -> {
              String eventId = String.format("%010d", baseObject.getEvent().getEventId());
              String marketId =
                  String.format("%010d", baseObject.getEvent().getMarket().getMarketId());

              int length = thisType.getSource().length();

              return String.format(
                  meaasgeHeaderMask,
                  thisType.name(),
                  eventId,
                  thisType.name(),
                  marketId,
                  length,
                  length);
            });
    priceMessage.setJsonData(write(compoundBaseObject.getEvent().getMarket()));
    BaseObjectBuilder builder =
        BaseObjectBuilder.create(priceMessage, jsonMapper)
            .eventMetaInfoRepository(eventMetaInfoRepository);

    BaseObject baseObject = builder.build();
    JSONAssert.assertEquals(TYPE_DEF.EVMKT.getSource(), write(baseObject), false);
  }

  @Test
  public void testSELCN_Structure_OK() throws Exception {
    // prepare date
    Message priceMessage =
        createMessage(
            TYPE_DEF.SELCN,
            (baseObject) -> {
              String eventId = String.format("%010d", baseObject.getEvent().getEventId());
              String outcomeId =
                  String.format(
                      "%010d", baseObject.getEvent().getMarket().getOutcome().getOutcomeId());
              int length = thisType.getSource().length();

              baseObject
                  .getEvent()
                  .getMarket()
                  .getOutcome()
                  .setEvMktId( // ev_mkt_id <- marketId
                      baseObject.getEvent().getMarket().getMarketId());
              baseObject.getEvent().getMarket().setMarketId(null);

              baseObject
                  .getEvent()
                  .getMarket()
                  .getOutcome()
                  .setLpDen( // lp_den
                      baseObject.getEvent().getMarket().getOutcome().getPrice().getLpDen());
              baseObject
                  .getEvent()
                  .getMarket()
                  .getOutcome()
                  .setLpNum( // lp_num
                      baseObject.getEvent().getMarket().getOutcome().getPrice().getLpNum());

              return String.format(
                  meaasgeHeaderMask,
                  thisType.name(),
                  eventId,
                  thisType.name(),
                  outcomeId,
                  length,
                  length);
            });
    priceMessage.setJsonData(write(compoundBaseObject.getEvent().getMarket().getOutcome()));

    BaseObjectBuilder builder =
        BaseObjectBuilder.create(priceMessage, jsonMapper)
            .eventMetaInfoRepository(eventMetaInfoRepository);

    BaseObject baseObject = builder.build();
    JSONAssert.assertEquals(TYPE_DEF.SELCN.getSource(), write(baseObject), false);
  }

  @Test
  public void testEVENT_Structure_OK() throws Exception {
    // prepare date
    Message priceMessage =
        createMessage(
            TYPE_DEF.EVENT,
            (baseObject) -> {
              // Produce IDs
              String eventId = String.format("%010d", baseObject.getEvent().getEventId());
              String outcomeId =
                  String.format(
                      "%010d", baseObject.getEvent().getMarket().getOutcome().getOutcomeId());
              int length = thisType.getSource().length();

              // inverse transformation
              baseObject.getEvent().getMarket().setOutcome(null);

              return String.format(
                  meaasgeHeaderMask,
                  thisType.name(),
                  eventId,
                  thisType.name(),
                  outcomeId,
                  length,
                  length);
            });
    // JSON data transform
    priceMessage.setJsonData(write(compoundBaseObject.getEvent()));

    BaseObjectBuilder builder =
        BaseObjectBuilder.create(priceMessage, jsonMapper)
            .eventMetaInfoRepository(eventMetaInfoRepository);

    BaseObject baseObject = builder.build();
    JSONAssert.assertEquals(TYPE_DEF.EVENT.getSource(), write(baseObject), false);
  }

  @Test
  public void testSCBRD_Structure_OK() throws Exception {
    // prepare date
    Message priceMessage =
        createMessage(
            TYPE_DEF.SCBRD,
            (baseObject) -> {
              // Produce IDs
              String eventId = String.format("%010d", baseObject.getEvent().getEventId());
              int length = thisType.getSource().length();

              // inverse transformation

              return String.format(
                  meaasgeHeaderMask,
                  thisType.name(),
                  eventId,
                  thisType.name(),
                  eventId,
                  length,
                  length);
            });
    // JSON data transform
    priceMessage.setJsonData(write(compoundBaseObject.getEvent().getScoreboard()));

    BaseObjectBuilder builder = BaseObjectBuilder.create(priceMessage, jsonMapper);

    BaseObject baseObject = builder.build();
    JSONAssert.assertEquals(TYPE_DEF.SCBRD.getSource(), write(baseObject), false);
  }

  @Test
  public void testSCBRD_Structure_Reverse_OK() throws Exception {
    // prepare date
    Message priceMessage =
        createMessage(
            TYPE_DEF.SCBRD,
            (baseObject) -> {
              // Produce IDs
              String eventId = String.format("%010d", baseObject.getEvent().getEventId());
              int length = thisType.getSource().length();

              // inverse transformation

              return String.format(
                  meaasgeHeaderMask,
                  thisType.name(),
                  eventId,
                  thisType.name(),
                  eventId,
                  length,
                  length);
            });
    // JSON data transform

    compoundBaseObject.getEvent().getScoreboard().setAll(createListWithReverseOrder());
    List<BaseObject.EventDetails> subPeriod = createListWithReverseOrder();
    subPeriod.addAll(createListWithReverseOrder());

    compoundBaseObject.getEvent().getScoreboard().setSubperiod(subPeriod);
    compoundBaseObject.getEvent().getScoreboard().setCurrent(createListWithReverseOrder());

    priceMessage.setJsonData(write(compoundBaseObject.getEvent().getScoreboard()));

    BaseObjectBuilder builder = BaseObjectBuilder.create(priceMessage, jsonMapper);

    BaseObject baseObject = builder.build();
    Assertions.assertEquals(
        DefaultCommentaryValuesType.PLAYER_1.getValue(),
        baseObject.getEvent().getScoreboard().all().get(0).getRoleCode());
  }

  @Test
  public void testSCBRD_Structure_Reverse_Exception() throws Exception {
    // prepare date
    Message priceMessage =
        createMessage(
            TYPE_DEF.SCBRD,
            (baseObject) -> {
              // Produce IDs
              String eventId = String.format("%010d", baseObject.getEvent().getEventId());
              int length = thisType.getSource().length();

              // inverse transformation

              return String.format(
                  meaasgeHeaderMask,
                  thisType.name(),
                  eventId,
                  thisType.name(),
                  eventId,
                  length,
                  length);
            });
    // JSON data transform

    List<BaseObject.EventDetails> all = createListWithReverseOrder();
    all.set(1, null);
    compoundBaseObject.getEvent().getScoreboard().setAll(all);
    List<BaseObject.EventDetails> subPeriod = createListWithReverseOrder();
    subPeriod.addAll(createListWithReverseOrder());

    compoundBaseObject.getEvent().getScoreboard().setSubperiod(subPeriod);
    compoundBaseObject.getEvent().getScoreboard().setCurrent(createListWithReverseOrder());

    priceMessage.setJsonData(write(compoundBaseObject.getEvent().getScoreboard()));

    BaseObjectBuilder builder = BaseObjectBuilder.create(priceMessage, jsonMapper);

    BaseObject baseObject = builder.build();
    Assertions.assertEquals(
        DefaultCommentaryValuesType.PLAYER_2.getValue(),
        baseObject.getEvent().getScoreboard().all().get(0).getRoleCode());

    compoundBaseObject.getEvent().getScoreboard().setAll(createListWithReverseOrder());

    compoundBaseObject.getEvent().getScoreboard().setSubperiod(subPeriod);
    List<BaseObject.EventDetails> current = createListWithReverseOrder();
    current.remove(1);
    compoundBaseObject.getEvent().getScoreboard().setCurrent(current);

    priceMessage.setJsonData(write(compoundBaseObject.getEvent().getScoreboard()));

    builder = BaseObjectBuilder.create(priceMessage, jsonMapper);

    baseObject = builder.build();
    Assertions.assertEquals(
        DefaultCommentaryValuesType.PLAYER_1.getValue(),
        baseObject.getEvent().getScoreboard().all().get(0).getRoleCode());

    // third scenario
    compoundBaseObject.getEvent().getScoreboard().setAll(new ArrayList<>());

    compoundBaseObject.getEvent().getScoreboard().setSubperiod(subPeriod);
    current = createListWithReverseOrder();
    compoundBaseObject.getEvent().getScoreboard().setCurrent(current);

    priceMessage.setJsonData(write(compoundBaseObject.getEvent().getScoreboard()));

    builder = BaseObjectBuilder.create(priceMessage, jsonMapper);

    baseObject = builder.build();
    Assertions.assertEquals(
        DefaultCommentaryValuesType.PLAYER_2.getValue(),
        baseObject.getEvent().getScoreboard().current().get(0).getRoleCode());
  }

  @Test
  public void testCLOCK_Structure_OK() throws Exception {
    // prepare date
    Message priceMessage =
        createMessage(
            TYPE_DEF.CLOCK,
            (baseObject) -> {
              // Produce IDs
              String eventId = String.format("%010d", baseObject.getEvent().getEventId());
              int length = thisType.getSource().length();

              // inverse transformation

              return String.format(
                  meaasgeHeaderMask,
                  thisType.name(),
                  eventId,
                  thisType.name(),
                  eventId,
                  length,
                  length);
            });
    // JSON data transform
    priceMessage.setJsonData(write(compoundBaseObject.getEvent().getClock()));

    BaseObjectBuilder builder = BaseObjectBuilder.create(priceMessage, jsonMapper);

    BaseObject baseObject = builder.build();
    JSONAssert.assertEquals(TYPE_DEF.CLOCK.getSource(), write(baseObject), false);
  }

  @Test
  public void testSubstr_OK() throws Exception {
    BaseObjectBuilder builder =
        BaseObjectBuilder.create(
            new Message("MS" + ChannelType.sEVENT.toString(), "", "", "", ""), jsonMapper);
    Assert.assertEquals("EVENT", builder.substr(ChannelType.sEVENT.toString(), 1, 5));
  }

  @Test
  public void testVerifyDeprecatedCases() {
    for (UNDEFINED_TYPES type : UNDEFINED_TYPES.values()) {
      List<Message> messages = new ResponseConverter().convert(type.getSource());
      assertThat(messages).isNotNull();
      BaseObjectBuilder builder = BaseObjectBuilder.create(messages.get(0), jsonMapper);
      assertThat(builder.build()).isNull();
      assertThat(builder.toJsonString()).isNull();
      assertThat(builder.isValidMessage()).isFalse();
    }
  }

  @Test
  public void testSubstr_OK_BaseObject() {
    BaseObject builder = new BaseObject();
    builder.setEvent(new Event());
    builder.getEvent().setMarket(new Market());
    builder.getEvent().getMarket().setOutcome(new Outcome());
    builder.getEvent().getMarket().getOutcome().setPrice(new Price());
    builder.getEvent().getMarket().getOutcome().getPrice().setPriceStreamType("Priceboost");
    builder.getEvent().getMarket().getOutcome().getPrice().setStatus("Active");
    builder.getEvent().getMarket().getOutcome().getPrice().setPsDen("2");
    builder.getEvent().getMarket().getOutcome().getPrice().setPsNum("1");
    builder.getEvent().getMarket().getOutcome().getPrice().psDen("3");
    builder.getEvent().getMarket().getOutcome().getPrice().psNum("4");
    Assert.assertEquals("3", builder.getEvent().getMarket().getOutcome().getPrice().getPsDen());
  }

  @Test
  public void testScoreBoardStatsEmpty() {
    BaseObject baseObject = new BaseObject();
    baseObject.setEvent(new Event());
    baseObject.getEvent().setScoreBoardStats(new BaseObject.ScoreBoardStats());
    baseObject.getEvent().getScoreBoardStats().setStats(new HashMap<>());
    Assert.assertEquals(0, baseObject.getEvent().getScoreBoardStats().getStats().size());
  }

  @Test
  public void testScoreBoardStats() {
    BaseObject.ScoreBoardStats stats = new BaseObject.ScoreBoardStats();
    Map<String, Object> stat = new HashMap<>();
    stat.put("provider", "opta");
    stats.setStats(stat);
    BaseObject baseObject = new BaseObject();
    baseObject.setEvent(new Event().scoreBoardStats(stats));
    Assert.assertEquals(
        "opta", baseObject.getEvent().getScoreBoardStats().getStats().get("provider"));
  }

  private List<BaseObject.EventDetails> createListWithReverseOrder() {
    List<BaseObject.EventDetails> all = new ArrayList<>();
    BaseObject.EventDetails eventDetails =
        new BaseObject.EventDetails.EventDetailsBuilder().evId(1).buildHomeEventScore();
    eventDetails.setRoleCode(DefaultCommentaryValuesType.PLAYER_2.getValue());
    BaseObject.EventDetails awayEventDetails =
        new BaseObject.EventDetails.EventDetailsBuilder().evId(4).buildAwayEventScore();
    awayEventDetails.setRoleCode(DefaultCommentaryValuesType.PLAYER_1.getValue());
    all.add(eventDetails);
    all.add(awayEventDetails);
    return all;
  }
}
