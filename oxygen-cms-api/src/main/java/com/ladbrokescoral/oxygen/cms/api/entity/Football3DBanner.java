package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "football3dbanners")
@Data
@EqualsAndHashCode(callSuper = true)
public class Football3DBanner extends BannerEntity implements HasBrand {

  private String targetUri;
  @NotNull private Integer displayDuration;
}
