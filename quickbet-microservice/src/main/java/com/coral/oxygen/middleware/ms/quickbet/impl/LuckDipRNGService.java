package com.coral.oxygen.middleware.ms.quickbet.impl;

import java.security.SecureRandom;
import org.springframework.stereotype.Service;

@Service
public class LuckDipRNGService {

  private final SecureRandom secureRandom;

  public LuckDipRNGService(SecureRandom secureRandom) {
    this.secureRandom = secureRandom;
  }

  public int getRandomNumber(int size) {
    return secureRandom.nextInt(size);
  }
}
