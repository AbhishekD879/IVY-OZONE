package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBet.SABChildElement;

import com.ladbrokescoral.oxygen.cms.api.dto.StreamAndBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBet;
import com.ladbrokescoral.oxygen.cms.api.exception.ElementAlreadyExistException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.SABSiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.StreamAndBetService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import java.util.List;
import java.util.Optional;
import org.springframework.http.HttpStatus;
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
public class StreamAndBets extends AbstractCrudController<StreamAndBet> {

  private final StreamAndBetService service;
  private final SABSiteServeService sabService;
  private final SiteServeService siteServeService;

  StreamAndBets(
      StreamAndBetService service,
      SABSiteServeService sabService,
      SiteServeService siteServeService) {
    super(service);
    this.service = service;
    this.sabService = sabService;
    this.siteServeService = siteServeService;
  }

  @GetMapping("stream-and-bet")
  @Override
  public List<StreamAndBet> readAll() {
    return super.readAll();
  }

  @GetMapping("stream-and-bet/{id}")
  @Override
  public StreamAndBet read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("stream-and-bet/brand/{brand}")
  @Override
  public List<StreamAndBet> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("stream-and-bet")
  @Override
  public ResponseEntity create(@RequestBody @Validated StreamAndBet entity) {
    service
        .findOneByBrand(entity.getBrand())
        .ifPresent(
            value -> {
              throw new ElementAlreadyExistException();
            });
    return super.create(entity);
  }

  @PutMapping("stream-and-bet/{id}")
  @Override
  public StreamAndBet update(
      @PathVariable String id, @RequestBody @Validated StreamAndBet updateEntity) {
    return super.update(id, updateEntity);
  }

  @DeleteMapping("stream-and-bet/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("stream-and-bet/brand/{brand}/category")
  public StreamAndBetDto createElement(
      @PathVariable String brand, @RequestBody SABChildElement element) {
    StreamAndBet streamAndBet = service.findOneByBrand(brand).orElseThrow(NotFoundException::new);
    streamAndBet.getChildren().stream()
        .filter(node -> node.getSiteServeId().equals(element.getSiteServeId()))
        .findFirst()
        .ifPresent(
            value -> {
              throw new ElementAlreadyExistException();
            });

    return service.addCategory(streamAndBet, element);
  }

  @PutMapping("stream-and-bet/brand/{brand}/category/{elementId}")
  public StreamAndBetDto updateElement(
      @PathVariable String brand,
      @PathVariable Integer elementId,
      @RequestBody SABChildElement element) {
    StreamAndBet streamAndBet = service.findOneByBrand(brand).orElseThrow(NotFoundException::new);
    if (!getCategory(streamAndBet, elementId).isPresent()) {
      throw new NotFoundException();
    }

    return service.addCategory(streamAndBet, element);
  }

  @DeleteMapping("stream-and-bet/brand/{brand}/category/{elementId}")
  public ResponseEntity deleteElement(@PathVariable String brand, @PathVariable Integer elementId) {
    StreamAndBet streamAndBet = service.findOneByBrand(brand).orElseThrow(NotFoundException::new);
    getCategory(streamAndBet, elementId)
        .ifPresent(category -> service.removeCategory(streamAndBet, category));

    return new ResponseEntity<>(HttpStatus.NO_CONTENT);
  }

  @GetMapping("stream-and-bet/brand/{brand}/fetch/category/{categoryId}")
  public ResponseEntity fetchCategoryEvents(
      @PathVariable String brand, @PathVariable Integer categoryId) {
    return new ResponseEntity<>(
        sabService.getActualStreamAndBetMap(brand, categoryId), HttpStatus.OK);
  }

  @GetMapping("stream-and-bet/brand/{brand}/fetch/category")
  public ResponseEntity fetchCategories(@PathVariable String brand) {
    return new ResponseEntity<>(siteServeService.getCategories(brand), HttpStatus.OK);
  }

  private Optional<SABChildElement> getCategory(StreamAndBet streamAndBet, Integer siteServeId) {
    return streamAndBet.getChildren().stream()
        .filter(node -> node.getSiteServeId().equals(siteServeId))
        .findFirst();
  }
}
