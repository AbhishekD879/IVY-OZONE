package com.ladbrokescoral.oxygen.questionengine.model;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class UserQuizSearchParams {
  private final String username;
  private final String sourceId;
}
