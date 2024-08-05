package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonProperty;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "ssopages")
@Data
@EqualsAndHashCode(callSuper = true)
public class SsoPage extends SortableEntity implements HasBrand {

  @JsonProperty("title_brand")
  @Field("title_brand")
  private String titleBrand;

  private String targetIOS;
  @NotNull @NotBlank private String title;
  private Boolean showOnIOS;
  private Boolean showOnAndroid;
  private Boolean disabled;
  @NotBlank private String brand;
  private Filename filename;
  private Integer heightMedium;
  private String uriMedium;
  private String uriOriginal;
  private Integer widthMedium;
  private String openLink;
  private String targetAndroid;
}
