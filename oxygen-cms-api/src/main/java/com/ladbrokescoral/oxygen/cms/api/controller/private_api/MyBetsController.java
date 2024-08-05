package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.MyBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.MyBet;
import com.ladbrokescoral.oxygen.cms.api.service.MyBetsService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class MyBetsController extends AbstractCrudController<MyBet> {
  private final MyBetsService myBetsService;

  @Autowired
  public MyBetsController(MyBetsService myBetsService) {
    super(myBetsService);
    this.myBetsService = myBetsService;
  }

  @PostMapping("{brand}/my-bets/{type}")
  public ResponseEntity<MyBet> create(
      @PathVariable String brand, @PathVariable String type, @RequestBody MyBetDto myBetDto) {
    return super.create(myBetsService.convertDtoToEntity(myBetDto));
  }

  @PutMapping("{brand}/my-bets/{type}/{id}")
  public MyBet update(
      @PathVariable String brand,
      @PathVariable String type,
      @PathVariable String id,
      @RequestBody MyBetDto myBetDto) {
    return super.update(id, myBetsService.convertDtoToEntity(myBetDto));
  }

  @GetMapping("{brand}/my-bets/{type}")
  public MyBet get(@PathVariable String brand, @PathVariable String type) {
    List<MyBet> myBetList = myBetsService.findByBrand(brand);
    return !myBetList.isEmpty() ? myBetList.get(0) : new MyBet();
  }

  @DeleteMapping("{brand}/my-bets/{type}/{id}")
  public ResponseEntity<MyBet> delete(
      @PathVariable String brand, @PathVariable String type, @PathVariable("id") String id) {
    return super.delete(id);
  }
}
