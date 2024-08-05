package com.coral.oxygen.middleware.common.configuration.cfcache;

import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.auth.DefaultAWSCredentialsProviderChain;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AWSCredentialsProviderConfig {

  @SuppressWarnings("squid:S6263")
  @Bean
  public AWSCredentialsProvider awsS3CredentialsProvider(
      @Value("${S3_AWS_ACCESS_KEY_ID}") String s3AwsAccessKeyId,
      @Value("${S3_AWS_SECRET_ACCESS_KEY}") String s3AwsSecretAccessKey) {
    // NOSONAR
    return (s3AwsAccessKeyId != null)
        ? new AWSStaticCredentialsProvider(
            new BasicAWSCredentials(s3AwsAccessKeyId, s3AwsSecretAccessKey))
        : new DefaultAWSCredentialsProviderChain();
  }
}
