package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.List;
import java.util.Optional;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.util.CollectionUtils;

@Document(collection = "systemconfigurations")
@Data
@EqualsAndHashCode(onlyExplicitlyIncluded = true, callSuper = false)
@CompoundIndex(name = "brand_name", def = "{'brand' : 1, 'name': 1}", unique = true)
public class SystemConfiguration extends AbstractEntity implements HasBrand {

  @EqualsAndHashCode.Include @NotBlank private String brand;
  @EqualsAndHashCode.Include @NotBlank private String name;
  @NotBlank private boolean isInitialDataConfig;
  private List<SystemConfigProperty> properties;
  @Transient private boolean overwrite;

  public Optional<SystemConfigProperty> getProperty(String propertyName) {
    if (CollectionUtils.isEmpty(properties)) {
      return Optional.empty();
    }
    return properties.stream().filter(item -> item.getName().equals(propertyName)).findAny();
  }
}
