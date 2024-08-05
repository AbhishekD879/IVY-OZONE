package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import java.util.List;
import lombok.Data;

@Data
public class QuizzesByBrandAndSourceId {
  private String brand;
  private String sourceId;
  private List<Quiz> quizzes;
}
