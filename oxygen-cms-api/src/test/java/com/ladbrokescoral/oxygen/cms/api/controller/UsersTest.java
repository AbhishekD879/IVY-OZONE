package com.ladbrokescoral.oxygen.cms.api.controller;

import static com.ladbrokescoral.oxygen.cms.api.controller.ApiConstants.PRIVATE_API;
import static org.hamcrest.Matchers.is;
import static org.mockito.AdditionalAnswers.returnsFirstArg;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Users;
import com.ladbrokescoral.oxygen.cms.api.entity.Name;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.entity.UserStatus;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import java.util.Optional;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

@RunWith(SpringRunner.class)
@WebMvcTest({Users.class, AuthenticationService.class})
@AutoConfigureMockMvc(addFilters = false)
public class UsersTest {
  @Autowired private MockMvc mockMvc;
  @MockBean private UserService userServiceMock;

  @Test
  public void testFindOne() throws Exception {
    String userId = "123";

    User user = createTestUser(userId);

    given(userServiceMock.findOne("123")).willReturn(Optional.of(user));

    mockMvc
        .perform(get(PRIVATE_API + "/user/{id}", userId))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.id", is("123")))
        .andExpect(jsonPath("$.name.first", is("F")))
        .andExpect(jsonPath("$.name.last", is("L")))
        .andExpect(jsonPath("$.status", is("ACTIVE")));
  }

  @Test
  public void testCreateUser() throws Exception {
    User expectedUser =
        User.builder()
            .email("test@test.com")
            .admin(false)
            .status(UserStatus.ACTIVE)
            .password("12345")
            .name(new Name("F", "L"))
            .build();

    given(userServiceMock.save(any(User.class))).willReturn(createTestUser("123"));
    when(userServiceMock.prepareModelBeforeSave(any())).then(returnsFirstArg());

    mockMvc
        .perform(
            post(PRIVATE_API + "/user")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.readFromFileAsBytes("controller/private_api/user.json")))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.new").doesNotExist());

    verify(userServiceMock).save(expectedUser);
  }

  @Test
  public void testUpdateExisting() throws Exception {
    User user =
        User.builder()
            .name(new Name("F", "L"))
            .admin(false)
            .password("12345")
            .email("some@test.com")
            .status(UserStatus.LOCKED)
            .build();
    user.setId("123");

    given(userServiceMock.findOne("123")).willReturn(Optional.of(user));

    User userBeforeSave =
        TestUtil.deserializeWithJackson("controller/private_api/user.json", User.class);
    given(userServiceMock.update(any(), any())).willReturn(userBeforeSave);

    mockMvc
        .perform(
            put(PRIVATE_API + "/user/{id}", "123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.readFromFileAsBytes("controller/private_api/user.json")))
        .andExpect(status().is2xxSuccessful());

    verify(userServiceMock)
        .update(
            any(),
            argThat(
                userArg ->
                    "123".equals(userArg.getId())
                        && !userArg.isAdmin()
                        && "test@test.com".equals(userArg.getEmail())
                        && new Name("F", "L").equals(userArg.getName())
                        && "12345".equals(userArg.getPassword())
                        && userArg.getStatus() == UserStatus.ACTIVE));
  }

  @Test
  public void testUpdateNonExisting() throws Exception {
    given(userServiceMock.findOne("123")).willReturn(Optional.empty());

    mockMvc
        .perform(
            put(PRIVATE_API + "/user/{id}", "123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.readFromFileAsBytes("controller/private_api/user.json")))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testCreateByUserNameIsFetched() throws Exception {
    given(userServiceMock.findOne("54f72facff63280a240aae2e"))
        .willReturn(Optional.of(User.builder().email("creator@test.com").build()));

    given(userServiceMock.findOne("55c9af744e6af9928394f8ac"))
        .willReturn(Optional.of(User.builder().email("updater@test.com").build()));

    User user = User.builder().email("test@test.com").build();
    user.setCreatedBy("54f72facff63280a240aae2e");
    user.setUpdatedBy("55c9af744e6af9928394f8ac");

    given(userServiceMock.findOne("123")).willReturn(Optional.of(user));

    mockMvc
        .perform(get(PRIVATE_API + "/user/{id}", "123"))
        .andExpect(jsonPath("$.createdByUserName", is("creator@test.com")))
        .andExpect(jsonPath("$.updatedByUserName", is("updater@test.com")));
  }

  private User createTestUser(String userId) {
    Name name = new Name();
    name.setFirst("F");
    name.setLast("L");
    User user = User.builder().name(name).status(UserStatus.ACTIVE).build();
    user.setId(userId);
    return user;
  }
}
