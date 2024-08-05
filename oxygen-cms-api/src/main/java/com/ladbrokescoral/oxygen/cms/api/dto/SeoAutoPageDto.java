package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@JsonIgnoreProperties(ignoreUnknown = true)
public class SeoAutoPageDto {
  @NotBlank private String brand;
  @NotNull @NotBlank private String uri;
  @NotBlank private String metaTitle;
  @NotBlank private String metaDescription;
}
