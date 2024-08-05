package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "rgy-meta-info")
@Data
@EqualsAndHashCode(callSuper = false)
public class RGYMetaInfoEntity extends SortableEntity implements HasBrand {
  @Indexed String brand;
  private boolean isRgyEnabled;
}
