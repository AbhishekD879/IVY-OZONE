package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Question;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz;
import com.ladbrokescoral.oxygen.cms.api.repository.BigQueryQuestionEngineRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.QuestionEngineRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.QuestionEngineService;
import com.ladbrokescoral.oxygen.cms.api.service.QuizPopupSettingService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgImageParser;
import java.time.Instant;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({QuestionEngineController.class, QuestionEngineService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBean({
  ImageService.class,
  SvgImageParser.class,
  QuizPopupSettingService.class,
  BigQueryQuestionEngineRepository.class
})
public class QuestionEngineControllerTest extends AbstractControllerTest {

  @MockBean private QuestionEngineRepository repository;

  private Quiz entity;

  @Before
  public void init() throws Exception {

    entity = TestUtil.deserializeWithJackson("service/questionengine/quiz.json", Quiz.class);
    this.entity.setId("5cdeb8c65eea9394d0728b0f");

    given(repository.findById(entity.getId())).willReturn(Optional.of(entity));
    given(repository.save(any(Quiz.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void create() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/question-engine")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isCreated());
  }

  @Test
  public void createFailedValidation() throws Exception {

    entity.setEntryDeadline(Instant.now());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/question-engine")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void readFullQuiz() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/question-engine")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void readById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/question-engine/5cdeb8c65eea9394d0728b0f")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void readQuestionById() throws Exception {

    this.entity.setFirstQuestion(new Question().setId("5ee80827-a5a6-472a-b9f5-e77c4ddd59aa"));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    "/v1/api/question-engine/question/5cdeb8c65eea9394d0728b0f/5ee80827-a5a6-472a-b9f5-e77c4ddd59aa")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void readQuizByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/question-engine/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void update() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/question-engine/5cdeb8c65eea9394d0728b0f")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isOk());
  }

  @Test
  public void delete() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/question-engine/5cdeb8c65eea9394d0728b0f")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void generateQuestionsSummaryReport() throws Exception {

    given(repository.existsById(entity.getId())).willReturn(true);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    "/v1/api/question-engine/5cdeb8c65eea9394d0728b0f/report/questions-summary")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }
}
