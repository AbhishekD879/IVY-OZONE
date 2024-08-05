package com.ladbrokescoral.oxygen.cms.api.service;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.entity.AccountCredentials;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.entity.UserStatus;
import com.ladbrokescoral.oxygen.cms.api.exception.UserInvalidCredentialsException;
import com.ladbrokescoral.oxygen.cms.api.exception.UserInvalidUsernameException;
import com.ladbrokescoral.oxygen.cms.api.exception.UserIsLockedException;
import com.ladbrokescoral.oxygen.cms.api.exception.UserWithSuchEmailAlreadyExistException;
import com.ladbrokescoral.oxygen.cms.api.repository.UsersRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserService extends AbstractService<User> implements UserDetailsService {

  private final UsersRepository usersRepository;
  private final PasswordEncoder passwordEncoder;

  @Autowired
  public UserService(UsersRepository usersRepository, PasswordEncoder passwordEncoder) {
    super(usersRepository);
    this.usersRepository = usersRepository;
    this.passwordEncoder = passwordEncoder;
  }

  @Override
  @CacheEvict(
      cacheNames = {"users"},
      key = "#entity.id")
  public User save(final User entity) {
    verifyIfUserIsUnique(entity);
    if (entity.getPassword().isEmpty()) {
      usersRepository
          .findById(entity.getId())
          .ifPresent(user -> entity.setPassword(user.getPassword()));
    } else {
      entity.setPassword(passwordEncoder.encode(entity.getPassword()));
    }
    return usersRepository.save(entity);
  }

  @FortifyXSSValidate("return")
  @Override
  @Cacheable(value = "users", key = "#id")
  public Optional<User> findOne(String id) {
    return usersRepository
        .findById(id)
        .map(
            (User user) -> {
              user.setPassword("*****");
              return user;
            });
  }

  @CacheEvict(
      cacheNames = {"users"},
      key = "#updateEntity.id")
  @Override
  public User update(User existingEntity, User updateEntity) {
    return super.update(existingEntity, updateEntity);
  }

  @Override
  public List<User> findAll() {
    List<User> entities = usersRepository.findAll();
    entities.forEach(entity -> entity.setPassword("*****"));
    return entities;
  }

  private void verifyIfUserIsUnique(User user) {
    usersRepository
        .findByEmailIgnoreCase(user.getEmail())
        .ifPresent(
            (User existingUser) -> {
              if (user.getId() == null || !user.getId().equals(existingUser.getId())) {
                throw new UserWithSuchEmailAlreadyExistException();
              }
            });
  }

  public User verify(final AccountCredentials authentication) {

    Optional<User> maybeUser = usersRepository.findByEmailIgnoreCase(authentication.getUsername());

    if (!maybeUser.isPresent()) {
      throw new UserInvalidUsernameException();
    }

    User user = maybeUser.get();
    if (UserStatus.LOCKED == user.getStatus()) {
      throw new UserIsLockedException();
    }

    boolean isPasswordValid =
        passwordEncoder.matches(authentication.getPassword(), user.getPassword());
    if (!isPasswordValid) {
      throw new UserInvalidCredentialsException();
    }

    return maybeUser.get();
  }

  @CacheEvict(
      cacheNames = {"users"},
      key = "#id")
  @Override
  public void delete(String id) {
    usersRepository.deleteById(id);
  }

  @Override
  @Transactional
  public UserDetails loadUserByUsername(String usernameOrEmail) {
    // TODO: rework with overkill AccountCredentials
    // // Let people login with either username or email
    // User user = userRepository.findByUsernameOrEmail(usernameOrEmail, usernameOrEmail)
    return usersRepository
        .findByEmailIgnoreCase(usernameOrEmail)
        .orElseThrow(
            () ->
                new UsernameNotFoundException(
                    "User not found with username or email : " + usernameOrEmail));
  }

  // This method is used by JWTAuthenticationFilter
  @Transactional
  public UserDetails loadUserById(String id) {
    return usersRepository
        .findById(id)
        .orElseThrow(() -> new UsernameNotFoundException("User not found with id : " + id));
  }
}
