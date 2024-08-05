package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Question;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz;
import com.ladbrokescoral.oxygen.cms.api.service.QuestionEngineCsvReport;
import com.ladbrokescoral.oxygen.cms.api.service.QuestionEngineService;
import java.io.IOException;
import java.util.List;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class QuestionEngineController extends AbstractCrudController<Quiz> {

  private final QuestionEngineService service;

  public QuestionEngineController(QuestionEngineService service) {
    super(service);
    this.service = service;
  }

  @PostMapping("question-engine")
  @Override
  public ResponseEntity create(@RequestBody @Valid Quiz entity) {
    return super.create(entity);
  }

  @GetMapping("question-engine")
  public List<Quiz> readFullQuiz() {
    return super.readAll();
  }

  @GetMapping("question-engine/{id}")
  public Quiz readById(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("question-engine/question/{quizId}/{questionId}")
  public Question readQuestionById(@PathVariable String quizId, @PathVariable String questionId) {
    return service.getQuestionTree(quizId, questionId);
  }

  @GetMapping("question-engine/brand/{brand}")
  public List<Quiz> readQuizByBrand(@PathVariable String brand) {
    return service.findByBrand(brand);
  }

  @PutMapping("question-engine/{id}")
  @Override
  public Quiz update(@PathVariable String id, @RequestBody @Valid Quiz entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("question-engine/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("question-engine/{id}/upsell/upload-fallback-image")
  public Quiz uploadImage(
      @PathVariable String id,
      @RequestParam(value = "fallback-image") MultipartFile fallbackImage) {
    return service.uploadFallbackImage(id, fallbackImage);
  }

  @DeleteMapping("question-engine/{id}/upsell/upload-fallback-image")
  public Quiz deleteImage(@PathVariable String id) {
    return service.deleteFallbackImage(id);
  }

  @PostMapping("question-engine/{brand}/question/{quizId}/{questionId}/question-details-images")
  public Quiz uploadQuestionDetailsImages(
      @PathVariable String brand,
      @PathVariable String quizId,
      @PathVariable String questionId,
      @RequestParam(value = "home", required = false) MultipartFile homeTeamKit,
      @RequestParam(value = "away", required = false) MultipartFile awayTeamKit,
      @RequestParam(value = "channel", required = false) MultipartFile channel) {
    return service.uploadQuestionDetailsImages(
        brand, quizId, questionId, homeTeamKit, awayTeamKit, channel);
  }

  @PostMapping("question-engine/{brand}/{quizId}/default-questions-details-images")
  public Quiz uploadQuizQuestionsDetailsImages(
      @PathVariable String brand,
      @PathVariable String quizId,
      @RequestParam(value = "home", required = false) MultipartFile homeTeamKit,
      @RequestParam(value = "away", required = false) MultipartFile awayTeamKit,
      @RequestParam(value = "channel", required = false) MultipartFile channel) {
    return service.uploadDefaultQuestionDetailsImages(
        brand, quizId, homeTeamKit, awayTeamKit, channel);
  }

  @DeleteMapping("question-engine/{quizId}/default-questions-details-images/{imageType}")
  public Quiz deleteQuizQuestionsDetailsImages(
      @PathVariable String quizId, @PathVariable String imageType) {
    return service.deleteDefaultQuestionDetailsImages(quizId, imageType);
  }

  @PostMapping(value = "question-engine/{brand}/{quizId}/quiz-logo-image")
  public Quiz uploadQuizLogoImage(
      @PathVariable String brand,
      @PathVariable String quizId,
      @RequestParam(value = "file") MultipartFile quizLogo) {
    return service.uploadQuizLogoImage(brand, quizId, quizLogo);
  }

  @DeleteMapping(value = "question-engine/{quizId}/quiz-logo-image")
  public Quiz deletedQuizLogoImage(@PathVariable String quizId) {
    return service.deleteQuizLogoImage(quizId);
  }

  @PostMapping(value = "question-engine/{brand}/{quizId}/quiz-background-image")
  public Quiz uploadQuizBackgroundImage(
      @PathVariable String brand,
      @PathVariable String quizId,
      @RequestParam(value = "file") MultipartFile quizBackground) {
    return service.uploadQuizBackgroundImage(brand, quizId, quizBackground);
  }

  @DeleteMapping(value = "question-engine/{quizId}/quiz-background-image")
  public Quiz deletedQuizBackgroundImage(@PathVariable String quizId) {
    return service.deleteQuizBackgroundImage(quizId);
  }

  @PostMapping("question-engine/{brand}/{quizId}/popup-icon/{iconType}")
  public Quiz uploadPopupIconImage(
      @PathVariable String brand,
      @PathVariable String quizId,
      @PathVariable String iconType,
      @RequestParam(value = "file") MultipartFile file) {
    return service.uploadPopupIconImage(brand, quizId, iconType, file);
  }

  @DeleteMapping("question-engine/{quizId}/popup-icon/{iconType}")
  public Quiz deletePopupIconImage(@PathVariable String quizId, @PathVariable String iconType) {
    return service.deletePopupIconImage(quizId, iconType);
  }

  @GetMapping("question-engine/{quizId}/report/questions-summary")
  public QuestionEngineCsvReport generateQuestionsSummaryReport(@PathVariable String quizId)
      throws IOException {
    return service.generateQuestionsSummaryCsvReport(quizId);
  }
}
