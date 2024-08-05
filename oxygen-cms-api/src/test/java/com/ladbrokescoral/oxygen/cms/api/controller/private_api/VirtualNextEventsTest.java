package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Type;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.VirtualNextEvent;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualNextEventsRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.VirtualNextEventsService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;
import java.util.UUID;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.MockBeans;
import org.springframework.data.domain.Sort;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

@WebMvcTest(value = {VirtualNextEvents.class, VirtualNextEventsService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBeans({@MockBean(BrandService.class)})
public class VirtualNextEventsTest extends AbstractControllerTest {

  @MockBean private VirtualNextEventsRepository repository;

  @MockBean private SiteServeApiProvider siteServeApiProvider;

  @MockBean private SiteServerApi siteServerApi;

  private VirtualNextEvent entity;

  @Before
  public void initialize() {
    this.entity = getVirtualNextEvent("football", "42", "224,225");
    given(this.repository.findById(Mockito.anyString())).willReturn(Optional.of(entity));
    given(this.repository.save(any(VirtualNextEvent.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(this.siteServeApiProvider.api(anyString())).willReturn(siteServerApi);
  }

  @Test
  public void testGetVirtualNextEvent() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-next-event/1122")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.title", Matchers.is("football")));
  }

  @Test
  public void testGetVirtualNextEventsAll() throws Exception {
    given(this.repository.findAll()).willReturn(Collections.singletonList(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-next-event")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$[0].classIds", Matchers.is("42")));
  }

  @Test
  public void testGetVirtualNextEventsByBrand() throws Exception {
    given(this.repository.findByBrand(anyString(), any(Sort.class)))
        .willReturn(Collections.singletonList(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-next-event/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$[0].typeIds", Matchers.is("224,225")));
  }

  @Test
  public void testSaveVirtualNextEvent() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/virtual-next-event")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(MockMvcResultMatchers.status().isCreated())
        .andExpect(MockMvcResultMatchers.jsonPath("$.title", Matchers.is("football")));
  }

  @Test
  public void testUpdateVirtualNextEvent() throws Exception {
    VirtualNextEvent event = entity;
    event.setTitle("Horse Racing");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/virtual-next-event/1122")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(event)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.title", Matchers.is("Horse Racing")));
  }

  @Test
  public void testDeleteVirtualNextEvent() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/virtual-next-event/1122")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().isNoContent());
  }

  @Test
  public void testOrdering() throws Exception {
    OrderDto orderDto = OrderDto.builder().id("11").order(Arrays.asList("1", "2", "3")).build();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/virtual-next-event/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(orderDto)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testEmptyOBTypesForClassId() throws Exception {
    given(siteServerApi.getClassToSubTypeForClass(anyList(), any(SimpleFilter.class)))
        .willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-next-event/bma/223")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testOBTypesForClassId() throws Exception {
    given(siteServerApi.getClassToSubTypeForClass(anyList(), any(SimpleFilter.class)))
        .willReturn(
            Optional.of(
                Arrays.asList(modelType(11, "|London|", 223), modelType(12, "Brighton", 223))));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-next-event/bma/223")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$[0].typeName", Matchers.is("Brighton")))
        .andExpect(MockMvcResultMatchers.jsonPath("$[1].typeName", Matchers.is("London")));
  }

  private VirtualNextEvent getVirtualNextEvent(String title, String classId, String typeIds) {
    entity = new VirtualNextEvent();
    entity.setId(UUID.randomUUID().toString());
    entity.setTitle(title);
    entity.setClassIds(classId);
    entity.setTypeIds(typeIds);
    entity.setBrand("bma");
    entity.setLimit(1);
    return entity;
  }

  private Type modelType(Integer id, String name, Integer classId) {
    Type type = new Type();
    type.setId(id);
    type.setName(name);
    type.setClassId(classId);
    return type;
  }
}
