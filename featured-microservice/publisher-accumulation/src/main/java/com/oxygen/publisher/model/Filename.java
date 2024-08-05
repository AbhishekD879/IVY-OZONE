package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.io.Serializable;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Filename implements Serializable {

  @JsonProperty("filename")
  private String file;

  private String originalname;
  private String path;
  private String size;
  private String filetype;
}
