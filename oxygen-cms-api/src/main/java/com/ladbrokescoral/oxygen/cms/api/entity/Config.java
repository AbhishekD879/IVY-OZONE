package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.List;
import java.util.Map;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

/** @deprecated use {@link SystemConfiguration} instead To be deleted after release-103.0.0 */
@Document(collection = "configs")
@Data
@EqualsAndHashCode(callSuper = true)
@Deprecated
public class Config extends AbstractEntity implements HasBrand {

  @NotBlank private String brand;
  private Map<String, List<SystemConfigProperty>> config;
}
