package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class LuckyDipMappingPublicDto {

  private String id;

  private String categoryId;

  private String typeIds;

  private String svgId;

  private Integer category;

  private Double sortOrder;
}
