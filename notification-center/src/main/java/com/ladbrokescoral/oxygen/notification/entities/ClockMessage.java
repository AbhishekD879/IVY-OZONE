package com.ladbrokescoral.oxygen.notification.entities;

import com.google.gson.annotations.SerializedName;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@Data
@EqualsAndHashCode
@ToString
public class ClockMessage {
  @SerializedName("ev_id")
  private Long eventId;

  @SerializedName("last_update")
  private String lastUpdateTimestamp;

  @SerializedName("period_code")
  private String periodCode;

  @SerializedName("period_index")
  private String periodIndex;

  @SerializedName("state")
  private String state;

  @SerializedName("clock_seconds")
  private String clockSeconds;

  @SerializedName("last_update_secs")
  private String lastUpdateSeconds;

  @SerializedName("start_time_secs")
  private String startTimeSeconds;

  @SerializedName("offset_secs")
  private String offsetSeconds;
}
