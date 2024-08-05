package com.coral.oxygen.middleware.pojos.model.cms.featured;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Filename implements Serializable {

  @JsonProperty("filename")
  @SerializedName("filename")
  private String file;

  private String originalname;
  private String path;
  private String size;
  private String filetype;
}
