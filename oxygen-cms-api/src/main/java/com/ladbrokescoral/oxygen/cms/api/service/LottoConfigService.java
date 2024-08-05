package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.LottoBannerConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.entity.LottoConfig;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.LottoConfigRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
public class LottoConfigService extends SortableService<LottoConfig> {

  private final LottoConfigRepository lottoConfigRepository;

  public LottoConfigService(LottoConfigRepository lottoConfigRepository) {
    super(lottoConfigRepository);
    this.lottoConfigRepository = lottoConfigRepository;
  }

  // INFO:while updating the lottoconfig banner link should not update as it is common across all
  // entities
  @Override
  public LottoConfig update(LottoConfig entity, LottoConfig updateEntity) {
    updateEntity.setBannerLink(entity.getBannerLink());
    return save(updateEntity);
  }

  public void updateBannerLink(LottoBannerConfigDTO lottoBannerConfigDTO, String brand) {

    List<LottoConfig> lottoConfig = lottoConfigRepository.findByBrand(brand);
    validateLottoConfig(lottoConfig, lottoBannerConfigDTO.getIds());
    lottoConfig.forEach(
        (LottoConfig config) -> {
          if (lottoBannerConfigDTO.getIds().contains(config.getId())) {
            config.setBannerLink(lottoBannerConfigDTO.getGlobalBannerLink());
            config.setBannerText(lottoBannerConfigDTO.getGlobalBannerText());
            config.setDayCount(lottoBannerConfigDTO.getDayCount());
          } else {
            throw new ValidationException("input ids and existing ids could not match");
          }
        });
    lottoConfigRepository.saveAll(lottoConfig);
  }

  private void validateLottoConfig(List<LottoConfig> entities, List<String> ids) {
    validateEntities(entities);
    validateSize(entities, ids);
  }

  private void validateSize(List<LottoConfig> entities, List<String> ids) {
    if (entities.size() != ids.size())
      throw new ValidationException("input ids and existing ids could not match");
  }

  private void validateEntities(List<LottoConfig> lottoConfig) {
    if (CollectionUtils.isEmpty(lottoConfig)) throw new ValidationException("lottoConfig is empty");
  }

  public Optional<LottoBannerConfigDTO> readByBrand(String brand) {
    Optional<List<LottoConfig>> lottoConfigs = Optional.ofNullable(super.findByBrand(brand));
    return lottoConfigs
        .filter(lottoConfig -> !CollectionUtils.isEmpty(lottoConfig))
        .map(
            lottoConfig ->
                LottoBannerConfigDTO.builder()
                    .globalBannerLink(lottoConfig.get(0).getBannerLink())
                    .globalBannerText(lottoConfig.get(0).getBannerText())
                    .dayCount(lottoConfig.get(0).getDayCount())
                    .lottoConfig(lottoConfig)
                    .build());
  }
}
