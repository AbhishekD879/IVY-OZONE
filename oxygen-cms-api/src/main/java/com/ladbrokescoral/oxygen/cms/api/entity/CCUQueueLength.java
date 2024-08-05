package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.ToString;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Data
@ToString
public class CCUQueueLength {
  private Integer httpStatus;
  private Integer queueLength;
  private String detail;
  private String supportId;
}
