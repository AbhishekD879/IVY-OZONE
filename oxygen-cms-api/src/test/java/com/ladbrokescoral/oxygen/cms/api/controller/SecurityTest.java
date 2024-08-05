package com.ladbrokescoral.oxygen.cms.api.controller;

import static com.ladbrokescoral.oxygen.cms.api.controller.ApiConstants.CMS_API;
import static com.ladbrokescoral.oxygen.cms.api.controller.ApiConstants.PRIVATE_API;
import static org.junit.Assert.assertNotNull;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.entity.AccountCredentials;
import com.ladbrokescoral.oxygen.cms.api.entity.TokenRequest;
import com.ladbrokescoral.oxygen.cms.api.entity.TokenResponse;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.repository.UsersRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ModuleRibbonTabService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BuildYourBetPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.SpringBootTestConfiguration;
import java.util.Collections;
import java.util.Optional;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

@ActiveProfiles({"UNIT", "SECURITY"})
@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Import(SpringBootTestConfiguration.class)
@AutoConfigureMockMvc
public class SecurityTest extends BDDMockito {

  @Autowired private MockMvc mockMvc;

  @Autowired private PasswordEncoder passwordEncoder;
  @MockBean private UsersRepository usersRepository;

  @MockBean private HomeModuleServiceImpl homeModuleService;
  @MockBean private ModuleRibbonTabService moduleRibbonTabService;
  @MockBean private BuildYourBetPublicService buildYourBetPublicService;

  @Autowired private ObjectMapper objectMapper;

  private User user;

  @Before
  public void init() {

    user =
        User.builder().id("1234").email("coral").password(passwordEncoder.encode("admin")).build();

    given(usersRepository.findById("1234")).willReturn(Optional.of(user));
    given(usersRepository.findByEmailIgnoreCase("coral")).willReturn(Optional.of(user));

    given(buildYourBetPublicService.isAtLeastOneBanachEventAvailable(anyString())).willReturn(true);
  }

  @Test
  public void testAccessPrivateApiShouldThrowUnauthorizedAccessError() throws Exception {

    mockMvc.perform(get(PRIVATE_API + "/user/1234")).andExpect(status().isUnauthorized());
  }

  @Test
  public void testAccessAnyPrivateApiShouldThrowUnauthorizedAccessError() throws Exception {

    mockMvc
        .perform(get(PRIVATE_API + "/this_is_any_private_path"))
        .andExpect(status().isUnauthorized());
  }

  @Test
  public void testAccessAnyPrivateApiWithRepeatedSlashesShouldThrowUnauthorizedAccessError()
      throws Exception {

    mockMvc.perform(get("////v1////api/////user/1234")).andExpect(status().isUnauthorized());
  }

  @Test
  public void testLogin() throws Exception {
    assertNotNull(loginForToken());
  }

  @Test
  public void testGenerateNewToken() throws Exception {

    String token = loginForToken();
    TokenRequest tokenRequest = new TokenRequest(token);

    mockMvc
        .perform(
            post(PRIVATE_API + "/token")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(tokenRequest))
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + token))
        .andExpect(status().isOk())
        .andExpect(jsonPath("token").exists());
  }

  @Test
  public void testGenerateNewTokenIfRefreshTokenIsExpiredOrInvalid() throws Exception {

    TokenRequest tokenRequest = new TokenRequest(loginForToken() + "_corrupted");

    mockMvc
        .perform(
            post(PRIVATE_API + "/token")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(tokenRequest)))
        .andExpect(status().isUnprocessableEntity());
  }

  @Test
  public void testAccessPrivateApiAfterLogin() throws Exception {

    mockMvc
        .perform(
            get(PRIVATE_API + "/user/1234")
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + loginForToken()))
        .andExpect(status().isOk());
  }

  @Test
  public void testAccessPublicApiShouldAllowAccess() throws Exception {

    when(homeModuleService.findByActiveStateAndPublishToChannel(true, "bma"))
        .thenReturn(Collections.emptyList());
    when(moduleRibbonTabService.findAllByBrandAndVisible("bma"))
        .thenReturn(Collections.emptyList());

    mockMvc.perform(get(CMS_API + "/bma/modular-content")).andExpect(status().isOk());
  }

  @Test
  public void testAccessAnyPublicApiShouldAllowAccess() throws Exception {

    mockMvc.perform(get(CMS_API + "/this_is_any_public_path")).andExpect(status().isNotFound());
  }

  @Ignore
  @Test
  public void testAccessSwaggerFilesShouldBeRestrictedWithBasicAuth() throws Exception {

    mockMvc.perform(get("/swagger-ui")).andExpect(status().isUnauthorized());
    mockMvc.perform(get("/api-docs")).andExpect(status().isUnauthorized());
    mockMvc.perform(get("/index.html")).andExpect(status().isUnauthorized());
  }

  private String loginForToken() throws Exception {

    AccountCredentials credentials = new AccountCredentials("coral", "admin");

    String result =
        mockMvc
            .perform(
                post(PRIVATE_API + "/login")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(objectMapper.writeValueAsString(credentials)))
            .andExpect(status().isOk())
            .andReturn()
            .getResponse()
            .getContentAsString();

    return objectMapper.readValue(result, TokenResponse.class).getToken();
  }
}
