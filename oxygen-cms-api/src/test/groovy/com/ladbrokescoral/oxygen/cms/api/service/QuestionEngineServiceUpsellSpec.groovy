package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.TestUtil
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException
import com.ladbrokescoral.oxygen.cms.api.repository.BigQueryQuestionEngineRepository
import com.ladbrokescoral.oxygen.cms.api.repository.QuestionEngineRepository
import spock.lang.Specification

class QuestionEngineServiceUpsellSpec extends Specification {
  private QuestionEngineRepository repository = Mock(QuestionEngineRepository)
  private ImageService imageService = Mock(ImageService)
  private SvgImageParser svgImageService = Mock(SvgImageParser)
  private QuizPopupSettingService quizPopupSettingService = Mock(QuizPopupSettingService)
  private BigQueryQuestionEngineRepository bigQueryQuestionEngineRepository = Mock(BigQueryQuestionEngineRepository)
  private QuestionEngineService service = new QuestionEngineService(repository, imageService, svgImageService, "quizUpsellFallback/path", "questionDetailsImages", quizPopupSettingService, bigQueryQuestionEngineRepository)

  def "Upsell All Set"() {
    given:
    def quiz = TestUtil.deserializeWithJackson("service/questionengine/upsell-all-set.json", Quiz.class);
    repository.save(quiz) >> {
      quiz.setId(UUID.randomUUID().toString())
      quiz
    }
    when:
    def savedQuiz = service.save(quiz)
    then:
    savedQuiz.getId() != null
  }

  def "Upsell wrong options format"() {
    given:
    def quiz = TestUtil.deserializeWithJackson("service/questionengine/upsell-wrong-options-format.json", Quiz.class);
    when:
    service.save(quiz)
    then:
    thrown(ValidationException)
  }

  def "Upsell options not set"() {
    given:
    def quiz = TestUtil.deserializeWithJackson("service/questionengine/upsell-options-not-set.json", Quiz.class);
    repository.save(quiz) >> {
      quiz.setId(UUID.randomUUID().toString())
      quiz
    }
    when:
    def savedQuiz = service.save(quiz)
    then:
    savedQuiz.getId() != null
  }

  def "Delete fallback image success"() {
    given:
    def quiz = TestUtil.deserializeWithJackson("service/questionengine/delete-upsell-fallback-image-success.json", Quiz.class);
    repository.findById("5cdeb8c65eea9394d0728b0f") >> Optional.of(quiz)
    imageService.removeImage(quiz.getBrand(), quiz.getUpsell().getFallbackImage().getFullPath()) >> true
    when:
    service.deleteFallbackImage(quiz.getId())
    then:
    quiz.getUpsell().getFallbackImage() == null
  }
}
