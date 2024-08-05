package com.coral.oxygen.middleware.pojos.model.cms.featured;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class LuckyDip extends SportPageModuleDataItem {
  private String id;
  private Integer sportId;
  private List<LuckyDipMapping> luckyDipMappings;
}
