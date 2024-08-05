package com.ladbrokescoral.oxygen.betpackmp.kafka.filter;

import static com.ladbrokescoral.oxygen.betpackmp.constants.BetPackConstants.ACTIVE_BET_PACK_IDS;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.betpackmp.configuration.JsonConfiguration;
import com.ladbrokescoral.oxygen.betpackmp.constants.BetPackConstants;
import com.ladbrokescoral.oxygen.betpackmp.model.PafExtractorPromotion;
import com.ladbrokescoral.oxygen.betpackmp.model.Promotion;
import com.ladbrokescoral.oxygen.betpackmp.redis.ActiveBetPacks;
import com.ladbrokescoral.oxygen.betpackmp.redis.BetPackRedisService;
import com.ladbrokescoral.oxygen.betpackmp.redis.PafBetPack;
import com.ladbrokescoral.oxygen.betpackmp.redis.PafBetPackRepository;
import com.ladbrokescoral.oxygen.betpackmp.service.CmsService;
import com.ladbrokescoral.oxygen.betpackmp.validator.BetPackValidator;
import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.record.TimestampType;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
class BetPackDFPafKafkaConsumerFilterTest implements WithAssertions {

  @Mock private BetPackRedisService betPackService;

  @Mock private CmsService cmsService;

  @Mock private PafBetPackRepository pafBetPackRepository;

  @InjectMocks private BetPackDFPafKafkaConsumerFilter betPackDFPafKafkaConsumerFilter;

  private final String dfBrand = "cd";

  private final String cmsBand = "bma";

  @BeforeEach
  void setUp() {
    betPackDFPafKafkaConsumerFilter =
        new BetPackDFPafKafkaConsumerFilter(cmsService, betPackService, pafBetPackRepository);
    ReflectionTestUtils.setField(betPackDFPafKafkaConsumerFilter, "dfBrand", "cd");
    ReflectionTestUtils.setField(betPackDFPafKafkaConsumerFilter, "cmsBand", "bma");
  }

  @Test // scenario-1 true  -  NA
  void filter_WithEmptyActiveBetPacksIdsTest() {
    when(betPackService.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(null);
    List<String> res = Arrays.asList("87687", "7688", "4343");
    when(cmsService.getActiveBetPackIds(cmsBand)).thenReturn(Mono.just(res));
    boolean result = betPackDFPafKafkaConsumerFilter.filter(getRecord("coral"));
    Assertions.assertTrue(result);
  }

  @Test // scenario-2 false - true, true
  void filter_InValidActiveBetPacksIdsTest() {
    ActiveBetPacks betPacks = new ActiveBetPacks(Collections.emptyList());
    when(betPackService.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(betPacks);
    List<String> res = Arrays.asList("87687", "7688", "4343");
    when(cmsService.getActiveBetPackIds(cmsBand)).thenReturn(Mono.just(res));
    boolean result = betPackDFPafKafkaConsumerFilter.filter(getRecord("coral"));
    Assertions.assertTrue(result);
  }

  @Test // scenario-3 false  - true, false
  void filter_ValidActiveBetPacksIdsTest() {
    ActiveBetPacks betPacks = new ActiveBetPacks(Arrays.asList("88", "656", "4345"));
    when(betPackService.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(betPacks);
    boolean result = betPackDFPafKafkaConsumerFilter.filter(getRecord(dfBrand));
    Assertions.assertTrue(result);
  }

  @Test
  void filter_EmptyActiveBetPacksIds_StatusMismatchTest() {
    ActiveBetPacks betPacks = new ActiveBetPacks(Collections.emptyList());
    when(betPackService.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(betPacks);
    List<String> res = Arrays.asList("87687", "7688", "4343");
    when(cmsService.getActiveBetPackIds(cmsBand)).thenReturn(Mono.just(res));
    ConsumerRecord<String, PafExtractorPromotion> consumerRecord = getRecord(dfBrand);
    consumerRecord.value().getPayload().setStatus("pending");
    boolean result = betPackDFPafKafkaConsumerFilter.filter(consumerRecord);
    Assertions.assertTrue(result);
  }

  @Test
  void filter_EmptyActiveBetPacksIds_CampaignRefMismatchTest() {
    ActiveBetPacks betPacks = new ActiveBetPacks(Collections.emptyList());
    when(betPackService.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(betPacks);
    List<String> res = Arrays.asList("87687", "7688", "4343");
    when(cmsService.getActiveBetPackIds(cmsBand)).thenReturn(Mono.just(res));
    ConsumerRecord<String, PafExtractorPromotion> consumerRecord = getRecord(dfBrand);
    consumerRecord.value().getPayload().setCampaignRef("87687");
    boolean result = betPackDFPafKafkaConsumerFilter.filter(consumerRecord);
    Assertions.assertFalse(result);
  }

  @Test
  void filter_EmptyActiveBetPacksIdsTest() {
    ActiveBetPacks betPacks = new ActiveBetPacks(Collections.emptyList());
    when(betPackService.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(betPacks);
    when(cmsService.getActiveBetPackIds(cmsBand)).thenReturn(Mono.just(Collections.emptyList()));
    boolean result = betPackDFPafKafkaConsumerFilter.filter(getRecord(dfBrand));
    Assertions.assertTrue(result);
  }

  @Test
  void filterWithNullActiveBetPacksTest() {
    ActiveBetPacks betPacks = new ActiveBetPacks(Arrays.asList("88", "656", "4345"));
    when(betPackService.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(betPacks);
    boolean result = betPackDFPafKafkaConsumerFilter.filter(getRecord(dfBrand));
    Assertions.assertTrue(result);
  }

  @Test
  void betPackValidator_Test() throws Exception {
    Constructor<BetPackValidator> constructor = BetPackValidator.class.getDeclaredConstructor();
    Assertions.assertTrue(Modifier.isPrivate(constructor.getModifiers()));
    constructor.setAccessible(true);
    Assertions.assertThrows(Exception.class, constructor::newInstance);
  }

  @Test
  void betPackConstants() throws Exception {
    Constructor<BetPackConstants> constructor = BetPackConstants.class.getDeclaredConstructor();
    Assertions.assertTrue(Modifier.isPrivate(constructor.getModifiers()));
    constructor.setAccessible(true);
    Assertions.assertThrows(Exception.class, constructor::newInstance);
  }

  @Test
  void filterWithDoOnError() {
    ActiveBetPacks betPacks = new ActiveBetPacks(Collections.emptyList());
    when(betPackService.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(betPacks);
    when(cmsService.getActiveBetPackIds(cmsBand)).thenReturn(Mono.error(Exception::new));
    Assertions.assertDoesNotThrow(() -> betPackDFPafKafkaConsumerFilter.filter(getRecord(dfBrand)));
  }

  @Test
  void filter_isValidTrue_Test() {
    ActiveBetPacks betPacks = new ActiveBetPacks(Arrays.asList("884", "656", "campaignRef"));
    PafBetPack pafBetPack = new PafBetPack();
    pafBetPack.setId("655456");
    when(betPackService.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(betPacks);
    when(pafBetPackRepository.findById(anyString())).thenReturn(Optional.of(pafBetPack));
    ConsumerRecord<String, PafExtractorPromotion> consumerRecord = getRecord(dfBrand);
    consumerRecord.value().getPayload().setBrand("cd");
    boolean result = betPackDFPafKafkaConsumerFilter.filter(consumerRecord);
    Assertions.assertTrue(result);
  }

  private ConsumerRecord<String, PafExtractorPromotion> getRecord(String brand) {
    String promotionStr =
        "{\n"
            + "  \"id\": \"8698698\",\n"
            + "  \"brand\": \"coral\",\n"
            + "  \"customerRef\": \"7687dsfs68sdf8\",\n"
            + "  \"offerName\": \"football\",\n"
            + "  \"amount\": \"2000\",\n"
            + "  \"status\": \"active\",\n"
            + "  \"campaignRef\": \"campaignRef\"\n"
            + "}";
    Promotion promotion =
        new JsonConfiguration().gsonInstance().fromJson(promotionStr, Promotion.class);
    PafExtractorPromotion extractorPromotion = new PafExtractorPromotion();
    extractorPromotion.setPayload(promotion);
    extractorPromotion.getPayload().setBrand(brand);
    extractorPromotion.getPayload().setStatus("Issued");
    return new ConsumerRecord<>(
        "test.scoreboards.1",
        0,
        0,
        123,
        TimestampType.NO_TIMESTAMP_TYPE,
        123,
        1,
        1,
        "someKey",
        extractorPromotion);
  }
}
