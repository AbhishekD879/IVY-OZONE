package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.InitialLuckyDipConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipV2ConfigurationDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipV2Config;
import com.ladbrokescoral.oxygen.cms.api.repository.LuckyDipV2ConfigRepository;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Service
public class LuckyDipV2ConfigService extends AbstractService<LuckyDipV2Config> {
  private final LuckyDipV2ConfigRepository luckyDipConfigRepository;
  private final ModelMapper modelMapper;
  private static final String TYPE_ID = "Type ID";

  @Autowired
  public LuckyDipV2ConfigService(LuckyDipV2ConfigRepository repository, ModelMapper modelMapper) {
    super(repository);
    this.luckyDipConfigRepository = repository;
    this.modelMapper = modelMapper;
  }

  public List<LuckyDipV2Config> findAllLuckyDipConfigByBrand(String brand, Sort sort) {
    return luckyDipConfigRepository.findByBrand(brand, sort);
  }

  public LuckyDipV2Config convertDtoToEntity(LuckyDipV2ConfigurationDto luckyDipConfigDto) {
    return modelMapper.map(luckyDipConfigDto, LuckyDipV2Config.class);
  }

  public Optional<LuckyDipV2Config> getLDByBrandAndLDConfigLevelId(
      String brand, String configLevelId) {
    return luckyDipConfigRepository
        .findByBrandAndLuckyDipConfigLevelId(brand, configLevelId)
        .filter(LuckyDipV2Config::getStatus);
  }

  public List<InitialLuckyDipConfigDto> getInitData(String brand) {
    return super.findByBrand(brand).stream()
        .filter(
            luckyDipV2Config -> TYPE_ID.equalsIgnoreCase(luckyDipV2Config.getLuckyDipConfigLevel()))
        .filter(LuckyDipV2Config::getStatus)
        .filter(LuckyDipV2Config::getDisplayOnCompetitions)
        .map(e -> modelMapper.map(e, InitialLuckyDipConfigDto.class))
        .collect(Collectors.toList());
  }

  public List<LuckyDipV2Config> getAllActiveLDByBrand(String brand) {
    return luckyDipConfigRepository.findAllByBrandAndStatusTrue(brand);
  }
}
