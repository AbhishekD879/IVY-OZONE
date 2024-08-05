package com.ladbrokescoral.oxygen.cms.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.dto.BrandMenuItemDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BrandMenuStructure;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandMenuStructureRepository;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Optional;
import java.util.UUID;
import javax.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.IOUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

@Component
@Profile("!UNIT")
@Slf4j
public class BrandMenusInitialPopulator {
  @Autowired private BrandMenuStructureRepository menuStructureRepo;

  @Autowired private ObjectMapper jacksonObjectMapper;

  @PostConstruct
  public void afterInit() {
    for (String filename :
        Arrays.asList(
            "/configuration/brand-menus/bma.json",
            "/configuration/brand-menus/connect.json",
            "/configuration/brand-menus/rcomb.json",
            "/configuration/brand-menus/retail.json",
            "/configuration/brand-menus/secondscreen.json")) {
      try {
        verifyBrandMenuFromFile(filename);
        log.info("Verified menu for {}" + filename);
      } catch (Exception e) {
        log.error(
            "Error occurred while verifying brand-based menu for {}: {}", filename, e.toString());
      }
    }
  }

  private void verifyBrandMenuFromFile(String filename) throws IOException {
    BrandMenuStructure menu =
        jacksonObjectMapper.readValue(
            IOUtils.resourceToString(filename, StandardCharsets.UTF_8), BrandMenuStructure.class);
    Optional<BrandMenuStructure> menuInMongo =
        menuStructureRepo.findByBrand(menu.getBrand()).stream().findFirst();

    if (!menuInMongo.isPresent()) {
      for (BrandMenuItemDto item : menu.getMenu()) {
        generateIdsRecursively(item);
      }
      menuStructureRepo.insert(menu);
    }
  }

  private void generateIdsRecursively(BrandMenuItemDto menuItem) {
    menuItem.setId(UUID.randomUUID().toString());
    if (menuItem.getSubMenu() != null) {
      menuItem.getSubMenu().forEach(this::generateIdsRecursively);
    }
  }
}
