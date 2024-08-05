package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Secret;
import com.ladbrokescoral.oxygen.cms.api.entity.SecretItem;
import com.ladbrokescoral.oxygen.cms.api.exception.InternalServerException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.SecretRepository;
import com.ladbrokescoral.oxygen.cms.api.service.vault.SecretVaultService;
import com.ladbrokescoral.oxygen.cms.api.service.vault.VaultException;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.codec.digest.Md5Crypt;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class SecretService extends AbstractService<Secret> {

  public static final String VAULT_KEY_FORMAT = "%s_%s";
  private final SecretRepository secretRepository;
  private final SecretVaultService vaultService;
  private final String hashSalt;
  private final String hashPrefix;

  @Autowired
  public SecretService(
      SecretRepository secretRepository,
      SecretVaultService vaultService,
      @Value("${secrets.hash.salt}") String hashSalt,
      @Value("${secrets.hash.prefix}") String hashPrefix) {
    super(secretRepository);
    this.secretRepository = secretRepository;
    this.vaultService = vaultService;
    this.hashSalt = hashSalt;
    this.hashPrefix = hashPrefix;
  }

  @Override
  public Secret prepareModelBeforeSave(Secret model) {
    validateNoDuplicates(model.getItems());
    if (Objects.isNull(model.getId())) {
      // new secret to be created
      model.setId(Util.randomUUID());
      model.getItems().stream()
          .filter(i -> StringUtils.isNotBlank(i.getValue()))
          .forEach(item -> saveValueToVault(model.getId(), item));
    }
    return model;
  }

  @Override
  public Secret update(Secret existingEntity, Secret updateEntity) {
    updateNewValues(existingEntity, updateEntity);
    removeOldValues(existingEntity, updateEntity);
    return super.update(existingEntity, updateEntity);
  }

  public Secret readDecoded(String id) {
    Secret secret = repository.findById(id).orElseThrow(NotFoundException::new);
    return decodeValues(secret);
  }

  public Optional<Secret> readActiveByBrandAndUri(String brand, String uri) {
    return secretRepository.findByBrandAndUriAndEnabledIsTrue(brand, uri).map(this::decodeValues);
  }

  public Optional<Secret> beforeDelete(String id) {
    Optional<Secret> secret = findOne(id);
    secret.ifPresent(s -> deleteFromVault(id, s.getItems()));
    return secret;
  }

  private void deleteFromVault(String id, List<SecretItem> secretItems) {
    secretItems.forEach(
        (SecretItem i) -> {
          removeFromVault(id, i.getKey());
          i.setValue(null);
        });
  }

  private Secret decodeValues(Secret secret) {
    String secretId = secret.getId();
    List<String> vaultKeys =
        secret.getItems().stream()
            .filter(i -> Objects.nonNull(i.getValue()))
            .map(i -> buildVaultKey(secretId, i.getKey()))
            .collect(Collectors.toList());
    Map<String, String> values = vaultService.getValues(vaultKeys);

    secret
        .getItems()
        .forEach(
            i ->
                i.setValue(values.getOrDefault(buildVaultKey(secretId, i.getKey()), i.getValue())));
    return secret;
  }

  private void validateNoDuplicates(List<SecretItem> items) {
    Map<String, Long> itemsCount =
        items.stream().collect(Collectors.groupingBy(SecretItem::getKey, Collectors.counting()));
    itemsCount.forEach(
        (String key, Long count) -> {
          if (count > 1) {
            throw new ValidationException("Unsupported duplicated key " + key);
          }
        });
  }

  private void removeOldValues(Secret existingEntity, Secret updateEntity) {
    Set<String> newConfigs =
        updateEntity.getItems().stream().map(SecretItem::getKey).collect(Collectors.toSet());
    existingEntity.getItems().stream()
        .filter(p -> !newConfigs.contains(p.getKey()))
        .forEach(p -> removeFromVault(existingEntity.getId(), p.getKey()));
  }

  private void updateNewValues(Secret existingEntity, Secret updateEntity) {
    Map<String, String> existingProperties =
        existingEntity.getItems().stream()
            .collect(
                HashMap::new,
                (map, item) -> map.put(item.getKey(), item.getValue()),
                HashMap::putAll);
    updateEntity.getItems().stream()
        .filter(
            newItem ->
                !existingProperties.containsKey(newItem.getKey())
                    || !Objects.equals(
                        newItem.getValue(), existingProperties.get(newItem.getKey())))
        .forEach(item -> saveValueToVault(existingEntity.getId(), item));
  }

  private String buildVaultKey(String secretId, String itemKey) {
    return String.format(VAULT_KEY_FORMAT, secretId, itemKey);
  }

  private void saveValueToVault(String secretId, SecretItem item) {
    String vaultKey = buildVaultKey(secretId, item.getKey());
    try {
      vaultService.save(vaultKey, item.getValue());
      item.setValue(checkSum(item.getValue()));
    } catch (VaultException e) {
      log.error("Failed to save {} key to the vault", vaultKey, e);
      throw new InternalServerException("Failed to save properties to Vault: " + e.getMessage(), e);
    }
  }

  private void removeFromVault(String secretId, String itemKey) {
    String vaultKey = buildVaultKey(secretId, itemKey);
    try {
      vaultService.remove(vaultKey);
    } catch (VaultException e) {
      log.error("Failed to remove {} key from the vault", vaultKey, e);
      throw new InternalServerException(
          "Failed to remove property from the Vault: " + e.getMessage(), e);
    }
  }

  private String checkSum(String value) {
    return Md5Crypt.md5Crypt(value.getBytes(), hashSalt, hashPrefix);
  }
}
