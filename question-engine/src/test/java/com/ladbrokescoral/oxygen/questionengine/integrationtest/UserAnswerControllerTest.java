/*
package com.ladbrokescoral.oxygen.questionengine.integrationtest;

import com.jayway.restassured.RestAssured;
import com.jayway.restassured.http.ContentType;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;
import com.ladbrokescoral.oxygen.questionengine.integrationtest.config.IntegrationTest;
import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.UserData;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Answer;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Question;
import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizHistory;
import com.ladbrokescoral.oxygen.questionengine.repository.UserAnswerRepository;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bpp.BppService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import com.ladbrokescoral.oxygen.questionengine.util.TestUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.http.HttpStatus;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.annotation.DirtiesContext.ClassMode;
import org.springframework.test.context.junit4.SpringRunner;
import uk.co.jemos.podam.api.PodamFactory;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Collections;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import static com.jayway.restassured.RestAssured.given;
import static org.hamcrest.Matchers.matchesPattern;
import static org.hamcrest.core.IsEqual.equalTo;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@IntegrationTest
@RunWith(SpringRunner.class)
@DirtiesContext(classMode = ClassMode.BEFORE_EACH_TEST_METHOD)
public class UserAnswerControllerTest {

  private static final String USERNAME = "testUser";
  private static final String QUIZ_ID = "12345";
  private static final String SOURCE_ID = "/test/source/id";

  @LocalServerPort
  private int port;

  @MockBean
  private UserAnswerRepository repository;

  @MockBean
  private CmsService cmsService;

  @MockBean
  private BppService bppService;

  @Autowired
  private PodamFactory podamFactory;

  @Before
  public void setUp() {
    RestAssured.port = port;
    RestAssured.basePath = "/api/v1/user-answer";

    UserData userData = new UserData();
    userData.setUsername(USERNAME);
    userData.setOxiApiToken("avgdhgsufhskfg");
    when(bppService.findUserData(any())).thenReturn(userData);
  }

  @Test
  public void findById() {

    when(repository.findById(any())).thenReturn(Optional.of(getUserAnswer()));

    given()
        .when()
        .header("token", "adgdfgksdf")
        .get("/{username}/{quiz-id}", USERNAME, QUIZ_ID)
        .then()
        .body("username", equalTo(USERNAME))
        .body("quizId", equalTo(QUIZ_ID))
        .statusCode(HttpStatus.OK.value());
  }

  @Test
  public void findByIdNotFound() {

    when(repository.findById(any())).thenReturn(Optional.empty());

    given()
        .when()
        .header("token", "adgdfgksdf")
        .get("/{username}/{quiz-id}", USERNAME, QUIZ_ID)
        .then()
        .body("httpStatus", equalTo("NOT_FOUND"))
        .statusCode(HttpStatus.NOT_FOUND.value());
  }

  @Test
  public void save() {

    QuizHistory quizHistory = getQuizHistory();
    when(cmsService.findHistory("test,source,id", 3)).thenReturn(Optional.of(quizHistory));
    when(repository.findById(any())).thenReturn(Optional.empty());
    when(repository.save(any())).thenReturn(getUserAnswer());

    given()
        .body(getQuizSubmitModel().setQuestionIdToAnswerId(quizHistory.getLive().getFirstQuestion()
            .flatten()
            .collect(Collectors.toMap(Question::getId, question -> question.getAnswers()
                .stream()
                .findAny()
                .map(Answer::getId)
                .map(Collections::singletonList)
                .get())
            )
        ))
        .contentType(ContentType.JSON)
        .header("token", "adgdfgksdf")
        .when()
        .post()
        .then()
        .statusCode(HttpStatus.CREATED.value())
        .body("username", equalTo(USERNAME))
        .body("quizId", equalTo(QUIZ_ID));

  }

  @Test
  public void saveBadRequest() {

    QuizHistory quizHistory = getQuizHistory();
    quizHistory.setLive(null);
    when(cmsService.findHistory("test,source,id", 3)).thenReturn(Optional.of(quizHistory));
    when(repository.findById(any())).thenReturn(Optional.empty());
    when(repository.save(any())).thenReturn(getUserAnswer());

    given()
        .body(getQuizSubmitModel())
        .contentType(ContentType.JSON)
        .header("token", "adgdfgksdf")
        .when()
        .post()
        .then()
        .statusCode(HttpStatus.BAD_REQUEST.value())
        .body("httpStatus", equalTo("BAD_REQUEST"))
        .body("reason", matchesPattern("You are trying to submit quiz that is no longer in live"));

  }

  @Test
  public void saveException() {

    QuizHistory quizHistory = getQuizHistory();
    quizHistory.setLive(null);
    when(cmsService.findHistory("test,source,id", 3)).thenReturn(Optional.of(quizHistory));
    when(repository.findById(any())).thenReturn(Optional.empty());
    when(repository.save(any())).thenReturn(getUserAnswer());

    QuizSubmitDto quizSubmitModel = getQuizSubmitModel();
    quizSubmitModel.setSourceId(null);
    given()
        .body(quizSubmitModel)
        .contentType(ContentType.JSON)
        .header("token", "adgdfgksdf")
        .when()
        .post()
        .then()
        .statusCode(HttpStatus.BAD_REQUEST.value())
        .body("httpStatus", equalTo("BAD_REQUEST"))
        .body("reason", matchesPattern("sourceId: must not be empty"));

  }

  private UserAnswer getUserAnswer() {
    return podamFactory.manufacturePojo(UserAnswer.class)
        .setUsername(USERNAME)
        .setQuizId(QUIZ_ID);
  }

  private QuizSubmitDto getQuizSubmitModel() {
    return podamFactory.manufacturePojo(QuizSubmitDto.class)
        .setQuizId(QUIZ_ID)
        .setUsername(USERNAME)
        .setCustomerId(UUID.randomUUID().toString())
        .setSourceId(SOURCE_ID);
  }

  private QuizHistory getQuizHistory() {
    QuizHistory quizHistory = podamFactory.manufacturePojo(QuizHistory.class);
    quizHistory.getLive()
        .setId(QUIZ_ID)
        .setDisplayFrom(Instant.now().minus(2, ChronoUnit.DAYS))
        .setDisplayTo(Instant.now().plus(5, ChronoUnit.DAYS))
        .setEntryDeadline(Instant.now().plus(1, ChronoUnit.DAYS));
    TestUtils.buildTree(quizHistory.getLive().getFirstQuestion());

    return quizHistory;
  }
}
*/
