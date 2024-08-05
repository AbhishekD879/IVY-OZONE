package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SportNameDto {

  private String sportName;
  private Integer categoryId;
  private String sportTier;
}
