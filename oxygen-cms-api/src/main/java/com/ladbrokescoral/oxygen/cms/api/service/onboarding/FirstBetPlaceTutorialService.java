package com.ladbrokescoral.oxygen.cms.api.service.onboarding;

import com.ladbrokescoral.oxygen.cms.api.dto.FirstBetPlaceCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.FirstBetPlaceTutorial;
import com.ladbrokescoral.oxygen.cms.api.exception.FirstBetPlaceTutorialCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.FirstBetPlaceTutorialRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import java.util.Optional;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class FirstBetPlaceTutorialService extends OnboardingService<FirstBetPlaceTutorial> {

  private final ModelMapper mapper;

  public FirstBetPlaceTutorialService(
      FirstBetPlaceTutorialRepository repository,
      ModelMapper mapper,
      ImageService imageService,
      @Value("${images.firstbet.medium}") String mediumPath,
      @Value("${images.firstbet.size}") String mediumImageSize) {
    super(repository, imageService, mediumPath, mediumImageSize);
    this.mapper = mapper;
  }

  @Override
  public FirstBetPlaceTutorial save(FirstBetPlaceTutorial firstBetPlaceTutorial) {
    if (isEntityValidToCreate(firstBetPlaceTutorial)) return super.save(firstBetPlaceTutorial);
    throw new FirstBetPlaceTutorialCreateException();
  }

  public Optional<FirstBetPlaceCFDto> convertToCFDto(FirstBetPlaceTutorial firstBetPlaceTutorial) {
    return Optional.ofNullable(mapper.map(firstBetPlaceTutorial, FirstBetPlaceCFDto.class));
  }
}
