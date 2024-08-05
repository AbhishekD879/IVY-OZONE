package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.BankingMenuExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.BankingMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BankingMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageEntityService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgEntityService;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.util.Collections;
import java.util.Optional;
import java.util.UUID;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({BankingMenus.class, BankingMenuService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBean({
  BankingMenuExtendedRepository.class,
  ImagePath.class,
  SvgEntityService.class,
  BrandService.class
})
public class BankingMenusTest extends AbstractControllerTest {

  @MockBean private BankingMenuRepository repository;
  @MockBean private ImageEntityService<BankingMenu> imageEntityService;

  private BankingMenu entity;
  private MockMultipartFile file;

  @Before
  public void init() {

    entity = new BankingMenu();

    entity.setBrand("bma");
    entity.setLinkTitle("title");

    file = new MockMultipartFile("file", "android.png", "image/png", "file".getBytes());

    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(BankingMenu.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testCreateBankingMenuError() throws Exception {

    BankingMenu entity = new BankingMenu();

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/banking-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateBankingMenu() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/banking-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateBankingMenu() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/banking-menu/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/banking-menu")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/banking-menu/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/banking-menu/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneError() throws Exception {
    given(repository.findById(anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/banking-menu/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testDelete() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/banking-menu/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
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
            MockMvcRequestBuilders.post("/v1/api/banking-menu/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateBankingMenuSecondScreenBrand() throws Exception {

    entity.setBrand("secondscreen");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/banking-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testInvalidTitle() throws Exception {

    entity.setLinkTitle("");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/banking-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadSvg() throws Exception {

    given(imageEntityService.attachAllSizesImage(any(), any(), any()))
        .willReturn(Optional.of(entity));

    mockMvc
        .perform(multipart("/v1/api/banking-menu/1/image").file(file))
        .andExpect(status().isOk());
  }

  @Test
  public void testInvalidIdUploadSvg() throws Exception {
    mockMvc
        .perform(multipart("/v1/api/banking-menu/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveInvalidIdSvg() throws Exception {
    mockMvc.perform(delete("/v1/api/banking-menu/1/image")).andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveInvalidImageSvg() throws Exception {

    when(imageEntityService.removeAllSizesImage(entity)).thenReturn(Optional.empty());

    mockMvc.perform(delete("/v1/api/banking-menu/1/image")).andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveSvg() throws Exception {

    when(imageEntityService.removeAllSizesImage(entity)).thenReturn(Optional.of(entity));

    mockMvc.perform(delete("/v1/api/banking-menu/1/image")).andExpect(status().is2xxSuccessful());
  }
}
