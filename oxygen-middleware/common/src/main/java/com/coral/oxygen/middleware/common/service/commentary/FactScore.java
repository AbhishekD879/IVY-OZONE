package com.coral.oxygen.middleware.common.service.commentary;

import java.util.Map;

/** Created by Aliaksei Yarotski on 5/17/18. */
public class FactScore extends AbstractModel {

  private static final String FACT_SCORE_MARKER = "SCORE";

  public enum FieldNames {
    id,
    eventId,
    eventParticipantId,
    eventPeriodId,
    fact,
    factCode,
    name
  }

  public static boolean isFactScore(Map<String, Object> fieldsMap) {
    return fieldsMap.containsKey(FieldNames.factCode.toString())
        && fieldsMap.get(FieldNames.factCode.toString()).equals(FACT_SCORE_MARKER);
  }

  public FactScore(Map<String, Object> fields) {
    super(fields);
  }

  public String getEventParticipantId() {
    return getField(FieldNames.eventParticipantId).toString();
  }

  public int getScore() {
    try {
      return Integer.parseInt(getField(FieldNames.fact).toString());
    } catch (Exception e) {
      return 0;
    }
  }
}
