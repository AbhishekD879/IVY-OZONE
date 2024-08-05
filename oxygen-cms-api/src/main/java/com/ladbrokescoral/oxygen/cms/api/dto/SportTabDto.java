package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.PublicApiFilters;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode
@JsonInclude(Include.NON_EMPTY)
public class SportTabDto {
  private String name;
  private String displayName;
  private PublicApiFilters filters;
}
