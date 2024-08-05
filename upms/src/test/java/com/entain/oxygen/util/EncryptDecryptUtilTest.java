package com.entain.oxygen.util;

import java.lang.reflect.Constructor;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class EncryptDecryptUtilTest {

  @Test
  void testForFileNotFoundExceptionInPasswordKeyFile() {
    String file = "profil.pem";
    EncryptAndDecryptUtil.setSecretKey(file, "DES");
    Assertions.assertDoesNotThrow(() -> EncryptAndDecryptUtil.setSecretKey(file, "DES"));
  }

  @Test
  void testForIOExceptionInPasswordFile() {
    EncryptAndDecryptUtil.setSecretKey("profilekey.pem", "DES");
    String file = "app/oxygen.bin";
    String decodedPassword = EncryptAndDecryptUtil.readString(file, "DES");
    Assertions.assertTrue(decodedPassword.isEmpty());
  }

  @Test
  void testForPrivateConstructorEncryptAndDecryptUtil() {
    IllegalAccessException thrown =
        Assertions.assertThrows(
            IllegalAccessException.class,
            () -> {
              Constructor declaredConstructor =
                  EncryptAndDecryptUtil.class.getDeclaredConstructor();
              // throws Exception while trying create the new instance with private constructor
              declaredConstructor.newInstance();
            });
    Assertions.assertNotNull(thrown.getMessage());
  }
}
