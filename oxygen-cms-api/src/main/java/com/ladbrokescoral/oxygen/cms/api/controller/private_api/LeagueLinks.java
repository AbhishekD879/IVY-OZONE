package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LeagueLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LeagueLink;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class LeagueLinks extends AbstractCrudController<LeagueLink> {

  @Autowired
  public LeagueLinks(CrudService<LeagueLink> crudService) {
    super(crudService);
  }

  @PostMapping("statistics-links/league-links")
  public ResponseEntity<LeagueLink> create(@RequestBody @Valid LeagueLinkDto leagueLinkDto) {
    LeagueLink leagueLink = new LeagueLink();
    BeanUtils.copyProperties(leagueLinkDto, leagueLink);
    return super.create(leagueLink);
  }

  @GetMapping("statistics-links/league-links/{id}")
  @Override
  public LeagueLink read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("statistics-links/league-links/brand/{brand}")
  @Override
  public List<LeagueLink> readByBrand(@PathVariable @Brand String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("statistics-links/league-links/{id}")
  public LeagueLink update(
      @PathVariable String id, @RequestBody @Valid LeagueLinkDto leagueLinkDto) {
    LeagueLink leagueLink = new LeagueLink();
    BeanUtils.copyProperties(leagueLinkDto, leagueLink);
    return super.update(id, leagueLink);
  }

  @DeleteMapping("statistics-links/league-links/{id}")
  @Override
  public ResponseEntity<LeagueLink> delete(@PathVariable String id) {
    return super.delete(id);
  }
}
