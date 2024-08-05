package com.coral.oxygen.middleware.pojos.model.cms.featured;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class SportsCategory {
  private Integer categoryId;
  private String ssCategoryCode;
}
