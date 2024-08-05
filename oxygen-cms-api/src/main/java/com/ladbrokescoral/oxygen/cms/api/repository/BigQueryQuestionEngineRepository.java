package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.QuestionSummaryReport;
import java.io.IOException;
import java.util.List;

public interface BigQueryQuestionEngineRepository {
  List<QuestionSummaryReport> findQuestionSummariesByQuizId(String quizId) throws IOException;
}
