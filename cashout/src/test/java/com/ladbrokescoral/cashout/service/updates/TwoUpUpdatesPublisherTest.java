package com.ladbrokescoral.cashout.service.updates;

import static org.mockito.Mockito.times;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.google.common.reflect.TypeToken;
import com.ladbrokescoral.cashout.config.InternalKafkaTopics;
import com.ladbrokescoral.cashout.model.response.TwoUpDto;
import com.ladbrokescoral.cashout.model.response.TwoUpResponse;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.util.GsonUtil;
import java.lang.reflect.Type;
import java.math.BigInteger;
import java.util.Arrays;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
class TwoUpUpdatesPublisherTest {

  @Mock private KafkaTemplate<String, Object> kafkaTemplate;
  @InjectMocks private TwoUpUpdatesPublisher twoUpUpdatesPublisher;
  private Selection selection;
  private String token;
  private List<BetSummaryModel> betSummaryModels;

  @BeforeEach
  public void setUp() {
    selection = getSelection("SelectionModel.json");
    token = "AUidu4cYsT9VJa6KYgBtRH0mE5XJ9XqJoiRxMu9Qc";
    betSummaryModels = getBets("BetSummaryModel9.json");
    ReflectionTestUtils.setField(twoUpUpdatesPublisher, "eventCategoryId", "16");
    ReflectionTestUtils.setField(twoUpUpdatesPublisher, "marketSortCode", "ES");
  }

  @Test
  void publishTwoUpUpdates_Success() {
    BigInteger selectionId = BigInteger.valueOf(776598);
    TwoUpResponse twoUpResponse =
        new TwoUpResponse(
            TwoUpDto.builder()
                .selectionId(String.valueOf(selectionId))
                .betIds(Arrays.asList("757587", "978754"))
                .isTwoUpSettled(true)
                .build());
    twoUpUpdatesPublisher.publishTwoUpUpdates(token, selection, betSummaryModels);
    String topicName = InternalKafkaTopics.TWOUP_UPDATES.getTopicName();
    Mockito.verify(kafkaTemplate, times(0)).send(token, topicName, twoUpResponse);
  }

  @Test
  void publishTwoUpUpdates_ResultCodeMismatched() {
    selection = getSelection("SelectionModel2.json");
    BigInteger selectionId = BigInteger.valueOf(776598);
    TwoUpResponse twoUpResponse =
        new TwoUpResponse(
            TwoUpDto.builder()
                .selectionId(String.valueOf(selectionId))
                .betIds(Arrays.asList("757587", "978754"))
                .isTwoUpSettled(false)
                .build());
    twoUpUpdatesPublisher.publishTwoUpUpdates(token, selection, betSummaryModels);
    String topicName = InternalKafkaTopics.TWOUP_UPDATES.getTopicName();
    Mockito.verify(kafkaTemplate, times(0)).send(token, topicName, twoUpResponse);
  }

  @Test
  void publishTwoUpUpdates_ResultCodeEmpty() {
    selection = getSelection("SelectionModel3.json");
    BigInteger selectionId = BigInteger.valueOf(776598);
    TwoUpResponse twoUpResponse =
        new TwoUpResponse(
            TwoUpDto.builder()
                .selectionId(String.valueOf(selectionId))
                .betIds(Arrays.asList("757587", "978754"))
                .isTwoUpSettled(false)
                .build());
    twoUpUpdatesPublisher.publishTwoUpUpdates(token, selection, betSummaryModels);
    String topicName = InternalKafkaTopics.TWOUP_UPDATES.getTopicName();
    Mockito.verify(kafkaTemplate, times(0)).send(token, topicName, twoUpResponse);
  }

  @Test
  void eventCategoryIdMismatched() {
    ReflectionTestUtils.setField(twoUpUpdatesPublisher, "marketSortCode", "MR");
    twoUpUpdatesPublisher.publishTwoUpUpdates(token, selection, betSummaryModels);
    Mockito.verify(kafkaTemplate, times(0)).send(token, null, null);
  }

  @Test
  void marketSortCodeMismatched() {
    ReflectionTestUtils.setField(twoUpUpdatesPublisher, "eventCategoryId", "21");
    twoUpUpdatesPublisher.publishTwoUpUpdates(token, selection, betSummaryModels);
    Mockito.verify(kafkaTemplate, times(0)).send(token, null, null);
  }

  @Test
  void marketSortCodeAndEventCategoryIdMismatched() {
    ReflectionTestUtils.setField(twoUpUpdatesPublisher, "marketSortCode", "CB");
    ReflectionTestUtils.setField(twoUpUpdatesPublisher, "eventCategoryId", "18");
    twoUpUpdatesPublisher.publishTwoUpUpdates(token, selection, betSummaryModels);
    Mockito.verify(kafkaTemplate, times(0)).send(token, null, null);
  }

  private List<BetSummaryModel> getBets(String fileName) {
    Type type =
        new TypeToken<List<BetSummaryModel>>() {
          private static final long serialVersionUID = 1L;
        }.getType();
    List<BetSummaryModel> bets = GsonUtil.fromJson(fileName, type);
    return bets;
  }

  private Selection getSelection(String fileName) {
    Type type =
        new TypeToken<Selection>() {
          private static final long serialVersionUID = 2L;
        }.getType();
    Selection selection = GsonUtil.fromJson(fileName, type);
    return selection;
  }
}
