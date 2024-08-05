package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.RightMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.RightMenuExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.RightMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageEntityService;
import com.ladbrokescoral.oxygen.cms.api.service.RightMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgEntityService;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({RightMenus.class, RightMenuService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBean({
  RightMenuExtendedRepository.class,
  ImageEntityService.class,
  SvgEntityService.class,
  ImagePath.class
})
public class RightMenusTest extends AbstractControllerTest {

  private static final String subHeaderName = "subHeader";
  private static final String subHeaderExpect = "subHeaderExpect";

  @MockBean private RightMenuRepository repository;

  private RightMenu entity = validMenu();

  @Before
  public void init() {
    given(repository.findAll()).willReturn(Arrays.asList(entity));
    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(RightMenu.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testFindAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/right-menu")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$[0].%s", subHeaderName).value(subHeaderExpect));
  }

  @Test
  public void testFindOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/right-menu/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.%s", subHeaderName).value(subHeaderExpect));
  }

  @Test
  public void testCreate() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/right-menu")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.%s", subHeaderName).value(subHeaderExpect));
  }

  private RightMenu validMenu() {
    RightMenu dto = new RightMenu();
    dto.setDisabled(false);
    dto.setBrand("dma");
    dto.setLinkTitle("linkTitle");
    dto.setSubHeader(subHeaderExpect);
    return dto;
  }
}
