package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import java.util.List;
import javax.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class ConfigDto extends AbstractEntity {

  @NotEmpty private String brand;
  @NotEmpty private List<ConfigItemDto> config;
}
