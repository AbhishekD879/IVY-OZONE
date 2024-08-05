package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class LuckyDipMappingDto {

  private String id;

  private String brand;

  private String categoryId;

  private String typeIds;

  private Boolean active;

  private Double sortOrder;
}
