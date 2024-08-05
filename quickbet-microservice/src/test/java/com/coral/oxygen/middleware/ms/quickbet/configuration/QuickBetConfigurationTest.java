package com.coral.oxygen.middleware.ms.quickbet.configuration;

import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.SecureRandom;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class QuickBetConfigurationTest {

  @InjectMocks private QuickBetConfiguration quickBetConfiguration;

  @Test
  void secureRandom() throws NoSuchAlgorithmException, NoSuchProviderException {
    Assertions.assertInstanceOf(SecureRandom.class, quickBetConfiguration.secureRandom());
  }
}
