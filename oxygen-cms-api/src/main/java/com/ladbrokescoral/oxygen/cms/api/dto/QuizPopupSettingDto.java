package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@NoArgsConstructor
@Accessors(chain = true)
public class QuizPopupSettingDto {
  private String id;

  private boolean enabled;
  private String pageUrls;
  private String sourceId;
  private String quizId;
}
