package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.QuizPopupSetting;
import com.ladbrokescoral.oxygen.cms.api.service.QuizPopupSettingService;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class QuizPopupSettingController extends AbstractCrudController<QuizPopupSetting> {
  private final QuizPopupSettingService quizPopupService;

  QuizPopupSettingController(QuizPopupSettingService quizPopupService) {
    super(quizPopupService);
    this.quizPopupService = quizPopupService;
  }

  @Override
  @PostMapping("/quiz-popup-setting")
  public ResponseEntity<QuizPopupSetting> create(@RequestBody @Valid QuizPopupSetting entity) {
    return super.create(entity);
  }

  @Override
  @PutMapping("/quiz-popup-setting/{id}")
  public QuizPopupSetting update(
      @PathVariable String id, @RequestBody @Valid QuizPopupSetting entity) {
    return super.update(id, entity);
  }

  @GetMapping("/quiz-popup-setting/brand/{brand}")
  public QuizPopupSetting readOneByBrand(@PathVariable String brand) {
    QuizPopupSetting settings = quizPopupService.getByBrand(brand);

    return populateCreatorAndUpdater(settings);
  }
}
