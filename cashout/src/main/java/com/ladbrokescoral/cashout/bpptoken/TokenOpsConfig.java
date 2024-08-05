package com.ladbrokescoral.cashout.bpptoken;

import com.coral.bpp.api.exception.BppUnauthorizedException;
import com.newrelic.api.agent.NewRelic;
import java.io.IOException;
import java.security.GeneralSecurityException;
import java.time.Clock;
import java.time.Duration;
import java.util.Base64;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class TokenOpsConfig {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Bean
  @ConditionalOnProperty(
      value = "token.decryption.enabled",
      matchIfMissing = true,
      havingValue = "true")
  public BppTokenOperations bppTokenOperations(
      @Value("${token.encryption.key}") byte[] bppEncryptionKey)
      throws GeneralSecurityException, IOException {
    BppTokenOperations cryptedTokenOperations =
        new CryptedTokenOperations(
            new JwtOperations(Clock.systemUTC()),
            new TinkCrypt(Base64.getDecoder().decode(bppEncryptionKey)));

    return token -> {
      try {
        return cryptedTokenOperations.parseToken(token);
      } catch (Exception e) {
        NewRelic.noticeError(e);
        ASYNC_LOGGER.warn("Failed to parse token {}", token, e);
        throw new BppUnauthorizedException(e.getMessage());
      }
    };
  }

  /** Can be used for local dev env */
  @Bean
  @ConditionalOnProperty(value = "token.decryption.enabled", havingValue = "false")
  public BppTokenOperations noopBppTokenOps() {
    return token ->
        BppToken.builder()
            .token(token)
            .timeLeftToExpire(Duration.ZERO)
            .encodedUser(User.builder().sportBookUserName(token).build())
            .build();
  }
}
