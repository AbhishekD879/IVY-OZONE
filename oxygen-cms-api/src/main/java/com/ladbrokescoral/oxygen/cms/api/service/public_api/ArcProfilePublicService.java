package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ArcProfileDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcData;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcMasterData;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcProfile;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.ArcMasterService;
import com.ladbrokescoral.oxygen.cms.api.service.ArcProfileService;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import javax.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class ArcProfilePublicService {

  private ArcProfileService service;
  private ArcMasterService masterService;
  private ModelMapper modelMapper;
  private List<ArcMasterData> arcMasterData;

  @Autowired
  public ArcProfilePublicService(
      ArcProfileService service, ArcMasterService masterService, ModelMapper modelMapper) {
    this.service = service;
    this.masterService = masterService;
    this.modelMapper = modelMapper;
  }

  @PostConstruct
  public void findAll() {
    arcMasterData = masterService.getAllMetadata();
  }

  public List<ArcProfileDto> findByBrand(String brand) {
    Optional<List<ArcProfile>> optionalArcProfile = service.findAllByBrand(brand);
    if (optionalArcProfile.isPresent()) {
      List<ArcProfile> arcProfiles = optionalArcProfile.get();
      return arcProfiles.stream().map(this::dtoMapper).collect(Collectors.toList());
    } else {
      throw new NotFoundException();
    }
  }

  public ArcProfileDto findById(String id) {
    Optional<ArcProfile> optionalArcProfile = service.findOne(id);
    if (optionalArcProfile.isPresent()) {
      return dtoMapper(optionalArcProfile.get());
    } else {
      throw new NotFoundException();
    }
  }

  public ArcProfileDto findArcProfileByBrandAndModelRiskLevelAndReasonCode(
      String brand, Integer modelAndRiskLevel, Integer reasonCode) {
    ArcProfile arcProfile =
        service.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
            brand, modelAndRiskLevel, reasonCode);
    if (null != arcProfile) {
      return dtoMapper(arcProfile);
    } else {
      throw new NotFoundException();
    }
  }

  private String getFormattedDemographicDetails(ArcData arcData) {
    String formattedDemographicDetails = null;
    if (null != arcData) {
      formattedDemographicDetails = arcData.getId() + "-" + arcData.getName();
    }
    return formattedDemographicDetails;
  }

  private ArcProfileDto dtoMapper(ArcProfile arcProfile) {
    ArcProfileDto arcProfileDto = modelMapper.map(arcProfile, ArcProfileDto.class);
    if (null != arcMasterData) {
      String modelRiskLevel = getFormattedDemographicDetails(getModelRiskLevel(arcProfile));
      String reasonCodes = getFormattedDemographicDetails(getReasonCodeWithDesc(arcProfile));
      if (StringUtils.isNotBlank(modelRiskLevel) && StringUtils.isNotBlank(reasonCodes)) {
        arcProfileDto.setModelRiskLevel(modelRiskLevel);
        arcProfileDto.setReasonCode(reasonCodes);
        log.info("ArcProfileDto : " + modelRiskLevel + "---------------" + reasonCodes);
      }
    }
    return arcProfileDto;
  }

  private ArcData getModelRiskLevel(ArcProfile arcProfile) {
    Optional<ArcData> arcData =
        arcMasterData.stream()
            .filter(d -> "modelRiskLevel".equals(d.getMasterLineName()))
            .flatMap(
                a ->
                    a.getValues().stream()
                        .filter(e -> e.getId().equals(arcProfile.getModelRiskLevel())))
            .findFirst();
    return arcData.orElse(null);
  }

  private ArcData getReasonCodeWithDesc(ArcProfile arcProfile) {
    Optional<ArcData> arcData =
        arcMasterData.stream()
            .filter(d -> "reasonCodes".equals(d.getMasterLineName()))
            .flatMap(
                a ->
                    a.getValues().stream()
                        .filter(e -> e.getId().equals(arcProfile.getReasonCode())))
            .findFirst();
    return arcData.orElse(null);
  }
}
