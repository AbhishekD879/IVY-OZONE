package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class CreatePotsResponseVO {
  private Boolean isPotsCreated;
  private String message;
}
