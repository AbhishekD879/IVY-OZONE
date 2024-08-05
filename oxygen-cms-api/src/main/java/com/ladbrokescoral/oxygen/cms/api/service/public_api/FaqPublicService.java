package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FaqDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Faq;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.FaqService;
import java.util.List;
import java.util.Optional;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class FaqPublicService {
  private final FaqService service;

  private ModelMapper modelMapper;

  @Autowired
  public FaqPublicService(FaqService service, ModelMapper modelMapper) {
    this.service = service;
    this.modelMapper = modelMapper;
  }

  public List<Faq> findByBrand(String brand) {
    return service.findAllByBrandSorted(brand);
  }

  public FaqDto findById(String id) {
    Optional<Faq> optionalFaq = service.findOne(id);
    if (optionalFaq.isPresent()) {
      return modelMapper.map(optionalFaq.get(), FaqDto.class);
    } else {
      throw new NotFoundException();
    }
  }
}
