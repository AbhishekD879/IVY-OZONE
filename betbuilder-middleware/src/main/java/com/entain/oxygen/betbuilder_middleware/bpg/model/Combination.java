package com.entain.oxygen.betbuilder_middleware.bpg.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Combination {
  private String id;
  private Integer sportId;
  private List<Selection> selections;
}
