package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.GameMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.TargetWindow;
import com.ladbrokescoral.oxygen.cms.api.repository.GameMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.GameMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgEntityService;
import java.util.Collections;
import java.util.Optional;
import java.util.UUID;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({GameMenus.class, GameMenuService.class})
@AutoConfigureMockMvc(addFilters = false)
public class GameMenusTest extends AbstractControllerTest {

  @MockBean private ImageService imageService;
  @MockBean private SvgEntityService<GameMenu> svgEntityService;
  @MockBean private GameMenuRepository repository;
  @MockBean private BrandService brandService;

  private GameMenu entity;
  private MockMultipartFile file;
  private Filename pngFilename = new Filename();

  private static GameMenu createValidQuickLink() {

    GameMenu entity = new GameMenu();
    entity.setBrand("bma");
    entity.setTitle("test title1 ; : # @ & - + * ( ) ! ? ' $");
    entity.setUrl("http://test.com");
    entity.setTarget(TargetWindow.CURRENT);
    return entity;
  }

  @Before
  public void init() {

    entity = createValidQuickLink();

    pngFilename.setFilename("file");
    pngFilename.setOriginalname("file.png");
    pngFilename.setPath("path");
    pngFilename.setFiletype("image/png");
    pngFilename.setFullPath("fullpath");

    entity.setPngFilename(pngFilename);

    file =
        new MockMultipartFile(
            pngFilename.getFilename(),
            pngFilename.getOriginalname(),
            pngFilename.getFiletype(),
            new byte[] {});

    given(brandService.findByBrandCode(anyString())).willReturn(Optional.of(new Brand()));
    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(GameMenu.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testCreateGameMenuError() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateGameMenu() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/game-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateGameMenu() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/game-menu/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAll() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/game-menu").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/game-menu/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/game-menu/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneError() throws Exception {

    given(repository.findById(anyString())).willReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/game-menu/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testDelete() throws Exception {

    entity.setPngFilename(new Filename());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/game-menu/1")
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
            MockMvcRequestBuilders.post("/v1/api/game-menu/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateGameMenuBrandSecondscreen() throws Exception {

    entity.setBrand("secondscreen");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/game-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @Ignore("`title` don't have restrictions")
  public void testInvalidTitle() throws Exception {

    entity.setTitle("test title1 %");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/game-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testInvalidURL() throws Exception {

    entity.setUrl("invalid");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/game-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testPutInvalidURL() throws Exception {

    entity.setUrl("invalid");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/game-menu/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  @Ignore("`title` don't have restrictions")
  public void testInvalidTitleAndSymbol() throws Exception {

    entity.setTitle("test title1 & test");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/game-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadSvg() throws Exception {

    when(svgEntityService.attachSvgImage(
            any(GameMenu.class), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(entity));

    mockMvc.perform(multipart("/v1/api/game-menu/1/image").file(file)).andExpect(status().isOk());
  }

  @Test
  public void testInvalidIdUploadSvg() throws Exception {

    when(svgEntityService.attachSvgImage(
            any(GameMenu.class), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.empty());

    mockMvc
        .perform(multipart("/v1/api/game-menu/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveInvalidIdSvg() throws Exception {

    mockMvc.perform(delete("/v1/api/game-menu/1/image")).andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveInvalidImageSvg() throws Exception {

    when(svgEntityService.removeSvgImage(any(GameMenu.class))).thenReturn(Optional.empty());

    mockMvc.perform(delete("/v1/api/game-menu/1/image")).andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveSvg() throws Exception {

    when(svgEntityService.removeSvgImage(any(GameMenu.class))).thenReturn(Optional.of(entity));

    mockMvc.perform(delete("/v1/api/game-menu/1/image")).andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUploadPng() throws Exception {

    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(pngFilename));

    mockMvc
        .perform(multipart("/v1/api/game-menu/1/image").file(file).param("fileType", "image"))
        .andExpect(status().isOk());
  }

  @Test
  public void testInvalidIdUploadPng() throws Exception {

    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.empty());

    mockMvc
        .perform(multipart("/v1/api/game-menu/1/image").file(file).param("fileType", "image"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveInvalidIdPng() throws Exception {

    mockMvc
        .perform(delete("/v1/api/game-menu/1/image").param("fileType", "image"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveInvalidImagePng() throws Exception {

    when(imageService.removeImage(any(), any())).thenReturn(Boolean.FALSE);

    mockMvc
        .perform(delete("/v1/api/game-menu/1/image").param("fileType", "image"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemovePng() throws Exception {

    when(imageService.removeImage(anyString(), anyString())).thenReturn(Boolean.TRUE);

    mockMvc
        .perform(delete("/v1/api/game-menu/1/image").param("fileType", "image"))
        .andExpect(status().is2xxSuccessful());
  }
}
