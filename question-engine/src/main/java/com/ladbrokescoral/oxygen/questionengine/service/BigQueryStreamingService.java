package com.ladbrokescoral.oxygen.questionengine.service;

import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;

import java.io.IOException;

/**
 * Streams data to BigQuery,
 */
public interface BigQueryStreamingService {

  void streamUserEntry(QuizSubmitDto quizSubmitDto) throws IOException;

  void streamCmsConfiguration() throws IOException;

  void streamResults() throws IOException;
}
