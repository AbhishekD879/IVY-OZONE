package com.ladbrokescoral.oxygen.cms.api.service;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoPage;
import com.ladbrokescoral.oxygen.cms.api.repository.SeoPageRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class SeoPageService extends AbstractService<SeoPage> {

  private final SeoPageRepository seoPageRepository;

  @Autowired
  public SeoPageService(SeoPageRepository repository) {
    super(repository);
    this.seoPageRepository = repository;
  }

  @FortifyXSSValidate("return")
  public Optional<SeoPage> findOneByIdAndBrand(String id, String brand) {
    return seoPageRepository.findOneByIdAndAndBrand(id, brand);
  }

  @FortifyXSSValidate("return")
  public List<SeoPage> findAllByBrandAndDisabled(String brand) {
    return seoPageRepository.findAllByBrandAndDisabled(brand, false);
  }

  @Override
  public SeoPage prepareModelBeforeSave(SeoPage seoPage) {
    seoPage.setUrlBrand(generateUrlBrand(seoPage));
    return seoPage;
  }

  private String generateUrlBrand(SeoPage seoPage) {
    return new StringBuilder(seoPage.getUrl())
        .append("-")
        .append(seoPage.getBrand())
        .toString()
        .replace("/", "");
  }
}
