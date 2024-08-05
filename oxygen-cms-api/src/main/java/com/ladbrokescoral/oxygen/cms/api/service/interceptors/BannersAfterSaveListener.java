package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BannerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Banner;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BannerPublicService;
import java.util.List;
import java.util.Optional;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BannersAfterSaveListener extends BasicMongoEventListener<Banner> {

  private final BannerPublicService service;
  private final SportCategoryRepository repository;
  private static final String PATH_TEMPLATE = "api/v2/{0}/banners";

  public BannersAfterSaveListener(
      final BannerPublicService service,
      final SportCategoryRepository repository,
      final DeliveryNetworkService context) {
    super(context);
    this.service = service;
    this.repository = repository;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Banner> event) {
    Optional<SportCategory> sportCategory =
        Optional.ofNullable(event.getSource())
            .map(Banner::getCategoryId)
            .map(ObjectId::toString)
            .flatMap(repository::findById);

    if (sportCategory.isPresent()) {
      String brand = event.getSource().getBrand();
      List<BannerDto> content = service.find(brand, sportCategory.get().getTargetUri());
      uploadCollection(brand, PATH_TEMPLATE, sportCategory.get().getTargetUri(), content);
    }
  }
}
