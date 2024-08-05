package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@EqualsAndHashCode(of = {"relationType", "refId"})
public class RelationDto {

  private String relationType;
  private String refId;
  private boolean enabled = Boolean.TRUE;
  private Double sortOrder;
}
