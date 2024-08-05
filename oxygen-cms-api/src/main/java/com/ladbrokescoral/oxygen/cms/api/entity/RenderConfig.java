package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "renderconfig")
@Data
@EqualsAndHashCode(callSuper = true)
public class RenderConfig extends AbstractEntity implements HasBrand {

  @NotBlank private String brand;
  @NotEmpty private String path;
  @NotEmpty private String device;
  @NotNull private Boolean enabled;
}
