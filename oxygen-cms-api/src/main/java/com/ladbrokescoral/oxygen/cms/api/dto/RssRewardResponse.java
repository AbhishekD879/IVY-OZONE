package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import javax.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.Range;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class RssRewardResponse {
  @Range(max = 500, message = "coin should be max of 500")
  private Integer coins;

  private String sitecoreTemplateId;
  @NotBlank private String source;
  private String subSource;
  private String product;
  private String brand;
  private String frontend;
  private Integer communicationType;
}
