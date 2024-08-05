package com.ladbrokescoral.oxygen.cms.api.service;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoAutoPage;
import com.ladbrokescoral.oxygen.cms.api.repository.SeoAutoPageRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class SeoAutoPageService extends AbstractService<SeoAutoPage> {

  private final SeoAutoPageRepository seoAutoPageRepository;

  @Autowired
  public SeoAutoPageService(SeoAutoPageRepository seoAutoPageRepository) {
    super(seoAutoPageRepository);
    this.seoAutoPageRepository = seoAutoPageRepository;
  }

  @FortifyXSSValidate("return")
  public List<SeoAutoPage> findAllByBrand(String brand) {
    return seoAutoPageRepository.findAllByBrand(brand);
  }
}
