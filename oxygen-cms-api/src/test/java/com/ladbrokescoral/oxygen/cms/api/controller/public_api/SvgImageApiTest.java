package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite.INITIAL;
import static org.mockito.BDDMockito.given;
import static org.mockito.Matchers.anyString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Users;
import com.ladbrokescoral.oxygen.cms.api.dto.SvgSpriteDto;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SvgImagePublicService;
import java.util.Collections;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Users.class,
      AuthenticationService.class,
      SvgImageApi.class,
      SvgImagePublicService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class SvgImageApiTest {

  @MockBean private UserService userServiceMock;

  @MockBean private SvgImagePublicService service;

  @Autowired private MockMvc mockMvc;

  @Before
  public void setUp() {
    given(service.getSvgSprite(anyString(), anyString()))
        .willReturn(new SvgSpriteDto(INITIAL.getSpriteName(), "SVG-SPRITE"));
    given(service.getAllSvgSprites(anyString()))
        .willReturn(
            Collections.singletonList(new SvgSpriteDto(INITIAL.getSpriteName(), "SVG-SPRITE")));
  }

  @Test
  public void getSpriteTest() throws Exception {
    mockMvc.perform(get("/cms/api/bma/svg-images/sprite/additional")).andExpect(status().isOk());
  }

  @Test
  public void getAllSpritesTest() throws Exception {
    mockMvc.perform(get("/cms/api/bma/svg-images/sprite")).andExpect(status().isOk());
  }
}
