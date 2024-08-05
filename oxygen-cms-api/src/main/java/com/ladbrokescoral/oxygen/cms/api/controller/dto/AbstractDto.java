package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import java.time.Instant;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class AbstractDto {
  private String id;
  private String createdBy;
  private String createdByUserName;
  private String updatedBy;
  private String updatedByUserName;

  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
      timezone = "UTC")
  private Instant createdAt;

  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
      timezone = "UTC")
  private Instant updatedAt;
}
