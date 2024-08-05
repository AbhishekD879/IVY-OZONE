package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.AccountCredentials;
import com.ladbrokescoral.oxygen.cms.api.entity.TokenRequest;
import com.ladbrokescoral.oxygen.cms.api.entity.TokenResponse;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.InvalidJwtException;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Authentication implements Abstract {

  private final UserService userService;
  private final AuthenticationService authenticationService;

  @Autowired
  public Authentication(UserService userService, AuthenticationService authenticationService) {
    this.userService = userService;
    this.authenticationService = authenticationService;
  }

  @PostMapping(value = "login")
  public TokenResponse login(@RequestBody AccountCredentials credentials) {
    User user = userService.verify(credentials);
    return authenticationService.createToken(user.getId());
  }

  @PostMapping(value = "token")
  public TokenResponse refreshToken(@RequestBody TokenRequest body) {

    String token = body.getRefreshToken();

    if (!authenticationService.validateToken(token)) {
      throw new InvalidJwtException();
    }

    return authenticationService.refreshToken(token);
  }
}
