package com.ladbrokescoral.oxygen.cms.api.service.df;

import com.coral.oxygen.df.api.DFClient;
import com.ladbrokescoral.oxygen.cms.Application;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.exception.UnknownBrandException;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.configuration.DFApiConfiguration;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import javax.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.DependsOn;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

@Slf4j
@Service
@DependsOn(Application.MONGOCK)
public class DFServiceProviderImpl implements DFServiceProvider {

  private final BrandService brandService;
  private final DFApiConfiguration configuration;

  public static final String DEFAULT_BRAND = "bma";

  private static final Map<String, DFClient> BRAND_API_CLIENTS = new HashMap<>();

  @Autowired
  public DFServiceProviderImpl(BrandService brandService, DFApiConfiguration configuration) {
    this.brandService = brandService;
    this.configuration = configuration;
  }

  // FIXME: nothing will happen on add/delete Brand
  @PostConstruct
  private void initApis() {
    brandService
        .findAll()
        .forEach(
            brand -> {
              DFClient client = getDfClient(brand);
              BRAND_API_CLIENTS.put(brand.getBrandCode(), client);
            });
  }

  private DFClient getDfClient(Brand brand) {
    DFClient client = configuration.api();
    if (!ObjectUtils.isEmpty(brand.getDataFabricEndPoint())) {
      client = configuration.api(brand);
    } else if (Brand.LADBROKES.equals(brand.getBrandCode())) {
      client = configuration.ladbrokesApi();
    } else {
      log.warn(
          "Brand {} has not specified dataFabricEndPoint. Initializing data fabric api with default url {}",
          brand.getBrandCode(),
          configuration.getDefaultUrl());
    }
    return client;
  }

  public DFClient api(String brand) {
    return Optional.ofNullable(BRAND_API_CLIENTS.get(brand))
        .orElseThrow(() -> new UnknownBrandException(brand));
  }
}
