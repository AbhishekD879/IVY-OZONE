package com.ladbrokescoral.oxygen.notification.entities;

import com.google.gson.annotations.SerializedName;
import lombok.Data;

@Data
public class EventLiveUpdate {

  @SerializedName("displayed")
  private String displayed;

  @SerializedName("start_time")
  private String startTime;

  @SerializedName("names")
  private Names names;

  @SerializedName("result_conf")
  private String resultConf;

  @SerializedName("race_stage")
  private String raceStage;

  @SerializedName("is_off")
  private String isOff;

  @SerializedName("suspend_at")
  private String suspendAt;

  @SerializedName("started")
  private String started;

  @SerializedName("start_time_xls")
  private StartTimeXls startTimeXls;

  @SerializedName("status")
  private String status;

  @SerializedName("disporder")
  private Integer disporder;
}
