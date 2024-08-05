package com.oxygen.publisher.model;

import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

/** Created by Aliaksei Yarotski on 2/26/18. */
@EqualsAndHashCode
@Builder
@Slf4j
public class LiveRawIndex {
  @Getter private final String eventId;
  @Getter private final String updatedType;
  @Getter private final String subjectId;

  public static String crateSubjectId(BaseObject baseObject) {
    String newSubjectId;
    switch (baseObject.getType()) {
      case "PRICE":
        newSubjectId = baseObject.getEvent().getMarket().getOutcome().getOutcomeId().toString();
        break;
      case "EVMKT":
        newSubjectId = baseObject.getEvent().getMarket().getMarketId().toString();
        break;
      case "SELCN":
        newSubjectId = baseObject.getEvent().getMarket().getOutcome().getOutcomeId().toString();
        break;
      case "EVENT":
        newSubjectId = baseObject.getEvent().getEventId().toString();
        break;
      case "SCBRD":
        newSubjectId = baseObject.getEvent().getEventId().toString();
        break;
      case "CLOCK":
        newSubjectId = baseObject.getEvent().getEventId().toString();
        break;
      default:
        log.error(
            "[LiveRawIndexBuilder:baseObject] Invalid message for type {}", baseObject.getType());
        return null;
    }
    return newSubjectId;
  }
}
