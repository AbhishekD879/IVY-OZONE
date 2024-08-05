package com.ladbrokescoral.oxygen.cms.api.service.vault;

import java.util.List;
import java.util.Map;

public interface SecretVaultService {
  /**
   * Save property safe
   *
   * @param key - secret key
   * @param value - secret value decrypted
   * @throws VaultException if value wasn't saved
   */
  void save(String key, String value) throws VaultException;

  /**
   * Returns stored value for a given key
   *
   * @param key - secret key
   * @return decrypted value for the key
   * @throws VaultException on getting value failure
   */
  String getValue(String key) throws VaultException;

  /**
   * Find decoded values for the following keys
   *
   * @param keys - list of keys to find, can be empty
   * @return map of existing key - value
   */
  Map<String, String> getValues(List<String> keys);

  /**
   * Remove property
   *
   * @param key - secret key
   * @throws VaultException if value wasn't saved
   */
  void remove(String key) throws VaultException;
}
