package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.MyStableDto;
import com.ladbrokescoral.oxygen.cms.api.entity.MyStable;
import com.ladbrokescoral.oxygen.cms.api.service.MyStableService;
import java.util.Optional;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class MyStableController extends AbstractSortableController<MyStable> {
  private MyStableService myStableService;

  private final ModelMapper modelMapper;

  public MyStableController(MyStableService myStableService, ModelMapper modelMapper) {
    super(myStableService);
    this.myStableService = myStableService;
    this.modelMapper = modelMapper;
  }

  @PostMapping("/my-stable/configuration")
  public ResponseEntity<MyStableDto> create(@RequestBody @Valid MyStableDto myStableDto) {
    MyStable myStable = modelMapper.map(myStableDto, MyStable.class);
    MyStable myStableSavedEntity = super.create(myStable).getBody();
    MyStableDto savedDto = modelMapper.map(myStableSavedEntity, MyStableDto.class);
    return new ResponseEntity<>(savedDto, HttpStatus.CREATED);
  }

  @PutMapping("/my-stable/configuration/{id}")
  public ResponseEntity<MyStableDto> update(
      @PathVariable String id, @RequestBody @Valid MyStableDto myStableDto) {
    MyStable myStable = modelMapper.map(myStableDto, MyStable.class);
    MyStable updatedEntity = super.update(id, myStable);
    MyStableDto savedDto = modelMapper.map(updatedEntity, MyStableDto.class);

    return new ResponseEntity<>(savedDto, HttpStatus.OK);
  }

  @GetMapping("/my-stable/configuration/brand/{brand}")
  public ResponseEntity<MyStableDto> getByBrand(@PathVariable String brand) {
    Optional<MyStable> myStable = Optional.ofNullable(myStableService.getByBrand(brand));
    return myStable
        .map(
            (MyStable myStableMap) -> {
              MyStableDto myStableDto = modelMapper.map(myStable.get(), MyStableDto.class);
              return new ResponseEntity<>(myStableDto, HttpStatus.OK);
            })
        .orElseGet(() -> new ResponseEntity<>(new MyStableDto(), HttpStatus.NO_CONTENT));
  }

  @GetMapping("/my-stable/configuration/{id}")
  public ResponseEntity<Object> getById(@PathVariable String id) {
    Optional<MyStable> myStable = myStableService.findByIds(id);
    if (myStable.isPresent()) {
      Optional<MyStableDto> optionalMyStableDto =
          Optional.of(modelMapper.map(myStable.get(), MyStableDto.class));
      return new ResponseEntity<>(optionalMyStableDto.get(), HttpStatus.OK);
    }
    return new ResponseEntity<>(HttpStatus.NOT_FOUND);
  }

  @DeleteMapping("my-stable/configuration/{id}")
  public ResponseEntity<HttpStatus> deleteById(@PathVariable String id) {
    return new ResponseEntity<>(HttpStatus.OK, super.delete(id).getStatusCode());
  }
}
