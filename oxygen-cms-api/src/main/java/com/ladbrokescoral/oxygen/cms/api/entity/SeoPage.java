package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.DecimalMax;
import javax.validation.constraints.DecimalMin;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = SeoPage.COLLECTION_NAME)
@Data
@EqualsAndHashCode(callSuper = true)
public class SeoPage extends AbstractEntity implements HasBrand {

  public static final String COLLECTION_NAME = "seopages";

  @NotBlank private String brand;
  @NotBlank private String changefreq;
  private String description;
  private Boolean disabled = false;
  private String lang;
  private String staticBlock;
  private String pageTitleBlock;
  @NotBlank private String title;
  @NotNull @NotBlank private String url;
  private String staticBlockTitle;

  @Field(value = "url_brand")
  private String urlBrand;

  @NotNull
  @DecimalMax(value = "1")
  @DecimalMin(value = "0")
  private Double priority;
}
