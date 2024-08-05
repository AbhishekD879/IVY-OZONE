package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.hamcrest.Matchers.is;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Users;
import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.BankingMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BankingMenuPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StaticBlockPublicService;
import java.util.Arrays;
import java.util.Collections;
import org.hamcrest.core.IsNull;
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
import org.springframework.test.web.servlet.result.MockMvcResultHandlers;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Users.class,
      AuthenticationService.class,
      BankingMenuApi.class,
      BankingMenuPublicService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class BankingMenuApiTest {

  @MockBean private UserService userServiceMock;
  @MockBean StaticBlockPublicService staticBlockService;
  @MockBean BankingMenuService bankingMenuService;
  @Autowired BankingMenuPublicService bankingMenuPublicService;
  @Autowired private MockMvc mockMvc;

  @Before
  public void init() {
    BankingMenu bankingMenu = new BankingMenu();
    bankingMenu.setLinkTitle("testTitle");
    bankingMenu.setType("test");
    bankingMenu.setTargetUri("bbbb");
    bankingMenu.setMenuItemView("itemView");
    bankingMenu.setUriMedium("mediumuri");
    given(bankingMenuService.findAllByBrand("bma")).willReturn(Arrays.asList(bankingMenu));
  }

  @Test
  public void testGetAllByBrand() throws Exception {
    this.mockMvc
        .perform(get("/cms/api/bma/banking-menu"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.[0].buttonClass", is("bbbb")))
        .andExpect(
            jsonPath(
                "$.[0].uriLarge", is("/images/uploads/right_menu/default/default-156x156.png")))
        .andExpect(jsonPath("$.[0].linkTitle", is("testTitle")))
        .andDo(MockMvcResultHandlers.print());
  }

  @Test
  public void testGetAllByBrandTypeLink() throws Exception {
    BankingMenu bankingMenu = new BankingMenu();
    bankingMenu.setLinkTitle("testTitle");
    bankingMenu.setType("link");
    bankingMenu.setTargetUri("bbbb");
    given(bankingMenuService.findAllByBrand("bma")).willReturn(Arrays.asList(bankingMenu));
    this.mockMvc
        .perform(get("/cms/api/bma/banking-menu"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.[0].buttonClass").value(IsNull.nullValue()))
        .andExpect(jsonPath("$.[0].linkTitle", is("testTitle")))
        .andDo(MockMvcResultHandlers.print());
  }

  @Test
  public void testGetAllByBrandEmpty() throws Exception {
    given(bankingMenuService.findAllByBrand("bma")).willReturn(Collections.emptyList());
    this.mockMvc
        .perform(get("/cms/api/bma/banking-menu").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is(204));
  }
}
