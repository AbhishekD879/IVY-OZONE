package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = SeoAutoPage.COLLECTION_NAME)
@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class SeoAutoPage extends AbstractEntity implements HasBrand {

  public static final String COLLECTION_NAME = "seoAutoPages";
  @NotBlank private String brand;
  @NotNull @NotBlank private String uri;
  @NotBlank private String metaTitle;
  @NotBlank private String metaDescription;
}
