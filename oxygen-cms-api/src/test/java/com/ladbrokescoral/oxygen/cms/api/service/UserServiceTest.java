package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.AccountCredentials;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.entity.UserStatus;
import com.ladbrokescoral.oxygen.cms.api.exception.UserInvalidCredentialsException;
import com.ladbrokescoral.oxygen.cms.api.exception.UserInvalidUsernameException;
import com.ladbrokescoral.oxygen.cms.api.exception.UserIsLockedException;
import com.ladbrokescoral.oxygen.cms.api.exception.UserWithSuchEmailAlreadyExistException;
import com.ladbrokescoral.oxygen.cms.api.repository.UsersRepository;
import java.util.Optional;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.security.crypto.password.PasswordEncoder;

@RunWith(MockitoJUnitRunner.class)
public class UserServiceTest {

  @Mock private UsersRepository repository;
  @Mock private PasswordEncoder passwordEncoder;

  @InjectMocks private UserService userService;

  @Test
  public void testFindNotExistingUser() {
    when(repository.findById("invalid_id")).thenReturn(Optional.empty());
    Optional<User> user = userService.findOne("invalid_id");
    assertFalse(user.isPresent());
  }

  @Test(expected = UserInvalidUsernameException.class)
  public void testVerifyIfUsernameIsInvalid() {
    when(repository.findByEmailIgnoreCase(any())).thenReturn(Optional.empty());
    userService.verify(new AccountCredentials("username", ""));
  }

  @Test(expected = UserIsLockedException.class)
  public void testVerifyIfUserIsLocked() {
    User user = User.builder().email("email").status(UserStatus.LOCKED).build();
    when(repository.findByEmailIgnoreCase("email")).thenReturn(Optional.of(user));
    userService.verify(new AccountCredentials("email", ""));
  }

  @Test(expected = UserInvalidCredentialsException.class)
  public void testVerifyIfPasswordIsInvalid() {
    User user = User.builder().email("email").password("not_encoded_password").build();
    when(repository.findByEmailIgnoreCase("email")).thenReturn(Optional.of(user));
    userService.verify(new AccountCredentials("email", "password"));
  }

  @Test(expected = UserWithSuchEmailAlreadyExistException.class)
  public void testSaveUserIfAnyWithSuchEmailAlreadyExist() {
    when(repository.findByEmailIgnoreCase("email@email.com")).thenReturn(Optional.of(new User()));

    User user = User.builder().email("email@email.com").build();
    userService.save(user);
  }

  @Test(expected = UserWithSuchEmailAlreadyExistException.class)
  public void testUpdateUserIfAnyWithSuchEmailAlreadyExist() {
    when(repository.findByEmailIgnoreCase("email@email.com")).thenReturn(Optional.of(new User()));

    User user = User.builder().email("email@email.com").build();
    user.setId("id");
    userService.save(user);
  }

  @Test
  public void testAllowUpdateUserIfEmailWasNotChanged() {
    User user = new User();
    user.setId("id");
    user.setPassword("12345");
    user.setEmail("email@email.com");

    when(repository.findByEmailIgnoreCase("email@email.com")).thenReturn(Optional.of(user));

    userService.save(user);

    ArgumentCaptor<User> argument = ArgumentCaptor.forClass(User.class);
    verify(repository).save(argument.capture());

    assertEquals("email@email.com", argument.getValue().getEmail());
  }

  @Test
  public void testSaveUserWithNotUpdatedPassword() {
    User receivedUser = new User();
    receivedUser.setId("id");
    receivedUser.setPassword("");
    receivedUser.setEmail("email@email.com");
    User existedUser = new User();
    existedUser.setPassword("12345");

    when(repository.findById("id")).thenReturn(Optional.of(existedUser));
    when(repository.findByEmailIgnoreCase("email@email.com")).thenReturn(Optional.of(receivedUser));

    userService.save(receivedUser);

    ArgumentCaptor<User> argument = ArgumentCaptor.forClass(User.class);
    verify(repository).save(argument.capture());

    assertEquals("12345", argument.getValue().getPassword());
  }
}
