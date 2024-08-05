package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.TokenResponse;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.MalformedJwtException;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.SignatureException;
import io.jsonwebtoken.UnsupportedJwtException;
import java.time.Instant;
import java.util.Date;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Service;

@Slf4j
@Setter
@Service
@ConfigurationProperties(prefix = "jwt")
public class TokenAuthenticationService implements AuthenticationService {

  private String secret;
  private long tokenExpiration;
  private long refreshTokenExpiration;

  public String generateToken(String subject) {
    return this.generateToken(subject, tokenExpiration);
  }

  @Override
  public TokenResponse createToken(String subject) {
    return new TokenResponse(
        this.generateToken(subject, tokenExpiration),
        this.generateToken(subject, refreshTokenExpiration));
  }

  @Override
  public TokenResponse refreshToken(String token) {
    return this.createToken(this.retrieveSubject(token));
  }

  private String generateToken(String subject, long expiration) {

    Instant now = Instant.now();
    return Jwts.builder()
        .setSubject(subject)
        .setIssuedAt(Date.from(now))
        .setExpiration(Date.from(now.plusSeconds(expiration)))
        .signWith(SignatureAlgorithm.HS512, secret)
        .compact();
  }

  public String retrieveSubject(String token) {
    return Jwts.parser().setSigningKey(secret).parseClaimsJws(token).getBody().getSubject();
  }

  public boolean validateToken(String authToken) {
    try {
      Jwts.parser().setSigningKey(secret).parseClaimsJws(authToken);
      return true;
    } catch (SignatureException ex) {
      log.error("Invalid JWT signature");
    } catch (MalformedJwtException ex) {
      log.error("Invalid JWT token");
    } catch (ExpiredJwtException ex) {
      log.error("Expired JWT token");
    } catch (UnsupportedJwtException ex) {
      log.error("Unsupported JWT token");
    } catch (IllegalArgumentException ex) {
      log.error("JWT claims string is empty.");
    }
    return false;
  }
}
