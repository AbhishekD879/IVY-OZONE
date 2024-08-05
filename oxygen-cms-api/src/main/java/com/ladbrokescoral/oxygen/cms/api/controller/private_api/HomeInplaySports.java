package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySportDTO;
import com.ladbrokescoral.oxygen.cms.api.service.HomeInplaySportService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.SegmentNamePattern;
import java.util.List;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Validated
public class HomeInplaySports extends AbstractSortableController<HomeInplaySport> {

  private final HomeInplaySportService homeInplaySportService;
  private ModelMapper modelMapper;

  public HomeInplaySports(HomeInplaySportService homeInplaySportService, ModelMapper modelMapper) {
    super(homeInplaySportService);
    this.homeInplaySportService = homeInplaySportService;
    this.modelMapper = modelMapper;
  }

  @PostMapping("home-inplay-sport")
  public ResponseEntity<HomeInplaySport> create(
      @RequestBody @Validated HomeInplaySportDTO homeInplaySportDTO) {
    HomeInplaySport entity = modelMapper.map(homeInplaySportDTO, HomeInplaySport.class);
    return super.create(entity);
  }

  @PutMapping("home-inplay-sport/{id}")
  public HomeInplaySport update(
      @PathVariable String id, @RequestBody @Validated HomeInplaySportDTO homeInplaySportDTO) {
    HomeInplaySport entity = modelMapper.map(homeInplaySportDTO, HomeInplaySport.class);
    return super.update(id, entity);
  }

  @GetMapping("home-inplay-sport/{id}")
  @Override
  public HomeInplaySport read(@PathVariable String id) {
    return super.read(id);
  }

  @DeleteMapping("home-inplay-sport/{id}")
  @Override
  public ResponseEntity<HomeInplaySport> delete(@PathVariable String id) {
    return super.delete(id);
  }

  @GetMapping("home-inplay-sport/brand/{brand}/segment/{segmentName}")
  public List<HomeInplaySport> readByBrandAndSegmentName(
      @PathVariable @Brand String brand, @PathVariable @SegmentNamePattern String segmentName) {
    return homeInplaySportService.findByBrandAndSegmentName(brand, segmentName);
  }

  @Override
  @PostMapping("home-inplay-sport/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
