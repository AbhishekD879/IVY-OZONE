package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import java.util.Map;
import javax.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class StructureDto extends AbstractEntity {

  @NotEmpty private String brand;
  @NotEmpty private Map<String, Map<String, Object>> structure;
}
