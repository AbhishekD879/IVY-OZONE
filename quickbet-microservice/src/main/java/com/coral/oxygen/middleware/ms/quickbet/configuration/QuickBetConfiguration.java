package com.coral.oxygen.middleware.ms.quickbet.configuration;

import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.SecureRandom;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class QuickBetConfiguration {
  public static final String ALGORITHM = "SHA1PRNG";
  public static final String PROVIDER = "SUN";

  @Bean
  public SecureRandom secureRandom() throws NoSuchAlgorithmException, NoSuchProviderException {
    return SecureRandom.getInstance(ALGORITHM, PROVIDER);
  }
}
