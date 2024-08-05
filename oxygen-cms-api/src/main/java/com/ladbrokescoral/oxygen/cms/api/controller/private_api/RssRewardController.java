package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.RssRewardDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.RssReward;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.RssRewardService;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
public class RssRewardController extends AbstractCrudController<RssReward> {
  private final RssRewardService service;
  private final ModelMapper modelMapper;

  @Autowired
  protected RssRewardController(
      CrudService<RssReward> crudService, RssRewardService service, ModelMapper modelMapper) {
    super(crudService);
    this.service = service;
    this.modelMapper = modelMapper;
  }

  @GetMapping("/rss-rewards/brand/{brand}")
  public RssReward getRssRewardByBrand(@PathVariable String brand) {
    RssReward rssReward = populateCreatorAndUpdater(service.getRssReward(brand));
    log.info("Get rss reward response entity {}", rssReward.toString());
    return rssReward;
  }

  @PutMapping("/rss-rewards/{id}")
  public RssReward update(@PathVariable String id, @RequestBody @Valid RssRewardDto rssRewardDto) {
    RssReward rssReward = modelMapper.map(rssRewardDto, RssReward.class);
    log.info("update rss reward response entity {}", rssReward.toString());
    return super.update(id, rssReward);
  }

  @PostMapping("/rss-rewards")
  public RssReward create(@RequestBody @Valid RssRewardDto rssRewardDto) {
    RssReward rssReward = modelMapper.map(rssRewardDto, RssReward.class);
    log.info("create rss reward response entity {}", rssReward.toString());
    return super.create(rssReward).getBody();
  }

  @DeleteMapping("/rss-rewards/{brand}")
  public ResponseEntity<String> deleteByBrand(@PathVariable("brand") String brand) {
    log.info("rss reward for {} has deleted ", brand);
    return service.deleteRssReward(brand);
  }
}
