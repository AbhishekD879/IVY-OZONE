package com.ladbrokescoral.oxygen.cms.configuration;

import com.google.api.client.googleapis.auth.oauth2.GoogleCredential;
import com.google.api.client.googleapis.util.Utils;
import com.google.api.client.util.PemReader;
import com.google.api.client.util.SecurityUtils;
import com.google.api.services.bigquery.Bigquery;
import com.google.api.services.bigquery.BigqueryScopes;
import com.ladbrokescoral.oxygen.cms.api.repository.BigQueryQuestionEngineRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.BigQueryTimelineRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.impl.BigQueryQuestionEngineRepositoryImpl;
import com.ladbrokescoral.oxygen.cms.api.repository.impl.BigQueryTimelineRepositoryImpl;
import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.Collections;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Profile("!UNIT")
@Configuration
public class BigQueryConfig {

  @Bean
  @Profile("!LOCAL")
  public Bigquery bigquery(BigQueryProperties bigQueryProperties)
      throws InvalidKeySpecException, NoSuchAlgorithmException, IOException {
    return new Bigquery.Builder(
            Utils.getDefaultTransport(),
            Utils.getDefaultJsonFactory(),
            googleCredential(bigQueryProperties))
        .build();
  }

  @Bean
  @Profile("!LOCAL")
  public GoogleCredential googleCredential(BigQueryProperties bigQueryProperties)
      throws InvalidKeySpecException, NoSuchAlgorithmException, IOException {
    return new GoogleCredential.Builder()
        .setTransport(Utils.getDefaultTransport())
        .setJsonFactory(Utils.getDefaultJsonFactory())
        .setServiceAccountId(bigQueryProperties.getClientEmail())
        .setServiceAccountPrivateKey(privateKeyFromPkcs8(bigQueryProperties.getPrivateKey()))
        .setServiceAccountScopes(Collections.singleton(BigqueryScopes.BIGQUERY))
        .build();
  }

  @Bean
  @Profile("!LOCAL")
  public BigQueryTimelineRepository bigQueryTimelineRepository(
      BigQueryProperties bigQueryProperties)
      throws InvalidKeySpecException, NoSuchAlgorithmException, IOException {
    return new BigQueryTimelineRepositoryImpl(bigquery(bigQueryProperties), bigQueryProperties);
  }

  @Bean
  @Profile("LOCAL")
  public BigQueryTimelineRepository localBigQueryTimelineRepository() {
    return changelog ->
        LoggerFactory.getLogger(getClass())
            .info("You're in development mode. No data will be streamed to BigQuery");
  }

  @Bean
  @Profile("!LOCAL")
  public BigQueryQuestionEngineRepository bigQueryQuestionEngineRepository(
      BigQueryProperties bigQueryProperties)
      throws InvalidKeySpecException, NoSuchAlgorithmException, IOException {
    return new BigQueryQuestionEngineRepositoryImpl(
        bigquery(bigQueryProperties), bigQueryProperties);
  }

  @Bean
  @Profile("LOCAL")
  public BigQueryQuestionEngineRepository localBigQueryQuestionEngineRepository() {
    return (String quizId) -> {
      LoggerFactory.getLogger(getClass())
          .info("You're in development mode. No data will be retrieved from BigQuery");

      return Collections.emptyList();
    };
  }

  private static PrivateKey privateKeyFromPkcs8(String privateKeyPem)
      throws IOException, InvalidKeySpecException, NoSuchAlgorithmException {
    Reader reader = new StringReader(privateKeyPem);
    PemReader.Section section = PemReader.readFirstSectionAndClose(reader, "PRIVATE KEY");
    if (section == null) {
      throw new IOException("Invalid PKCS8 data.");
    }
    return SecurityUtils.getRsaKeyFactory()
        .generatePrivate(new PKCS8EncodedKeySpec(section.getBase64DecodedBytes()));
  }
}
