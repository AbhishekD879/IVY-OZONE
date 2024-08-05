package com.ladbrokescoral.reactions.util;

import java.io.IOException;
import java.io.InputStream;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import lombok.experimental.UtilityClass;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.ArrayUtils;
import org.springframework.core.io.ClassPathResource;

/**
 * @author PBalarangakumar 12-09-2023
 */
@UtilityClass
@Slf4j
@SuppressWarnings("java:S2674")
public class EncryptAndDecryptUtil {

  private static final int CONST = 2;

  private static SecretKeySpec generatedKey;

  public static void setSecretKey(String passwordKeyFile, String algorithm) {
    try {
      InputStream fis = new ClassPathResource(passwordKeyFile).getInputStream();
      byte[] bytes = new byte[fis.available()];
      fis.read(bytes);
      EncryptAndDecryptUtil.generatedKey = new SecretKeySpec(bytes, algorithm);
    } catch (Exception fe) {
      log.error(fe.getMessage());
    }
  }

  public static String readString(final String jksPasswordFile, String algorithm) {

    byte[] bytes1 = new byte[0];
    try {
      InputStream fis = new ClassPathResource(jksPasswordFile).getInputStream();
      bytes1 = new byte[fis.available()];
      fis.read(bytes1);
    } catch (IOException fe) {
      log.error(fe.getMessage());
    }
    return getUnGarbledString(new String(getDecryptedBytes(bytes1, algorithm)));
  }

  private static byte[] getDecryptedBytes(final byte[] bArr, String algorithm) {

    try {
      final Cipher desCipher = Cipher.getInstance(algorithm);
      desCipher.init(CONST, EncryptAndDecryptUtil.generatedKey);
      return desCipher.doFinal(bArr);
    } catch (Exception e) {
      log.error(e.getMessage());
    }
    return ArrayUtils.EMPTY_BYTE_ARRAY;
  }

  private static String getUnGarbledString(final String str) {
    final char[] chars = str.toCharArray();
    for (int size = chars.length, i = 0; i < size; ++i) {
      if (i % CONST == 0) {
        final char[] array = chars;
        final int n = i;
        array[n] -= (char) fib(i / CONST);
      } else {
        final char[] array2 = chars;
        final int n2 = i;
        array2[n2] += (char) size;
      }
    }
    return new String(chars);
  }

  private static int fib(final int n) {
    if (n <= 1) {
      return n;
    }
    return fib(n - 1) + fib(n - CONST);
  }
}
