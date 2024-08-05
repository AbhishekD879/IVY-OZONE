package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.mockito.Matchers.any;
import static org.mockito.Matchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.StaticTextOtf;
import com.ladbrokescoral.oxygen.cms.api.repository.StaticTextOtfRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.StaticTextOtfService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.stubbing.Answer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Users.class,
      AuthenticationService.class,
      StaticTextOtfs.class,
      StaticTextOtfService.class,
      BrandService.class,
      StaticTextOtfRepository.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class StaticTextOtfServiceTest {

  @MockBean StaticTextOtfRepository repository;

  @MockBean private BrandService brandService;

  @MockBean private UserService userServiceMock;

  @Autowired private MockMvc mockMvc;

  @Before
  public void init() {
    List<StaticTextOtf> staticTextOtfs = new ArrayList<>();
    given(brandService.findByBrandCode(any())).willReturn(Optional.empty());
    given(brandService.findByBrandCode(eq("bma"))).willReturn(Optional.of(new Brand()));
    given(repository.save(any(StaticTextOtf.class))).will(new StaticTextOtfAnswer(staticTextOtfs));
    given(repository.findById(any())).willReturn(Optional.of(createStaticTextOtf()));
    given(repository.existsByPageNameAndEnabledIsTrueAndIdNotAndBrandIs(any(), any(), any()))
        .willReturn(false);
  }

  @Test
  public void getStaticTextOtfs() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/static-text-otf/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testCreateStaticTextOtf() throws Exception {
    StaticTextOtf dto = createStaticTextOtf();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/static-text-otf")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testCreateStaticTextOtActiveAlreadyExists() throws Exception {
    StaticTextOtf dto = createStaticTextOtf();
    dto.setEnabled(true);

    when(repository.existsByPageNameAndEnabledIsTrueAndIdNotAndBrandIs(
            dto.getPageName(), dto.getId(), dto.getBrand()))
        .thenReturn(true);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/static-text-otf")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateStaticTextOtfError() throws Exception {
    StaticTextOtf dto = new StaticTextOtf();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/static-text-otf")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void testUpdateStaticTextOtf() throws Exception {
    StaticTextOtf dto = createStaticTextOtf();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/static-text-otf/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().isOk());
  }

  @Test
  public void testUpdateActiveStaticTextOtf() throws Exception {
    StaticTextOtf dto = createStaticTextOtf();
    dto.setEnabled(true);

    when(repository.existsByPageNameAndEnabledIsTrueAndIdNotAndBrandIs(
            dto.getPageName(), dto.getId(), dto.getBrand()))
        .thenReturn(false);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/static-text-otf/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetStaticTextOtfs() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/static-text-otf")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/static-text-otf/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/static-text-otf/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetByIdError() throws Exception {
    given(repository.findById(anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/static-text-otf/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testDelete() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/static-text-otf/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void testOrder() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .id(UUID.randomUUID().toString())
            .order(Collections.singletonList("-1"))
            .build();

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/static-text-otf/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().isOk());
  }

  private final class StaticTextOtfAnswer implements Answer<StaticTextOtf> {
    private List<StaticTextOtf> list;

    StaticTextOtfAnswer(List<StaticTextOtf> list) {
      this.list = list;
    }

    @Override
    public StaticTextOtf answer(InvocationOnMock invocation) throws Throwable {
      StaticTextOtf staticTextOtf = (StaticTextOtf) invocation.getArguments()[0];
      list.add(staticTextOtf);
      return staticTextOtf;
    }
  }

  public StaticTextOtf createStaticTextOtf() {
    StaticTextOtf staticText = new StaticTextOtf();
    staticText.setBrand("bma");
    staticText.setPageName("testStaticTextOtfId");
    staticText.setPageText1("PageText1");
    staticText.setCtaText2("CtaText2");
    staticText.setEnabled(false);
    return staticText;
  }
}
