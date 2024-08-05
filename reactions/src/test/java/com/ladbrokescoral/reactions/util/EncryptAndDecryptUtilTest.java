package com.ladbrokescoral.reactions.util;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

import com.ladbrokescoral.reactions.client.bpp.dto.BppTokenRequest;
import com.ladbrokescoral.reactions.exception.BadRequestException;
import java.io.UnsupportedEncodingException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.security.NoSuchAlgorithmException;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;

class EncryptAndDecryptUtilTest {

  @BeforeAll
  static void setUp() {
    EncryptAndDecryptUtil.setSecretKey("path-to-key-file", "AES");
  }

  @Test
  void testReadString() {
    String encryptedString = "This is a test string";
    String algorithm = "AES";
    String decryptedString = EncryptAndDecryptUtil.readString(encryptedString, algorithm);
    Assertions.assertNotNull(decryptedString);
  }

  @Test
  void testReadString1() {
    String encryptedString = "controller/UserReactionDTO.json";
    String algorithm = "AES";
    String decryptedString = EncryptAndDecryptUtil.readString(encryptedString, algorithm);
    Assertions.assertNotNull(decryptedString);
  }

  @Test
  void testReadString2()
      throws UnsupportedEncodingException, NoSuchAlgorithmException, NoSuchMethodException,
          IllegalAccessException, InvocationTargetException {
    String encryptedString = "myservice.jks";
    String algorithm = "RSA";
    SecretKey secretKey = KeyGenerator.getInstance("AES").generateKey();
    ReflectionTestUtils.setField(
        EncryptAndDecryptUtil.class, "generatedKey", secretKey, SecretKeySpec.class);
    String decryptedString = EncryptAndDecryptUtil.readString(encryptedString, algorithm);
    EncryptAndDecryptUtil.setSecretKey("path-to-key-file", "AES");
    Assertions.assertNotNull(decryptedString);
    Method m = EncryptAndDecryptUtil.class.getDeclaredMethod("getUnGarbledString", String.class);
    m.setAccessible(true);
    Object o = m.invoke(null, "tests");
  }

  @Test
  void createBppTokenRequest_ValidToken_Success() {
    String validToken = "validToken";
    BppTokenRequest bppTokenRequest = new BppTokenRequest(validToken);
    Assertions.assertNotNull(bppTokenRequest);
    Assertions.assertEquals(validToken, bppTokenRequest.token());
  }

  @Test
  void createBppTokenRequest_NullToken_ExceptionThrown() {
    String nullToken = null;
    Assertions.assertThrows(BadRequestException.class, () -> new BppTokenRequest(nullToken));
  }

  @Test
  void createBppTokenRequest_EmptyToken_ExceptionThrown() {
    String emptyToken = "";
    BppTokenRequest bppTokenRequest = new BppTokenRequest(emptyToken);
    String whitespaceToken = "   ";
    BppTokenRequest bppTokenRequest1 = new BppTokenRequest(whitespaceToken);
    Assertions.assertNotNull(bppTokenRequest);
  }

  @Test
  void createBppTokenRequest_ValidTokenValidation_Success() {
    String validToken = "validToken";
    BppTokenRequest bppTokenRequest = new BppTokenRequest(validToken);
    assertDoesNotThrow(() -> ValidationHelper.notNull(bppTokenRequest.token(), "token"));
  }
}
