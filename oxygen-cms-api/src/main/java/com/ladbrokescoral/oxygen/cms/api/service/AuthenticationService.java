package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.TokenResponse;

public interface AuthenticationService {

  TokenResponse createToken(String subject);

  TokenResponse refreshToken(String token);

  String retrieveSubject(String token);

  boolean validateToken(String token);
}
