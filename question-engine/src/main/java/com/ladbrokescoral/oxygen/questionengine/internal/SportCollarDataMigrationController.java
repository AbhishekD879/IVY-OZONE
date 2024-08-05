package com.ladbrokescoral.oxygen.questionengine.internal;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@Controller
@RequiredArgsConstructor
public class SportCollarDataMigrationController {
  private final SportCollarDataMigration sportCollarDataMigration;

  @PostMapping("api/internal/sport-collar-data-migration/{quiz-id}")
  public ResponseEntity migrate(@PathVariable("quiz-id") String quizId, @RequestParam("data") MultipartFile data) throws IOException {
    sportCollarDataMigration.migrate(quizId, data);

    return ResponseEntity.ok().build();
  }
}
