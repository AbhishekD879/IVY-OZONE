package com.coral.oxygen.middleware.common.service.commentary;

import java.util.Map;
import lombok.ToString;

/** Created by Aliaksei Yarotski on 5/16/18. */
@ToString
public class TeamScore extends AbstractModel {

  public enum FieldNames {
    id,
    eventId,
    name,
    type,
    roleCode,
    role,
    score,
    extraTimeScore,
    penaltyScore
  }

  public static final boolean isTeamScore(Map<String, Object> fieldsMap) {
    return fieldsMap.containsKey(FieldNames.score.toString());
  }

  public TeamScore(Map<String, Object> fields) {
    super(fields);
  }

  public String getId() {
    return getField(FieldNames.id).toString();
  }

  public String getScore() {
    return (String) getField(FieldNames.score);
  }

  public void setScore(String score) {
    setField(FieldNames.score, score);
  }

  public String getExtraTimeScore() {
    return (String) getField(FieldNames.extraTimeScore);
  }

  public void setExtraTimeScore(String score) {
    setField(FieldNames.extraTimeScore, score);
  }

  public String getPenaltyScore() {
    return (String) getField(FieldNames.penaltyScore);
  }

  public void setPenaltyScore(String score) {
    setField(FieldNames.penaltyScore, score);
  }

  public String getRoleCode() {
    return (String) getField(FieldNames.roleCode);
  }
}
