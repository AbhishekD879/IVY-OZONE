package com.ladbrokescoral.oxygen.cms.api.entity.segment;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@SuperBuilder
@NoArgsConstructor
@Document(value = "segments")
@EqualsAndHashCode(callSuper = true)
@CompoundIndex(
    name = "brand_segmentName_unique",
    def = "{ 'brand': 1, 'segmentName': 1}",
    unique = true)
public class Segment extends AbstractEntity implements HasBrand {
  private String segmentName;
  private boolean isActive;
  @Brand private String brand;
  private String archivalId;
}
