package com.egalacoral.spark.timeform.configuration;

import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.client.builder.AwsClientBuilder;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBMapperConfig;
import org.socialsignin.spring.data.dynamodb.core.DynamoDBOperations;
import org.socialsignin.spring.data.dynamodb.core.DynamoDBTemplate;
import org.socialsignin.spring.data.dynamodb.repository.config.EnableDynamoDBRepositories;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableDynamoDBRepositories(
    basePackages = "com.egalacoral.spark.timeform.repository",
    dynamoDBOperationsRef = "dynamoDBOperations")
public class DynamoDb {

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

  @Value("${application.name}")
  private String applictionName = "timeform";

  @Value("${dynamodb.prefix}")
  private String prefix;

  @Bean(name = "tablePrefix")
  public String tablePrefix() {
    return applictionName + "-" + prefix + "-";
  }

  @Bean(name = "dynamoDBMapperConfig")
  public DynamoDBMapperConfig dynamoDBMapperConfig(@Qualifier("tablePrefix") String tablePrefix) {
    final DynamoDBMapperConfig config =
        DynamoDBMapperConfig.builder()
            .withTableNameOverride(
                DynamoDBMapperConfig.TableNameOverride.withTableNamePrefix(tablePrefix))
            .build();
    return config;
  }

  @Bean
  public AmazonDynamoDB amazonDynamoDB() {
    AmazonDynamoDBClientBuilder amazonDynamoDBClientBuilder =
        AmazonDynamoDBClientBuilder.standard()
            .withEndpointConfiguration(
                new AwsClientBuilder.EndpointConfiguration(dynamoEndpoint, dynamoRegion));
    if ("local".equals(profile)) {
      BasicAWSCredentials awsCreds = new BasicAWSCredentials(accessKey, secretKey);
      amazonDynamoDBClientBuilder.withCredentials(new AWSStaticCredentialsProvider(awsCreds));
    }
    return amazonDynamoDBClientBuilder.build();
  }

  @Bean
  public DynamoDBOperations dynamoDBOperations(
      AmazonDynamoDB amazonDynamoDB, DynamoDBMapperConfig dynamoDBMapperConfig) {
    final DynamoDBTemplate dynamoDBTemplate =
        new DynamoDBTemplate(amazonDynamoDB, dynamoDBMapperConfig);
    return dynamoDBTemplate;
  }
}
