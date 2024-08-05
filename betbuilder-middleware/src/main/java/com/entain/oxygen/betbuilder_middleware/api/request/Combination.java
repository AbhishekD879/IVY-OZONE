package com.entain.oxygen.betbuilder_middleware.api.request;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Combination {
  private String id;
  private Integer sportId;
  private List<Selection> selections;

  @JsonProperty("oEId")
  private String oEId;
}
