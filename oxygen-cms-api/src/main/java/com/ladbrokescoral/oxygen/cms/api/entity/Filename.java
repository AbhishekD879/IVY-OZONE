package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.apache.commons.lang3.StringUtils;

@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Filename {
  private String filename;
  private String originalname;
  private String path;
  private String size;
  private String filetype;
  @JsonIgnore private String fullPath;
  private String svgId;
  private String svg;

  public Filename(String filename) {
    super();
    this.filename = filename;
  }

  @JsonIgnore
  public String relativePath() {
    return StringUtils.isNotEmpty(path) && StringUtils.isNotEmpty(filename)
        ? path + "/" + filename
        : "";
  }
}
