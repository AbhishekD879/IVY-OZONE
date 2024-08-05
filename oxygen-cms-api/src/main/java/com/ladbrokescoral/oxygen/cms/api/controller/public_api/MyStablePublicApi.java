package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.MyStableDto;
import com.ladbrokescoral.oxygen.cms.api.entity.MyStable;
import com.ladbrokescoral.oxygen.cms.api.service.MyStableService;
import java.util.List;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MyStablePublicApi implements Public {

  private final MyStableService myStableService;
  private final ModelMapper modelMapper;

  @Autowired
  MyStablePublicApi(MyStableService myStableService, ModelMapper modelMapper) {
    this.myStableService = myStableService;
    this.modelMapper = modelMapper;
  }

  @GetMapping(value = "{brand}/my-stable/configuration")
  public ResponseEntity<List<MyStableDto>> findByBrand(@PathVariable String brand) {
    List<MyStable> myStableList = myStableService.findByBrand(brand);
    List<MyStableDto> myStableDtoList =
        myStableList.stream()
            .map(myStable -> modelMapper.map(myStable, MyStableDto.class))
            .collect(Collectors.toList());
    if (myStableDtoList.isEmpty()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    } else {
      return new ResponseEntity<>(myStableDtoList, HttpStatus.OK);
    }
  }
}
