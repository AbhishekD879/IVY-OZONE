package com.ladbrokescoral.oxygen.notification.entities;

import com.google.gson.annotations.SerializedName;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@Data
@EqualsAndHashCode
@ToString
public class ScoreboardItem {
  @SerializedName("ev_id")
  private Long eventId;

  @SerializedName("ev_class_id")
  private Long eventClassId;

  @SerializedName("period_code")
  private String periodCode;

  @SerializedName("code")
  private String code;

  @SerializedName("value")
  private String value;

  @SerializedName("participant_id")
  private String participantId;

  @SerializedName("role_code")
  private String roleCode;

  @SerializedName("period_index")
  private String periodIndex;

  @SerializedName("is_active")
  private String isActive;
}
