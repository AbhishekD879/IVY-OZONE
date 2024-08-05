package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.TeamKit;
import com.ladbrokescoral.oxygen.cms.api.service.TeamKitService;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class TeamKits extends AbstractCrudController<TeamKit> {

  private final TeamKitService service;

  TeamKits(TeamKitService crudService) {
    super(crudService);
    service = crudService;
  }

  @Override
  @GetMapping("/team-kit")
  public List<TeamKit> readAll() {
    return super.readAll();
  }

  @Override
  @PostMapping("/team-kit")
  public ResponseEntity<TeamKit> create(@RequestBody TeamKit entity) {
    service.validate(entity);
    return super.create(entity);
  }

  @Override
  @GetMapping("/team-kit/{id}")
  public TeamKit read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @GetMapping("/team-kit/brand/{brand}")
  public List<TeamKit> readByBrand(@PathVariable("brand") String brand) {
    return super.readByBrand(brand);
  }

  @Override
  @PutMapping("/team-kit/{id}")
  public TeamKit update(@PathVariable("id") String id, @RequestBody TeamKit entity) {
    service.validate(entity);
    return super.update(id, entity);
  }

  @Override
  @DeleteMapping("/team-kit/{id}")
  public ResponseEntity<TeamKit> delete(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @PostMapping("/team-kit/brand/{brand}/{teamName}/image")
  public void saveTeamKit(
      @PathVariable("teamName") String teamName,
      @PathVariable("brand") String brand,
      @RequestParam("file") MultipartFile file) {

    TeamKit teamKit = new TeamKit(brand, teamName, null, null, null);
    service.uploadImage(file, teamKit);
    service.save(teamKit);
  }

  @PostMapping("/team-kit/{id}/image")
  public void uploadTeamKitImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {
    TeamKit teamKit = service.uploadSvgImage(file, id);
    service.save(teamKit);
  }

  @GetMapping("/team-kit/brand/{brand}/{name}")
  public List<TeamKit> getAllByName(
      @PathVariable("brand") String brand, @PathVariable("name") String name) {
    return service.findTeamKits(brand, name);
  }
}
