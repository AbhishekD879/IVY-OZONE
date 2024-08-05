package com.ladbrokescoral.oxygen.questionengine.service;

import com.ladbrokescoral.oxygen.questionengine.exception.InvalidBppTokenException;

public interface AuthenticationService {

  /**
   * Verifies user authenticity. Throws exception if user's bpp token is either invalid or expired.
   *
   * @throws InvalidBppTokenException if user's bpp toke is either invalid or expired
   */
  void verifyUser(String username);
}
