package com.coral.oxygen.middleware.common.configuration.cfcache;

import com.amazonaws.ClientConfiguration;
import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.PreDestroy;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class BrandCacheServiceProviderImpl implements BrandCacheServiceProvider {

  private final Map<String, List<BrandCacheService>> brandAkamaiServices;
  private final CloudFlareClient cloudFlareClient;
  private final Integer purgeQueueCapacity;
  private final Integer purgeInitialDelaySeconds;
  private final Integer purgeFixedDelaySeconds;
  private final Integer purgeItemsMaxLimit;
  private final AWSCredentialsProvider awsS3CredentialsProvider;

  @Autowired
  public BrandCacheServiceProviderImpl(
      S3BrandProperties s3Properties,
      CloudFlareClient cloudFlareClient,
      @Value("${fastpurge.queue.capacity}") Integer queueCapacity,
      @Value("${fastpurge.initial.delay.seconds}") Integer initialDelay,
      @Value("${fastpurge.fixed.delay.seconds}") Integer fixedDelay,
      @Value("${fastpurge.purgeItems.maxlimit}") Integer purgeItemsMaxLimit,
      AWSCredentialsProvider awsS3CredentialsProvider) {
    this.cloudFlareClient = cloudFlareClient;
    this.purgeQueueCapacity = queueCapacity;
    this.purgeInitialDelaySeconds = initialDelay;
    this.purgeFixedDelaySeconds = fixedDelay;
    this.purgeItemsMaxLimit = purgeItemsMaxLimit;
    this.awsS3CredentialsProvider = awsS3CredentialsProvider;
    brandAkamaiServices = initServices(s3Properties);
  }

  @Override
  public List<BrandCacheService> getCacheService(String brand) {
    return brandAkamaiServices.getOrDefault(brand, Collections.emptyList());
  }

  @PreDestroy
  public void shutdown() {
    brandAkamaiServices.forEach((brand, services) -> services.forEach(CachePurgeService::shutdown));
  }

  private Map<String, List<BrandCacheService>> initServices(S3BrandProperties s3BrandProperties) {
    Map<String, List<BrandCacheService>> cacheServices = new HashMap<>();

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

  private BrandCacheService createS3Service(S3BrandProperties.S3BrandConfig config) {
    ClientConfiguration clientConfig = new ClientConfiguration();
    clientConfig.setRequestTimeout(config.getReqTimeout());
    AmazonS3 s3Client =
        AmazonS3ClientBuilder.standard()
            .withCredentials(awsS3CredentialsProvider)
            .withRegion(config.getRegion())
            .withClientConfiguration(clientConfig)
            .build();

    CachePurgeService purgeService = createS3PurgeService(config);

    return new AmazonS3ServiceImpl(
        s3Client, config.getBucket(), config.getBasePath(), purgeService);
  }

  private CachePurgeService createS3PurgeService(S3BrandProperties.S3BrandConfig config) {
    return createCloudFlarePurgeService(config.getPurgeZoneId(), config.getPurgeUrl());
  }

  private CloudFlareDelayedPurgeService createCloudFlarePurgeService(
      String zoneId, String[] purgeUrls) {
    return new CloudFlareDelayedPurgeService(
        cloudFlareClient,
        purgeQueueCapacity,
        purgeInitialDelaySeconds,
        purgeFixedDelaySeconds,
        purgeItemsMaxLimit,
        zoneId,
        purgeUrls);
  }
}
