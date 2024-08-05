package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.fasterxml.jackson.annotation.JsonSetter;
import java.util.UUID;
import lombok.Data;
import lombok.experimental.Accessors;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.mongodb.core.mapping.DBRef;

@Data
@Accessors(chain = true)
public class Answer {

  private String id = UUID.randomUUID().toString();
  private String text;
  private String questionAskedId;
  private String nextQuestionId;
  private boolean correctAnswer;
  private String selectionId;
  @DBRef private EndPage endPage;

  @JsonSetter
  public Answer setId(String id) {
    if (StringUtils.isNotEmpty(id)) {
      this.id = id;
    }
    return this;
  }
}
