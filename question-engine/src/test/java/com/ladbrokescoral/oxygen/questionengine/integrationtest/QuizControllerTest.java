/*

package com.ladbrokescoral.oxygen.questionengine.integrationtest;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.matchesPattern;
import static org.hamcrest.core.IsEqual.equalTo;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.when;

import io.restassured.RestAssured;
import com.ladbrokescoral.oxygen.questionengine.integrationtest.config.IntegrationTest;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.UserData;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Question;
import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizHistory;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bpp.BppService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Optional;
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

@IntegrationTest
@RunWith(SpringRunner.class)
@DirtiesContext(classMode = ClassMode.BEFORE_EACH_TEST_METHOD)
public class QuizControllerTest {

  private static final String USERNAME = "testUser";
  private static final String QUIZ_ID = "12345";
  private static final String SOURCE_ID = "/test/source/id";
  private static final String QUESTION_ID = "questionId";
  private static final int HISTORY_PREVIOUS_LIMIT = 3;

//  @LocalServerPort
  private int port = 8080;

  @MockBean
  private CmsService cmsService;

  @MockBean
  private BppService bppService;

  @Autowired
  private PodamFactory podamFactory;

  @Before
  public void setUp() {
    RestAssured.port = port;
    RestAssured.basePath = "/api/v1/quiz";
  }

  @Test
  public void findById() {
    when(cmsService.findHistory("test,source,id", HISTORY_PREVIOUS_LIMIT)).thenReturn(Optional.of(getQuizHistory()));

    given()
        .when()
        .get("/history/?source-id={sourceId}&previous-limit={previousLimit}", SOURCE_ID, HISTORY_PREVIOUS_LIMIT)
        .then()
        .body("live.id", equalTo(QUIZ_ID))
        .statusCode(HttpStatus.OK.value());
  }

  @Test
  public void findByIdInternalServerError() {

    doThrow(RuntimeException.class).when(cmsService).findHistory("test,source,id", HISTORY_PREVIOUS_LIMIT);

    given()
        .when()
        .get("/history/?source-id={sourceId}&previous-limit={previousLimit}", SOURCE_ID, HISTORY_PREVIOUS_LIMIT)
        .then()
        .body("httpStatus", equalTo("INTERNAL_SERVER_ERROR"))
        .body("reason", matchesPattern("Oops... Something went wrong. Please ensure you're referring to the existing resource or contact our support team"))
        .statusCode(HttpStatus.INTERNAL_SERVER_ERROR.value());
  }

  @Test
  public void findByIdReasonUnavailableException() {

    given()
        .when()
        .get("/history/?source-id={sourceId}&previous-limit={previousLimit}", SOURCE_ID, "somestring")
        .then()
        .body("httpStatus", equalTo("BAD_REQUEST"))
        .body("reason", matchesPattern("Reason unavailable. See Status Code or contact our support team for more details"))
        .statusCode(HttpStatus.BAD_REQUEST.value());
  }

  @Test
  public void findByIdNullSourceId() {

    given()
        .when()
        .get("/history/")
        .then()
        .body("httpStatus", equalTo("BAD_REQUEST"))
        .body("reason", matchesPattern("Required String parameter 'source-id' is not present"))
        .statusCode(HttpStatus.BAD_REQUEST.value());
  }

  @Test
  public void findByIdEmptySourceId() {

    given()
        .when()
        .get("/history/?source-id=&previous-limit=4")
        .then()
        .body("httpStatus", equalTo("BAD_REQUEST"))
        .body("reason", matchesPattern("'source-id' must not be blank"))
        .statusCode(HttpStatus.BAD_REQUEST.value());
  }

  @Test
  public void findUserQuizHistory() {
    when(cmsService.findHistory("test,source,id", HISTORY_PREVIOUS_LIMIT)).thenReturn(Optional.of(getQuizHistory()));

    UserData userData = new UserData();
    userData.setUsername(USERNAME);
    userData.setOxiApiToken("avgdhgsufhskfg");
    when(bppService.findUserData(any())).thenReturn(userData);

    given()
        .when()
        .header("token", "adgdfgksdf")
        .get("/history/{username}/?source-id={sourceId}&previous-limit={previousLimit}", USERNAME, SOURCE_ID, HISTORY_PREVIOUS_LIMIT)
        .then()
        .body("live.id", equalTo(QUIZ_ID))
        .statusCode(HttpStatus.OK.value());
  }

  @Test
  public void findUserQuizHistoryBppError() {
    when(cmsService.findHistory("test,source,id", HISTORY_PREVIOUS_LIMIT)).thenReturn(Optional.of(getQuizHistory()));

    doThrow(RuntimeException.class).when(bppService).findUserData(any());

    given()
        .when()
        .header("token", "adgdfgksdf")
        .get("/history/{username}/?source-id={sourceId}&previous-limit={previousLimit}", USERNAME, SOURCE_ID, HISTORY_PREVIOUS_LIMIT)
        .then()
        .body("httpStatus", equalTo("INTERNAL_SERVER_ERROR"))
        .body("reason", matchesPattern("Oops... Something went wrong. Please ensure you're referring to the existing resource or contact our support team"))
        .statusCode(HttpStatus.INTERNAL_SERVER_ERROR.value());
  }

  @Test
  public void findUserQuizHistoryUnauthorized() {
    when(cmsService.findHistory("test,source,id", HISTORY_PREVIOUS_LIMIT)).thenReturn(Optional.of(getQuizHistory()));

    UserData userData = new UserData();
    userData.setUsername("notTheSameUser");
    userData.setOxiApiToken("avgdhgsufhskfg");
    when(bppService.findUserData(any())).thenReturn(userData);

    given()
        .when()
        .header("token", "adgdfgksdf")
        .get("/history/{username}/?source-id={sourceId}&previous-limit={previousLimit}", USERNAME, SOURCE_ID, HISTORY_PREVIOUS_LIMIT)
        .then()
        .body("httpStatus", equalTo("UNAUTHORIZED"))
        .body("reason", matchesPattern("Unauthorized"))
        .statusCode(HttpStatus.UNAUTHORIZED.value());
  }

  @Test
  public void findUserQuizHistoryWithoutTokenHeader() {
    when(cmsService.findHistory("test,source,id", HISTORY_PREVIOUS_LIMIT)).thenReturn(Optional.of(getQuizHistory()));

    UserData userData = new UserData();
    userData.setUsername("notTheSameUser");
    userData.setOxiApiToken("avgdhgsufhskfg");
    when(bppService.findUserData(any())).thenReturn(userData);

    given()
        .when()
        .get("/history/{username}/?source-id={sourceId}&previous-limit={previousLimit}", USERNAME, SOURCE_ID, HISTORY_PREVIOUS_LIMIT)
        .then()
        .body("httpStatus", equalTo("UNAUTHORIZED"))
        .body("reason", matchesPattern("Unauthorized"))
        .statusCode(HttpStatus.UNAUTHORIZED.value());
  }

  @Test
  public void findQuestion() {

    when(cmsService.findQuestion(QUIZ_ID, QUESTION_ID)).thenReturn(Optional.of(getQuestion()));

    given()
        .when()
        .get("/question/{quiz-id}/{question-id}", QUIZ_ID, QUESTION_ID)
        .then()
        .body("id", equalTo(QUIZ_ID))
        .body("text", equalTo("Question1"))
        .statusCode(HttpStatus.OK.value());

  }

  private QuizHistory getQuizHistory() {
    QuizHistory quizHistory = podamFactory.manufacturePojo(QuizHistory.class);
    quizHistory.getLive().setId(QUIZ_ID)
        .setDisplayFrom(Instant.now().minus(2, ChronoUnit.DAYS))
        .setDisplayTo(Instant.now().plus(5, ChronoUnit.DAYS))
        .setEntryDeadline(Instant.now().plus(1, ChronoUnit.DAYS));
    return quizHistory;
  }

  private Question getQuestion() {
    return podamFactory.manufacturePojo(Question.class)
        .setId(QUIZ_ID)
        .setText("Question1");
  }
}
*/