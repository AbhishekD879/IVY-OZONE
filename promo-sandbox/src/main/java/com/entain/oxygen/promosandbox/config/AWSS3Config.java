package com.entain.oxygen.promosandbox.config;

import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.auth.DefaultAWSCredentialsProviderChain;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.util.StringUtils;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@SuppressWarnings("java:S6263")
public class AWSS3Config {

  private static final String ACCESS_S3_KEY_ENV_VAR = "AWS_S3_ACCESS_KEY_ID";
  private static final String SECRET_S3_KEY_ENV_VAR = "AWS_S3_SECRET_KEY";

  @Bean
  public AmazonS3 getAmazonS3Client(S3BrandProperties s3BrandConfig) {
    return AmazonS3ClientBuilder.standard()
        .withRegion(Regions.fromName(s3BrandConfig.getRegion()))
        .withCredentials(awsS3CredentialsProvider())
        .build();
  }

  private static AWSCredentialsProvider awsS3CredentialsProvider() {
    String accessKeyId = StringUtils.trim(System.getenv(ACCESS_S3_KEY_ENV_VAR));
    String secretKeyId = StringUtils.trim(System.getenv(SECRET_S3_KEY_ENV_VAR));
    return (accessKeyId != null)
        ? new AWSStaticCredentialsProvider(new BasicAWSCredentials(accessKeyId, secretKeyId))
        : new DefaultAWSCredentialsProviderChain();
  }
}
