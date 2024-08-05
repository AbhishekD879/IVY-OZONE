package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.ladbrokescoral.oxygen.cms.Application;
import com.ladbrokescoral.oxygen.cms.api.exception.UnknownBrandException;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.configuration.SiteServerApiConfiguration;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import javax.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.DependsOn;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@DependsOn(Application.MONGOCK)
public class SiteServeApiProviderImpl implements SiteServeApiProvider {

  private final BrandService brandService;
  private final SiteServerApiConfiguration apiConfiguration;

  public static final String DEFAULT_BRAND = "bma";

  private static final Map<String, SiteServerApi> BRAND_API_CLIENTS = new HashMap<>();

  @Autowired
  public SiteServeApiProviderImpl(
      BrandService brandService, SiteServerApiConfiguration siteServerApiConfiguration) {
    this.brandService = brandService;
    this.apiConfiguration = siteServerApiConfiguration;
  }

  // FIXME: nothing will happen on add/delete Brand
  @PostConstruct
  private void initApis() {
    brandService
        .findAll()
        .forEach(
            brand -> {
              SiteServerApi siteServerApi =
                  // FIXME: just add url validation
                  Optional.ofNullable(brand.getSiteServerEndPoint())
                      .filter(StringUtils::isNotBlank)
                      .map(
                          siteServerUrl -> {
                            log.info(
                                "[{}] Initializing siteserver with url={}", brand, siteServerUrl);
                            return apiConfiguration.siteServerAPI(siteServerUrl);
                          })
                      .orElseGet(
                          () -> {
                            log.warn(
                                "Brand {} has not specified siteServerEndPoint. Initializing SiteServeApi with default url {}",
                                brand.getBrandCode(),
                                apiConfiguration.getSiteServerUrl());
                            return apiConfiguration.siteServerAPI();
                          });
              BRAND_API_CLIENTS.put(brand.getBrandCode(), siteServerApi);
            });
  }

  public SiteServerApi api(String brand) {
    return Optional.ofNullable(BRAND_API_CLIENTS.get(brand))
        .orElseThrow(() -> new UnknownBrandException(brand));
  }
}
