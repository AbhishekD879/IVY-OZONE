package com.ladbrokescoral.oxygen.questionengine.dto.userquiz;

import lombok.Data;

import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import java.util.List;
import java.util.Map;

@Data
public class UserAnswerDto {

  @NotEmpty
  private String username;

  @NotEmpty
  private String quizId;

  @NotEmpty
  private String rewardStatus;

  @Valid
  @NotEmpty
  private Map<@NotEmpty String, @Valid @NotEmpty List<@NotEmpty String>> questionIdToAnswerId;
}
