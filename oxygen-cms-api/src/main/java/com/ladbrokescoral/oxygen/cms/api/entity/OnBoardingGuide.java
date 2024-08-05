package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "onBoardingGuides")
@Data
@EqualsAndHashCode(callSuper = true)
public class OnBoardingGuide extends SortableEntity implements HasBrand {

  @NotBlank private String brand;
  @NotBlank private String guideName;
  private String guidePath;
  private SvgFilename svgFilename;
  private boolean enabled;
}
