package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
@NoArgsConstructor // remove to make immutable
public class ModularContentDto {
  @JsonProperty("title")
  private String title;

  @JsonProperty("directiveName")
  private String directiveName;

  @JsonProperty("visible")
  private Boolean visible;

  @JsonProperty("id")
  private String id;

  @JsonProperty("url")
  private String url;

  @JsonProperty("showTabOn")
  private String showTabOn;

  @JsonProperty("devices")
  private List<String> devices;

  private Integer hubIndex;
}
