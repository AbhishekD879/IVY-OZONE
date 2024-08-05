package com.ladbrokescoral.oxygen.notification.entities;

import com.google.gson.annotations.SerializedName;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@Data
@EqualsAndHashCode
@ToString
public class ScoreboardMessage {
  @SerializedName("min_periods")
  private String minPeriods;

  @SerializedName("ALL")
  private List<ScoreboardItem> all;

  @SerializedName("SUBPERIOD")
  private List<ScoreboardItem> subperiod;

  @SerializedName("CURRENT")
  private List<ScoreboardItem> current;
}
