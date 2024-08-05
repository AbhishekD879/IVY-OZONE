package com.ladbrokescoral.oxygen.questionengine.internal;

import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

public interface SportCollarDataMigration {
  void migrate(String questionEngineQuizId, MultipartFile data) throws IOException;
}
