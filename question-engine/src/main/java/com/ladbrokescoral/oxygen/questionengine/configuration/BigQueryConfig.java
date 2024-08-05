package com.ladbrokescoral.oxygen.questionengine.configuration;

import com.google.api.client.googleapis.auth.oauth2.GoogleCredential;
import com.google.api.client.googleapis.util.Utils;
import com.google.api.client.util.PemReader;
import com.google.api.client.util.SecurityUtils;
import com.google.api.services.bigquery.Bigquery;
import com.google.api.services.bigquery.BigqueryScopes;
import com.ladbrokescoral.oxygen.questionengine.configuration.properties.BigQueryProperties;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Lazy;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.Collections;

@Lazy
@Configuration
@RequiredArgsConstructor
public class BigQueryConfig {
  private final BigQueryProperties bigQueryProperties;

  @Bean
  public Bigquery bigquery() throws InvalidKeySpecException, NoSuchAlgorithmException, IOException {
    return new Bigquery.Builder(Utils.getDefaultTransport(), Utils.getDefaultJsonFactory(), googleCredential()).build();
  }

  @Bean
  public GoogleCredential googleCredential() throws InvalidKeySpecException, NoSuchAlgorithmException, IOException {
    return new GoogleCredential.Builder()
        .setTransport(Utils.getDefaultTransport())
        .setJsonFactory(Utils.getDefaultJsonFactory())
        .setServiceAccountId(bigQueryProperties.getClientEmail())
        .setServiceAccountPrivateKey(privateKeyFromPkcs8(bigQueryProperties.getPrivateKey()))
        .setServiceAccountScopes(Collections.singleton(BigqueryScopes.BIGQUERY))
        .build();
  }

  private static PrivateKey privateKeyFromPkcs8(String privateKeyPem) throws IOException, InvalidKeySpecException, NoSuchAlgorithmException {
    Reader reader = new StringReader(privateKeyPem);
    PemReader.Section section = PemReader.readFirstSectionAndClose(reader, "PRIVATE KEY");
    if (section == null) {
      throw new IOException("Invalid PKCS8 data.");
    }
    return SecurityUtils.getRsaKeyFactory().generatePrivate(new PKCS8EncodedKeySpec(section.getBase64DecodedBytes()));
  }

  @Bean
  public TaskExecutor streamToBigQueryTaskExecutor() {
    ThreadPoolTaskExecutor threadPoolTaskExecutor = new ThreadPoolTaskExecutor();

    threadPoolTaskExecutor.setCorePoolSize(15);
    threadPoolTaskExecutor.setMaxPoolSize(15);
    threadPoolTaskExecutor.setWaitForTasksToCompleteOnShutdown(true);

    return threadPoolTaskExecutor;
  }
}
