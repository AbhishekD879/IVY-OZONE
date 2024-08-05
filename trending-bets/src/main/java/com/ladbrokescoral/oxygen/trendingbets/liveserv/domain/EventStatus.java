package com.ladbrokescoral.oxygen.trendingbets.liveserv.domain;

import com.fasterxml.jackson.annotation.JsonSetter;
import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
@Data
public class EventStatus implements AbstractStatus {

  private String status; // "status": "A" or "S"
  private String displayed; // "displayed": "Y" or "N",
  private Boolean resulted; // "result_conf": "N",
  private Boolean started; // "started": "Y" or "N"
  private String startTime;

  @JsonSetter("status")
  private void setStatus(String status) {
    this.status = status;
  }

  @JsonSetter("displayed")
  private void setDisplayed(String displayed) {
    this.displayed = displayed;
  }

  @JsonSetter("result_conf")
  private void setResulted(String resulted) {
    this.resulted = "Y".equals(resulted);
  }

  @JsonSetter("started")
  private void setStarted(String started) {
    this.started = "Y".equals(started);
  }

  @JsonSetter("start_time")
  private void setStartTime(String startTime) {
    this.startTime = startTime;
  }
}
