package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.ToString;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@JsonInclude(JsonInclude.Include.NON_NULL)
@Data
@ToString
public class CCUStatusResponse {
  private Integer originalEstimatedSeconds;
  private Integer originalQueueLength;
  private String purgeId;
  private String supportId;
  private Integer httpStatus;
  private String completionTime;
  private String submittedBy;
  private String purgeStatus;
  private String submissionTime;
  private Integer pingAfterSeconds;
  private String progressUri;
}
