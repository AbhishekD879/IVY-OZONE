package com.gvc.oxygen.betreceipts.liveserv.domain;

import com.fasterxml.jackson.annotation.JsonSetter;
import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
@Data
public class EventStatus implements AbstractStatus {

  private Boolean active; // "status": "A" or "S"
  private Boolean displayed; // "displayed": "Y" or "N",
  private Boolean resulted; // "result_conf": "N",
  private Boolean started; // "started": "Y" or "N"

  @JsonSetter("status")
  private void setActive(String status) {
    this.active = "A".equals(status);
  }

  @JsonSetter("displayed")
  private void setDisplayed(String displayed) {
    this.displayed = "Y".equals(displayed);
  }

  @JsonSetter("result_conf")
  private void setResulted(String resulted) {
    this.resulted = "Y".equals(resulted);
  }

  @JsonSetter("started")
  private void setStarted(String started) {
    this.started = "Y".equals(started);
  }
}
