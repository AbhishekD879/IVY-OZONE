package com.ladbrokescoral.cashout.service.updates;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Outcome;
import com.ladbrokescoral.cashout.config.InternalKafkaTopics;
import com.ladbrokescoral.cashout.model.response.TwoUpDto;
import com.ladbrokescoral.cashout.model.response.TwoUpResponse;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
public class TwoUpUpdatesPublisher {

  @Value("${twoup.eventCategory.id}")
  private String eventCategoryId;

  @Value("${twoup.marketSort.code}")
  private String marketSortCode;

  private final KafkaTemplate<String, Object> kafkaTemplate;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public TwoUpUpdatesPublisher(KafkaTemplate<String, Object> kafkaTemplate) {
    this.kafkaTemplate = kafkaTemplate;
  }

  public void publishTwoUpUpdates(
      String token, Selection selectionUpdate, List<BetSummaryModel> betSummaryModels) {
    List<String> betIds =
        betSummaryModels.stream()
            .filter(this::is2UpEnabled)
            .map(BetSummaryModel::getId)
            .collect(Collectors.toList());
    if (!CollectionUtils.isEmpty(betIds)) {
      boolean twoUpSettled = isTwoUpSettled(selectionUpdate);
      TwoUpResponse twoUpResponse =
          new TwoUpResponse(
              TwoUpDto.builder()
                  .selectionId(String.valueOf(selectionUpdate.getSelectionKey()))
                  .betIds(betIds)
                  .isTwoUpSettled(twoUpSettled)
                  .build());
      ASYNC_LOGGER.debug(
          "Published twoUp updates for betIds {}, selectionId {}",
          betIds,
          selectionUpdate.getSelectionKey());
      String topicName = InternalKafkaTopics.TWOUP_UPDATES.getTopicName();
      kafkaTemplate.send(topicName, token, twoUpResponse);
    }
  }

  private boolean isTwoUpSettled(Selection selectionUpdate) {
    Optional<String> resCode = selectionUpdate.getResultCode();
    return resCode.isPresent() && "Win".equalsIgnoreCase(resCode.get());
  }

  private boolean is2UpEnabled(BetSummaryModel betSummaryModel) {
    return betSummaryModel.getLeg().get(0).getPart().get(0).getOutcome().stream()
        .anyMatch(this::isSportAndMarketCodeMatched);
  }

  private boolean isSportAndMarketCodeMatched(Outcome outcome) {
    return eventCategoryId.equals(outcome.getEventCategory().getId())
        && marketSortCode.equalsIgnoreCase(outcome.getMarket().getMarketSort().getCode());
  }
}
