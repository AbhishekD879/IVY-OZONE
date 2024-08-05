package com.ladbrokescoral.oxygen.questionengine.configuration;

import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.client.builder.AwsClientBuilder;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBMapperConfig;
import com.ladbrokescoral.oxygen.questionengine.configuration.annotation.ExcludeFromIntegrationTests;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@ExcludeFromIntegrationTests
public class DynamoDbConfig {

  @Value("${amazon.dynamodb.endpoint}")
  private String dynamoEndpoint;

  @Value("${amazon.dynamodb.region}")
  private String dynamoRegion;

  @Value("${amazon.dynamodb.access.key}")
  private String accessKey;

  @Value("${amazon.dynamodb.secret.key}")
  private String secretKey;

  @Value("${spring.profiles.active}")
  private String profile;

  @Bean
  public DynamoDBMapperConfig dynamoDBMapperConfig() {
    return DynamoDBMapperConfig.builder()
        .withTableNameOverride(
            DynamoDBMapperConfig.TableNameOverride.withTableNamePrefix(profile.toLowerCase() + "-"))
        .withPaginationLoadingStrategy(DynamoDBMapperConfig.PaginationLoadingStrategy.LAZY_LOADING)
        .build();
  }

  @Bean
  public AmazonDynamoDB amazonDynamoDB() {
    AmazonDynamoDBClientBuilder amazonDynamoDBClientBuilder = AmazonDynamoDBClientBuilder.standard()
        .withEndpointConfiguration(new AwsClientBuilder.EndpointConfiguration(dynamoEndpoint, dynamoRegion));
    if ("LOCAL".equals(profile)) {
      BasicAWSCredentials awsCreds = new BasicAWSCredentials(accessKey, secretKey);
      amazonDynamoDBClientBuilder.withCredentials(new AWSStaticCredentialsProvider(awsCreds));
    }
    return amazonDynamoDBClientBuilder.build();
  }
}
