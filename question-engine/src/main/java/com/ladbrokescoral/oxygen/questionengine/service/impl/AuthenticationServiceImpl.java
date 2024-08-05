package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.exception.InvalidBppTokenException;
import com.ladbrokescoral.oxygen.questionengine.exception.UnauthorizedException;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.BppTokenRequest;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.UserData;
import com.ladbrokescoral.oxygen.questionengine.service.AuthenticationService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bpp.BppService;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;

@Service
@RequiredArgsConstructor
public class AuthenticationServiceImpl implements AuthenticationService {
  private final BppService bppService;
  private final HttpServletRequest request;

  @Override
  public void verifyUser(String username) {
    String tokenHeader = request.getHeader(BppTokenRequest.TOKEN_PROPERTY_NAME);
    if (StringUtils.isEmpty(tokenHeader)) {
      throw new UnauthorizedException(String.format("User '%s' is trying to execute request without token", username));
    }

    UserData userData = bppService.findUserData(new BppTokenRequest().setToken(tokenHeader));

    if (userData == null) {
      throw new InvalidBppTokenException(String.format("Authentication failed. No UserData for user: %s", username));
    } else if (!userData.getUsername().equals(username)) {
      throw new InvalidBppTokenException(
          String.format("Authentication failed. Username does not match. Passed: '%s', Actual: '%s'", username,
              userData.getUsername()));
    }

  }
}
