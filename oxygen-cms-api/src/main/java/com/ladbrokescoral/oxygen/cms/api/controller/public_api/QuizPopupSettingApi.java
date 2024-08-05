package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.QuizPopupSettingDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.*;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class QuizPopupSettingApi implements Public {
  private final QuizPopupSettingPublicService quizPopupService;

  @GetMapping("{brand}/quiz-popup-setting-details")
  public ResponseEntity<QuizPopupSettingDetailsDto> findQuizPopupDetailsByBrand(
      @PathVariable String brand) {
    return quizPopupService
        .findPopupDetailsByBrand(brand)
        .map(ResponseEntity::ok)
        .orElse(new ResponseEntity<>(HttpStatus.NO_CONTENT));
  }
}
