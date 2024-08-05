package com.entain.oxygen.promosandbox.dto;

import java.time.Instant;
import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
@Getter
public class StatusDto {
  private Boolean status = Boolean.FALSE;
  private Instant lastFileModified;
  private Integer noOfRecord;

  public StatusDto(Boolean status, Instant lastFileModified) {
    this.status = status;
    this.lastFileModified = lastFileModified;
  }
}
