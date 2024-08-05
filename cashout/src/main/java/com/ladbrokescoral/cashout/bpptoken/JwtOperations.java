package com.ladbrokescoral.cashout.bpptoken;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.util.Date;

// FIXME copy-past from bpp - to be moved to separate library for token management
// Library will be created in scope of BMA-54770
@Deprecated
public class JwtOperations implements BppTokenOperations {

  private static final String OXI_API_TOKEN = "oxiApiToken";
  private static final String SPORT_BOOK_USER_NAME = "sportBookUserName";
  private static final String CUSTOMER_REF = "customerRef";
  private static final String CURRENCY = "currency";
  private Algorithm algorithm;
  private Clock clock;

  public JwtOperations(Clock clock) {
    this.algorithm = Algorithm.none();
    this.clock = clock;
  }

  @Override
  public BppToken parseToken(String token) {
    DecodedJWT decodedJWT = this.parseAndVerifyPayload(token);
    User encodedUser = this.extractUserFromPayload(decodedJWT);
    return BppToken.builder()
        .token(token)
        .encodedUser(encodedUser)
        .timeLeftToExpire(calculateTimeLeftToExpire(decodedJWT.getExpiresAt()))
        .build();
  }

  private Duration calculateTimeLeftToExpire(Date expiresAt) {
    return Duration.between(Instant.now(clock), expiresAt.toInstant());
  }

  private User extractUserFromPayload(DecodedJWT jwtPayload) {
    User user = new User(jwtPayload.getClaim(SPORT_BOOK_USER_NAME).asString());
    user.setOxiApiToken(jwtPayload.getClaim(OXI_API_TOKEN).asString());
    user.setCustomerRef(jwtPayload.getClaim(CUSTOMER_REF).asString());
    user.setCurrency(jwtPayload.getClaim(CURRENCY).asString());
    return user;
  }

  private DecodedJWT parseAndVerifyPayload(String jwt) {
    return JWT.require(algorithm).build().verify(jwt);
  }
}
