package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = YourCallStaticBlock.COLLECTION_NAME)
@Data
@EqualsAndHashCode(callSuper = true)
public class YourCallStaticBlock extends AbstractEntity implements HasBrand {

  public static final String COLLECTION_NAME = "ycstaticblocks";

  @Field("title_brand")
  private String titleBrand;

  @NotNull @NotBlank private String title;
  private String lang = "en";
  @NotBlank private String brand;
  private Boolean enabled = true;
  private String htmlMarkup;
  private Boolean fiveASide = false;
}
