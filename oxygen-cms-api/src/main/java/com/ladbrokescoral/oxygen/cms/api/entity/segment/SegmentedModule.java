package com.ladbrokescoral.oxygen.cms.api.entity.segment;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;
import org.springframework.data.mongodb.core.mapping.Document;

@SuperBuilder
@Data
@NoArgsConstructor
@Document(value = "segmentedModules")
@EqualsAndHashCode(callSuper = true)
public class SegmentedModule extends AbstractEntity implements HasBrand {

  private String moduleName;
  private PageType pageType;
  private String pageId;
  private DeviceType channel;
  @Brand private String brand;
}
