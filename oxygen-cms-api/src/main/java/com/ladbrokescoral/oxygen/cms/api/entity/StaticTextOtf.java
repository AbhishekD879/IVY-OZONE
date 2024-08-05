package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "static-text-otf")
@Data
@EqualsAndHashCode(callSuper = true)
public class StaticTextOtf extends SortableEntity implements HasBrand {

  @NotBlank private String brand;
  private boolean enabled;
  private String lang = "en";
  @NotBlank private String pageName;
  private String title;
  private String pageText1;
  private String pageText2;
  private String pageText3;
  private String pageText4;
  private String pageText5;
  private String ctaText1;
  private String ctaText2;
}
