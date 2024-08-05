package com.entain.oxygen.promosandbox.utils;

import java.io.InputStream;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ClassPathResource;

@Slf4j
@SuppressWarnings("java:S2674")
public class EncryptAndDecryptUtil {

  private EncryptAndDecryptUtil() {}

  private static final Integer TWO = 2;

  private static SecretKeySpec generatedKey;

  public static void setSecretKey(String passwordKeyFile, String algorithm) {
    try (InputStream fis = new ClassPathResource(passwordKeyFile).getInputStream()) {
      byte[] bytes = new byte[fis.available()];
      fis.read(bytes);
      EncryptAndDecryptUtil.generatedKey = new SecretKeySpec(bytes, algorithm);
    } catch (Exception ex) {
      log.error("Error while setting secret key : {} ", ex.getMessage());
    }
  }

  public static String readString(final String jksPasswordFile, String algorithm) {
    byte[] bytes1 = new byte[0];
    try (InputStream fis = new ClassPathResource(jksPasswordFile).getInputStream()) {
      bytes1 = new byte[fis.available()];
      fis.read(bytes1);
    } catch (Exception ex) {
      log.error("Error while readString() method call : {} ", ex.getMessage());
    }
    return getUnGarbledString(new String(getDecryptedBytes(bytes1, algorithm)));
  }

  private static byte[] getDecryptedBytes(final byte[] bArr, String algorithm) {
    try {
      final Cipher desCipher = Cipher.getInstance(algorithm);
      desCipher.init(TWO, EncryptAndDecryptUtil.generatedKey);
      return desCipher.doFinal(bArr);
    } catch (Exception ex) {
      log.error("Error while getDecryptedBytes() method call : {} ", ex.getMessage());
    }
    return new byte[0];
  }

  private static String getUnGarbledString(final String str) {
    final char[] chars = str.toCharArray();
    for (int size = chars.length, i = 0; i < size; ++i) {
      if (i % TWO == 0) {
        final char[] array = chars;
        final int n = i;
        array[n] -= (char) fib(i / TWO);
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
    return fib(n - 1) + fib(n - TWO);
  }
}
