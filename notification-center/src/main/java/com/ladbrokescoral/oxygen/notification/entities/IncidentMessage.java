package com.ladbrokescoral.oxygen.notification.entities;

import com.google.gson.annotations.SerializedName;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@Data
@EqualsAndHashCode
@ToString
public class IncidentMessage {
  @SerializedName("ev_id")
  private Long eventId;

  @SerializedName("period_code")
  private String periodCode;

  @SerializedName("incident_code")
  private String incidentCode;

  @SerializedName("relative_time")
  private Long relativeTime;

  @SerializedName("participant_name")
  private String participantName;

  @SerializedName("ev_incident_id")
  private Long eventIncidentId;

  @SerializedName("free_text")
  private String text;

  @SerializedName("participant_id")
  private Long participantId;
}
