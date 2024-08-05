package com.coral.oxygen.middleware.ms.quickbet.impl;

import java.security.SecureRandom;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class LuckDipRNGServiceTest extends BDDMockito {

  @Mock private SecureRandom secureRandom;
  @InjectMocks private LuckDipRNGService luckDipRNGService;

  @BeforeEach
  public void setUp() {}

  @Test
  void processLuckyDipPlaceBetTestHappyPath() {
    when(secureRandom.nextInt(anyInt())).thenReturn(1);
    int resp = luckDipRNGService.getRandomNumber(5);
    Assertions.assertEquals(1, resp);
  }
}
