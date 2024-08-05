package com.ladbrokescoral.oxygen.cms.api.service.vault;

import com.ladbrokescoral.oxygen.cms.api.entity.SecretVault;
import com.ladbrokescoral.oxygen.cms.api.repository.SecretVaultRepository;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class MongoSecretVaultServiceImpl implements SecretVaultService {

  private final SecretVaultRepository repository;

  @Autowired
  public MongoSecretVaultServiceImpl(SecretVaultRepository repository) {
    this.repository = repository;
  }

  @Override
  public void save(String key, String value) throws VaultException {
    try {
      SecretVault secret = new SecretVault();
      secret.setKey(key);
      secret.setValue(value);
      repository.save(secret);
    } catch (Exception e) {
      log.error("Failed to save secret {}", key, e);
      throw new VaultException(e.getMessage());
    }
  }

  @Override
  public String getValue(String key) throws VaultException {
    return repository.findById(key).map(SecretVault::getValue).orElse(null);
  }

  @Override
  public Map<String, String> getValues(List<String> keys) {
    if (keys.isEmpty()) {
      return Collections.emptyMap();
    }
    Iterable<SecretVault> secrets = repository.findAllById(keys);
    return StreamSupport.stream(secrets.spliterator(), false)
        .collect(Collectors.toMap(SecretVault::getKey, SecretVault::getValue));
  }

  @Override
  public void remove(String key) throws VaultException {
    repository.deleteById(key);
  }
}
