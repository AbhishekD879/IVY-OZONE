package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.Map;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

/** @deprecated use {@link SystemConfiguration} instead to be removed after release-103.0.0 */
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "structures")
@Data
@EqualsAndHashCode(callSuper = true)
@Deprecated
public class Structure extends AbstractEntity implements HasBrand {

  private String lang;
  @NotBlank private String brand;
  @NotEmpty private Map<String, Map<String, Object>> structure;
}
