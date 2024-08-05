package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.BDDMockito.given;
import static org.mockito.Matchers.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Users;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.GameMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StaticBlockPublicService;
import java.util.Arrays;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
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
    value = {Users.class, AuthenticationService.class, GameMenuApi.class, GameMenuService.class})
@AutoConfigureMockMvc(addFilters = false)
public class GameMenuApiTest {

  @MockBean private ImageService imageService;
  @MockBean private GameMenuRepository repository;
  @MockBean private SvgEntityService<GameMenu> entityService;
  @MockBean private UserService userServiceMock;
  @MockBean StaticBlockPublicService staticBlockService;
  @Autowired private MockMvc mockMvc;

  @Before
  public void init() {
    GameMenu gameMenu = new GameMenu();
    gameMenu.setSortOrder(5555.0);
    gameMenu.setTitle("test title");
    gameMenu.setSvg("test.svg");
    gameMenu.setUrl("http://test.com");
    Filename pngFilename = new Filename();
    pngFilename.setFilename("testfile.png");
    gameMenu.setPngFilename(pngFilename);
    given(repository.findByBrand(anyString(), any())).willReturn(Arrays.asList(gameMenu));
  }

  @Test
  public void testGetAllByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/game-menu")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("5555")))
        .andExpect(content().string(Matchers.containsString("http://test.com")))
        .andExpect(content().string(Matchers.containsString("test.svg")))
        .andExpect(content().string(Matchers.containsString("testfile.png")))
        .andExpect(content().string(Matchers.containsString("test title")));
  }
}
