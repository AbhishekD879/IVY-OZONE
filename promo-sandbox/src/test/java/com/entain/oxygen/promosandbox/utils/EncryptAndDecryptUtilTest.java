package com.entain.oxygen.promosandbox.utils;

import static org.junit.jupiter.api.Assertions.*;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import org.junit.jupiter.api.*;
import org.wildfly.common.Assert;

public class EncryptAndDecryptUtilTest {

  @BeforeAll
  public static void setup() {
    EncryptAndDecryptUtil.setSecretKey("path/value", "ABC");
  }

  @Test
  void testReadStringWhenFileIsEmpyty() {
    String passwordKeyFile = "empty-file";
    String algorithm = "empty";
    EncryptAndDecryptUtil.setSecretKey(passwordKeyFile, algorithm);
    byte[] encryptedBytes = new byte[0];
    String decryptedString =
        EncryptAndDecryptUtil.readString(new String(encryptedBytes), algorithm);
    assertEquals("", decryptedString);
  }

  @Test
  void testForFileNotFoundExceptionInPasswordFile() {
    EncryptAndDecryptUtil.setSecretKey("profilekey.pem", "DES");
    String passwordFile = "app/oxygen.bin";
    String decodedPassword = EncryptAndDecryptUtil.readString(passwordFile, "DES");
    Assert.assertTrue(decodedPassword.isEmpty());
  }

  @Test
  void testGetUnGarbledString() throws Exception {
    Method getUnGarbledString =
        EncryptAndDecryptUtil.class.getDeclaredMethod("getUnGarbledString", String.class);
    getUnGarbledString.setAccessible(true);

    String garbledString = "VALUE-STRING";
    try {
      String result = (String) getUnGarbledString.invoke(null, garbledString);
    } catch (InvocationTargetException ex) {
      fail("Exception occurred : " + ex.getCause().getMessage());
    }
  }
}
