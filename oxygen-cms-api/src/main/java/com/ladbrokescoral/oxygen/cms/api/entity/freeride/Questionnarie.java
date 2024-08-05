package com.ladbrokescoral.oxygen.cms.api.entity.freeride;

import java.util.List;
import lombok.Data;

@Data
public class Questionnarie {
  private List<Question> questions;
  private String summaryMsg;
  private String welcomeMessage;
  private String horseSelectionMsg;
}
