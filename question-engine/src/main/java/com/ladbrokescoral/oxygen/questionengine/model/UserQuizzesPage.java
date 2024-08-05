package com.ladbrokescoral.oxygen.questionengine.model;

import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserQuizDto;
import lombok.Data;
import lombok.RequiredArgsConstructor;

import java.util.List;

@Data
@RequiredArgsConstructor
public class UserQuizzesPage {
  private final int totalRecords;
  private final List<UserQuizDto> quizzes;
}
