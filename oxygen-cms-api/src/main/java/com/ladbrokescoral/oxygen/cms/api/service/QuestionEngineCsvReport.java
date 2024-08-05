package com.ladbrokescoral.oxygen.cms.api.service;

import java.time.Instant;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class QuestionEngineCsvReport {
  private final String csvContent;
  private final Instant createdDate;
}
