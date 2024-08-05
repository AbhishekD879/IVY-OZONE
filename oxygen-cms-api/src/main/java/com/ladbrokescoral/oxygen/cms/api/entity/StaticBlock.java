package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidURI;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = StaticBlock.COLLECTION_NAME)
@Data
@EqualsAndHashCode(callSuper = true)
public class StaticBlock extends AbstractEntity implements HasBrand {

  public static final String COLLECTION_NAME = "staticblocks";

  @NotBlank private String brand;
  private Boolean enabled = true;
  private String htmlMarkup;
  private String lang = "en";
  @NotNull @NotBlank private String title;

  @JsonProperty("title_brand")
  @Field("title_brand")
  private String titleBrand;

  @NotBlank @ValidURI private String uri;
}
