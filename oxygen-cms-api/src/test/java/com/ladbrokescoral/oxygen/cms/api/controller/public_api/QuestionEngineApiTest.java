package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Users;
import com.ladbrokescoral.oxygen.cms.api.repository.QuestionEngineRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.QuestionEnginePublicService;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Users.class,
      AuthenticationService.class,
      QuestionEnginePublicService.class,
      QuestionEngineApi.class,
      BrandService.class,
      QuestionEngineRepository.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class QuestionEngineApiTest {

  @MockBean private QuestionEnginePublicService publicService;
  @MockBean private BrandService brandService;
  @MockBean private UserService userServiceMock;
  @MockBean private QuestionEngineRepository repository;
  @MockBean private MongoTemplate mongoTemplate;
  @Autowired private MockMvc mockMvc;

  @Test
  public void getAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/question-engine")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void getAllByBrandWithSourceID() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/question-engine/source-id/1,2,3")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void getQuestionById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/brand/question-engine/question/123/567")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void getHistoryWithLimit() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/brand/question-engine/history/3")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void getHistoryWithoutLimit() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/brand/question-engine/history")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void getHistoryWithWrongLimit() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/brand/question-engine/history/-1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void getHistoryWithoutSourceID() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/question-engine/history/source-id")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void getHistoryWithSourceID() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/question-engine/history/source-id/1,2,3")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void getAllQuizzes() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/question-engine/allquizzes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }
}
