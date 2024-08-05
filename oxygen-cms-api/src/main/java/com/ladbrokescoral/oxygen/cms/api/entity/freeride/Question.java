package com.ladbrokescoral.oxygen.cms.api.entity.freeride;

import java.util.List;
import lombok.Data;

@Data
public class Question {
  private Integer questionId;
  private String quesDescription;
  private List<Option> options;
  private String chatBoxResp;
}
