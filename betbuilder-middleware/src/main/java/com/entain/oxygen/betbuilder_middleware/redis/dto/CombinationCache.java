package com.entain.oxygen.betbuilder_middleware.redis.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.io.Serializable;
import java.util.List;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class CombinationCache implements Serializable {
  private static final long serialVersionUID = 8700132876665387314L;
  String id;
  String hash;
  private Integer sportId;
  String oEId;
  private List<SelectionDto> selections;
}
