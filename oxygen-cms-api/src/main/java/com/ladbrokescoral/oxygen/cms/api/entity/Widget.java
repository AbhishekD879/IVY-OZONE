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
@Document(collection = "widgets")
@Data
@EqualsAndHashCode(callSuper = true)
public class Widget extends SortableEntity implements HasBrand {

  @NotBlank private String brand;
  private String columns;
  private Boolean disabled;
  private Boolean showExpanded;
  private boolean showOnDesktop;
  private boolean showOnMobile;
  private boolean showOnTablet;
  private String title;
  @NotNull @NotBlank private String type;

  @Field("type_brand")
  @JsonProperty("type_brand")
  private String typeBrand;

  private boolean showFirstEvent = true;
  private ShowOn showOn;
}
