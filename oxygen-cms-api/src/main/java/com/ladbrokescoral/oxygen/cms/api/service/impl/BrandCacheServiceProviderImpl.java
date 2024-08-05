package com.ladbrokescoral.oxygen.cms.api.service.impl;

import com.akamai.netstorage.DefaultCredential;
import com.akamai.netstorage.NetStorage;
import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.auth.DefaultAWSCredentialsProviderChain;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.util.StringUtils;
import com.ladbrokescoral.oxygen.cms.api.service.BrandCacheService;
import com.ladbrokescoral.oxygen.cms.api.service.BrandCacheServiceProvider;
import com.ladbrokescoral.oxygen.cms.api.service.DashboardService;
import com.ladbrokescoral.oxygen.cms.configuration.AkamaiBrandProperties;
import com.ladbrokescoral.oxygen.cms.configuration.S3BrandProperties;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.PreDestroy;
import javax.validation.constraints.NotNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class BrandCacheServiceProviderImpl implements BrandCacheServiceProvider {

  private static final String ACCESS_S3_KEY_ENV_VAR = "AWS_S3_ACCESS_KEY_ID";
  private static final String SECRET_S3_KEY_ENV_VAR = "AWS_S3_SECRET_ACCESS_KEY";

  private final Map<String, List<BrandCacheService>> brandAkamaiServices;
  private final AkamaiPurgeClient akamaiPurgeClient;
  private final CloudFlareClient cloudFlareClient;
  private final DashboardService dashboardService;
  private final Integer purgeQueueCapacity;
  private final Integer purgeInitialDelaySeconds;
  private final Integer purgeFixedDelaySeconds;

  @Autowired
  public BrandCacheServiceProviderImpl(
      AkamaiBrandProperties akamaiProperties,
      S3BrandProperties s3Properties,
      AkamaiPurgeClient akamaiPurgeClient,
      CloudFlareClient cloudFlareClient,
      DashboardService dashboardService,
      @Value("${fastpurge.queue.capacity}") Integer queueCapacity,
      @Value("${fastpurge.initial.delay.seconds}") Integer initialDelay,
      @Value("${fastpurge.fixed.delay.seconds}") Integer fixedDelay) {
    this.akamaiPurgeClient = akamaiPurgeClient;
    this.cloudFlareClient = cloudFlareClient;
    this.dashboardService = dashboardService;
    this.purgeQueueCapacity = queueCapacity;
    this.purgeInitialDelaySeconds = initialDelay;
    this.purgeFixedDelaySeconds = fixedDelay;
    brandAkamaiServices = initServices(akamaiProperties, s3Properties);
  }

  @Override
  public List<BrandCacheService> getCacheService(String brand) {
    return brandAkamaiServices.getOrDefault(brand, Collections.emptyList());
  }

  @PreDestroy
  public void shutdown() {
    brandAkamaiServices.forEach((brand, services) -> services.forEach(CachePurgeService::shutdown));
  }

  private Map<String, List<BrandCacheService>> initServices(
      AkamaiBrandProperties akamaiConfigs, S3BrandProperties s3BrandProperties) {
    Map<String, List<BrandCacheService>> cacheServices = new HashMap<>();

    akamaiConfigs
        .getConfigs()
        .forEach(
            (String brand, AkamaiBrandProperties.AkamaiBrandConfig config) -> {
              if (config.isEnabled()) {
                cacheServices
                    .computeIfAbsent(brand, b -> new ArrayList<>())
                    .add(createAkamaiService(config));
              }
            });
    s3BrandProperties
        .getConfigs()
        .forEach(
            (String brand, S3BrandProperties.S3BrandConfig config) -> {
              if (config.isEnabled()) {
                cacheServices
                    .computeIfAbsent(brand, b -> new ArrayList<>())
                    .add(createS3Service(config));
              }
            });

    return cacheServices;
  }

  private static AWSCredentialsProvider awsS3CredentialsProvider() {

    String accessKeyId = StringUtils.trim(System.getenv(ACCESS_S3_KEY_ENV_VAR));
    String secretKeyId = StringUtils.trim(System.getenv(SECRET_S3_KEY_ENV_VAR));

    return (accessKeyId != null)
        ? new AWSStaticCredentialsProvider(new BasicAWSCredentials(accessKeyId, secretKeyId))
        : new DefaultAWSCredentialsProviderChain();
  }

  private BrandCacheService createS3Service(S3BrandProperties.S3BrandConfig config) {

    AmazonS3 s3Client =
        AmazonS3ClientBuilder.standard()
            .withCredentials(awsS3CredentialsProvider())
            .withRegion(config.getRegion())
            .build();

    CachePurgeService purgeService = createS3PurgeService(config);

    return new AmazonS3ServiceImpl(
        s3Client, config.getBucket(), config.getBasePath(), purgeService);
  }

  private CachePurgeService createS3PurgeService(S3BrandProperties.S3BrandConfig config) {
    if (config.isCloudFlarePurgeService()) {
      return createCloudFlarePurgeService(config.getPurgeZoneId(), config.getPurgeUrl());
    }
    return createAkamaiPurgeService(config.getPurgeUrl());
  }

  private BrandCacheService createAkamaiService(
      @NotNull AkamaiBrandProperties.AkamaiBrandConfig brandConfig) {
    NetStorage netStorage =
        new NetStorage(
            new DefaultCredential(
                brandConfig.getHost(), brandConfig.getKeyName(), brandConfig.getKey()));

    return new AkamaiServiceImpl(
        netStorage,
        brandConfig.getBasePath(),
        brandConfig.getUploadCpcode(),
        createAkamaiPurgeService(brandConfig.getUrl()));
  }

  private AkamaiDelayedPurgeService createAkamaiPurgeService(String[] purgeUrls) {
    return new AkamaiDelayedPurgeService(
        dashboardService,
        akamaiPurgeClient,
        purgeQueueCapacity,
        purgeInitialDelaySeconds,
        purgeFixedDelaySeconds,
        purgeUrls);
  }

  private CloudFlareDelayedPurgeService createCloudFlarePurgeService(
      String zoneId, String[] purgeUrls) {
    return new CloudFlareDelayedPurgeService(
        dashboardService,
        cloudFlareClient,
        purgeQueueCapacity,
        purgeInitialDelaySeconds,
        purgeFixedDelaySeconds,
        zoneId,
        purgeUrls);
  }
}
