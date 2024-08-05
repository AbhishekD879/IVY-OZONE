package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "bybWidget")
public class BybWidget extends AbstractEntity implements HasBrand {
  @Brand protected String brand;
  private String title;
  private int marketCardVisibleSelections;
  private boolean showAll;
}
