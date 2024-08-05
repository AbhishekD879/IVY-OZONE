package com.coral.oxygen.middleware.pojos.model.output;

import java.io.Serializable;
import java.util.Map;
import lombok.Data;

@Data
public class InplayScoreBoardStats implements Serializable {

  private Map<String, Object> stats;
}
