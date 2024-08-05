package com.ladbrokescoral.cashout.bpptoken;

import com.google.crypto.tink.Aead;
import com.google.crypto.tink.BinaryKeysetReader;
import com.google.crypto.tink.CleartextKeysetHandle;
import com.google.crypto.tink.KeysetHandle;
import com.google.crypto.tink.aead.AeadConfig;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.util.Base64;
import java.util.Objects;
import lombok.SneakyThrows;

public class TinkCrypt implements CryptOperations {

  private final KeysetHandle keysetHandle;
  private final Aead primitive;

  public TinkCrypt(byte[] secret) throws GeneralSecurityException, IOException {
    AeadConfig.register();
    keysetHandle = CleartextKeysetHandle.read(BinaryKeysetReader.withBytes(secret));
    primitive = keysetHandle.getPrimitive(Aead.class);
  }

  /** Decodes input Base64 url encoded string and decrypts it. */
  @SneakyThrows
  @Override
  public String decrypt(String token) {
    Objects.requireNonNull(token);
    byte[] encryptedBytes = Base64.getUrlDecoder().decode(token);
    byte[] decrypt = primitive.decrypt(encryptedBytes, null);
    return new String(decrypt, StandardCharsets.UTF_8);
  }
}
