package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.EventHub;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.repository.EventHubRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.DeleteEntityService;
import com.ladbrokescoral.oxygen.cms.api.service.EventHubService;
import java.util.Collections;
import java.util.Optional;
import java.util.UUID;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      EventHubs.class,
      EventHubService.class,
    })
@MockBean({DeleteEntityService.class, BrandService.class})
@AutoConfigureMockMvc(addFilters = false)
public class EventHubsTest extends AbstractControllerTest {

  @MockBean private EventHubRepository repository;
  @MockBean private HomeModuleRepository homeModuleRepository;

  private EventHub entity;

  @Before
  public void init() {

    entity = createEventHub();

    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(EventHub.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testCreateEventHubError() throws Exception {

    entity = new EventHub();

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/event-hub")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateEventHub() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/event-hub")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateEventHubMoreThenMaxCount() throws Exception {

    entity.setIndexNumber(23);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/event-hub")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateEventHubZeroIndex() throws Exception {

    entity.setIndexNumber(0);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/event-hub")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateEventHub() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/event-hub/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/event-hub").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/event-hub/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/event-hub/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneError() throws Exception {
    given(repository.findById(anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/event-hub/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Ignore("deleteAll is not calling")
  @Test
  public void testDelete() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/event-hub/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());

    then(homeModuleRepository).should(atLeastOnce()).deleteAll("bma", PageType.eventhub, "16");
  }

  @Test
  public void testOrder() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Collections.singletonList("-1"))
            .id(UUID.randomUUID().toString())
            .build();

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/event-hub/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  private static EventHub createEventHub() {
    EventHub entity = new EventHub();
    entity.setBrand("bma");
    entity.setSortOrder(1.0);
    entity.setId("100");
    entity.setIndexNumber(16);
    entity.setTitle("test title1");
    return entity;
  }

  @Test
  public void testInvalidTitle() throws Exception {

    entity.setTitle("test title1 $");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/event-hub")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testInvalidTitleAndSymbol() throws Exception {

    entity.setTitle("test title1 & test");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/event-hub")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }
}
