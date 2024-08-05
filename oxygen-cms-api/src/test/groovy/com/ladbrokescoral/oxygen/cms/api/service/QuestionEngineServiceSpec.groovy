package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.TestUtil
import com.ladbrokescoral.oxygen.cms.api.entity.QuestionSummaryReport
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException
import com.ladbrokescoral.oxygen.cms.api.repository.BigQueryQuestionEngineRepository
import com.ladbrokescoral.oxygen.cms.api.repository.QuestionEngineRepository
import spock.lang.Specification

import java.time.Instant

class QuestionEngineServiceSpec extends Specification {

  private QuestionEngineRepository repository = Mock(QuestionEngineRepository)
  private ImageService imageService = Mock(ImageService)
  private SvgImageParser svgImageService = Mock(SvgImageParser)
  private QuizPopupSettingService quizPopupSettingService = Mock(QuizPopupSettingService)
  private BigQueryQuestionEngineRepository bigQueryQuestionEngineRepository = Mock(BigQueryQuestionEngineRepository)
  private QuestionEngineService service = new QuestionEngineService(repository, imageService, svgImageService, "quizUpsellFallback/path", "questionDetailsImages", quizPopupSettingService, bigQueryQuestionEngineRepository)
  private Quiz quiz

  void setup() {
    quiz = TestUtil.deserializeWithJackson("service/questionengine/quiz.json", Quiz.class)
  }

  def "GetQuestionTree"() {
    given:
    repository.findById("5cdeb8c65eea9394d0728b0f") >> Optional.of(quiz)
    when:
    def tree = service.getQuestionTree("5cdeb8c65eea9394d0728b0f", "37200a9b-05f8-4434-bb19-1f162a899ff5")
    then:
    tree != null
    tree.getText() == "Three"
    tree.getAnswers().size() == 4
  }

  def "GetQuestionTree - No results"() {
    given:
    repository.findById("5cdeb8c65eea9394d0728b0f") >> Optional.of(quiz)
    when:
    service.getQuestionTree("5cdeb8c65eea9394d0728b0f", "1234")
    then:
    thrown(NotFoundException)
  }

  def "Generate QuestionsSummary Csv Report"() {
    def quizId = "5e4bec2ec9e77c00010a7313"
    def sourceId = "/test-quiz"
    given:
    def bigQueryResults = Arrays.asList(
        new QuestionSummaryReport()
        .setQuizId(quizId)
        .setSourceId(sourceId)
        .setQuestionNumber(0)
        .setUserOption("Chose not to take a Quiz")
        .setNumberOfEntries(1),
        new QuestionSummaryReport()
        .setQuizId(quizId)
        .setSourceId(sourceId)
        .setQuestionNumber(1)
        .setUserOption("A")
        .setNumberOfEntries(5),
        new QuestionSummaryReport()
        .setQuizId(quizId)
        .setSourceId(sourceId)
        .setQuestionNumber(2)
        .setUserOption("A")
        .setNumberOfEntries(4),
        new QuestionSummaryReport()
        .setQuizId(quizId)
        .setSourceId(sourceId)
        .setQuestionNumber(2)
        .setUserOption("B")
        .setNumberOfEntries(1)
        )
    repository.existsById(quizId) >> true
    bigQueryQuestionEngineRepository.findQuestionSummariesByQuizId(quizId) >> bigQueryResults
    when:
    def report = service.generateQuestionsSummaryCsvReport(quizId)
    then:
    report.getCreatedDate().isBefore(Instant.now())
    report.getCsvContent() == "quizId,sourceId,questionNumber,userOption,totalNumberOfEntries,numberOfEntries,percentOfTotalEntries\n" +
        "5e4bec2ec9e77c00010a7313,/test-quiz,0,\"Chose not to take a Quiz\",1,1,100.0\n" +
        "5e4bec2ec9e77c00010a7313,/test-quiz,1,A,5,5,100.0\n" +
        "5e4bec2ec9e77c00010a7313,/test-quiz,2,A,5,4,80.0\n" +
        "5e4bec2ec9e77c00010a7313,/test-quiz,2,B,5,1,20.0\n"
  }

  def "Generate QuestionsSummary Csv Report - Quiz does not exist"() {
    def quizId = "5e4bec2ec9e77c00010a7313"
    given:
    repository.exists(quizId) >> false
    when:
    service.generateQuestionsSummaryCsvReport(quizId)
    then:
    thrown(NotFoundException)
  }
}
