package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.Map;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class InplayScoreBoardStats {

  private Map<String, Object> stats;
}
