package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.Secret;
import com.ladbrokescoral.oxygen.cms.api.entity.SecretItem;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

public class SecretUpdate extends AbstractBrandMongoUpdate {

  private static final String SECRETS_COLLECTION_NAME = "secrets";
  private MongockTemplate mongockTemplate;

  public SecretUpdate(MongockTemplate mongockTemplate) {
    this.mongockTemplate = mongockTemplate;
  }

  @Getter
  @RequiredArgsConstructor(access = AccessLevel.PRIVATE)
  private enum OptInSecretSettings {
    AT_THE_RACES("AtTheRaces", new String[] {"partnerCode", "password", "secret"}),
    IMG_STREAMING("IMGStreaming", new String[] {"operatorId", "secret"}),
    PERFORM_GROUP(
        "PerformGroup",
        new String[] {
          "desktopPartnerId",
          "desktopUserId",
          "desktopSeed",
          "mobilePartnerId",
          "mobileUserId",
          "mobileSeed"
        });

    private final String uri;
    private final String[] keys;
  }

  public void initOptInSecrets(String brand) {
    List<Secret> existingSecrets =
        findAllByBrand(mongockTemplate, brand, SECRETS_COLLECTION_NAME, Secret.class);
    Map<String, Secret> existingByUri =
        existingSecrets.stream().collect(Collectors.toMap(Secret::getUri, Function.identity()));

    Arrays.stream(OptInSecretSettings.values())
        .forEach(
            secretSettings ->
                createSecretIfNotExist(
                    brand, secretSettings.getUri(), secretSettings.getKeys(), existingByUri));
  }

  private void createSecretIfNotExist(
      String brand, String uri, String[] secretKeys, Map<String, Secret> existingSecrets) {
    if (!existingSecrets.containsKey(uri)) {
      createNewSecret(brand, uri, secretKeys);
    } else {
      addMissingSecretKeys(existingSecrets.get(uri), secretKeys);
    }
  }

  private void addMissingSecretKeys(Secret existing, String[] secretKeys) {
    List<SecretItem> missingItems =
        Arrays.stream(secretKeys)
            .filter(k -> existing.getItems().stream().noneMatch(i -> k.equals(i.getKey())))
            .map(k -> new SecretItem(k, null))
            .collect(Collectors.toCollection(ArrayList::new));
    if (!missingItems.isEmpty()) {
      missingItems.addAll(existing.getItems());
      existing.setItems(missingItems);
      mongockTemplate.save(existing, SECRETS_COLLECTION_NAME);
    }
  }

  private void createNewSecret(String brand, String uri, String[] secretKeys) {
    Secret newSecret = new Secret();
    newSecret.setBrand(brand);
    newSecret.setUri(uri);
    newSecret.setName(uri);
    newSecret.setEnabled(false);
    newSecret.setItems(
        Arrays.stream(secretKeys).map(k -> new SecretItem(k, null)).collect(Collectors.toList()));
    mongockTemplate.insert(newSecret, SECRETS_COLLECTION_NAME);
  }
}
