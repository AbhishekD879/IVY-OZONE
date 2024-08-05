package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BankingMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.BankingMenuMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.BankingMenuService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class BankingMenuPublicService implements ApiService<BankingMenuDto> {

  private final BankingMenuService service;

  public BankingMenuPublicService(BankingMenuService service) {
    this.service = service;
  }

  public List<BankingMenuDto> findByBrand(String brand) {
    brand = Util.updateBrand(brand);
    List<BankingMenu> list = service.findAllByBrand(brand);
    return list.stream().map(BankingMenuMapper.INSTANCE::toDto).collect(Collectors.toList());
  }
}
