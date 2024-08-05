package com.ladbrokescoral.oxygen.cms.configuration;

import com.coral.oxygen.df.api.DFClient;
import com.coral.oxygen.df.api.impl.DFClientImpl;
import com.coral.oxygen.df.api.impl.DFHttpClient;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.exception.DFApiInitializationException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import lombok.extern.slf4j.Slf4j;
import okhttp3.logging.HttpLoggingInterceptor.Level;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
public class DFApiConfiguration {

  @Value("${df.base.url}")
  private String dfBaseUrl;

  @Value("${df.api.key}")
  private String dfApiKey = "PleaseSetCorrectApiKey";

  @Value("${df.ladbrokes.base.url}")
  private String ladbrokesBaseUrl;

  @Value("${df.ladbrokes.api.key}")
  private String ladbrokesApiKey = "PleaseSetCorrectApiKey";

  @Value("${df.api.version}")
  private String dfApiVersion = "2.31";

  @Value("${df.connection.timeout}")
  private int dfConnectionTimeout;

  @Value("${df.read.timeout}")
  private int dfReadTimeout;

  @Value("${df.retries.number}")
  private int dfRetriesNumber;

  @Value("${df.logging.level}")
  private String dfLoggingLevel = "BASIC";

  /** @return SiteServerApi with default url */
  public DFClient api() {
    Brand brand = buildBrand(dfBaseUrl, dfApiKey);
    return api(brand);
  }

  private Brand buildBrand(String baseUrl, String apiKey) {
    Brand brand = new Brand();
    brand.setDataFabricEndPoint(baseUrl);
    brand.setDataFabricApiKey(apiKey);
    return brand;
  }

  /** @return SiteServerApi with specified siteServe url */
  public DFClient api(Brand brand) {
    try {

      DFHttpClient dfHttpClient =
          DFHttpClient.builder()
              .loggerLevel(Level.valueOf(dfLoggingLevel))
              .connectTimeout(dfConnectionTimeout)
              .readTimeout(dfReadTimeout)
              .build();

      return DFClientImpl.builder()
          .baseUrl(brand.getDataFabricEndPoint(), dfHttpClient.getHttpClient())
          .maxNumberOfRetries(dfRetriesNumber)
          .version(dfApiVersion)
          .apiKey(brand.getDataFabricApiKey())
          .build();

    } catch (NoSuchAlgorithmException | KeyManagementException e) {
      log.error("Error initializing SiteServerApi", e);
      throw new DFApiInitializationException(e);
    }
  }

  /** @return default siteServe */
  public String getDefaultUrl() {
    return dfBaseUrl;
  }

  public DFClient ladbrokesApi() {
    Brand ladbrokesBrand = buildBrand(ladbrokesBaseUrl, ladbrokesApiKey);
    return api(ladbrokesBrand);
  }
}
