package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.ToString;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Data
@ToString
public class CCUPurgeResponse {
  private Integer estimatedSeconds;
  private String progressUri;
  private String purgeId;
  private String supportId;
  private Integer httpStatus;
  private String detail;
  private Integer pingAfterSeconds;
}
