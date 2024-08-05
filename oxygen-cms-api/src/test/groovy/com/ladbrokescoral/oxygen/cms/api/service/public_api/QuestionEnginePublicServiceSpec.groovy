package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.TestUtil
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz
import com.ladbrokescoral.oxygen.cms.api.repository.QuestionEngineRepository
import com.ladbrokescoral.oxygen.cms.api.service.QuestionEngineService
import org.springframework.data.mongodb.core.MongoTemplate
import spock.lang.Specification

class QuestionEnginePublicServiceSpec extends Specification {

  private QuestionEngineService service = Mock(QuestionEngineService)
  private QuestionEngineRepository repository = Mock(QuestionEngineRepository)
  private QuestionEnginePublicService publicService = new QuestionEnginePublicService(service, repository, null)
  private Quiz quiz

  void setup() {
    quiz = TestUtil.deserializeWithJackson("service/questionengine/quiz.json", Quiz.class)
  }

  def "GetAllQuizzes"() {
    given:
    service.findAll() >> Collections.singletonList(this.quiz)
    when:
    def quizzes = publicService.getAllQuizzes()
    then:
    quizzes.size() == 1
    quizzes.get(0).getFirstQuestion().getText() == "One"
  }

  def "GetQuizByBrand"() {
    given:
    service.findByBrand("bma") >> Collections.singletonList(this.quiz)
    when:
    def quizzes = publicService.getQuizByBrand("bma")
    then:
    quizzes.size() == 1
    quizzes.get(0).getBrand() == "bma"
    quizzes.get(0).getFirstQuestion().getText() == "One"
  }

  def "GetQuestion"() {
    given:
    service.getQuestionTree("5cdeb8c65eea9394d0728b0f", "1a7b4d10-71f5-4382-84cb-64f48f3b277c") >> this.quiz.getFirstQuestion()
    when:
    def question = publicService.getQuestion("5cdeb8c65eea9394d0728b0f", "1a7b4d10-71f5-4382-84cb-64f48f3b277c")
    then:
    question.getText() == "One"
    question.getAnswers().size() == 3
  }
}
