package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.OddsBoostConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostConfigEntity;
import com.ladbrokescoral.oxygen.cms.api.mapping.OddsBoostConfigurationMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.OddsBoostConfigurationRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class OddsBoostConfigurationService extends AbstractService<OddsBoostConfigEntity> {

  private final OddsBoostConfigurationRepository boostConfigurationRepository;
  private final SvgEntityService<OddsBoostConfigEntity> svgEntityService;
  private final String svgMenuPath;

  public OddsBoostConfigurationService(
      final OddsBoostConfigurationRepository boostConfigurationRepository,
      final SvgEntityService<OddsBoostConfigEntity> svgEntityService,
      @Value("${images.oddsboost.svg}") String svgMenuPath) {
    super(boostConfigurationRepository);
    this.boostConfigurationRepository = boostConfigurationRepository;
    this.svgEntityService = svgEntityService;
    this.svgMenuPath = svgMenuPath;
  }

  public OddsBoostConfigDTO getPublicDTO(final String brand) {
    return boostConfigurationRepository
        .findById(brand)
        .map(OddsBoostConfigurationMapper.INSTANCE::toDTO)
        .orElse(new OddsBoostConfigDTO());
  }

  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<OddsBoostConfigEntity> attachSvgImage(
      OddsBoostConfigEntity entity, @ValidFileType("svg") MultipartFile file) {
    return svgEntityService.attachSvgImage(entity, file, svgMenuPath);
  }

  /**
   * @deprecated use SvgImages api to remove images and use update the menu endpoint to set the
   *     svgId to null delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<OddsBoostConfigEntity> removeSvgImage(OddsBoostConfigEntity entity) {
    return svgEntityService.removeSvgImage(entity);
  }
}
