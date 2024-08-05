package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode
@AllArgsConstructor
public class OfferModuleDto {
  @JsonProperty("name")
  private String moduleName;

  @JsonProperty("offers")
  private List<OfferDto> offerDtoList;

  @JsonIgnore private Double sortCode;
}
